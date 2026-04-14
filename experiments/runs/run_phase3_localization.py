"""Phase 3: Localization scoring for MRLF clues.

For each gold task:
  1. Parse the MRLF clue text
  2. Extract all mentioned file paths and symbol names
  3. Compare against gold files and gold symbols
  4. Compute file_recall, symbol_recall, localization_accuracy, sufficient

Scoring formula (same as v0.8.1 for direct comparison):
  loc = 0.4 * file_recall + 0.6 * symbol_recall
  sufficient = loc >= 0.60
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, _token_count


def extract_mentioned_files(clue_text: str) -> set[str]:
    """Extract all file paths mentioned in the MRLF clue."""
    files = set()
    # Match patterns like: src/flask/app.py, httpx/_auth.py, auth.go, etc.
    for match in re.finditer(r'[\w./\-]+\.\w{1,4}', clue_text):
        candidate = match.group()
        # Filter: must look like a file path (has extension, not a URL)
        if '/' in candidate or candidate.endswith(('.py', '.go', '.ts', '.js', '.tsx', '.jsx')):
            files.add(candidate)
        elif re.match(r'^[\w_]+\.\w{1,4}$', candidate):
            # Root-level files like gin.go, context.go
            files.add(candidate)
    return files


def extract_mentioned_symbols(clue_text: str) -> set[str]:
    """Extract all symbol names mentioned in the MRLF clue.
    
    Three extraction strategies:
    1. Parse L2 SYM section structurally (first column of each line)
    2. Parse L3 FOCUS section structurally (symbol name before parentheses)
    3. Regex fallback for symbols mentioned anywhere else
    """
    symbols = set()
    
    # Strategy 1: Parse L2 SYM lines — first whitespace-delimited token per line
    in_sym = False
    for line in clue_text.split("\n"):
        if line.strip() == "-- SYM":
            in_sym = True
            continue
        if line.startswith("-- ") and in_sym:
            in_sym = False
            continue
        if in_sym and line.strip() and not line.strip().startswith("..."):
            # First token is the symbol name
            first_token = line.split()[0] if line.split() else ""
            if first_token and len(first_token) > 1:
                symbols.add(first_token)
                # Also add the short name if it's qualified
                if "." in first_token:
                    symbols.add(first_token.rsplit(".", 1)[-1])
    
    # Strategy 2: Parse L3 FOCUS entries — "SymbolName (file:lines)" pattern
    in_focus = False
    for line in clue_text.split("\n"):
        if line.strip() == "-- FOCUS":
            in_focus = True
            continue
        if line.startswith("-- ") and in_focus:
            in_focus = False
            continue
        if in_focus and line.strip() and not line.startswith("  "):
            # Focus entry header: "symbol_name (file:line-line)"
            paren_pos = line.find(" (")
            if paren_pos > 0:
                sym = line[:paren_pos].strip()
                if sym:
                    symbols.add(sym)
                    if "." in sym:
                        symbols.add(sym.rsplit(".", 1)[-1])
    
    # Strategy 3: Regex fallback — PascalCase and snake_case identifiers
    for match in re.finditer(r'\b([A-Z]\w+(?:\.[a-z_A-Z]\w+)*)\b', clue_text):
        symbols.add(match.group(1))
        # Also add short form
        name = match.group(1)
        if "." in name:
            symbols.add(name.rsplit(".", 1)[-1])
    
    for match in re.finditer(r'\b([a-z_]\w{2,})\b', clue_text):
        name = match.group(1)
        if name not in {'the', 'and', 'for', 'not', 'but', 'that', 'this', 'with',
                       'from', 'are', 'was', 'has', 'have', 'been', 'more',
                       'modules', 'symbols', 'files', 'words', 'tokens', 'mod', 'sym',
                       'tree', 'index', 'focus', 'gaps', 'drill', 'called_by', 'calls',
                       'lines', 'function', 'class', 'module', 'async_function',
                       'files', 'extracting', 'rendering', 'impact', 'modifying',
                       'downstream', 'configuration', 'loading', 'what'}:
            symbols.add(name)
    
    return symbols


def score_task(clue_text: str, gold: dict) -> dict:
    """Score a single task against its gold answer."""
    mentioned_files = extract_mentioned_files(clue_text)
    mentioned_symbols = extract_mentioned_symbols(clue_text)

    # File recall: fraction of gold files found in clue
    gold_files = set(gold["gold_files"])
    if gold_files:
        # Partial match: gold file "src/flask/app.py" matches if "flask/app.py" or "app.py" appears
        file_hits = 0
        for gf in gold_files:
            gf_parts = gf.split("/")
            # Check if full path or any suffix appears
            found = False
            for mf in mentioned_files:
                if gf == mf or gf.endswith("/" + mf) or mf.endswith("/" + gf.split("/")[-1]):
                    found = True
                    break
                # Also check if just the filename matches
                if gf.split("/")[-1] == mf.split("/")[-1]:
                    found = True
                    break
            if found:
                file_hits += 1
        file_recall = file_hits / len(gold_files)
    else:
        file_recall = 1.0

    # Symbol recall: fraction of gold symbols found in clue
    gold_symbols = set(gold["gold_symbols"])
    if gold_symbols:
        sym_hits = 0
        for gs in gold_symbols:
            # Check exact match, or match just the short name
            gs_short = gs.rsplit(".", 1)[-1] if "." in gs else gs
            found = gs in mentioned_symbols or gs_short in mentioned_symbols
            if not found:
                # Check if it appears as substring of any mentioned symbol
                for ms in mentioned_symbols:
                    if gs_short.lower() == ms.lower():
                        found = True
                        break
            if found:
                sym_hits += 1
        symbol_recall = sym_hits / len(gold_symbols)
    else:
        symbol_recall = 1.0

    loc = 0.4 * file_recall + 0.6 * symbol_recall
    sufficient = loc >= 0.60

    return {
        "task_id": gold["task_id"],
        "repo": gold["repo"],
        "family": gold["family"],
        "file_recall": round(file_recall, 4),
        "symbol_recall": round(symbol_recall, 4),
        "localization_accuracy": round(loc, 4),
        "sufficient": sufficient,
        "file_hits": f"{file_hits if gold_files else 0}/{len(gold_files)}",
        "sym_hits": f"{sym_hits if gold_symbols else 0}/{len(gold_symbols)}",
    }


def main():
    gold_path = Path("experiments/runs/mrlf-benchmark/gold-tasks.json")
    golds = json.loads(gold_path.read_text(encoding="utf-8"))
    out_dir = Path("experiments/runs/mrlf-benchmark")

    results = []
    print("Phase 3: Localization Scoring")
    print("=" * 90)

    # Group golds by repo
    repos = {}
    for g in golds:
        repos.setdefault(g["repo"], []).append(g)

    for repo_name, tasks in sorted(repos.items()):
        repo_path = Path(tasks[0]["repo_path"])
        if not repo_path.exists():
            print(f"\n  {repo_name}: SKIP (repo not found)")
            continue

        print(f"\n  {repo_name}: extracting + rendering...", end=" ", flush=True)
        t0 = time.time()
        graph = extract_graph(repo_path)
        elapsed = time.time() - t0
        print(f"({elapsed:.1f}s)")

        for gold in tasks:
            t0 = time.time()
            clue = render_mrlf(graph, gold["question"], repo_root=str(repo_path))
            t_render = time.time() - t0
            toks = _token_count(clue)

            # Save clue for this specific task
            clue_file = out_dir / f"{gold['task_id']}.codeclue"
            clue_file.write_text(clue, encoding="utf-8")

            # Score
            result = score_task(clue, gold)
            result["clue_tokens"] = toks
            result["render_time_s"] = round(t_render, 2)
            results.append(result)

            status = "PASS" if result["sufficient"] else "FAIL"
            print(f"    {gold['task_id']:40s} loc={result['localization_accuracy']:.3f} "
                  f"files={result['file_hits']} sym={result['sym_hits']} "
                  f"tok={toks:>5d} {status}")

    # Summary
    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)

    # Per-repo averages
    by_repo = {}
    for r in results:
        by_repo.setdefault(r["repo"], []).append(r)

    print(f"\n{'Repo':12s} | {'Mean Loc':>8s} | {'Sufficient':>10s} | {'File Recall':>11s} | {'Sym Recall':>10s}")
    print("-" * 65)
    for repo, rs in sorted(by_repo.items()):
        mean_loc = sum(r["localization_accuracy"] for r in rs) / len(rs)
        suff = sum(1 for r in rs if r["sufficient"])
        mean_fr = sum(r["file_recall"] for r in rs) / len(rs)
        mean_sr = sum(r["symbol_recall"] for r in rs) / len(rs)
        print(f"{repo:12s} | {mean_loc:>8.3f} | {suff:>5d}/{len(rs):<4d} | {mean_fr:>11.3f} | {mean_sr:>10.3f}")

    # Per-TF averages
    by_tf = {}
    for r in results:
        by_tf.setdefault(r["family"], []).append(r)

    print(f"\n{'Family':8s} | {'Mean Loc':>8s} | {'Sufficient':>10s}")
    print("-" * 35)
    for tf, rs in sorted(by_tf.items()):
        mean_loc = sum(r["localization_accuracy"] for r in rs) / len(rs)
        suff = sum(1 for r in rs if r["sufficient"])
        print(f"{tf:8s} | {mean_loc:>8.3f} | {suff:>5d}/{len(rs)}")

    # Overall
    overall_loc = sum(r["localization_accuracy"] for r in results) / len(results) if results else 0
    overall_suff = sum(1 for r in results if r["sufficient"])
    total = len(results)
    print(f"\nOverall: mean_loc={overall_loc:.3f}, sufficient={overall_suff}/{total} ({overall_suff/total*100:.1f}%)")

    # Gates
    flask_rs = by_repo.get("flask", [])
    flask_loc = sum(r["localization_accuracy"] for r in flask_rs) / len(flask_rs) if flask_rs else 0
    gate_overall = overall_loc >= 0.50
    gate_flask = flask_loc >= 0.80
    print(f"\nGate: mean_loc ≥ 0.50: {overall_loc:.3f} → {'PASS' if gate_overall else 'FAIL'}")
    print(f"Gate: Flask loc ≥ 0.80: {flask_loc:.3f} → {'PASS' if gate_flask else 'FAIL'}")

    # Save
    results_path = out_dir / "phase3-localization-results.json"
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
