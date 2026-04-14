from pathlib import Path
from codeclue_research.extractor import extract_graph  
from codeclue_research.clue_view_mrlf import _select_focus_nodes

graph = extract_graph(Path("experiments/external-repos/flask"))
q = "How would you refactor Flask to move all session-related code to a new dedicated module while maintaining backwards compatibility?"
focus = _select_focus_nodes(graph, q)

# Print ALL focus nodes with 'session' in name or file
golds = {"SessionInterface", "SecureCookieSessionInterface", "SecureCookieSession", "NullSession"}
print(f"Focus: {len(focus)} nodes")
print(f"\nSession-related focus nodes:")
for fn in focus:
    sc = fn.semantic_contract or {}
    sym = sc.get("symbol_name", "")
    fp = fn.source_anchor.file_path
    if "session" in sym.lower() or "session" in fp.lower():
        matched = sym in golds or sym.rsplit(".", 1)[-1] in golds
        tag = " << GOLD MATCH" if matched else ""
        print(f"  {sym:45s} type={fn.node_type:15s} file={fp}{tag}")

# Check if golds are in focus at all
print(f"\nGold symbol presence in focus:")
focus_syms = set()
for fn in focus:
    sc = fn.semantic_contract or {}
    s = sc.get("symbol_name", "")
    focus_syms.add(s)
    focus_syms.add(s.rsplit(".", 1)[-1])

for g in sorted(golds):
    gs = g.rsplit(".", 1)[-1]
    in_focus = g in focus_syms or gs in focus_syms
    print(f"  {g:35s} -> {'IN FOCUS' if in_focus else 'NOT IN FOCUS'}")
