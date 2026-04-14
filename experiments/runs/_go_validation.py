"""Go validation: Gin + Chi (n=2 Go repos).

Tests the Go extractor with doc comments on two different Go repos.
"""
import sys
import time
import json
import traceback
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/go-validation.log")
LOG.parent.mkdir(parents=True, exist_ok=True)
log_file = LOG.open("w", encoding="utf-8", buffering=1)
orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

OUT = Path("experiments/runs/mrlf-benchmark")

REPOS = {
    "gin": {
        "path": Path("experiments/external-repos/gin"),
        "tasks": [
            {"task_id": "gin-tf1-context-pooling", "question": "How would you refactor context allocation to use object pooling for better performance?",
             "gold_symbols": ["Context", "Engine", "Engine.pool"]},
            {"task_id": "gin-tf2-routing-tree-impact", "question": "What is the downstream impact of changing the routing tree structure?",
             "gold_symbols": ["methodTree", "node", "Engine.trees", "addRoute"]},
            {"task_id": "gin-tf3-middleware-integration", "question": "Where should I add custom middleware, and what are the integration points?",
             "gold_symbols": ["HandlerFunc", "RouterGroup.Use", "HandlersChain", "Context.Next"]},
            {"task_id": "gin-tf4-basic-auth-flow", "question": "Trace how BasicAuth validates credentials. What could fail?",
             "gold_symbols": ["BasicAuth", "BasicAuthForRealm", "authPairs", "searchCredential"]},
            {"task_id": "gin-tf5-credential-handling", "question": "What security controls exist for handling credentials and preventing timing attacks?",
             "gold_symbols": ["Context.Set", "Context.Get", "AuthUserKey", "searchCredential"]},
        ],
    },
    "chi": {
        "path": Path("experiments/external-repos/chi"),
        "tasks": [
            {"task_id": "chi-tf1-router-refactor", "question": "How would you refactor the chi router tree for better performance?",
             "gold_symbols": ["Mux", "node", "addRoute"]},
            {"task_id": "chi-tf2-middleware-impact", "question": "What is the downstream impact of modifying middleware handling in chi?",
             "gold_symbols": ["Mux", "Use", "Handler", "Chain"]},
            {"task_id": "chi-tf3-route-integration", "question": "Where should I add a new route group and what integration points exist in chi?",
             "gold_symbols": ["Route", "Group", "Mount"]},
        ],
    },
}

try:
    print("=== Go Validation: Gin + Chi (n=2) ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    from codeclue_research.extractor import extract_graph
    from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, BUDGET_TOTAL

    all_results = []

    for repo_name, config in REPOS.items():
        repo_path = config["path"]
        if not repo_path.exists():
            print(f"\n{repo_name}: SKIP (not found)")
            continue

        print(f"\n{'='*60}")
        print(f"{repo_name}: Extracting...")
        sys.stdout.flush()
        t0 = time.time()
        graph = extract_graph(repo_path)
        t_extract = time.time() - t0
        n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
        n_sym = len(graph.nodes) - n_mod
        n_edges = len(graph.edges)
        print(f"  {n_mod} mod, {n_sym} sym, {n_edges} edges ({t_extract:.1f}s)")

        # Check doc comment coverage
        has_doc = sum(1 for n in graph.nodes
                     if n.node_type != "module"
                     and n.semantic_contract.get("purpose", "").replace(f"{n.node_type} ", "").replace(f"type ", "") != n.semantic_contract.get("symbol_name", "")
                     and n.semantic_contract.get("purpose", "") not in (f"function {n.semantic_contract.get('symbol_name', '')}", f"type {n.semantic_contract.get('symbol_name', '')}", f"class {n.semantic_contract.get('symbol_name', '')}"))
        print(f"  Symbols with doc comments: {has_doc}/{n_sym} ({has_doc*100//max(n_sym,1)}%)")

        for task in config["tasks"]:
            t0 = time.time()
            try:
                clue = render_mrlf(graph, task["question"], repo_root=str(repo_path))
                t_render = time.time() - t0
                toks = _token_count(clue)
                pct = toks / BUDGET_TOTAL * 100
                budget_ok = toks <= BUDGET_TOTAL
                (OUT / f"{task['task_id']}.codeclue").write_text(clue, encoding="utf-8")

                hits = sum(1 for g in task["gold_symbols"] if g in clue)
                total = len(task["gold_symbols"])

                print(f"  {task['task_id']:35s} {t_render:.1f}s {toks:>5d}tok ({pct:.0f}%) gold={hits}/{total} {'PASS' if budget_ok else 'FAIL'}")
                all_results.append({"task": task["task_id"], "repo": repo_name, "tokens": toks, "budget_ok": budget_ok, "gold": f"{hits}/{total}", "status": "OK"})
            except Exception as e:
                print(f"  {task['task_id']:35s} FAILED: {e}")
                traceback.print_exc()
                all_results.append({"task": task["task_id"], "repo": repo_name, "status": "FAIL", "error": str(e)})

    # Summary
    print(f"\n{'='*60}")
    print("GO VALIDATION SUMMARY")
    ok = sum(1 for r in all_results if r["status"] == "OK")
    budget_ok = sum(1 for r in all_results if r.get("budget_ok"))
    print(f"Tasks: {ok}/{len(all_results)} OK, Budget: {budget_ok}/{ok} pass")
    for r in all_results:
        print(f"  {r['task']:35s} {r.get('tokens','?'):>5} tok {r.get('gold','?'):>5} {r['status']}")

    (OUT / "go-validation.json").write_text(json.dumps(all_results, indent=2), encoding="utf-8")

except Exception as e:
    print(f"FATAL: {e}")
    traceback.print_exc()
finally:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    log_file.close()
    print(LOG.read_text(encoding="utf-8"))
