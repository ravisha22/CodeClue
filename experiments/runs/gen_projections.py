import json
import yaml
import sys
from pathlib import Path
from codeclue_research.io import load_graph, save_data
from codeclue_research.operation_projection import project_operation

tasks = yaml.safe_load(Path("tests/fixtures/lane_a_extended_tasks.yaml").read_text())["tasks"]

repo_graph_map = {
    "pallets/flask": "experiments/runs/lane-a-flask/graph.json",
    "fastapi/fastapi": "experiments/runs/lane-a-fastapi/graph.json",
    "nestjs/nest": "experiments/runs/lane-a-nest/graph.json",
}
repo_run_dir = {
    "pallets/flask": "experiments/runs/lane-a-flask",
    "fastapi/fastapi": "experiments/runs/lane-a-fastapi",
    "nestjs/nest": "experiments/runs/lane-a-nest",
}

graphs = {}
for repo, gpath in repo_graph_map.items():
    p = Path(gpath)
    if p.exists():
        print(f"Loading graph: {gpath}")
        graphs[repo] = load_graph(p)
    else:
        print(f"MISSING graph: {gpath}")

for t in tasks:
    tid = t["task_id"]
    repo = t["repo"]
    of = t["operation_family"]
    run_dir = repo_run_dir[repo]
    pp_path = Path(f"{run_dir}/pp-{tid}.yaml")
    out_path = Path(f"{run_dir}/task-proj-{tid}.json")

    if repo not in graphs:
        print(f"SKIP {tid}: no graph for {repo}")
        continue

    pp = yaml.safe_load(pp_path.read_text())
    print(f"Projecting {tid} ({of}) on {repo}...", end=" ", flush=True)

    trace = project_operation(
        graph=graphs[repo],
        operation_family=of,
        prompt_profile=pp,
    )
    save_data(out_path, trace)

    conf = trace.get("confidence", {})
    print(f"nodes={trace['stats']['projected_node_count']} conf={conf.get('confidence_overall', -1)} hint={conf.get('lookup_decision_hint', '?')}")

print("\nDone.")
