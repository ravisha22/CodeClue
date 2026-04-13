"""Root cause: check if gold symbols appear in blind eval clue files."""
import json
from pathlib import Path

TASKS_PATH = Path("experiments/runs/blind-eval/blind-gold-tasks.json")
CLUES_DIR = Path("experiments/runs/blind-eval/clues")

with open(TASKS_PATH) as f:
    tasks = json.load(f)

for t in tasks:
    tid = t["task_id"]
    repo = t["repo"]
    gold_syms = t.get("gold_symbols", [])

    # Find clue file
    clue_file = CLUES_DIR / f"{tid}.codeclue"
    if not clue_file.exists():
        print(f"--- {tid}: NO CLUE FILE ---")
        continue

    content = clue_file.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    # Parse sections
    sections: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line.strip().startswith("-- "):
            current = line.strip()[3:]
            sections[current] = []
        elif current:
            sections.setdefault(current, []).append(line)

    print(f"\n=== {tid} ({repo}) ===")
    print(f"  Question: {t['question'][:80]}...")
    print(f"  Clue file: {len(lines)} lines")

    # Check each gold symbol
    for sym in gold_syms:
        # Check SYM section
        in_sym = any(sym in line for line in sections.get("SYM", []))
        # Check FOCUS section
        in_focus = any(sym in line for line in sections.get("FOCUS", []))
        # Check anywhere in file
        in_file = sym in content

        status = "FOCUS" if in_focus else ("SYM" if in_sym else ("SOMEWHERE" if in_file else "ABSENT"))
        print(f"  [{status:9s}] {sym}")

    # Show what IS in FOCUS
    focus_lines = sections.get("FOCUS", [])
    focus_entries = [l.rstrip() for l in focus_lines if l.strip() and not l.startswith("  ")]
    print(f"\n  FOCUS entries ({len(focus_entries)}):")
    for e in focus_entries[:15]:
        print(f"    {e[:80]}")
    if len(focus_entries) > 15:
        print(f"    ... and {len(focus_entries) - 15} more")
