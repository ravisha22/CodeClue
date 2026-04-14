"""Profile render_mrlf on Django: per-stage timing breakdown.

Writes results to experiments/runs/mrlf-benchmark/django-profile.log
"""
import sys
import time
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/django-profile.log")
LOG.parent.mkdir(parents=True, exist_ok=True)

log_file = LOG.open("w", encoding="utf-8")
orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

REPO = Path("experiments/external-repos/django")

try:
    print("=== Django Render Profiling ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Extract graph (reuse from previous run if possible)
    print("\n--- EXTRACTION ---")
    t0 = time.time()
    from codeclue_research.extractor import extract_graph
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    print(f"Extraction: {t_extract:.1f}s ({n_mod} mod, {n_sym} sym, {len(graph.edges)} edges)")

    # Now profile each render sub-stage manually
    print("\n--- RENDER STAGE PROFILING ---")
    question = "How would you refactor Django settings loading to support multiple config sources?"
    repo_root = str(REPO)

    from codeclue_research.clue_view_mrlf import (
        _render_l0, _render_l1, _render_l2, _render_l3, _render_gaps,
        _select_focus_nodes, _token_count, _extract_question_keywords,
        BUDGET_L0, BUDGET_L1, BUDGET_L2, BUDGET_L3, BUDGET_GAPS, BUDGET_TOTAL,
    )

    # L0
    t0 = time.time()
    l0 = _render_l0(graph)
    t_l0 = time.time() - t0
    l0_toks = _token_count(l0)
    print(f"L0 TREE:    {t_l0:>8.2f}s  {l0_toks:>5d} tokens")

    # L1
    t0 = time.time()
    l1 = _render_l1(graph, repo_root)
    t_l1 = time.time() - t0
    l1_toks = _token_count(l1)
    print(f"L1 INDEX:   {t_l1:>8.2f}s  {l1_toks:>5d} tokens")

    # L2
    t0 = time.time()
    l2 = _render_l2(graph, repo_root)
    t_l2 = time.time() - t0
    l2_toks = _token_count(l2)
    print(f"L2 SYM:     {t_l2:>8.2f}s  {l2_toks:>5d} tokens")

    # L3 (includes focus selection)
    t0 = time.time()
    focus = _select_focus_nodes(graph, question)
    t_focus = time.time() - t0
    print(f"L3 select:  {t_focus:>8.2f}s  {len(focus)} focus nodes")

    t0 = time.time()
    l3 = _render_l3(graph, question, repo_root)
    t_l3 = time.time() - t0
    l3_toks = _token_count(l3)
    print(f"L3 FOCUS:   {t_l3:>8.2f}s  {l3_toks:>5d} tokens (includes re-selection)")

    # GAPS
    l2_symbols = [n for n in graph.nodes if n.node_type != "module"]
    t0 = time.time()
    gaps = _render_gaps(graph, question, focus, l2_symbols)
    t_gaps = time.time() - t0
    gaps_toks = _token_count(gaps)
    print(f"GAPS:       {t_gaps:>8.2f}s  {gaps_toks:>5d} tokens")

    # Total
    total_render = t_l0 + t_l1 + t_l2 + t_l3 + t_gaps
    total_toks = l0_toks + l1_toks + l2_toks + l3_toks + gaps_toks
    print(f"\nTOTAL:      {total_render:>8.2f}s  {total_toks:>5d} tokens")
    print(f"Budget:     {total_toks}/{BUDGET_TOTAL} ({total_toks/BUDGET_TOTAL*100:.0f}%)")

    # Breakdown percentages
    print(f"\n--- TIME BREAKDOWN ---")
    stages = [("L0 TREE", t_l0), ("L1 INDEX", t_l1), ("L2 SYM", t_l2),
              ("L3 FOCUS", t_l3), ("GAPS", t_gaps)]
    for name, t in stages:
        pct = t / total_render * 100 if total_render > 0 else 0
        bar = "#" * int(pct / 2)
        print(f"  {name:12s} {t:>8.2f}s ({pct:>5.1f}%) {bar}")

    # Sub-profile L2 SYM (suspected main bottleneck)
    print(f"\n--- L2 SYM SUB-PROFILE ---")

    # PageRank only
    from codeclue_research.clue_view_mrlf import _pagerank
    prod_nodes = [n for n in graph.nodes
                  if n.node_type != "module"
                  and "test" not in n.source_anchor.file_path.lower()]
    prod_ids = {n.node_id for n in prod_nodes}
    call_edges = [(e.from_node, e.to_node) for e in graph.edges
                  if e.edge_type == "calls" and e.from_node in prod_ids and e.to_node in prod_ids]

    t0 = time.time()
    ranks = _pagerank([n.node_id for n in prod_nodes], call_edges)
    t_pr = time.time() - t0
    print(f"  PageRank ({len(prod_nodes)} nodes, {len(call_edges)} edges): {t_pr:.2f}s")

    # File reads for line numbers (count unique files accessed)
    files_accessed = set()
    for n in prod_nodes[:500]:  # Sample first 500
        files_accessed.add(n.source_anchor.file_path)
    t0 = time.time()
    for fp in files_accessed:
        rp = Path(repo_root) / fp
        if rp.is_file():
            try:
                rp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
    t_reads = time.time() - t0
    print(f"  File reads (sample {len(files_accessed)} files): {t_reads:.2f}s")
    print(f"  Estimated full file reads ({len(set(n.source_anchor.file_path for n in prod_nodes))} unique files): {t_reads * len(set(n.source_anchor.file_path for n in prod_nodes)) / max(len(files_accessed), 1):.2f}s")

    # tiktoken per-entry (sample)
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    sample_entries = ["some_function M django/db/models/query.py:123 function some_function"] * 100
    t0 = time.time()
    for entry in sample_entries:
        len(enc.encode(entry + "\n"))
    t_tik = time.time() - t0
    print(f"  tiktoken 100 entries: {t_tik:.4f}s → estimated 42K entries: {t_tik * 420:.2f}s")

    print("\n=== Profile complete ===")

except Exception as e:
    import traceback
    print(f"ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()

finally:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    log_file.close()
    print(LOG.read_text(encoding="utf-8"))
