"""Diagnose Django MRLF failure: stage-by-stage timing with file output.

Writes all output to experiments/runs/mrlf-benchmark/django-diagnostic.log
to avoid terminal output capture issues.
"""
import sys
import time
import traceback
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/django-diagnostic.log")
LOG.parent.mkdir(parents=True, exist_ok=True)

# Redirect all output to log file
log_file = LOG.open("w", encoding="utf-8")
orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

REPO = Path("experiments/external-repos/django")

TASKS = [
    ("django-tf1-settings-refactor", "How would you refactor Django settings loading to support multiple config sources?"),
    ("django-tf2-middleware-impact", "What is the downstream impact of modifying Django middleware handling?"),
    ("django-tf3-admin-customization", "Where should I add custom admin actions and what integration points exist?"),
    ("django-tf4-orm-query-execution", "Trace how a Django ORM queryset executes a SQL query. What could go wrong?"),
    ("django-tf5-csrf-protection", "What security mechanisms implement CSRF protection in Django?"),
]

try:
    print(f"=== Django MRLF Diagnostic ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repo: {REPO}")
    print()

    # Stage 1: Extract graph (once, reuse for all tasks)
    print("STAGE 1: Graph extraction")
    sys.stdout.flush()
    t0 = time.time()
    from codeclue_research.extractor import extract_graph
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    n_edges = len(graph.edges)
    print(f"  OK: {n_mod} modules, {n_sym} symbols, {n_edges} edges in {t_extract:.1f}s")
    print(f"  Memory: graph object created")
    print()

    # Stage 2: Render each task with timing
    from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, _word_count, BUDGET_TOTAL

    for task_id, question in TASKS:
        print(f"STAGE 2: Rendering {task_id}")
        sys.stdout.flush()

        # Sub-stage 2a: render_mrlf call
        print(f"  2a: Calling render_mrlf...")
        sys.stdout.flush()
        t0 = time.time()
        try:
            clue = render_mrlf(graph, question, repo_root=str(REPO))
            t_render = time.time() - t0
            print(f"  2a: OK in {t_render:.1f}s, {len(clue)} chars")
        except Exception as e:
            t_render = time.time() - t0
            print(f"  2a: FAILED after {t_render:.1f}s")
            print(f"  2a: Error: {type(e).__name__}: {e}")
            traceback.print_exc()
            print()
            continue

        # Sub-stage 2b: token count
        print(f"  2b: Counting tokens...")
        sys.stdout.flush()
        t0 = time.time()
        try:
            toks = _token_count(clue)
            t_count = time.time() - t0
            words = _word_count(clue)
            pct = toks / BUDGET_TOTAL * 100
            print(f"  2b: OK in {t_count:.1f}s: {words} words, {toks} tokens ({pct:.0f}%)")
        except Exception as e:
            t_count = time.time() - t0
            print(f"  2b: FAILED after {t_count:.1f}s")
            print(f"  2b: Error: {type(e).__name__}: {e}")
            traceback.print_exc()
            print()
            continue

        # Sub-stage 2c: save clue
        out_path = Path("experiments/runs/mrlf-benchmark") / f"{task_id}.codeclue"
        out_path.write_text(clue, encoding="utf-8")
        print(f"  2c: Saved to {out_path}")

        # Sub-stage 2d: check budget
        budget_ok = toks <= BUDGET_TOTAL
        print(f"  Budget: {'PASS' if budget_ok else 'FAIL'} ({toks}/{BUDGET_TOTAL})")
        print()

    print("=== Diagnostic complete ===")

except Exception as e:
    print(f"FATAL ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()

finally:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    log_file.close()
    # Print the log to real stdout
    print(LOG.read_text(encoding="utf-8"))
