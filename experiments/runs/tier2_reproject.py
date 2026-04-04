"""Re-project Flask tasks using Tier 2 enriched graph and compare with Tier 1."""
import json
import yaml
from pathlib import Path
from codeclue_research.io import load_graph, save_data
from codeclue_research.operation_projection import project_operation

tier2_graph_path = Path("experiments/runs/v2-lane-a-flask/graph-tier2.json")
if not tier2_graph_path.exists():
    print("ERROR: Tier 2 graph not found. Run inject_tier2.py first.")
    exit(1)

graph = load_graph(tier2_graph_path)
print(f"Loaded Tier 2 graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

# Count Tier 2 nodes
tier2_count = sum(1 for n in graph.nodes if n.semantic_contract.get("tier") == 2)
print(f"Tier 2 enriched nodes: {tier2_count}")

# Load Flask tasks
all_tasks = []
for tf in ["tests/fixtures/lane_a_flask_tasks.yaml", "tests/fixtures/lane_a_extended_tasks.yaml"]:
    p = Path(tf)
    if p.exists():
        tasks = yaml.safe_load(p.read_text())["tasks"]
        for t in tasks:
            if t.get("repo", "pallets/flask") == "pallets/flask":
                all_tasks.append(t)

print(f"Flask tasks to re-project: {len(all_tasks)}")

results = []
for t in all_tasks:
    tid = t["task_id"]
    of = t["operation_family"]
    pp = t["prompt_profile"]

    print(f"  {tid} ({of})...", end=" ", flush=True)
    trace = project_operation(graph=graph, operation_family=of, prompt_profile=pp)
    out = Path(f"experiments/runs/v2-lane-a-flask/tier2-proj-{tid}.json")
    save_data(out, trace)

    conf = trace.get("confidence", {})
    r = {
        "task_id": tid,
        "of": of,
        "family": t["family"],
        "tier2_nodes": trace["stats"]["projected_node_count"],
        "tier2_conf": round(conf.get("confidence_overall", -1), 4),
        "tier2_hint": conf.get("lookup_decision_hint", "?"),
    }

    # Load v2 Tier 1 projection for comparison
    tier1_path = Path(f"experiments/runs/v2-lane-a-flask/v2-proj-{tid}.json")
    if tier1_path.exists():
        t1 = json.loads(tier1_path.read_text())
        t1_conf = t1.get("confidence", {})
        r["tier1_nodes"] = t1["stats"]["projected_node_count"]
        r["tier1_conf"] = round(t1_conf.get("confidence_overall", -1), 4)
        r["tier1_hint"] = t1_conf.get("lookup_decision_hint", "?")
        r["conf_delta"] = round(r["tier2_conf"] - r["tier1_conf"], 4)

    results.append(r)
    print(f"conf={r['tier2_conf']} (Δ={r.get('conf_delta', '?')})")

save_data(Path("experiments/reports/tier2-flask-comparison.json"), {
    "tier2_enriched_nodes": tier2_count,
    "total_nodes": len(graph.nodes),
    "tasks": results,
})
print(f"\nDone. Comparison saved to experiments/reports/tier2-flask-comparison.json")
