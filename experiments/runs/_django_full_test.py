"""Django full 5-task test with profiled render_mrlf.

Writes all output to django-full-test.log.
"""
import sys
import time
import json
import traceback
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/django-full-test.log")
LOG.parent.mkdir(parents=True, exist_ok=True)
log_file = LOG.open("w", encoding="utf-8", buffering=1)  # line-buffered
orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

REPO = Path("experiments/external-repos/django")
OUT = Path("experiments/runs/mrlf-benchmark")

TASKS = [
    {"task_id": "django-tf1-settings-refactor", "question": "How would you refactor Django settings loading to support multiple config sources?",
     "gold_symbols": ["LazySettings", "Settings", "UserSettingsHolder"]},
    {"task_id": "django-tf2-middleware-impact", "question": "What is the downstream impact of modifying Django middleware handling?",
     "gold_symbols": ["BaseHandler", "MiddlewareMixin", "get_response"]},
    {"task_id": "django-tf3-admin-customization", "question": "Where should I add custom admin actions and what integration points exist?",
     "gold_symbols": ["ModelAdmin", "AdminSite", "get_action"]},
    {"task_id": "django-tf4-orm-query-execution", "question": "Trace how a Django ORM queryset executes a SQL query. What could go wrong?",
     "gold_symbols": ["QuerySet", "Query", "SQLCompiler"]},
    {"task_id": "django-tf5-csrf-protection", "question": "What security mechanisms implement CSRF protection in Django?",
     "gold_symbols": ["CsrfViewMiddleware", "csrf_protect", "csrf_token"]},
]

try:
    print(f"=== Django Full 5-Task Test ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Extract once
    print(f"\nExtracting graph...", flush=True)
    t0 = time.time()
    from codeclue_research.extractor import extract_graph
    from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, BUDGET_TOTAL
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    print(f"Extraction: {t_extract:.1f}s ({n_mod} mod, {n_sym} sym, {len(graph.edges)} edges)", flush=True)

    results = []
    for task in TASKS:
        print(f"\nRendering {task['task_id']}...", flush=True)
        t0 = time.time()
        try:
            clue = render_mrlf(graph, task["question"], repo_root=str(REPO))
            t_render = time.time() - t0
            toks = _token_count(clue)
            pct = toks / BUDGET_TOTAL * 100
            budget_ok = toks <= BUDGET_TOTAL

            # Save
            (OUT / f"{task['task_id']}.codeclue").write_text(clue, encoding="utf-8")

            # Check gold
            hits = sum(1 for g in task["gold_symbols"] if g in clue)
            total = len(task["gold_symbols"])

            print(f"  OK: {t_render:.1f}s, {toks} tok ({pct:.0f}%), gold={hits}/{total}, budget={'PASS' if budget_ok else 'FAIL'}", flush=True)
            results.append({"task": task["task_id"], "time_s": round(t_render, 1), "tokens": toks,
                           "budget_pct": round(pct, 1), "budget_ok": budget_ok,
                           "gold_hits": f"{hits}/{total}", "status": "OK"})
        except Exception as e:
            t_render = time.time() - t0
            print(f"  FAILED: {t_render:.1f}s - {type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            results.append({"task": task["task_id"], "time_s": round(t_render, 1),
                           "status": "FAIL", "error": str(e)})

    # Summary
    ok = sum(1 for r in results if r["status"] == "OK")
    budgets = [r for r in results if r.get("budget_ok")]
    print(f"\n=== SUMMARY ===")
    print(f"Tasks: {ok}/{len(results)} OK")
    print(f"Budget: {len(budgets)}/{ok} under ceiling")
    mean_time = sum(r["time_s"] for r in results) / len(results)
    print(f"Mean render time: {mean_time:.1f}s")
    for r in results:
        print(f"  {r['task']:40s} {r.get('time_s',0):>6.1f}s {r.get('tokens','?'):>5} tok {r.get('gold_hits','?')} {r['status']}")

    # Save JSON
    (OUT / "django-full-test.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {OUT / 'django-full-test.json'}")

except Exception as e:
    print(f"FATAL: {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()
finally:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    log_file.close()
    print(LOG.read_text(encoding="utf-8"))
