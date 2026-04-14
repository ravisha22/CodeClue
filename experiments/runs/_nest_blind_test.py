"""Blind validation: Run MRLF on NestJS (TypeScript repo never tested with current code).

Tests: extraction, rendering, budget, token count, render time.
Writes results to nest-blind-test.log
"""
import sys
import time
import json
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/nest-blind-test.log")
LOG.parent.mkdir(parents=True, exist_ok=True)
log_file = LOG.open("w", encoding="utf-8", buffering=1)
orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

REPO = Path("experiments/external-repos/nest")
OUT = Path("experiments/runs/mrlf-benchmark")

TASKS = [
    {"task_id": "nest-tf1-module-refactor", 
     "question": "How would you refactor NestJS dependency injection to support lazy-loaded modules?",
     "gold_symbols": ["Injector", "Module", "ModuleRef"]},
    {"task_id": "nest-tf2-middleware-impact",
     "question": "What is the downstream impact of modifying NestJS middleware pipeline?",
     "gold_symbols": ["MiddlewareModule", "MiddlewareConsumer", "NestMiddleware"]},
    {"task_id": "nest-tf3-guard-integration",
     "question": "Where should I add custom guards and what integration points exist?",
     "gold_symbols": ["GuardsConsumer", "CanActivate", "AuthGuard"]},
    {"task_id": "nest-tf4-exception-handling",
     "question": "Trace how NestJS handles uncaught exceptions. What could go wrong?",
     "gold_symbols": ["ExceptionHandler", "BaseExceptionFilter", "ExceptionsZone"]},
    {"task_id": "nest-tf5-cors-security",
     "question": "What security mechanisms control CORS and request validation in NestJS?",
     "gold_symbols": ["CorsMiddleware", "ValidationPipe", "ParseIntPipe"]},
]

try:
    import traceback
    from codeclue_research.extractor import extract_graph
    from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, _word_count, BUDGET_TOTAL

    print(f"=== Blind Validation: NestJS ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repo: {REPO}")

    # Extract
    print(f"\nExtracting...", flush=True)
    t0 = time.time()
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    print(f"Extraction: {t_extract:.1f}s ({n_mod} mod, {n_sym} sym, {len(graph.edges)} edges)", flush=True)

    # Render each task
    results = []
    for task in TASKS:
        print(f"\nRendering {task['task_id']}...", flush=True)
        t0 = time.time()
        try:
            clue = render_mrlf(graph, task["question"], repo_root=str(REPO))
            t_render = time.time() - t0
            toks = _token_count(clue)
            words = _word_count(clue)
            pct = toks / BUDGET_TOTAL * 100
            budget_ok = toks <= BUDGET_TOTAL

            (OUT / f"{task['task_id']}.codeclue").write_text(clue, encoding="utf-8")

            hits = sum(1 for g in task["gold_symbols"] if g in clue)
            total = len(task["gold_symbols"])

            print(f"  OK: {t_render:.1f}s, {words} words, {toks} tok ({pct:.0f}%), gold={hits}/{total}, budget={'PASS' if budget_ok else 'FAIL'}", flush=True)
            results.append({"task": task["task_id"], "time_s": round(t_render, 1),
                           "tokens": toks, "words": words, "budget_pct": round(pct, 1),
                           "budget_ok": budget_ok, "gold_hits": f"{hits}/{total}", "status": "OK"})
        except Exception as e:
            t_render = time.time() - t0
            print(f"  FAILED: {t_render:.1f}s - {type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            results.append({"task": task["task_id"], "time_s": round(t_render, 1),
                           "status": "FAIL", "error": str(e)})

    # Summary
    ok = sum(1 for r in results if r["status"] == "OK")
    budgets = sum(1 for r in results if r.get("budget_ok"))
    mean_time = sum(r["time_s"] for r in results) / len(results) if results else 0
    mean_toks = sum(r.get("tokens", 0) for r in results if r["status"] == "OK") / max(ok, 1)

    print(f"\n=== SUMMARY ===")
    print(f"Tasks:       {ok}/{len(results)} OK")
    print(f"Budget:      {budgets}/{ok} under ceiling")
    print(f"Mean render: {mean_time:.1f}s")
    print(f"Mean tokens: {mean_toks:.0f}")
    for r in results:
        print(f"  {r['task']:40s} {r.get('time_s',0):>6.1f}s {r.get('tokens','?'):>5} tok {r.get('gold_hits','?')} {r['status']}")

    (OUT / "nest-blind-test.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

except Exception as e:
    import traceback
    print(f"FATAL: {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()
finally:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    log_file.close()
    print(LOG.read_text(encoding="utf-8"))
