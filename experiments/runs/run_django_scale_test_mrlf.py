"""Django scale test: extract graph, render MRLF clue, measure tokens and budget.

Also runs the focus diagnostic for 5 Django gold tasks.
"""
import json
import time
from pathlib import Path

import tiktoken

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import (
    render_mrlf, generate_detail_store, write_detail_store,
    _token_count, _word_count, BUDGET_TOTAL,
)

ENC = tiktoken.get_encoding("cl100k_base")

REPO = Path("experiments/external-repos/django")
OUT = Path("experiments/runs/mrlf-benchmark")

# Django gold tasks (TF1-TF5)
DJANGO_GOLDS = [
    {
        "task_id": "django-tf1-settings-refactor",
        "repo": "django",
        "family": "TF1",
        "question": "How would you refactor Django settings loading to support multiple config sources?",
        "gold_files": ["django/conf/__init__.py", "django/conf/global_settings.py"],
        "gold_symbols": ["LazySettings", "Settings", "UserSettingsHolder"],
        "gold_facts": ["LazySettings is a lazy proxy that defers import until first access",
                       "Settings reads DJANGO_SETTINGS_MODULE environment variable",
                       "UserSettingsHolder supports per-test overrides"]
    },
    {
        "task_id": "django-tf2-middleware-impact",
        "repo": "django",
        "family": "TF2",
        "question": "What is the downstream impact of modifying Django middleware handling?",
        "gold_files": ["django/core/handlers/base.py", "django/utils/deprecation.py"],
        "gold_symbols": ["BaseHandler", "MiddlewareMixin", "get_response"],
        "gold_facts": ["BaseHandler._get_response chains middleware callables",
                       "MiddlewareMixin provides backward compat for old-style middleware",
                       "Middleware ordering in MIDDLEWARE setting controls execution order"]
    },
    {
        "task_id": "django-tf3-admin-customization",
        "repo": "django",
        "family": "TF3",
        "question": "Where should I add custom admin actions and what integration points exist?",
        "gold_files": ["django/contrib/admin/options.py", "django/contrib/admin/sites.py"],
        "gold_symbols": ["ModelAdmin", "AdminSite", "get_action"],
        "gold_facts": ["ModelAdmin.get_actions returns available actions for the changelist",
                       "AdminSite.register connects model to admin interface",
                       "Actions are callables that receive queryset and request"]
    },
    {
        "task_id": "django-tf4-orm-query-execution",
        "repo": "django",
        "family": "TF4",
        "question": "Trace how a Django ORM queryset executes a SQL query. What could go wrong?",
        "gold_files": ["django/db/models/query.py", "django/db/models/sql/query.py", "django/db/models/sql/compiler.py"],
        "gold_symbols": ["QuerySet", "Query", "SQLCompiler"],
        "gold_facts": ["QuerySet is lazy - SQL only executes on iteration/evaluation",
                       "Query builds the SQL AST which SQLCompiler converts to SQL string",
                       "N+1 queries occur when accessing related objects without select_related"]
    },
    {
        "task_id": "django-tf5-csrf-protection",
        "repo": "django",
        "family": "TF5",
        "question": "What security mechanisms implement CSRF protection in Django?",
        "gold_files": ["django/middleware/csrf.py", "django/template/defaulttags.py"],
        "gold_symbols": ["CsrfViewMiddleware", "csrf_protect", "csrf_token"],
        "gold_facts": ["CsrfViewMiddleware checks POST requests for valid CSRF token",
                       "Token is generated per-session and rotated",
                       "csrf_exempt decorator skips CSRF check for specific views"]
    },
]


