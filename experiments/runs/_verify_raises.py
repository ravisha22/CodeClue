from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf

graph = extract_graph(Path("experiments/external-repos/flask"))

# Check raises in graph
print("=== Symbols with raises ===")
for n in graph.nodes:
    sc = n.semantic_contract
    r = sc.get("raises", [])
    if r:
        sym = sc.get("symbol_name", "")
        print(f"  {sym:40s} raises: {r}")

# Render and check
print("\n=== Clue raises lines ===")
clue = render_mrlf(graph, "What security measures protect Flask session data?", repo_root="experiments/external-repos/flask")
for line in clue.split("\n"):
    if "raises" in line.lower():
        print(f"  {line}")

# Also check NullSession specifically
print("\n=== NullSession entry in FOCUS ===")
in_focus = False
for line in clue.split("\n"):
    if "-- FOCUS" in line:
        in_focus = True
        continue
    if line.startswith("-- ") and in_focus:
        break
    if in_focus and "NullSession" in line:
        idx = clue.index(line)
        print(clue[idx:idx+300])
        break
