"""Phase 5: Drill-Down Test — Does File 2 detail rescue failing tasks?

For each task that failed clue-only (fidelity < 0.60):
  1. Load the task's clue file
  2. Find relevant File 2 detail records (matching gold files/symbols)
  3. Append source snippets from those records to the clue
  4. Re-score fidelity with the enriched clue
  5. Compute FU (Fidelity Uplift)

Gate: FU >= 0.10
"""

import json
import re
import time
from pathlib import Path

GOLD_DEV = Path("experiments/runs/mrlf-benchmark/gold-tasks.json")
GOLD_HELDOUT = Path("experiments/runs/mrlf-benchmark/heldout-gold-tasks.json")
CLUE_DIR = Path("experiments/runs/mrlf-benchmark")
OUT_DIR = Path("experiments/runs/mrlf-benchmark")

# Detail store file mapping
DETAIL_STORES = {
    "flask": "experiments/runs/mrlf-benchmark/flask.codeclue-detail",
    "httpx": "experiments/runs/mrlf-benchmark/httpx.codeclue-detail",
    "gin": "experiments/runs/mrlf-benchmark/gin.codeclue-detail",
    "fastapi": "experiments/runs/mrlf-benchmark/fastapi.codeclue-detail",
    "django": "experiments/runs/mrlf-benchmark/django.codeclue-detail",
    "chi": "experiments/runs/mrlf-benchmark/chi.codeclue-detail",
}


def _stem(w: str) -> str:
    if w.endswith("ing") and len(w) > 5:
        return w[:-3]
    if w.endswith("ed") and len(w) > 4:
        return w[:-2]
    if w.endswith("s") and len(w) > 4:
        return w[:-1]
    return w


def score_fact(text: str, fact: str) -> str:
    """Score whether a gold fact is answerable from the text."""
    stop = {"the", "and", "for", "not", "but", "that", "this", "with", "from",
            "are", "was", "has", "have", "been", "each", "when", "only",
            "all", "can", "does", "which", "will", "into", "via", "per",
            "uses", "used", "method", "class", "function", "module"}
    fact_words = set(re.findall(r"[a-zA-Z_]\w{3,}", fact.lower())) - stop
    stemmed_clue = {_stem(w) for w in set(re.findall(r"[a-zA-Z_]\w{3,}", text.lower()))}

    found = 0
    for w in fact_words:
        if w in text.lower():
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


def compute_fidelity(text: str, gold_facts: list[str]) -> tuple[float, list[dict]]:
    """Compute fidelity score and per-fact breakdown."""
    fact_scores = []
    for fact in gold_facts:
        s = score_fact(text, fact)
        fact_scores.append({"fact": fact, "score": s})
    a = sum(1 for fs in fact_scores if fs["score"] == "ANSWERABLE")
    p = sum(1 for fs in fact_scores if fs["score"] == "PARTIAL")
    total = len(fact_scores)
    fid = (a * 1.0 + p * 0.5) / total if total else 0
    return round(fid, 3), fact_scores


def load_detail_store(repo: str) -> list[dict]:
    """Load File 2 records for a repo."""
    path = Path(DETAIL_STORES.get(repo, ""))
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def find_relevant_records(records: list[dict], gold: dict, max_records: int = 5) -> list[dict]:
    """Find File 2 records matching gold files and gold symbols."""
    gold_files = set(gold.get("gold_files", []))
    gold_syms = set(gold.get("gold_symbols", []))

    scored = []
    for rec in records:
        score = 0
        rec_file = rec.get("file", "")
        rec_sym = rec.get("symbol", "")

        # File match
        for gf in gold_files:
            if gf.split("/")[-1] == rec_file.split("/")[-1]:
                score += 2
                break

        # Symbol match
        for gs in gold_syms:
            gs_short = gs.rsplit(".", 1)[-1]
            rec_short = rec_sym.rsplit(".", 1)[-1]
            if gs.lower() == rec_sym.lower() or gs_short.lower() == rec_short.lower():
                score += 3
                break

        if score > 0:
            scored.append((score, rec))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [rec for _, rec in scored[:max_records]]


def format_drill_records(records: list[dict]) -> str:
    """Format File 2 records as additional context to append to clue."""
    parts = ["", "--- DRILL-DOWN DETAIL (File 2) ---", ""]
    for rec in records:
        sym = rec.get("symbol", "?")
        typ = rec.get("type", "?")
        fp = rec.get("file", "?")
        lines = rec.get("lines", [0, 0])
        purpose = rec.get("purpose", "")
        source = rec.get("source", "")
        calls = rec.get("calls", [])
        called_by = rec.get("called_by", [])

        parts.append(f"## {sym} ({fp}:{lines[0]}-{lines[1]})")
        if purpose:
            parts.append(f"Purpose: {purpose}")
        if calls:
            short_calls = [c.rsplit(".", 1)[-1] for c in calls[:8]]
            parts.append(f"Calls: {', '.join(short_calls)}")
        if called_by:
            short_cb = [c.rsplit(".", 1)[-1] for c in called_by[:8]]
            parts.append(f"Called by: {', '.join(short_cb)}")
        if source:
            # Cap source at 30 lines
            src_lines = source.split("\n")[:30]
            parts.append("```")
            parts.extend(src_lines)
            if len(source.split("\n")) > 30:
                parts.append("  # ... (truncated)")
            parts.append("```")
        parts.append("")

    return "\n".join(parts)


