"""Check which click symbols the extractor finds vs gold symbols."""
from pathlib import Path
from codeclue_research.extractor import extract_python_nodes_edges

repo = Path("experiments/external-repos/click")
nodes, edges = extract_python_nodes_edges(repo)

GOLD = [
    "consume_value", "type_cast_value", "Choice", "convert",
    "File", "Path", "LazyFile", "normalize_choice"
]

print(f"Total nodes: {len(nodes)}")
print(f"Total edges: {len(edges)}")
print()

# Find gold symbols
for gold_name in GOLD:
    matches = [n for n in nodes
              if gold_name == n.semantic_contract.get("symbol_name", "")
              or gold_name in n.semantic_contract.get("symbol_name", "")]
    if matches:
        for m in matches[:3]:
            sn = m.semantic_contract.get("symbol_name", "")
            sf = m.source_anchor.file_path
            print(f"  FOUND {gold_name}: symbol_name='{sn}' file={sf} id={m.node_id}")
    else:
        print(f"  MISSING: {gold_name}")

# Count call edges
call_edges = [e for e in edges if e.edge_type == "calls"]
print(f"\nCall edges: {len(call_edges)}")
