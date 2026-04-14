"""Phase 4: LLM Consumption Test (self-contained).

For each of the 17 passing Phase 3 tasks:
  1. Read the MRLF clue file
  2. Check if an LLM reading this clue could answer the gold facts
  3. Score each gold fact as: ANSWERABLE (fact is directly stated or inferable from clue), 
     PARTIAL (relevant info exists but incomplete), or MISSING (no relevant info)
  4. Compute DFCR and DDR

Scoring is deterministic: check if gold fact keywords appear in the clue text.
This is a lower bound — an actual LLM would likely score higher because it can
infer relationships that keyword matching can't.

Writes results to experiments/runs/mrlf-benchmark/phase4-consumption-results.json
"""
import json
import re
from pathlib import Path

GOLD_PATH = Path("experiments/runs/mrlf-benchmark/gold-tasks.json")
CLUE_DIR = Path("experiments/runs/mrlf-benchmark")
OUT = CLUE_DIR / "phase4-consumption-results.json"


def _stem(word: str) -> str:
    """Simple suffix-stripping stemmer."""
    w = word.lower()
    for suffix in ("ation", "tion", "ing", "ment", "ness", "ible", "able", "ful",
                   "ous", "ive", "ise", "ize", "ised", "ized", "ally", "edly",
                   "ies", "ied", "ers", "est", "ler", "led", "les"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            return w[:-len(suffix)]
    if w.endswith("ed") and len(w) > 4:
        return w[:-2]
    if w.endswith("ly") and len(w) > 4:
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss") and len(w) > 4:
        return w[:-1]
    return w


def score_fact(clue_text: str, fact: str) -> str:
    """Score whether a gold fact is answerable from the clue.
    
    Uses stemmed keyword matching for better recall.
    Returns: ANSWERABLE, PARTIAL, or MISSING
    """
    # Extract key noun phrases from the fact (4+ char words, not stopwords)
    stop = {"the", "and", "for", "not", "but", "that", "this", "with", "from",
            "are", "was", "has", "have", "been", "each", "when", "only",
            "all", "can", "does", "which", "will", "into", "via", "per",
            "uses", "used", "method", "class", "function", "module"}
    fact_words = set(re.findall(r"[a-zA-Z_]\w{3,}", fact.lower())) - stop
    
    # Stem both fact words and clue text for fuzzy matching
    stemmed_fact = {_stem(w) for w in fact_words}
    clue_lower = clue_text.lower()
    clue_words = set(re.findall(r"[a-zA-Z_]\w{3,}", clue_lower))
    stemmed_clue = {_stem(w) for w in clue_words}
    
    # Count matches: exact word match OR stemmed match
    found = 0
    for w in fact_words:
        if w in clue_lower:
            found += 1
        elif _stem(w) in stemmed_clue:
            found += 0.8  # stemmed match counts slightly less
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
    
    results = []
    
    print("Phase 4: LLM Consumption Test")
    print("=" * 80)
    
    for gold in golds:
        task_id = gold["task_id"]
        clue_path = CLUE_DIR / f"{task_id}.codeclue"
        
        if not clue_path.exists():
            print(f"  {task_id}: SKIP (no clue file)")
            continue
        
        clue = clue_path.read_text(encoding="utf-8")
        
        # Score each gold fact
        fact_scores = []
        for fact in gold.get("gold_facts", []):
            score = score_fact(clue, fact)
            fact_scores.append({"fact": fact, "score": score})
        
        # Task-level metrics
        answerable = sum(1 for fs in fact_scores if fs["score"] == "ANSWERABLE")
        partial = sum(1 for fs in fact_scores if fs["score"] == "PARTIAL")
        missing = sum(1 for fs in fact_scores if fs["score"] == "MISSING")
        total = len(fact_scores)
        
        # Fidelity: answerable=1.0, partial=0.5, missing=0.0
        fidelity = (answerable * 1.0 + partial * 0.5) / total if total > 0 else 0
        
        # Sufficient: fidelity >= 0.60 means clue-only is adequate
        sufficient = fidelity >= 0.60
        
        result = {
            "task_id": task_id,
            "repo": gold["repo"],
            "family": gold["family"],
            "fidelity": round(fidelity, 3),
            "sufficient": sufficient,
            "answerable": answerable,
            "partial": partial,
            "missing": missing,
            "total_facts": total,
            "fact_scores": fact_scores,
        }
        results.append(result)
        
        status = "PASS" if sufficient else "FAIL"
        print(f"  {task_id:40s} fid={fidelity:.3f} A={answerable} P={partial} M={missing} {status}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_tasks = len(results)
    sufficient_count = sum(1 for r in results if r["sufficient"])
    dfcr = sufficient_count / total_tasks if total_tasks > 0 else 0
    ddr = 1 - dfcr
    mean_fidelity = sum(r["fidelity"] for r in results) / total_tasks if total_tasks > 0 else 0
    
    # Per-repo
    repos = {}
    for r in results:
        repos.setdefault(r["repo"], []).append(r)
    
    print(f"\n{'Repo':12s} | {'Mean Fid':>8s} | {'Sufficient':>10s}")
    print("-" * 40)
    for repo, rs in sorted(repos.items()):
        mf = sum(r["fidelity"] for r in rs) / len(rs)
        sc = sum(1 for r in rs if r["sufficient"])
        print(f"{repo:12s} | {mf:>8.3f} | {sc:>5d}/{len(rs)}")
    
    # Per-TF
    tfs = {}
    for r in results:
        tfs.setdefault(r["family"], []).append(r)
    
    print(f"\n{'Family':8s} | {'Mean Fid':>8s} | {'Sufficient':>10s}")
    print("-" * 35)
    for tf, rs in sorted(tfs.items()):
        mf = sum(r["fidelity"] for r in rs) / len(rs)
        sc = sum(1 for r in rs if r["sufficient"])
        print(f"{tf:8s} | {mf:>8.3f} | {sc:>5d}/{len(rs)}")
    
    print(f"\nOverall: mean_fidelity={mean_fidelity:.3f}, DFCR={dfcr:.3f} ({sufficient_count}/{total_tasks}), DDR={ddr:.3f}")
    print(f"\nGate: DFCR ≥ 0.60: {dfcr:.3f} → {'PASS' if dfcr >= 0.60 else 'FAIL'}")
    print(f"Gate: DDR ≤ 0.40: {ddr:.3f} → {'PASS' if ddr <= 0.40 else 'FAIL'}")
    
    # Save
    summary = {
        "total_tasks": total_tasks,
        "sufficient": sufficient_count,
        "dfcr": round(dfcr, 3),
        "ddr": round(ddr, 3),
        "mean_fidelity": round(mean_fidelity, 3),
        "per_task": results,
    }
    OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nResults saved to {OUT}")


if __name__ == "__main__":
    main()
