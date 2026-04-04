import json
import sys

proj_file = sys.argv[1] if len(sys.argv) > 1 else "experiments/runs/lane-a-flask/task-proj-flask-tf4-001.json"
d = json.load(open(proj_file))

print("=== PROJECTED NODES ===")
for n in d["projected_nodes"]:
    sc = n["semantic_contract"]
    name = sc.get("symbol_name", "")
    purpose = sc.get("purpose", "")
    stype = sc.get("symbol_type", "")
    fpath = n.get("source_anchor", {}).get("file_path", "")
    print(f"  {n['node_id']}")
    print(f"    type={stype} purpose={purpose} file={fpath}")

print(f"\n=== PROJECTED EDGES ({len(d['projected_edges'])}) ===")
for e in d["projected_edges"][:20]:
    print(f"  {e['edge_type']}: {e['from_node']} -> {e['to_node']}")

print(f"\n=== CONFIDENCE ===")
conf = d.get("confidence", {})
print(f"  overall: {conf.get('confidence_overall')} hint: {conf.get('lookup_decision_hint')}")
print(f"  p_context_miss: {conf.get('p_context_miss')}")
print(f"  p_dependency_miss: {conf.get('p_dependency_miss')}")

print(f"\n=== NODES WITH SUGGESTED ACTIONS ===")
for nc in conf.get("per_node_confidence", []):
    actions = nc.get("suggested_actions", [])
    if actions:
        print(f"  {nc['node_id']}: conf={nc['confidence']}")
        for a in actions[:2]:
            print(f"    -> {a['tool']}: {a['rationale'][:80]}")
