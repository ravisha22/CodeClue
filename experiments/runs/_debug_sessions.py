from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _select_focus_nodes

graph = extract_graph(Path("experiments/external-repos/flask"))

# Find all session-related symbols in the graph
print("=== Session symbols in graph ===")
for n in graph.nodes:
    sc = n.semantic_contract or {}
    sym = sc.get("symbol_name", "")
    if "session" in sym.lower() and n.node_type != "module":
        print(f"  {n.node_type:15s} sym={sym:40s} id={n.node_id[:70]}")

# Now check focus selection
print("\n=== Focus selection for 'refactor sessions' ===")
q = "How would you refactor Flask to move all session-related code to a new dedicated module while maintaining backwards compatibility?"
focus = _select_focus_nodes(graph, q)
print(f"Total focus nodes: {len(focus)}")
session_focus = [fn for fn in focus if "session" in fn.semantic_contract.get("symbol_name", "").lower()]
print(f"Session-related in focus: {len(session_focus)}")
for fn in session_focus:
    print(f"  {fn.semantic_contract.get('symbol_name', '')} ({fn.node_type})")

# Check gold names vs actual names
golds = ["SessionInterface", "SecureCookieSessionInterface", "SecureCookieSession"]
print("\n=== Gold name matching ===")
for g in golds:
    # Does any focus node have this exact name or short name?
    for fn in focus:
        sym = fn.semantic_contract.get("symbol_name", "")
        short = sym.rsplit(".", 1)[-1] if "." in sym else sym
        if g == sym or g == short:
            print(f"  {g} -> MATCH: {sym}")
            break
    else:
        # Check if it exists in the full graph
        for n in graph.nodes:
            sym = n.semantic_contract.get("symbol_name", "")
            short = sym.rsplit(".", 1)[-1] if "." in sym else sym
            if g == sym or g == short:
                print(f"  {g} -> IN GRAPH but NOT in focus: {sym} ({n.node_id[:50]})")
                break
        else:
            print(f"  {g} -> NOT IN GRAPH")
