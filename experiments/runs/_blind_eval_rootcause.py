"""Investigate blind eval root cause: what's in the clue vs what gold facts need."""
import json
from pathlib import Path

TASKS_PATH = Path("experiments/runs/blind-eval/blind-gold-tasks.json")
RESULTS_PATH = Path("experiments/runs/blind-eval/blind-eval-results.jsonl")

# Load gold tasks
with open(TASKS_PATH) as f:
    tasks = json.load(f)

# Load results
results = {}
with open(RESULTS_PATH) as f:
    for line in f:
        r = json.loads(line.strip())
        results[r["task_id"]] = r

print("=== BLIND EVAL ROOT CAUSE ANALYSIS ===\n")

for t in tasks:
    tid = t["task_id"]
    print(f"--- {tid} ({t['repo']}) ---")
    print(f"  Q: {t['question'][:100]}...")
    print(f"  Gold symbols: {t.get('gold_symbols', [])}")
    print(f"  Gold files: {t.get('gold_files', [])}")

    if tid in results:
        r = results[tid]
        print(f"  Score: {r['total_covered']}/{r['total_facts']}")
        for s in r["scores"]:
            print(f"    FACT {s['fact']}: {s['verdict']} - {s['reason'][:80]}")
    else:
        print(f"  NOT EVALUATED YET")
    print()

# Now check what symbols ARE in the clue files
print("\n=== CHECKING CLUE FILE CONTENTS ===\n")
clue_dir = Path("experiments/runs/blind-eval")
for clue_file in sorted(clue_dir.glob("*.codeclue")):
    print(f"--- {clue_file.name} ---")
    content = clue_file.read_text(encoding="utf-8", errors="replace")
    # Count sections
    lines = content.splitlines()
    focus_start = None
    focus_end = None
    sym_start = None
    sym_end = None
    for i, line in enumerate(lines):
        if line.strip() == "-- FOCUS":
            focus_start = i
        elif line.strip() == "-- GAPS" and focus_start is not None:
            focus_end = i
        elif line.strip() == "-- SYM":
            sym_start = i
        elif line.strip() == "-- FOCUS" and sym_start is not None:
            sym_end = i

    if focus_start and focus_end:
        focus_lines = lines[focus_start:focus_end]
        focus_symbols = [l.strip().split(" (")[0] for l in focus_lines
                        if l and not l.startswith(" ") and not l.startswith("--")]
        print(f"  FOCUS symbols: {len(focus_symbols)}")
        for s in focus_symbols[:10]:
            print(f"    {s}")
        if len(focus_symbols) > 10:
            print(f"    ... and {len(focus_symbols) - 10} more")
    print(f"  Total lines: {len(lines)}")
    print()
