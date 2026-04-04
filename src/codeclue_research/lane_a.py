from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .confidence import compute_structural_confidence
from .extractor import extract_graph
from .fidelity import evaluate_projection_fidelity
from .graph_analysis import analyze_graph_integrity
from .io import load_data, save_data, save_graph
from .operation_projection import project_operation
from .roundtrip import run_roundtrip
from .schema_validator import validate_graph


_OPERATION_FAMILIES = ["OF1", "OF2", "OF3", "OF4", "OF5"]


def _load_replay_set(replay_set_path: Path) -> list[dict[str, Any]]:
    return json.loads(replay_set_path.read_text(encoding="utf-8"))


def run_lane_a_extraction(
    repo_root: Path,
    output_dir: Path,
    commit_id: str,
    repo_name: str,
    language: str = "auto",
    generator_model: str = "codeclue-structural-v1",
) -> dict[str, Any]:
    """Phase 1 of Lane A: Extract, validate, and project a single external repo."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract
    graph = extract_graph(
        repo_root=repo_root,
        commit_id=commit_id,
        language=language,
        generator_model=generator_model,
    )
    graph_path = output_dir / "graph.json"
    save_graph(graph_path, graph)

    # Validate
    validation_errors = validate_graph(graph, repo_root)
    roundtrip_result = run_roundtrip(graph)
    integrity_result = analyze_graph_integrity(graph)

    integrity_checks = integrity_result.get("invariant_checks", {})
    integrity_passed = bool(
        integrity_checks.get("connectivity_invariant", False)
        and integrity_checks.get("no_gap_invariant", False)
    )

    # Project OF1-OF5 with confidence
    projections: dict[str, dict[str, Any]] = {}
    for of in _OPERATION_FAMILIES:
        trace = project_operation(
            graph=graph,
            operation_family=of,
        )
        proj_path = output_dir / f"projection-{of}.json"
        save_data(proj_path, trace)
        projections[of] = {
            "nodes": trace["stats"]["projected_node_count"],
            "edges": trace["stats"]["projected_edge_count"],
            "confidence_overall": trace.get("confidence", {}).get("confidence_overall", -1),
            "lookup_hint": trace.get("confidence", {}).get("lookup_decision_hint", "unknown"),
            "tool_call_budget": trace.get("confidence", {}).get("tool_call_budget", 0),
            "suggested_actions_count": sum(
                len(n.get("suggested_actions", []))
                for n in trace.get("confidence", {}).get("per_node_confidence", [])
            ),
        }

    summary = {
        "repo_name": repo_name,
        "commit_id": commit_id,
        "language": language,
        "generator_model": generator_model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graph_stats": {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
        },
        "validation_passed": len(validation_errors) == 0,
        "validation_error_count": len(validation_errors),
        "roundtrip_passed": roundtrip_result.get("passed", False),
        "integrity_passed": integrity_passed,
        "projections": projections,
    }

    save_data(output_dir / "lane-a-extraction-summary.json", summary)
    return summary


def run_lane_a_confidence_report(
    output_dir: Path,
) -> dict[str, Any]:
    """Phase 2 of Lane A: Aggregate confidence metrics across OF families."""
    summary_path = output_dir / "lane-a-extraction-summary.json"
    if not summary_path.exists():
        return {"error": "Run extraction first"}

    summary = load_data(summary_path)
    projections = summary.get("projections", {})

    confidence_report = {
        "repo_name": summary["repo_name"],
        "commit_id": summary["commit_id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "per_family": {},
        "aggregate": {},
    }

    overall_scores: list[float] = []
    total_actions = 0
    families_needing_lookup = []

    for of, proj_data in projections.items():
        conf = proj_data.get("confidence_overall", -1)
        hint = proj_data.get("lookup_hint", "unknown")
        actions = proj_data.get("suggested_actions_count", 0)

        confidence_report["per_family"][of] = {
            "confidence_overall": conf,
            "lookup_decision_hint": hint,
            "suggested_actions_count": actions,
            "tool_call_budget": proj_data.get("tool_call_budget", 0),
        }

        if conf >= 0:
            overall_scores.append(conf)
        total_actions += actions
        if hint in ("targeted_lookup", "expanded_lookup"):
            families_needing_lookup.append(of)

    if overall_scores:
        avg_conf = sum(overall_scores) / len(overall_scores)
    else:
        avg_conf = 0.0

    confidence_report["aggregate"] = {
        "mean_confidence": round(avg_conf, 6),
        "families_needing_lookup": families_needing_lookup,
        "total_suggested_actions": total_actions,
        "clue_only_families": [
            of for of, d in confidence_report["per_family"].items()
            if d["lookup_decision_hint"] == "clue_only"
        ],
    }

    save_data(output_dir / "lane-a-confidence-report.json", confidence_report)
    return confidence_report


def run_lane_a_batch(
    replay_set_path: Path,
    external_repos_dir: Path,
    runs_base_dir: Path,
) -> dict[str, Any]:
    """Run Lane A extraction across all repos in the replay set."""
    entries = _load_replay_set(replay_set_path)

    # Group by repo
    repos: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        repos.setdefault(entry["repo"], []).append(entry)

    batch_results: list[dict[str, Any]] = []

    for repo_full, pr_entries in repos.items():
        repo_short = repo_full.split("/")[-1]
        repo_dir = external_repos_dir / repo_short

        if not repo_dir.exists():
            batch_results.append({
                "repo": repo_full,
                "status": "skipped",
                "reason": f"repo directory not found: {repo_dir}",
            })
            continue

        # Use the first merged-core entry as the pinned commit
        merged = [e for e in pr_entries if e["tier"] == "merged-core"]
        if not merged:
            continue

        entry = merged[0]
        commit_id = entry.get("merge_commit_sha", "unknown")
        language = "python"
        if repo_short == "nest":
            language = "typescript"

        output_dir = runs_base_dir / f"lane-a-{repo_short}"

        try:
            summary = run_lane_a_extraction(
                repo_root=repo_dir,
                output_dir=output_dir,
                commit_id=commit_id,
                repo_name=repo_full,
                language=language,
            )
            conf_report = run_lane_a_confidence_report(output_dir)
            batch_results.append({
                "repo": repo_full,
                "status": "ok",
                "commit_id": commit_id,
                "graph_nodes": summary["graph_stats"]["node_count"],
                "graph_edges": summary["graph_stats"]["edge_count"],
                "validation_passed": summary["validation_passed"],
                "integrity_passed": summary["integrity_passed"],
                "mean_confidence": conf_report["aggregate"]["mean_confidence"],
                "families_needing_lookup": conf_report["aggregate"]["families_needing_lookup"],
                "total_suggested_actions": conf_report["aggregate"]["total_suggested_actions"],
            })
        except Exception as e:
            batch_results.append({
                "repo": repo_full,
                "status": "error",
                "error": str(e),
            })

    batch_summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "replay_set": str(replay_set_path),
        "repos_attempted": len(repos),
        "repos_succeeded": sum(1 for r in batch_results if r["status"] == "ok"),
        "results": batch_results,
    }

    save_data(runs_base_dir / "lane-a-batch-summary.json", batch_summary)
    return batch_summary
