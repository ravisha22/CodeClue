"""Check if get_signing_serializer has its own FOCUS entry."""
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _select_focus_nodes

graph = extract_graph(Path("experiments/external-repos/flask"))
focus = _select_focus_nodes(graph, "What security measures protect Flask session data?")
for i, n in enumerate(focus):
    sc = n.semantic_contract or {}
    name = sc.get("symbol_name", "")
    uses = sc.get("uses", [])
    if "signing" in name.lower() or "get_signing" in name.lower():
        print(f"  #{i+1:2d}: {name:45s} type={n.node_type:15s} uses={uses}")

# Also check: is get_signing_serializer a node in the graph at all?
print("\n=== get_signing_serializer in graph ===")
for node in graph.nodes:
    sc = node.semantic_contract or {}
    if "get_signing_serializer" in sc.get("symbol_name", ""):
        print(f"  {node.node_id}")
        print(f"  uses: {sc.get('uses', [])}")
