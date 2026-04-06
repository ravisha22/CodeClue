"""Phase 2: Measure token compression for Plan A and Plan B across all tasks.

Reads existing projections from experiments/runs/v2-lane-a-*/ directories,
renders both Plan A and Plan B clue views, and computes CCR metrics.

Usage:
    python -m experiments.runs.measure_compression_ab
    # or
    python experiments/runs/measure_compression_ab.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add src to path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.clue_view_plan_a import render_clue_plan_a
from codeclue_research.clue_view_plan_b import render_clue_plan_b
from codeclue_research.io import load_graph
from codeclue_research.token_metrics import compute_compression_metrics


# Task definitions: (task_id, repo_dir, projection_file, question, family)
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


def main() -> None:
    runs_dir = ROOT / "experiments" / "runs"
    reports_dir = ROOT / "experiments" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    external_repos = ROOT / "experiments" / "external-repos"

    results: list[dict] = []
    skipped: list[str] = []

    # Repo directory mapping
    repo_dirs = {
        "flask": external_repos / "flask",
        "fastapi": external_repos / "fastapi",
        "nest": external_repos / "nest",
        "httpx": external_repos / "httpx",
        "express": external_repos / "express",
        "typeorm": external_repos / "typeorm",
        "gin": external_repos / "gin",
    }

    for task_id, lane_dir, proj_file, question, family in TASKS:
        proj_path = runs_dir / lane_dir / proj_file
        graph_path = runs_dir / lane_dir / "graph.json"

        if not proj_path.is_file():
            skipped.append(f"{task_id}: projection not found at {proj_path}")
            continue
        if not graph_path.is_file():
            skipped.append(f"{task_id}: graph not found at {graph_path}")
            continue

        # Determine repo root
        repo_key = lane_dir.replace("v2-lane-a-", "")
        repo_root = repo_dirs.get(repo_key, ROOT)

        # Load projection and graph
        with open(proj_path, "r", encoding="utf-8") as f:
            projection = json.load(f)

        graph = load_graph(str(graph_path))

        # Render Plan A
        clue_a = render_clue_plan_a(projection, graph, question, str(repo_root))
        metrics_a = compute_compression_metrics(
            task_id=task_id, clue_view=clue_a, projection_trace=projection,
            repo_root=str(repo_root), plan="a",
        )
        metrics_a["family"] = family
        results.append(metrics_a)

        # Render Plan B
        clue_b = render_clue_plan_b(projection, graph, question, str(repo_root))
        metrics_b = compute_compression_metrics(
            task_id=task_id, clue_view=clue_b, projection_trace=projection,
            repo_root=str(repo_root), plan="b",
        )
        metrics_b["family"] = family
        results.append(metrics_b)

        print(f"  {task_id}: A={metrics_a['ccr']:.3f}  B={metrics_b['ccr']:.3f}  raw={metrics_a['raw_first_tokens']}t")

    # Aggregate
    plan_a = [r for r in results if r["plan"] == "a"]
    plan_b = [r for r in results if r["plan"] == "b"]

    def _summary(rows: list[dict], label: str) -> dict:
        if not rows:
            return {"plan": label, "task_count": 0}
        ccrs = [r["ccr"] for r in rows]
        pass_count = sum(1 for c in ccrs if c >= 0.85)
        return {
            "plan": label,
            "task_count": len(rows),
            "mean_ccr": round(sum(ccrs) / len(ccrs), 4),
            "min_ccr": round(min(ccrs), 4),
            "max_ccr": round(max(ccrs), 4),
            "pass_count_85": pass_count,
            "pass_rate_85": round(pass_count / len(ccrs), 4) if ccrs else 0,
            "mean_clue_tokens": round(sum(r["clue_tokens"] for r in rows) / len(rows)),
            "mean_raw_tokens": round(sum(r["raw_first_tokens"] for r in rows) / len(rows)),
        }

    output = {
        "per_task": results,
        "summary_a": _summary(plan_a, "A"),
        "summary_b": _summary(plan_b, "B"),
        "skipped": skipped,
    }

    out_path = reports_dir / "compression-ab-results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n=== COMPRESSION RESULTS ===")
    print(f"Plan A: {output['summary_a']}")
    print(f"Plan B: {output['summary_b']}")
    print(f"Skipped: {len(skipped)} tasks")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
