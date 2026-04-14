"""Validation test: Run MRLF on Nest (TypeScript) — untested repo.

Tests:
  1. Extraction works for TypeScript
  2. Clue fits under 4150 token budget
  3. Render completes in reasonable time
  4. Gold symbols present in clue
  5. Localization scoring against gold tasks

Writes all output to experiments/runs/mrlf-benchmark/nest-validation.log
"""
import sys
import time
import json
import traceback
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/nest-validation.log")
LOG.parent.mkdir(parents=True, exist_ok=True)
log_file = LOG.open("w", encoding="utf-8", buffering=1)
orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

REPO = Path("experiments/external-repos/nest")
OUT = Path("experiments/runs/mrlf-benchmark")

# Nest gold tasks (5 TFs)
TASKS = [
    {
        "task_id": "nest-tf1-module-refactor",
        "repo": "nest",
        "repo_path": str(REPO),
        "family": "TF1",
        "question": "How would you refactor the NestJS dependency injection container to support lazy loading of modules?",
        "gold_files": ["packages/core/injector/injector.ts", "packages/core/injector/module.ts"],
        "gold_symbols": ["Injector", "Module", "ModuleRef"],
        "gold_facts": ["Injector resolves dependencies via a provider registry",
                       "Module wraps providers, controllers, and imports for a feature boundary",
                       "ModuleRef provides runtime access to the module's provider scope"]
    },
    {
        "task_id": "nest-tf2-middleware-impact",
        "repo": "nest",
        "repo_path": str(REPO),
        "family": "TF2",
        "question": "What is the downstream impact of modifying the NestJS middleware pipeline?",
        "gold_files": ["packages/core/middleware/middleware-module.ts", "packages/core/router/router-module.ts"],
        "gold_symbols": ["MiddlewareModule", "RoutesResolver", "MiddlewareContainer"],
        "gold_facts": ["MiddlewareModule registers and resolves middleware for routes",
                       "RoutesResolver maps controller routes to handlers",
                       "Middleware executes before guards and interceptors in the request pipeline"]
    },
    {
        "task_id": "nest-tf3-guard-integration",
        "repo": "nest",
        "repo_path": str(REPO),
        "family": "TF3",
        "question": "Where should I add a custom guard and what integration points exist in NestJS?",
        "gold_files": ["packages/core/guards/guards-consumer.ts", "packages/common/decorators/core/use-guards.decorator.ts"],
        "gold_symbols": ["GuardsConsumer", "UseGuards", "CanActivate"],
        "gold_facts": ["GuardsConsumer iterates guards and calls canActivate on each",
                       "UseGuards decorator attaches guard metadata to controllers or handlers",
                       "Guards implement CanActivate interface with canActivate method"]
    },
    {
        "task_id": "nest-tf4-exception-handling",
        "repo": "nest",
        "repo_path": str(REPO),
        "family": "TF4",
        "question": "Trace the exception handling flow in NestJS. What could go wrong?",
        "gold_files": ["packages/core/exceptions/base-exception-filter.ts", "packages/core/router/router-execution-context.ts"],
        "gold_symbols": ["BaseExceptionFilter", "RouterExecutionContext", "ExceptionsHandler"],
        "gold_facts": ["BaseExceptionFilter catches unhandled exceptions and sends HTTP error responses",
                       "RouterExecutionContext creates the execution pipeline for each route handler",
                       "ExceptionsHandler wraps route execution to catch and delegate exceptions"]
    },
    {
        "task_id": "nest-tf5-auth-security",
        "repo": "nest",
        "repo_path": str(REPO),
        "family": "TF5",
        "question": "What security patterns exist for authentication and authorization in NestJS core?",
        "gold_files": ["packages/core/guards/guards-consumer.ts", "packages/common/decorators/core/use-guards.decorator.ts"],
        "gold_symbols": ["GuardsConsumer", "UseGuards", "SetMetadata"],
        "gold_facts": ["Guards are the primary mechanism for auth in NestJS",
                       "SetMetadata decorator attaches role/permission data to route handlers",
                       "Guards execute after middleware but before interceptors"]
    },
]

