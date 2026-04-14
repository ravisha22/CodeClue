"""Diagnose the 2 remaining Phase 5 failures."""
import json

data = json.load(open("experiments/runs/mrlf-benchmark/phase5-drilldown-results.json"))
for t in data["per_task"]:
    tid = t["task_id"]
    if tid in ("gin-tf5-credential-handling", "httpx-tf5-redirect-security"):
        print(f"=== {tid} ===")
        print(f"  clue={t['fid_clue']}, drill={t['fid_drill']}, records={t['drill_records']}")
        scores = t.get("fact_scores_drill", t.get("fact_scores_clue", []))
        for fs in scores:
            print(f"  [{fs['score']:10s}] {fs['fact']}")
        print()

        # Check: what did the drill records contain?
        # Load the relevant detail store
        repo = t["repo"]
        detail_path = f"experiments/runs/mrlf-benchmark/{repo}.codeclue-detail"
        try:
            records = [json.loads(line) for line in open(detail_path) if line.strip()]
            # Find the records that were selected
            gold_path = "experiments/runs/mrlf-benchmark/gold-tasks.json"
            golds = json.load(open(gold_path))
            gold = next(g for g in golds if g["task_id"] == tid)
            gold_syms = set(gold.get("gold_symbols", []))
            gold_files = set(gold.get("gold_files", []))
            
            print(f"  Gold symbols: {gold_syms}")
            print(f"  Gold files: {gold_files}")
            
            # Check if ANY detail record contains the missing fact keywords
            for fact in gold.get("gold_facts", []):
                # Extract key terms
                terms = [w for w in fact.lower().split() if len(w) > 4]
                found_in_any = False
                for rec in records:
                    src = rec.get("source", "").lower()
                    if any(t in src for t in terms[:3]):
                        found_in_any = True
                        break
                status = "IN FILE2" if found_in_any else "NOT IN FILE2"
                print(f"  [{status:12s}] {fact[:80]}")
            print()
        except Exception as e:
            print(f"  Error loading detail: {e}")
