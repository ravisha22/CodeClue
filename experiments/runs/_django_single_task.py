"""Run a single Django MRLF task with full error tracing.

Usage: python experiments/runs/_django_single_task.py
"""
import sys
import time
import traceback
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, _word_count, BUDGET_TOTAL

REPO = Path("experiments/external-repos/django")
OUT = Path("experiments/runs/mrlf-benchmark")

TASK = {
    "task_id": "django-tf2-middleware-impact",
    "question": "What is the downstream impact of modifying Django middleware handling?",
    "gold_symbols": ["BaseHandler", "MiddlewareMixin", "get_response"],
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("1. Extracting Django graph...")
    sys.stdout.flush()
    t0 = time.time()
    try:
        graph = extract_graph(REPO)
    except Exception as e:
        print(f"EXTRACT FAILED: {e}")
        traceback.print_exc()
        return
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    print(f"   {n_mod} mod, {n_sym} sym ({t_extract:.1f}s)")
    sys.stdout.flush()

    print(f"2. Rendering clue for: {TASK['task_id']}...")
    sys.stdout.flush()
    t0 = time.time()
    try:
        clue = render_mrlf(graph, TASK["question"], repo_root=str(REPO))
    except Exception as e:
        print(f"RENDER FAILED: {e}")
        traceback.print_exc()
        return
    t_render = time.time() - t0
    print(f"   Render completed in {t_render:.1f}s")
    sys.stdout.flush()

    print("3. Counting tokens...")
    sys.stdout.flush()
    t0 = time.time()
    toks = _token_count(clue)
    words = _word_count(clue)
    t_count = time.time() - t0
    pct = toks / BUDGET_TOTAL * 100
    print(f"   {words} words, {toks} tokens ({pct:.0f}% budget) ({t_count:.1f}s)")

    # Save
    clue_path = OUT / f"{TASK['task_id']}.codeclue"
    clue_path.write_text(clue, encoding="utf-8")

    # Check gold symbols
    print("4. Gold symbol check:")
    for g in TASK["gold_symbols"]:
        found = g in clue
        print(f"   {g:25s} -> {'FOUND' if found else 'MISSING'}")

    print("DONE")


if __name__ == "__main__":
    main()
