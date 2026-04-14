"""Check: where does SecureCookieSessionInterface rank in FOCUS selection for flask-tf5."""
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _select_focus_nodes, _token_count

repo_path = Path("experiments/external-repos/flask")
graph = extract_graph(repo_path)
question = "What security measures protect Flask session data, and what are the attack vectors?"

focus_nodes = _select_focus_nodes(graph, question)

# Show first 40 focus nodes
print("=== Focus node order (first 40) ===")
for i, node in enumerate(focus_nodes[:40]):
    sc = node.semantic_contract or {}
    sym_name = sc.get("symbol_name", "")
    fp = node.source_anchor.file_path
    # Mark if session-relevant
    mark = " ***" if "Session" in sym_name or "Cookie" in sym_name or "session" in sym_name.lower() else ""
    print(f"  #{i+1:2d}: {sym_name:40s} ({node.node_type:15s}) {fp}{mark}")

print(f"\nTotal focus nodes: {len(focus_nodes)}")

# Actually render and check token usage
from codeclue_research.clue_view_mrlf import render_mrlf
clue = render_mrlf(graph, question, repo_root=str(repo_path))
toks = _token_count(clue)
print(f"Total clue tokens: {toks}")

# Count lines in FOCUS section
lines = clue.split("\n")
in_focus = False
focus_entry_count = 0
for line in lines:
    if "-- FOCUS" in line:
        in_focus = True
    if "-- GAPS" in line:
        in_focus = False
    if in_focus and line and not line.startswith("  ") and not line.startswith("--"):
        focus_entry_count += 1

print(f"Focus entries that fit in budget: {focus_entry_count}")
