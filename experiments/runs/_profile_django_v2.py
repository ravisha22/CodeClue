"""Profile Django render: explicit file.write() for reliable output."""
import time
import traceback
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/django-profile.log")
LOG.parent.mkdir(parents=True, exist_ok=True)
REPO = Path("experiments/external-repos/django")


def log(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()


try:
    LOG.write_text("")  # Clear
    log(f"=== Django Render Profiling ===")
    log(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    log("\n--- EXTRACTION ---")
    t0 = time.time()
    from codeclue_research.extractor import extract_graph
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    log(f"Extraction: {t_extract:.1f}s ({n_mod} mod, {n_sym} sym, {len(graph.edges)} edges)")

    log("\n--- RENDER STAGE PROFILING ---")
    question = "How would you refactor Django settings loading to support multiple config sources?"
    repo_root = str(REPO)

    from codeclue_research.clue_view_mrlf import (
        _render_l0, _render_l1, _render_l2, _render_l3, _render_gaps,
        _select_focus_nodes, _token_count,
        BUDGET_TOTAL,
    )

    t0 = time.time()
    l0 = _render_l0(graph)
    t_l0 = time.time() - t0
    log(f"L0 TREE:    {t_l0:>8.2f}s  {_token_count(l0):>5d} tokens")

    t0 = time.time()
    l1 = _render_l1(graph, repo_root)
    t_l1 = time.time() - t0
    log(f"L1 INDEX:   {t_l1:>8.2f}s  {_token_count(l1):>5d} tokens")

    t0 = time.time()
    l2 = _render_l2(graph, repo_root)
    t_l2 = time.time() - t0
    log(f"L2 SYM:     {t_l2:>8.2f}s  {_token_count(l2):>5d} tokens")

    t0 = time.time()
    l3 = _render_l3(graph, question, repo_root)
    t_l3 = time.time() - t0
    log(f"L3 FOCUS:   {t_l3:>8.2f}s  {_token_count(l3):>5d} tokens")

    l2_symbols = [n for n in graph.nodes if n.node_type != "module"]
    focus = _select_focus_nodes(graph, question)
    t0 = time.time()
    gaps = _render_gaps(graph, question, focus, l2_symbols)
    t_gaps = time.time() - t0
    log(f"GAPS:       {t_gaps:>8.2f}s  {_token_count(gaps):>5d} tokens")

    total_render = t_l0 + t_l1 + t_l2 + t_l3 + t_gaps
    log(f"\nTOTAL:      {total_render:>8.2f}s")

    log(f"\n--- TIME BREAKDOWN ---")
    for name, t in [("L0 TREE", t_l0), ("L1 INDEX", t_l1), ("L2 SYM", t_l2), ("L3 FOCUS", t_l3), ("GAPS", t_gaps)]:
        pct = t / total_render * 100 if total_render > 0 else 0
        bar = "#" * int(pct / 2)
        log(f"  {name:12s} {t:>8.2f}s ({pct:>5.1f}%) {bar}")

    log("\n=== Profile complete ===")

except Exception as e:
    log(f"ERROR: {type(e).__name__}: {e}")
    log(traceback.format_exc())
