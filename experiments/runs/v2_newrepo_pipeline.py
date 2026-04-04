"""Generate projections for new-repo tasks using v2 code."""
import json
import yaml
from pathlib import Path
from codeclue_research.io import load_graph, save_data
from codeclue_research.operation_projection import project_operation

tasks = yaml.safe_load(Path("tests/fixtures/lane_a_newrepo_tasks.yaml").read_text())["tasks"]

repo_graph_map = {
    "httpx": "experiments/runs/v2-lane-a-httpx/graph.json",
    "express": "experiments/runs/v2-lane-a-express/graph.json",
    "typeorm": "experiments/runs/v2-lane-a-typeorm/graph.json",
    "gin": "experiments/runs/v2-lane-a-gin/graph.json",
}

graphs = {}
for name, gpath in repo_graph_map.items():
    p = Path(gpath)
    if p.exists():
        graphs[name] = load_graph(p)
        print(f"Loaded {name}: {len(graphs[name].nodes)} nodes, {len(graphs[name].edges)} edges")

results = []
for t in tasks:
    tid = t["task_id"]
    repo_dir = t["repo_dir"]
    of = t["operation_family"]
    pp = t["prompt_profile"]

    if repo_dir not in graphs:
        print(f"SKIP {tid}: no graph for {repo_dir}")
        continue

    run_dir = Path(f"experiments/runs/v2-lane-a-{repo_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save prompt profile
    pp_path = run_dir / f"pp-{tid}.yaml"
    pp_path.write_text(yaml.safe_dump(pp, sort_keys=False))

    print(f"Projecting {tid} ({of}) on {repo_dir}...", end=" ", flush=True)
    trace = project_operation(graph=graphs[repo_dir], operation_family=of, prompt_profile=pp)
    save_data(run_dir / f"v2-proj-{tid}.json", trace)

    conf = trace.get("confidence", {})
    r = {
        "task_id": tid,
        "repo": t["repo"],
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

save_data(Path("experiments/reports/v2-newrepo-projections.json"), {"version": "v2-fixes", "tasks": results})
print(f"\nDone. {len(results)} tasks projected.")
