import json

d = json.load(open("experiments/runs/sprint6-test/projection-of2.json"))
c = d.get("confidence", {})

summary = {k: v for k, v in c.items() if k not in ("per_node_confidence", "per_edge_confidence")}
print(json.dumps(summary, indent=2))

nodes = c.get("per_node_confidence", [])
edges = c.get("per_edge_confidence", [])
print(f"\nNodes with confidence: {len(nodes)}")
print(f"Edges with confidence: {len(edges)}")

nodes_with_actions = [n for n in nodes if n.get("suggested_actions")]
print(f"Nodes with suggested_actions: {len(nodes_with_actions)}")
for n in nodes_with_actions[:5]:
    print(f"  {n['node_id']}: conf={n['confidence']}, actions={len(n['suggested_actions'])}")
