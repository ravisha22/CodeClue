"""Debug: check containment edges for SecureCookieSessionInterface."""
from pathlib import Path
from codeclue_research.extractor import extract_graph

graph = extract_graph(Path("experiments/external-repos/flask"))

# Find SecureCookieSessionInterface node
sci_id = None
for n in graph.nodes:
    sc = n.semantic_contract or {}
    if sc.get("symbol_name") == "SecureCookieSessionInterface":
        sci_id = n.node_id
        print(f"SecureCookieSessionInterface node_id: {sci_id}")
        break

# Find all edges FROM this node
print("\n=== Edges FROM SecureCookieSessionInterface ===")
for e in graph.edges:
    if e.from_node == sci_id:
        print(f"  {e.edge_type}: -> {e.to_node}")

# Find get_signing_serializer node
print("\n=== get_signing_serializer nodes ===")
for n in graph.nodes:
    sc = n.semantic_contract or {}
    if "get_signing_serializer" in sc.get("symbol_name", ""):
        print(f"  id: {n.node_id}")
        print(f"  uses: {sc.get('uses', [])}")
