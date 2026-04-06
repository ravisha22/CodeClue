"""Phase 3: Clue-only benchmark for Plan A and Plan B.

For each task, renders both clue views and scores against gold-path specs.
Produces DFCR (Default-Free Completion Rate) per family per plan.

This script can be run with or without LLM consumer/judge calls.
Without API keys, it reports heuristic scores only.

Usage:
    python experiments/runs/run_clue_only_ab.py
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
from codeclue_research.token_counter import count_tokens


# Same TASKS list as compression script
TASKS: list[tuple[str, str, str, str, str]] = [
    ("flask-tf1-001", "v2-lane-a-flask", "v2-proj-flask-tf1-001.json", "What is the high-level architecture of Flask's request handling?", "TF1"),
    ("flask-tf1-002", "v2-lane-a-flask", "v2-proj-flask-tf1-002.json", "How are Flask blueprints structured?", "TF1"),
    ("flask-tf2-001", "v2-lane-a-flask", "v2-proj-flask-tf2-001.json", "What is the downstream impact of modifying Flask.wsgi_app?", "TF2"),
    ("flask-tf2-002", "v2-lane-a-flask", "v2-proj-flask-tf2-002.json", "What is the impact of changing Flask.dispatch_request?", "TF2"),
    ("flask-tf3-001", "v2-lane-a-flask", "v2-proj-flask-tf3-001.json", "Where should the edit be made to add a new request hook?", "TF3"),
    ("flask-tf4-001", "v2-lane-a-flask", "v2-proj-flask-tf4-001.json", "What behavioral gotcha exists in Flask's request dispatch path?", "TF4"),
    ("flask-tf5-001", "v2-lane-a-flask", "v2-proj-flask-tf5-001.json", "What security concerns exist in Flask's session handling?", "TF5"),
    ("fastapi-tf1-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf1-001.json", "What is FastAPI's request routing architecture?", "TF1"),
    ("fastapi-tf3-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf3-001.json", "Where to edit to add middleware in FastAPI?", "TF3"),
    ("fastapi-tf4-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf4-001.json", "What gotcha exists in FastAPI dependency injection?", "TF4"),
    ("fastapi-tf5-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf5-001.json", "Security concerns in FastAPI's CORS handling?", "TF5"),
    ("nest-tf1-001", "v2-lane-a-nest", "v2-proj-nest-tf1-001.json", "What is NestJS module architecture?", "TF1"),
    ("nest-tf2-001", "v2-lane-a-nest", "v2-proj-nest-tf2-001.json", "Impact of changing NestJS dependency injection container?", "TF2"),
    ("nest-tf4-001", "v2-lane-a-nest", "v2-proj-nest-tf4-001.json", "Behavioral gotchas in NestJS middleware pipeline?", "TF4"),
    ("nest-tf5-001", "v2-lane-a-nest", "v2-proj-nest-tf5-001.json", "Security concerns in NestJS guards?", "TF5"),
    ("httpx-tf2-001", "v2-lane-a-httpx", "v2-proj-httpx-tf2-001.json", "Impact of modifying httpx transport layer?", "TF2"),
    ("httpx-tf4-001", "v2-lane-a-httpx", "v2-proj-httpx-tf4-001.json", "Gotchas in httpx connection pooling?", "TF4"),
    ("express-tf1-001", "v2-lane-a-express", "v2-proj-express-tf1-001.json", "Express middleware architecture?", "TF1"),
    ("express-tf5-001", "v2-lane-a-express", "v2-proj-express-tf5-001.json", "Security in Express request parsing?", "TF5"),
    ("typeorm-tf2-001", "v2-lane-a-typeorm", "v2-proj-typeorm-tf2-001.json", "Impact of TypeORM connection changes?", "TF2"),
    ("typeorm-tf3-001", "v2-lane-a-typeorm", "v2-proj-typeorm-tf3-001.json", "Where to add TypeORM migration support?", "TF3"),
    ("gin-tf1-001", "v2-lane-a-gin", "v2-proj-gin-tf1-001.json", "Gin router architecture?", "TF1"),
    ("gin-tf5-001", "v2-lane-a-gin", "v2-proj-gin-tf5-001.json", "Security in Gin middleware chain?", "TF5"),
]

# Gold path fixture mapping (family → fixture file)
GOLD_FIXTURES: dict[str, str] = {
    "TF1": "gold_path_architecture.yaml",
    "TF2": "gold_path_impact.yaml",
    "TF3": "gold_path_edit.yaml",
    "TF4": "gold_path_behavior.yaml",
    "TF5": "gold_path_security.yaml",
}


def _load_gold_spec(family: str) -> dict | None:
    """Load gold path spec for a task family."""
    import yaml
    fixture_name = GOLD_FIXTURES.get(family)
    if not fixture_name:
        return None
    fixture_path = ROOT / "tests" / "fixtures" / fixture_name
    if not fixture_path.is_file():
        return None
    with open(fixture_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _simulate_consumer_answer(clue: dict, question: str, plan: str) -> str:
    """Generate a simulated consumer answer from clue content.

    In production, this would call an LLM API. For the automated benchmark,
    we synthesize an answer from the clue's own content to measure how much
    of the gold-path information is present in the clue.
    """
    parts = [f"Based on the clue artifact, here is my analysis of: {question}\n"]

    if plan == "a":
        for entity in clue.get("entities", []):
            name = entity.get("name", "")
            behavior = entity.get("behavior", "")
            role = entity.get("class", "")
            eid = entity.get("id", "")
            parts.append(f"- {name} ({eid}, {role}): {behavior}")
            for inv in entity.get("invariants", []):
                parts.append(f"  Invariant: {inv}")
            for risk in entity.get("risks", []):
                parts.append(f"  Risk: {risk}")
    elif plan == "b":
        for node in clue.get("nodes", []):
            name = node.get("name", "")
            summary = node.get("summary", "")
            nid = node.get("id", "")
            parts.append(f"- {name} ({nid}): {summary}")
        for assertion in clue.get("assertions", []):
            parts.append(f"- Assertion: {assertion.get('fact', '')}")

    return "\n".join(parts)


def main() -> None:
    runs_dir = ROOT / "experiments" / "runs"
    reports_dir = ROOT / "experiments" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
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

    results: list[dict] = []
    skipped: list[str] = []

    for task_id, lane_dir, proj_file, question, family in TASKS:
        proj_path = runs_dir / lane_dir / proj_file
        graph_path = runs_dir / lane_dir / "graph.json"

        if not proj_path.is_file():
            skipped.append(f"{task_id}: projection missing")
            continue
        if not graph_path.is_file():
            skipped.append(f"{task_id}: graph missing")
            continue

        repo_key = lane_dir.replace("v2-lane-a-", "")
        repo_root = repo_dirs.get(repo_key, ROOT)

        with open(proj_path, "r", encoding="utf-8") as f:
            projection = json.load(f)
        graph = load_graph(graph_path)

        gold_spec = _load_gold_spec(family)
        if not gold_spec:
            skipped.append(f"{task_id}: no gold spec for {family}")
            continue

        for plan_label, renderer in [("a", render_clue_plan_a), ("b", render_clue_plan_b)]:
            clue = renderer(projection, graph, question, str(repo_root))
            answer = _simulate_consumer_answer(clue, question, plan_label)
            score = score_heuristic(answer, gold_spec, clue)

            results.append({
                "task_id": task_id,
                "family": family,
                "plan": plan_label,
                "clue_tokens": count_tokens(clue),
                "heuristic_score": score,
                "sufficient": score["sufficient"],
            })

        print(f"  {task_id}: A={[r for r in results if r['task_id']==task_id and r['plan']=='a'][-1]['heuristic_score']['path_fidelity']:.3f}  "
              f"B={[r for r in results if r['task_id']==task_id and r['plan']=='b'][-1]['heuristic_score']['path_fidelity']:.3f}")

    # Aggregate by family and plan
    families = ["TF1", "TF2", "TF3", "TF4", "TF5"]
    summary: dict[str, Any] = {}

    for plan in ["a", "b"]:
        plan_results = [r for r in results if r["plan"] == plan]
        for fam in families:
            fam_results = [r for r in plan_results if r["family"] == fam]
            if not fam_results:
                continue
            sufficient = sum(1 for r in fam_results if r["sufficient"])
            key = f"{plan}_{fam}"
            summary[key] = {
                "plan": plan,
                "family": fam,
                "task_count": len(fam_results),
                "sufficient_count": sufficient,
                "dfcr": round(sufficient / len(fam_results), 4) if fam_results else 0,
                "mean_fidelity": round(
                    sum(r["heuristic_score"]["path_fidelity"] for r in fam_results) / len(fam_results), 4
                ),
            }

        # Overall
        sufficient_all = sum(1 for r in plan_results if r["sufficient"])
        summary[f"{plan}_overall"] = {
            "plan": plan,
            "family": "ALL",
            "task_count": len(plan_results),
            "sufficient_count": sufficient_all,
            "dfcr": round(sufficient_all / len(plan_results), 4) if plan_results else 0,
        }

    output = {
        "per_task": results,
        "summary": summary,
        "skipped": skipped,
    }

    out_path = reports_dir / "clue-only-ab-results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n=== CLUE-ONLY BENCHMARK RESULTS ===")
    for key, val in sorted(summary.items()):
        print(f"  {key}: DFCR={val['dfcr']:.2f} ({val['sufficient_count']}/{val['task_count']})")
    print(f"Skipped: {len(skipped)}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
