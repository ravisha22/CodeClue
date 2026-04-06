"""Phase 4: Drill-down trial for Plan A and Plan B.

For tasks that failed clue-only in Phase 3, runs confidence-gated drill-down
and measures fidelity uplift.

Usage:
    python experiments/runs/run_drilldown_ab.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.clue_view_plan_a import render_clue_plan_a
from codeclue_research.clue_view_plan_b import render_clue_plan_b
from codeclue_research.io import load_graph
from codeclue_research.judge import score_heuristic
from codeclue_research.drilldown_orchestrator import run_gated_drilldown
from codeclue_research.token_metrics import compute_compression_metrics
from codeclue_research.token_counter import count_tokens


def main() -> None:
    reports_dir = ROOT / "experiments" / "reports"
    runs_dir = ROOT / "experiments" / "runs"
    external_repos = ROOT / "experiments" / "external-repos"

    repo_dirs = {
        "flask": external_repos / "flask",
        "fastapi": external_repos / "fastapi",
        "nest": external_repos / "nest",
        "httpx": external_repos / "httpx",
        "express": external_repos / "express",
        "typeorm": external_repos / "typeorm",
        "gin": external_repos / "gin",
    }

    # Load Phase 3 results
    phase3_path = reports_dir / "clue-only-ab-results.json"
    if not phase3_path.is_file():
        print("ERROR: Phase 3 results not found. Run run_clue_only_ab.py first.")
        return

    with open(phase3_path, "r", encoding="utf-8") as f:
        phase3 = json.load(f)

    # Find tasks that failed clue-only
    failed_tasks = [
        r for r in phase3.get("per_task", [])
        if not r.get("sufficient", True)
    ]

    print(f"Found {len(failed_tasks)} failed tasks for drill-down trial")

    results: list[dict] = []
    skipped: list[str] = []

    # Gold spec loader
    import yaml
    GOLD_FIXTURES = {
        "TF1": "gold_path_architecture.yaml",
        "TF2": "gold_path_impact.yaml",
        "TF3": "gold_path_edit.yaml",
        "TF4": "gold_path_behavior.yaml",
        "TF5": "gold_path_security.yaml",
    }

    def _load_gold_spec(family: str):
        fixture_name = GOLD_FIXTURES.get(family)
        if not fixture_name:
            return None
        fixture_path = ROOT / "tests" / "fixtures" / fixture_name
        if not fixture_path.is_file():
            return None
        with open(fixture_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # Task → projection file mapping (shared with other scripts)
    from run_clue_only_ab import TASKS  # noqa: E402

    task_map = {t[0]: t for t in TASKS}

    for failed in failed_tasks:
        task_id = failed["task_id"]
        plan = failed["plan"]
        family = failed["family"]

        task_info = task_map.get(task_id)
        if not task_info:
            skipped.append(f"{task_id}: not in task map")
            continue

        _, lane_dir, proj_file, question, _ = task_info
        proj_path = runs_dir / lane_dir / proj_file
        graph_path = runs_dir / lane_dir / "graph.json"

        if not proj_path.is_file() or not graph_path.is_file():
            skipped.append(f"{task_id}: files missing")
            continue

        repo_key = lane_dir.replace("v2-lane-a-", "")
        repo_root = repo_dirs.get(repo_key, ROOT)

        with open(proj_path, "r", encoding="utf-8") as f:
            projection = json.load(f)
        graph = load_graph(graph_path)

        gold_spec = _load_gold_spec(family)
        if not gold_spec:
            skipped.append(f"{task_id}: no gold spec")
            continue

        # Render clue
        if plan == "a":
            clue = render_clue_plan_a(projection, graph, question, str(repo_root))
        else:
            clue = render_clue_plan_b(projection, graph, question, str(repo_root))

        # Run gated drill-down
        op_family = {"TF1": "OF1", "TF2": "OF2", "TF3": "OF3", "TF4": "OF4", "TF5": "OF5"}.get(family, "OF2")
        drilldown = run_gated_drilldown(
            clue=clue, plan=plan, graph=graph,
            repo_root=str(repo_root), operation_family=op_family,
        )

        # Score post-drill answer (simulated by combining clue content + drill-down)
        clue_text = json.dumps(clue, indent=2)
        drill_text = json.dumps(drilldown.get("drilldown_results", []), indent=2)
        combined_answer = f"Based on clue and drill-down:\n{clue_text}\n\nDrill-down evidence:\n{drill_text}"
        post_score = score_heuristic(combined_answer, gold_spec, clue)

        # Compute uplift
        clue_only_fidelity = failed["heuristic_score"]["path_fidelity"]
        post_drill_fidelity = post_score["path_fidelity"]
        fidelity_uplift = post_drill_fidelity - clue_only_fidelity

        results.append({
            "task_id": task_id,
            "family": family,
            "plan": plan,
            "clue_only_fidelity": clue_only_fidelity,
            "post_drill_fidelity": post_drill_fidelity,
            "fidelity_uplift": round(fidelity_uplift, 4),
            "drilldown_triggered": drilldown["drilldown_triggered"],
            "tools_used": len(drilldown.get("tools_used", [])),
            "drilldown_tokens": drilldown.get("drilldown_tokens", 0),
            "clue_tokens": count_tokens(clue),
        })

        print(f"  {task_id}/{plan}: FU={fidelity_uplift:+.3f} (clue={clue_only_fidelity:.3f} → post={post_drill_fidelity:.3f})")

    # Aggregate
    total_tasks_all = len(phase3.get("per_task", [])) // 2  # divided by 2 plans
    for plan in ["a", "b"]:
        plan_failed = [r for r in results if r["plan"] == plan]
        plan_total = sum(1 for t in phase3.get("per_task", []) if t["plan"] == plan)
        drilled = sum(1 for r in plan_failed if r["drilldown_triggered"])

        ddr = drilled / plan_total if plan_total > 0 else 0
        mean_fu = sum(r["fidelity_uplift"] for r in plan_failed) / len(plan_failed) if plan_failed else 0

        print(f"\n  Plan {plan.upper()}: DDR={ddr:.3f}, Mean FU={mean_fu:+.3f}, Drilled={drilled}/{plan_total}")

    output = {
        "per_task": results,
        "skipped": skipped,
    }

    out_path = reports_dir / "drilldown-ab-results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
