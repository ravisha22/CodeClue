"""Held-out validation: Phase 3+4 on tasks the extractor was NEVER tuned against.

This script MUST be run without modifying the extractor or renderer first.
It measures generalization, not training performance.
"""

import json
import re
import time
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, _token_count

GOLD_PATH = Path("experiments/runs/mrlf-benchmark/heldout-gold-tasks.json")
OUT_DIR = Path("experiments/runs/mrlf-benchmark")


def _stem(w: str) -> str:
    if w.endswith("ing") and len(w) > 5:
        return w[:-3]
    if w.endswith("ed") and len(w) > 4:
        return w[:-2]
    if w.endswith("s") and len(w) > 4:
        return w[:-1]
    return w


def extract_mentioned_symbols(clue_text: str) -> set[str]:
    symbols = set()
    in_sym = False
    for line in clue_text.split("\n"):
        if line.strip() == "-- SYM":
            in_sym = True
            continue
        if line.startswith("-- ") and in_sym:
            in_sym = False
            continue
        if in_sym and line.strip() and not line.strip().startswith("..."):
            first_token = line.split()[0] if line.split() else ""
            if first_token and len(first_token) > 1:
                symbols.add(first_token)
                if "." in first_token:
                    symbols.add(first_token.rsplit(".", 1)[-1])
    in_focus = False
    for line in clue_text.split("\n"):
        if line.strip() == "-- FOCUS":
            in_focus = True
            continue
        if line.startswith("-- ") and in_focus:
            in_focus = False
            continue
        if in_focus and line.strip() and not line.startswith("  "):
            paren_pos = line.find(" (")
            if paren_pos > 0:
                sym = line[:paren_pos].strip()
                if sym:
                    symbols.add(sym)
    for match in re.finditer(r'\b([A-Z]\w+)\b', clue_text):
        symbols.add(match.group(1))
    for match in re.finditer(r'\b([a-z_]\w{2,})\b', clue_text):
        name = match.group(1)
        if name not in {'the', 'and', 'for', 'not', 'function', 'class', 'module',
                       'extends', 'imports', 'calls', 'called_by', 'raises', 'attrs',
                       'files', 'symbols', 'more', 'modules', 'async_function', 'uses'}:
            symbols.add(name)
    return symbols


def score_fact(clue_text: str, fact: str) -> str:
    stop = {"the", "and", "for", "not", "but", "that", "this", "with", "from",
            "are", "was", "has", "have", "been", "each", "when", "only",
            "all", "can", "does", "which", "will", "into", "via", "per",
            "uses", "used", "method", "class", "function", "module"}
    fact_words = set(re.findall(r"[a-zA-Z_]\w{3,}", fact.lower())) - stop
    stemmed_fact = {_stem(w) for w in fact_words}
    clue_lower = clue_text.lower()
    clue_words = set(re.findall(r"[a-zA-Z_]\w{3,}", clue_lower))
    stemmed_clue = {_stem(w) for w in clue_words}

    found = 0
    for w in fact_words:
        if w in clue_lower:
            found += 1
        elif _stem(w) in stemmed_clue:
            found += 0.8
    total = len(fact_words)
    if total == 0:
        return "ANSWERABLE"
    ratio = found / total
    if ratio >= 0.6:
        return "ANSWERABLE"
    elif ratio >= 0.3:
        return "PARTIAL"
    else:
        return "MISSING"