def count_raw_tokens(repo_path: Path) -> tuple[int, int]:
    """Count raw Python source tokens excluding tests/docs."""
    exclude = {"__pycache__", ".git", ".tox", "tests", "test", "docs"}
    total = 0
    count = 0
    for f in repo_path.rglob("*.py"):
        parts = set(f.relative_to(repo_path).parts)
        if parts & exclude:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            total += len(ENC.encode(text))
            count += 1
        except OSError:
            pass
    return total, count


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    if not REPO.exists():
        print("Django repo not found at", REPO)
        return

    # Step 1: Count raw tokens
    print("Step 1: Counting raw Django source tokens...")
    t0 = time.time()
    raw_tokens, raw_files = count_raw_tokens(REPO)
    print(f"  {raw_tokens:,} tokens across {raw_files} files ({time.time()-t0:.1f}s)")

    # Step 2: Extract graph
    print("Step 2: Extracting Django graph...")
    t0 = time.time()
    graph = extract_graph(REPO)
    t_extract = time.time() - t0
    n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
    n_sym = len(graph.nodes) - n_mod
    n_edges = len(graph.edges)
    print(f"  {n_mod} modules, {n_sym} symbols, {n_edges} edges ({t_extract:.1f}s)")

    # Step 3: Render MRLF clue for each gold task
    print("Step 3: Rendering MRLF clues for 5 Django tasks...")
    results = []

    for gold in DJANGO_GOLDS:
        t0 = time.time()
        clue = render_mrlf(graph, gold["question"], repo_root=str(REPO))
        t_render = time.time() - t0
        toks = _token_count(clue)
        words = _word_count(clue)
        pct = toks / BUDGET_TOTAL * 100

        # Save clue
        clue_path = OUT / f"{gold['task_id']}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")

        # Score localization
        from experiments.runs.run_phase3_localization import score_task
        score = score_task(clue, gold)

        ccr = 1 - (toks / raw_tokens) if raw_tokens > 0 else 0
        status = "PASS" if score["sufficient"] else "FAIL"

        print(f"  {gold['task_id']:35s} tok={toks:>5d} ({pct:.0f}%) "
              f"loc={score['localization_accuracy']:.3f} "
              f"files={score['file_hits']} sym={score['sym_hits']} "
              f"{status}  ({t_render:.1f}s)")

        results.append({
            **score,
            "clue_tokens": toks,
            "budget_pct": round(pct, 1),
            "ccr": round(ccr, 4),
            "render_time_s": round(t_render, 1),
        })

    # Step 4: Generate detail store
    print("Step 4: Generating detail store...")
    t0 = time.time()
    detail = generate_detail_store(graph, repo_root=str(REPO))
    t_detail = time.time() - t0
    detail_path = OUT / "django.codeclue-detail"
    write_detail_store(detail, detail_path)
    detail_kb = detail_path.stat().st_size / 1024
    print(f"  {len(detail)} records, {detail_kb:.0f} KB ({t_detail:.1f}s)")

    # Summary
    mean_loc = sum(r["localization_accuracy"] for r in results) / len(results)
    suff = sum(1 for r in results if r["sufficient"])
    mean_toks = sum(r["clue_tokens"] for r in results) / len(results)
    ccr = results[0]["ccr"] if results else 0

    print(f"\n{'='*70}")
    print(f"DJANGO SCALE TEST SUMMARY")
    print(f"{'='*70}")
    print(f"  Graph:        {n_mod} modules, {n_sym} symbols, {n_edges} edges")
    print(f"  Raw source:   {raw_tokens:,} tokens across {raw_files} files")
    print(f"  Mean clue:    {mean_toks:.0f} tokens ({mean_toks/BUDGET_TOTAL*100:.0f}% of budget)")
    print(f"  Budget OK:    {'YES' if all(r['clue_tokens'] <= BUDGET_TOTAL for r in results) else 'NO'}")
    print(f"  CCR:          {ccr:.4f} ({ccr*100:.1f}%)")
    print(f"  Mean loc:     {mean_loc:.3f}")
    print(f"  Sufficient:   {suff}/{len(results)}")
    print(f"  Extract time: {t_extract:.1f}s")

    # Save results
    summary = {
        "repo": "django",
        "modules": n_mod,
        "symbols": n_sym,
        "edges": n_edges,
        "raw_tokens": raw_tokens,
        "raw_files": raw_files,
        "extract_time_s": round(t_extract, 1),
        "detail_records": len(detail),
        "detail_size_kb": round(detail_kb, 1),
        "per_task": results,
        "mean_loc": round(mean_loc, 3),
        "sufficient": f"{suff}/{len(results)}",
        "mean_clue_tokens": round(mean_toks),
        "budget_pass": all(r["clue_tokens"] <= BUDGET_TOTAL for r in results),
    }
    (OUT / "django-scale-test.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(f"\nResults saved to {OUT / 'django-scale-test.json'}")


if __name__ == "__main__":
    main()
