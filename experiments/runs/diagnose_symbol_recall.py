"""Diagnostic: Why are gold symbols missing from MRLF clues?

Tests three competing hypotheses:
  A: Test symbols crowd out production symbols in PageRank
  B: Extractor misses call edges (gold symbols disconnected)  
  C: Gold symbols exist and rank well but are truncated by budget

Run from repo root: python experiments/runs/diagnose_symbol_recall.py
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _pagerank

FLASK_GOLDS = {
    "TF1": ["SessionInterface", "SecureCookieSessionInterface", "SecureCookieSession", "session_interface"],
    "TF2": ["RequestContext", "AppContext", "_AppCtxGlobals", "Request"],
    "TF3": ["Blueprint", "BlueprintSetupState", "errorhandler", "register_blueprint"],
    "TF4": ["wsgi_app", "dispatch_request", "RequestContext", "request_started"],
    "TF5": ["SecureCookieSessionInterface", "SecureCookieSession", "NullSession"],
}


def main():
    repo = Path("experiments/external-repos/flask")
    graph = extract_graph(repo)

    # Build lookups
    node_by_id = {n.node_id: n for n in graph.nodes}
    short_name_to_ids: dict[str, list[str]] = defaultdict(list)
    for n in graph.nodes:
        sc = n.semantic_contract or {}
        sym = sc.get("symbol_name", "")
        # Store both full and short name
        short_name_to_ids[sym].append(n.node_id)
        short = sym.rsplit(".", 1)[-1] if "." in sym else sym
        if short != sym:
            short_name_to_ids[short].append(n.node_id)

    # Edge indexes
    in_degree: dict[str, int] = defaultdict(int)
    out_degree: dict[str, int] = defaultdict(int)
    call_edges = []
    for e in graph.edges:
        if e.edge_type == "calls":
            in_degree[e.to_node] += 1
            out_degree[e.from_node] += 1
            call_edges.append((e.from_node, e.to_node))

    # PageRank
    sym_ids = [n.node_id for n in graph.nodes if n.node_type != "module"]
    ranks = _pagerank(sym_ids, call_edges)
    ranked = sorted(sym_ids, key=lambda x: ranks.get(x, 0), reverse=True)
    rank_pos = {nid: i + 1 for i, nid in enumerate(ranked)}

    total_syms = len(sym_ids)

    # === REPORT ===
    print("=" * 100)
    print("DIAGNOSTIC: Gold Symbol Connectivity in Flask Graph")
    print(f"Total symbols: {total_syms}, Total call edges: {len(call_edges)}")
    print("=" * 100)

    all_gold_syms = set()
    for syms in FLASK_GOLDS.values():
        all_gold_syms.update(syms)

    # Hypothesis testing
    hyp_a_evidence = 0  # symbols in graph, ranked > budget cut
    hyp_b_evidence = 0  # symbols NOT in graph or in-degree=0, out-degree=0
    hyp_c_evidence = 0  # symbols in graph, ranked within budget, but still missing

    print(f"\n{'Gold Symbol':<35s} | {'Found?':>7s} | {'In-Deg':>6s} | {'Out-Deg':>7s} | {'PR Rank':>7s}/{total_syms} | {'File':<40s}")
    print("-" * 110)

    for gs in sorted(all_gold_syms):
        matches = short_name_to_ids.get(gs, [])
        if matches:
            nid = matches[0]
            n = node_by_id[nid]
            ind = in_degree.get(nid, 0)
            outd = out_degree.get(nid, 0)
            rk = rank_pos.get(nid, -1)
            fp = n.source_anchor.file_path

            if ind == 0 and outd == 0:
                hyp_b_evidence += 1
                tag = " <-- HYP B: disconnected"
            elif rk > 89:  # budget cut at ~89 symbols for Flask
                hyp_a_evidence += 1
                tag = f" <-- HYP A: ranked #{rk}, outside budget"
            else:
                hyp_c_evidence += 1
                tag = " <-- in budget, should appear"

            print(f"{gs:<35s} | {'YES':>7s} | {ind:>6d} | {outd:>7d} | {rk:>7d}/{total_syms} | {fp:<40s}{tag}")
        else:
            hyp_b_evidence += 1
            print(f"{gs:<35s} | {'NO':>7s} |      - |       - |       - |{'':40s} <-- HYP B: not in graph")

    print()
    print("=" * 100)
    print("HYPOTHESIS SUMMARY")
    print("=" * 100)
    print(f"  Hypothesis A (test symbols crowd out production): {hyp_a_evidence} gold symbols affected")
    print(f"  Hypothesis B (extractor missed / disconnected):   {hyp_b_evidence} gold symbols affected")
    print(f"  Hypothesis C (in budget but still missing):       {hyp_c_evidence} gold symbols affected")
    print()

    # Top 20 by PageRank
    print("Top 20 by PageRank (what fills L2 SYM budget):")
    for i, nid in enumerate(ranked[:20]):
        n = node_by_id[nid]
        sc = n.semantic_contract or {}
        sname = sc.get("symbol_name", nid)
        fp = n.source_anchor.file_path
        ind = in_degree.get(nid, 0)
        outd = out_degree.get(nid, 0)
        is_test = "test" in fp.lower()
        tag = " [TEST]" if is_test else ""
        print(f"  #{i+1:>3d}  {sname:<40s} in={ind:>3d} out={outd:>3d}  {fp}{tag}")

    # Test symbol contamination
    test_top100 = sum(1 for nid in ranked[:100]
                      if "test" in node_by_id[nid].source_anchor.file_path.lower())
    test_top300 = sum(1 for nid in ranked[:300]
                      if "test" in node_by_id[nid].source_anchor.file_path.lower())
    print(f"\nTest file symbols in top 100: {test_top100}/100 ({test_top100}%)")
    print(f"Test file symbols in top 300: {test_top300}/300 ({test_top300*100//300}%)")

    # If Hyp A dominates, show what rank gold symbols need to reach
    if hyp_a_evidence > 0:
        print(f"\nFor Hyp A symbols: they exist and are connected, but ranked too low.")
        print(f"Current budget shows ~89 symbols. These gold symbols would need")
        print(f"to be in the top 89 to appear in L2 SYM.")


if __name__ == "__main__":
    main()
