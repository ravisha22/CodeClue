"""Quick debug: check name_to_symbol keys and call edge resolution."""
from pathlib import Path
import tempfile
from codeclue_research.extractor import extract_python_nodes_edges

tmp = Path(tempfile.mkdtemp())
(tmp / "mod.py").write_text(
    "class A:\n"
    "    def __init__(self):\n"
    "        self.n()\n"
    "    def m(self):\n"
    "        self.n()\n"
    "    def n(self):\n"
    "        pass\n"
    "def helper():\n"
    "    return A()\n",
    encoding="utf-8",
)

nodes, edges = extract_python_nodes_edges(tmp)

print("=== SYMBOLS ===")
for n in nodes:
    sn = n.semantic_contract.get("symbol_name", "")
    if sn and n.node_type != "module":
        print(f"  {n.node_id}  name={sn}  type={n.node_type}")

print("\n=== CALL EDGES ===")
nm = {n.node_id: n.semantic_contract.get("symbol_name", "") for n in nodes}
for e in edges:
    if e.edge_type == "calls":
        print(f"  {nm.get(e.from_node, e.from_node)} -> {nm.get(e.to_node, e.to_node)}")

# Also check name_to_symbol mapping
print("\n=== name_to_symbol KEYS ===")
name_map: dict[str, list[str]] = {}
for n in nodes:
    sn = n.semantic_contract.get("symbol_name", "")
    if sn and n.node_type != "module":
        name_map.setdefault(sn, []).append(n.node_id)
for k, v in sorted(name_map.items()):
    print(f"  '{k}': {v}")
