"""V2 benchmark pipeline: re-run all 15 existing tasks + extract 5 new repos."""
import json
import yaml
from pathlib import Path
from codeclue_research.io import load_graph, save_data
from codeclue_research.operation_projection import project_operation
from codeclue_research.extractor import extract_graph

# === Phase 1: Re-run projections on existing 3 repos with v2 graphs ===
print("=== PHASE 1: Re-projecting 15 existing tasks with fixed code ===")

repo_graph_map = {
    "pallets/flask": "experiments/runs/v2-lane-a-flask/graph.json",
    "fastapi/fastapi": "experiments/runs/v2-lane-a-fastapi/graph.json",
    "nestjs/nest": "experiments/runs/v2-lane-a-nest/graph.json",
}
repo_run_dir = {
    "pallets/flask": "experiments/runs/v2-lane-a-flask",
    "fastapi/fastapi": "experiments/runs/v2-lane-a-fastapi",
    "nestjs/nest": "experiments/runs/v2-lane-a-nest",
}

# Load graphs
graphs = {}
for repo, gpath in repo_graph_map.items():
    p = Path(gpath)
    if p.exists():
        graphs[repo] = load_graph(p)
        n = len(graphs[repo].nodes)
        e = len(graphs[repo].edges)
        print(f"  Loaded {repo}: {n} nodes, {e} edges")

# Load all tasks (initial 5 + extended 10)
all_tasks = []
for tf in ["tests/fixtures/lane_a_flask_tasks.yaml", "tests/fixtures/lane_a_extended_tasks.yaml"]:
    p = Path(tf)
    if p.exists():
        tasks = yaml.safe_load(p.read_text())["tasks"]
        for t in tasks:
            if "repo" not in t:
                t["repo"] = "pallets/flask"
            all_tasks.append(t)

print(f"  Total tasks: {len(all_tasks)}")

# Project each task
results = []
for t in all_tasks:
    tid = t["task_id"]
    repo = t["repo"]
    of = t["operation_family"]
    run_dir = repo_run_dir.get(repo)
    if not run_dir or repo not in graphs:
        print(f"  SKIP {tid}: no graph for {repo}")
        continue

    pp = t["prompt_profile"]
    print(f"  {tid} ({of}) on {repo}...", end=" ", flush=True)

    trace = project_operation(graph=graphs[repo], operation_family=of, prompt_profile=pp)
    out = Path(f"{run_dir}/v2-proj-{tid}.json")
    save_data(out, trace)

    conf = trace.get("confidence", {})
    r = {
        "task_id": tid,
        "repo": repo,
        "family": t["family"],
        "of": of,
        "nodes": trace["stats"]["projected_node_count"],
        "edges": trace["stats"]["projected_edge_count"],
        "conf": round(conf.get("confidence_overall", -1), 4),
        "hint": conf.get("lookup_decision_hint", "?"),
        "actions": sum(len(n.get("suggested_actions", [])) for n in conf.get("per_node_confidence", [])),
    }
    results.append(r)
    print(f"nodes={r['nodes']} conf={r['conf']} hint={r['hint']}")

# Save v2 summary
save_data(Path("experiments/reports/v2-existing-projections.json"), {
    "version": "v2-fixes",
    "tasks": results,
})

# === Phase 2: Extract 5 new repos ===
print("\n=== PHASE 2: Extracting 5 new repos ===")
new_repos = {
    "httpx": {"path": "experiments/external-repos/httpx", "lang": "python"},
    "express": {"path": "experiments/external-repos/express", "lang": "typescript"},
    "typeorm": {"path": "experiments/external-repos/typeorm", "lang": "typescript"},
    "gin": {"path": "experiments/external-repos/gin", "lang": "go"},
}

# Add click if it exists
click_path = Path("experiments/external-repos/click")
if click_path.exists():
    new_repos["click"] = {"path": str(click_path), "lang": "python"}

for name, info in new_repos.items():
    repo_path = Path(info["path"])
    if not repo_path.exists():
        print(f"  SKIP {name}: not found")
        continue

    out_dir = Path(f"experiments/runs/v2-lane-a-{name}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_graph = out_dir / "graph.json"

    print(f"  Extracting {name} ({info['lang']})...", end=" ", flush=True)
    try:
        graph = extract_graph(repo_root=repo_path, commit_id="HEAD", language=info["lang"])
        from codeclue_research.io import save_graph
        save_graph(out_graph, graph)
        print(f"nodes={len(graph.nodes)} edges={len(graph.edges)}")
    except Exception as e:
        print(f"ERROR: {e}")

print("\nDone.")
