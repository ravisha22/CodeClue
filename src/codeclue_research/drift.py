"""Delta drift testing module per PRD Section 6.3 and H3/H4.

Provides:
- apply_single_delta: apply one commit delta and measure fidelity change
- run_drift_protocol: sequential N-commit drift with fidelity tracking
- detect_reset_trigger: check if drift exceeds guard bands
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .extractor import extract_graph
from .fidelity import evaluate_projection_fidelity
from .io import save_graph
from .models import CanonicalClueGraph
from .operation_projection import project_operation


def _git_log_commits(repo_root: Path, n: int) -> list[str]:
    """Get the last N commit hashes from oldest to newest."""
    result = subprocess.run(
        ["git", "log", "--oneline", "--format=%H", f"-{n}"],
        cwd=str(repo_root), capture_output=True, text=True,
    )
    hashes = result.stdout.strip().split("\n")
    hashes = [h for h in hashes if h]
    hashes.reverse()  # oldest first
    return hashes


def _git_checkout(repo_root: Path, commit: str) -> bool:
    """Checkout a specific commit."""
    result = subprocess.run(
        ["git", "checkout", commit, "--force"],
        cwd=str(repo_root), capture_output=True, text=True,
    )
    return result.returncode == 0


def _git_diff_stat(repo_root: Path, from_commit: str, to_commit: str) -> dict[str, Any]:
    """Get diff stats between two commits."""
    result = subprocess.run(
        ["git", "diff", "--stat", from_commit, to_commit],
        cwd=str(repo_root), capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    return {
        "from": from_commit[:8],
        "to": to_commit[:8],
        "diff_lines": len(lines),
        "summary": lines[-1] if lines else "",
    }


def apply_single_delta(
    graph: CanonicalClueGraph,
    repo_root: Path,
    from_commit: str,
    to_commit: str,
    operation_family: str = "OF2",
    language: str = "auto",
) -> dict[str, Any]:
    """Apply one commit delta and measure fidelity change.

    1. Extract graph at to_commit (full regen for comparison).
    2. Project both graphs with same OF.
    3. Compute DNG = |FS_full - FS_delta|.
    """
    repo_root = Path(repo_root).resolve()

    # Checkout to_commit and extract fresh graph
    _git_checkout(repo_root, to_commit)
    full_graph = extract_graph(repo_root, commit_id=to_commit, language=language)

    # Project both graphs
    proj_old = project_operation(graph=graph, operation_family=operation_family)
    proj_new = project_operation(graph=full_graph, operation_family=operation_family)

    # Compute fidelity of old projection against new graph's projection as gold
    # Use the new projection's nodes/edges as gold standard
    gold_nodes = [n["node_id"] for n in proj_new.get("projected_nodes", [])]
    gold_edges = [e["edge_id"] for e in proj_new.get("projected_edges", [])]

    gold_spec = {
        "gold_id": f"delta-{from_commit[:8]}-to-{to_commit[:8]}",
        "operation_family": operation_family,
        "gold_path": {"nodes": gold_nodes, "edges": gold_edges},
        "thresholds": {"node_f1_min": 0.0, "edge_f1_min": 0.0, "path_fidelity_min": 0.0},
    }

    fidelity = evaluate_projection_fidelity(proj_old, gold_spec)
    path_fidelity = fidelity["metrics"]["path_fidelity"]

    # DNG: how much does the old graph's projection differ from fresh
    dng = 1.0 - path_fidelity

    # Identify recomputed nodes (nodes in files that changed)
    diff_stat = _git_diff_stat(repo_root, from_commit, to_commit)
    changed_files = set()
    diff_result = subprocess.run(
        ["git", "diff", "--name-only", from_commit, to_commit],
        cwd=str(repo_root), capture_output=True, text=True,
    )
    for line in diff_result.stdout.strip().split("\n"):
        if line:
            changed_files.add(line)

    recomputed_nodes = [
        n.node_id for n in full_graph.nodes
        if n.source_anchor.file_path in changed_files
    ]

    return {
        "from_commit": from_commit,
        "to_commit": to_commit,
        "dng": round(dng, 6),
        "fidelity_delta": round(path_fidelity, 6),
        "updated_graph": full_graph,
        "diff_stat": diff_stat,
        "recomputed_nodes": recomputed_nodes,
        "fidelity_report": fidelity,
    }


def detect_reset_trigger(
    history: list[dict[str, Any]],
    floor: float = 0.80,
    slope_guard: float = -0.002,
) -> bool:
    """Check if drift history triggers a full regeneration reset.

    Triggers when:
    - Any fidelity drops below floor, OR
    - Drift slope exceeds guard band
    """
    if not history:
        return False

    # Floor check
    for step in history:
        if step.get("fidelity", 1.0) < floor:
            return True

    # Slope check (linear regression)
    if len(history) >= 3:
        n = len(history)
        xs = list(range(n))
        ys = [s.get("fidelity", 1.0) for s in history]
        x_mean = sum(xs) / n
        y_mean = sum(ys) / n
        numerator = sum((xs[i] - x_mean) * (ys[i] - y_mean) for i in range(n))
        denominator = sum((xs[i] - x_mean) ** 2 for i in range(n))
        if denominator > 0:
            slope = numerator / denominator
            if slope < slope_guard:
                return True

    return False


def run_drift_protocol(
    repo_root: Path,
    n_commits: int = 10,
    operation_family: str = "OF2",
    language: str = "auto",
) -> dict[str, Any]:
    """Run sequential N-commit drift protocol.

    Starting from the oldest commit, extract a graph, then step forward
    one commit at a time measuring how the old graph's projection
    differs from a fresh extraction.
    """
    repo_root = Path(repo_root).resolve()
    commits = _git_log_commits(repo_root, n_commits + 1)  # +1 for the baseline

    if len(commits) < 2:
        return {
            "steps_completed": 0,
            "error": f"Not enough commits: found {len(commits)}, need at least 2",
            "steps": [],
            "slope": 0.0,
            "floor_maintained": True,
        }

    # Extract baseline at oldest commit
    baseline_commit = commits[0]
    _git_checkout(repo_root, baseline_commit)
    current_graph = extract_graph(repo_root, commit_id=baseline_commit, language=language)

    steps: list[dict[str, Any]] = []
    history: list[dict[str, float]] = []

    for i in range(1, min(len(commits), n_commits + 1)):
        from_commit = commits[i - 1]
        to_commit = commits[i]

        try:
            result = apply_single_delta(
                graph=current_graph,
                repo_root=repo_root,
                from_commit=from_commit,
                to_commit=to_commit,
                operation_family=operation_family,
                language=language,
            )

            fidelity = result["fidelity_delta"]
            steps.append({
                "index": i,
                "from_commit": from_commit[:8],
                "to_commit": to_commit[:8],
                "fidelity": fidelity,
                "dng": result["dng"],
                "changed_files": len(result["recomputed_nodes"]),
            })
            history.append({"fidelity": fidelity})

            # Update current graph to the fresh extraction for next step
            current_graph = result["updated_graph"]

        except Exception as e:
            steps.append({
                "index": i,
                "from_commit": from_commit[:8],
                "to_commit": to_commit[:8],
                "error": str(e),
                "fidelity": 0.0,
                "dng": 1.0,
            })
            history.append({"fidelity": 0.0})

    # Compute overall slope
    slope = 0.0
    if len(history) >= 2:
        n = len(history)
        xs = list(range(n))
        ys = [h["fidelity"] for h in history]
        x_mean = sum(xs) / n
        y_mean = sum(ys) / n
        num = sum((xs[i] - x_mean) * (ys[i] - y_mean) for i in range(n))
        den = sum((xs[i] - x_mean) ** 2 for i in range(n))
        if den > 0:
            slope = num / den

    floor_maintained = all(s.get("fidelity", 0) >= 0.80 for s in steps)

    # Restore to latest commit
    if commits:
        _git_checkout(repo_root, commits[-1])

    return {
        "steps_completed": len(steps),
        "total_commits": len(commits) - 1,
        "operation_family": operation_family,
        "steps": steps,
        "slope": round(slope, 6),
        "floor_maintained": floor_maintained,
        "reset_triggered": detect_reset_trigger(history),
    }