try:
    print(f"=== Nest TypeScript Validation Test ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repo: {REPO} ({sum(1 for _ in REPO.rglob('*.ts'))} .ts files)")

    # Count raw tokens
    print(f"\nCounting raw source tokens...", flush=True)
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    raw_tokens = 0
    raw_files = 0
    for f in REPO.rglob("*.ts"):
        rel = f.relative_to(REPO)
        parts = set(str(rel).replace("\\", "/").split("/"))
        if parts & {"node_modules", ".git", "dist", "test", "tests", "__tests__"}:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            raw_tokens += len(enc.encode(text))
            raw_files += 1
        except OSError:
            pass
    print(f"Raw source: {raw_tokens:,} tokens across {raw_files} files", flush=True)

    # Extract
    print(f"\nExtracting graph...", flush=True)
    t0 = time.time()
    from codeclue_research.extractor import extract_graph
    from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, BUDGET_TOTAL
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    print(f"Extraction: {t_extract:.1f}s ({n_mod} mod, {n_sym} sym, {len(graph.edges)} edges)", flush=True)

    # Render + score each task
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

            # Gold check
            hits = sum(1 for g in task["gold_symbols"] if g in clue)
            total = len(task["gold_symbols"])

            # File check
            file_hits = sum(1 for gf in task["gold_files"]
                          if any(gf.split("/")[-1] in line for line in clue.split("\n")))
            file_total = len(task["gold_files"])

            ccr = 1 - (toks / raw_tokens) if raw_tokens > 0 else 0

            print(f"  OK: {t_render:.1f}s, {toks} tok ({pct:.0f}%), "
                  f"gold_sym={hits}/{total}, gold_files={file_hits}/{file_total}, "
                  f"CCR={ccr:.4f}, budget={'PASS' if budget_ok else 'FAIL'}", flush=True)

            results.append({
                "task_id": task["task_id"], "family": task["family"],
                "render_time_s": round(t_render, 1), "tokens": toks,
                "budget_pct": round(pct, 1), "budget_ok": budget_ok,
                "ccr": round(ccr, 4),
                "gold_sym": f"{hits}/{total}", "gold_files": f"{file_hits}/{file_total}",
                "status": "OK"
            })
        except Exception as e:
            t_render = time.time() - t0
            print(f"  FAILED: {t_render:.1f}s - {type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            results.append({"task_id": task["task_id"], "status": "FAIL", "error": str(e)})

    # Summary
    ok = sum(1 for r in results if r["status"] == "OK")
    budgets_ok = sum(1 for r in results if r.get("budget_ok"))
    mean_time = sum(r.get("render_time_s", 0) for r in results) / len(results) if results else 0

    print(f"\n{'='*70}")
    print(f"NEST VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"  Graph:        {n_mod} modules, {n_sym} symbols, {len(graph.edges)} edges")
    print(f"  Raw source:   {raw_tokens:,} tokens across {raw_files} files")
    print(f"  Extract time: {t_extract:.1f}s")
    print(f"  Tasks:        {ok}/{len(results)} OK")
    print(f"  Budget:       {budgets_ok}/{ok} under ceiling")
    print(f"  Mean render:  {mean_time:.1f}s")
    for r in results:
        print(f"  {r['task_id']:40s} {r.get('render_time_s',0):>5.1f}s "
              f"{r.get('tokens','?'):>5} tok {r.get('gold_sym','?'):>5} sym "
              f"{r.get('gold_files','?'):>5} files {r['status']}")

    # Save
    (OUT / "nest-validation.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved.")

except Exception as e:
    print(f"FATAL: {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()
finally:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    log_file.close()
    print(LOG.read_text(encoding="utf-8"))