def main():
    golds = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    print("=" * 80)
    print("HELD-OUT VALIDATION — Tasks the extractor was NEVER tuned against")
    print("=" * 80)

    # Group by repo
    repos = {}
    for g in golds:
        repos.setdefault(g["repo"], []).append(g)

    results = []
    for repo_name, tasks in sorted(repos.items()):
        repo_path = Path(tasks[0]["repo_path"])
        if not repo_path.exists():
            print(f"\n  {repo_name}: SKIP (repo not found)")
            continue

        print(f"\n  {repo_name}: extracting...", end=" ", flush=True)
        t0 = time.time()
        graph = extract_graph(repo_path)
        print(f"({time.time()-t0:.1f}s)")

        for gold in tasks:
            clue = render_mrlf(graph, gold["question"], repo_root=str(repo_path))
            toks = _token_count(clue)

            # Save clue
            clue_file = OUT_DIR / f"{gold['task_id']}.codeclue"
            clue_file.write_text(clue, encoding="utf-8")

            # Phase 3: localization
            mentioned_syms = extract_mentioned_symbols(clue)
            mentioned_files = set(re.findall(r'[\w./\-]+\.\w{1,4}', clue))
            gold_syms = set(gold["gold_symbols"])
            gold_files = set(gold["gold_files"])

            sym_hits = sum(1 for gs in gold_syms
                         if gs in mentioned_syms
                         or gs.rsplit(".", 1)[-1] in mentioned_syms
                         or any(gs.lower() == ms.lower() for ms in mentioned_syms))
            sym_recall = sym_hits / len(gold_syms) if gold_syms else 1.0

            file_hits = sum(1 for gf in gold_files
                          if any(gf.split("/")[-1] == mf.split("/")[-1] for mf in mentioned_files))
            file_recall = file_hits / len(gold_files) if gold_files else 1.0

            loc = 0.4 * file_recall + 0.6 * sym_recall
            loc_suff = loc >= 0.60

            # Phase 4: consumption
            fact_scores = []
            for fact in gold.get("gold_facts", []):
                score = score_fact(clue, fact)
                fact_scores.append({"fact": fact, "score": score})

            answerable = sum(1 for fs in fact_scores if fs["score"] == "ANSWERABLE")
            partial = sum(1 for fs in fact_scores if fs["score"] == "PARTIAL")
            missing = sum(1 for fs in fact_scores if fs["score"] == "MISSING")
            total_facts = len(fact_scores)
            fidelity = (answerable * 1.0 + partial * 0.5) / total_facts if total_facts else 0
            fid_suff = fidelity >= 0.60

            result = {
                "task_id": gold["task_id"],
                "repo": gold["repo"],
                "family": gold["family"],
                "tokens": toks,
                "loc": round(loc, 3),
                "sym_recall": round(sym_recall, 3),
                "file_recall": round(file_recall, 3),
                "loc_sufficient": loc_suff,
                "fidelity": round(fidelity, 3),
                "answerable": answerable,
                "partial": partial,
                "missing": missing,
                "fid_sufficient": fid_suff,
                "fact_scores": fact_scores,
            }
            results.append(result)

            loc_status = "PASS" if loc_suff else "FAIL"
            fid_status = "PASS" if fid_suff else "FAIL"
            print(f"    {gold['task_id']:45s} loc={loc:.3f}({loc_status}) "
                  f"fid={fidelity:.3f}({fid_status}) A={answerable} P={partial} M={missing} "
                  f"tok={toks}")

    # Summary
    print("\n" + "=" * 80)
    print("HELD-OUT SUMMARY")
    print("=" * 80)

    total = len(results)
    loc_pass = sum(1 for r in results if r["loc_sufficient"])
    fid_pass = sum(1 for r in results if r["fid_sufficient"])
    mean_loc = sum(r["loc"] for r in results) / total if total else 0
    mean_fid = sum(r["fidelity"] for r in results) / total if total else 0

    print(f"\n  Held-out tasks:      {total}")
    print(f"  Phase 3 (loc):       {loc_pass}/{total} sufficient (mean={mean_loc:.3f})")
    print(f"  Phase 4 (fidelity):  {fid_pass}/{total} sufficient (mean={mean_fid:.3f})")
    print(f"  Held-out DFCR:       {fid_pass/total:.3f}" if total else "  N/A")
    print(f"  Held-out DDR:        {(total-fid_pass)/total:.3f}" if total else "  N/A")

    # Compare with development set
    print(f"\n  --- COMPARISON ---")
    print(f"  Development DFCR:    0.750 (15/20)")
    print(f"  Held-out DFCR:       {fid_pass/total:.3f} ({fid_pass}/{total})" if total else "  N/A")
    gap = 0.750 - (fid_pass/total) if total else 0
    print(f"  Overfitting gap:     {gap:+.3f}")
    if gap > 0.10:
        print(f"  WARNING: Gap > 0.10 — improvements may be overfit to development set")
    elif gap > 0.05:
        print(f"  CAUTION: Gap > 0.05 — some overfitting possible")
    else:
        print(f"  OK: Gap <= 0.05 — improvements appear to generalize")

    # Per-repo breakdown
    print(f"\n  Per-repo held-out:")
    by_repo = {}
    for r in results:
        by_repo.setdefault(r["repo"], []).append(r)
    for repo, rs in sorted(by_repo.items()):
        rp = sum(1 for r in rs if r["fid_sufficient"])
        print(f"    {repo:12s}: {rp}/{len(rs)} fid-sufficient")

    # Save results
    out_file = OUT_DIR / "heldout-validation-results.json"
    json.dump({"total": total, "loc_pass": loc_pass, "fid_pass": fid_pass,
               "mean_loc": round(mean_loc, 3), "mean_fid": round(mean_fid, 3),
               "heldout_dfcr": round(fid_pass/total, 3) if total else 0,
               "dev_dfcr": 0.750, "overfitting_gap": round(gap, 3),
               "per_task": results},
              open(out_file, "w"), indent=2)
    print(f"\n  Results saved to {out_file}")


if __name__ == "__main__":
    main()