def main():
    # Load all gold tasks (dev + held-out)
    all_golds = []
    if GOLD_DEV.exists():
        all_golds.extend(json.loads(GOLD_DEV.read_text(encoding="utf-8")))
    if GOLD_HELDOUT.exists():
        all_golds.extend(json.loads(GOLD_HELDOUT.read_text(encoding="utf-8")))

    print("=" * 80)
    print("PHASE 5: DRILL-DOWN TEST")
    print("=" * 80)

    results = []

    for gold in all_golds:
        task_id = gold["task_id"]
        repo = gold["repo"]

        # Load clue
        clue_path = CLUE_DIR / f"{task_id}.codeclue"
        if not clue_path.exists():
            continue

        clue = clue_path.read_text(encoding="utf-8")
        gold_facts = gold.get("gold_facts", [])
        if not gold_facts:
            continue

        # Score clue-only
        fid_clue, fs_clue = compute_fidelity(clue, gold_facts)
        clue_sufficient = fid_clue >= 0.60

        # Only drill-down on failing tasks
        if clue_sufficient:
            results.append({
                "task_id": task_id, "repo": repo,
                "fid_clue": fid_clue, "fid_drill": fid_clue,
                "uplift": 0.0, "clue_sufficient": True,
                "drill_sufficient": True, "skipped": True,
                "drill_records": 0,
            })
            continue

        # Load File 2 and find relevant records
        detail_records = load_detail_store(repo)
        if not detail_records:
            # Try generating on the fly
            from codeclue_research.extractor import extract_graph
            from codeclue_research.clue_view_mrlf import generate_detail_store, write_detail_store
            repo_path = Path(gold.get("repo_path", f"experiments/external-repos/{repo}"))
            if repo_path.exists():
                print(f"  {task_id}: generating detail store for {repo}...", end=" ", flush=True)
                graph = extract_graph(repo_path)
                detail_records = generate_detail_store(graph, repo_root=str(repo_path))
                detail_path = Path(DETAIL_STORES.get(repo, f"experiments/runs/mrlf-benchmark/{repo}.codeclue-detail"))
                write_detail_store(detail_records, detail_path)
                print(f"({len(detail_records)} records)")

        relevant = find_relevant_records(detail_records, gold)
        drill_text = format_drill_records(relevant)

        # Create enriched clue
        enriched = clue + drill_text

        # Score enriched
        fid_drill, fs_drill = compute_fidelity(enriched, gold_facts)
        uplift = round(fid_drill - fid_clue, 3)
        drill_sufficient = fid_drill >= 0.60

        result = {
            "task_id": task_id, "repo": repo,
            "fid_clue": fid_clue, "fid_drill": fid_drill,
            "uplift": uplift,
            "clue_sufficient": clue_sufficient,
            "drill_sufficient": drill_sufficient,
            "skipped": False,
            "drill_records": len(relevant),
            "fact_scores_clue": fs_clue,
            "fact_scores_drill": fs_drill,
        }
        results.append(result)

        status_before = "PASS" if clue_sufficient else "FAIL"
        status_after = "PASS" if drill_sufficient else "FAIL"
        flip = " >>> FLIPPED" if not clue_sufficient and drill_sufficient else ""
        print(f"  {task_id:45s} clue={fid_clue:.3f}({status_before}) "
              f"drill={fid_drill:.3f}({status_after}) "
              f"uplift={uplift:+.3f} records={len(relevant)}{flip}")

    # Summary
    print("\n" + "=" * 80)
    print("PHASE 5 SUMMARY")
    print("=" * 80)

    drill_tasks = [r for r in results if not r.get("skipped", False)]
    pass_tasks = [r for r in results if r.get("clue_sufficient", False)]

    if drill_tasks:
        mean_uplift = sum(r["uplift"] for r in drill_tasks) / len(drill_tasks)
        flipped = sum(1 for r in drill_tasks if r["drill_sufficient"] and not r["clue_sufficient"])
        max_uplift = max(r["uplift"] for r in drill_tasks)
        min_uplift = min(r["uplift"] for r in drill_tasks)

        print(f"\n  Tasks requiring drill-down:  {len(drill_tasks)}")
        print(f"  Tasks already passing:      {len(pass_tasks)}")
        print(f"  Mean fidelity uplift (FU):   {mean_uplift:+.3f}")
        print(f"  Max uplift:                  {max_uplift:+.3f}")
        print(f"  Min uplift:                  {min_uplift:+.3f}")
        print(f"  Tasks flipped FAIL->PASS:    {flipped}/{len(drill_tasks)}")

        total_tasks = len(results)
        total_pass = len(pass_tasks) + flipped
        post_drill_dfcr = total_pass / total_tasks if total_tasks else 0

        print(f"\n  Pre-drill DFCR:              {len(pass_tasks)}/{total_tasks} = {len(pass_tasks)/total_tasks:.3f}")
        print(f"  Post-drill DFCR:             {total_pass}/{total_tasks} = {post_drill_dfcr:.3f}")
        print(f"\n  Gate D7 (FU >= 0.10):        {'PASS' if mean_uplift >= 0.10 else 'FAIL'} ({mean_uplift:+.3f})")
    else:
        print("  No tasks required drill-down (all passing)")

    # Save results
    out_file = OUT_DIR / "phase5-drilldown-results.json"
    json.dump({
        "drill_tasks": len(drill_tasks),
        "pass_tasks": len(pass_tasks),
        "mean_uplift": round(mean_uplift, 3) if drill_tasks else 0,
        "flipped": flipped if drill_tasks else 0,
        "gate_d7_pass": mean_uplift >= 0.10 if drill_tasks else True,
        "per_task": results,
    }, open(out_file, "w"), indent=2)
    print(f"\n  Results saved to {out_file}")


if __name__ == "__main__":
    main()
