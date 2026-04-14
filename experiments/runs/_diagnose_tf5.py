"""Diagnostic: What does TF5 clue actually contain vs what gold facts ask?

For each TF5 task, show:
1. The gold facts
2. What the clue's FOCUS section says about each relevant symbol
3. Whether the information gap is content (missing from clue) or semantic (present but worded differently)
"""
import json
from pathlib import Path

golds = json.loads(Path("experiments/runs/mrlf-benchmark/gold-tasks.json").read_text())
clue_dir = Path("experiments/runs/mrlf-benchmark")

for gold in golds:
    if gold["family"] != "TF5":
        continue
    
    task_id = gold["task_id"]
    clue_path = clue_dir / f"{task_id}.codeclue"
    if not clue_path.exists():
        continue
    
    clue = clue_path.read_text()
    
    print(f"{'='*70}")
    print(f"TASK: {task_id}")
    print(f"Question: {gold['question']}")
    print()
    
    # Extract FOCUS section
    focus_text = ""
    in_focus = False
    for line in clue.split("\n"):
        if line.strip() == "-- FOCUS":
            in_focus = True
            continue
        if line.startswith("-- ") and in_focus:
            break
        if in_focus:
            focus_text += line + "\n"
    
    # For each gold fact, check if relevant keywords exist in FOCUS
    for i, fact in enumerate(gold.get("gold_facts", []), 1):
        # Find relevant content in focus
        relevant_lines = []
        for line in focus_text.split("\n"):
            fact_words = set(w.lower() for w in fact.split() if len(w) > 3)
            line_words = set(w.lower() for w in line.split() if len(w) > 3)
            if fact_words & line_words:
                relevant_lines.append(line.strip())
        
        print(f"  FACT {i}: {fact}")
        if relevant_lines:
            for rl in relevant_lines[:3]:
                print(f"    CLUE: {rl}")
            print(f"    VERDICT: CONTENT PRESENT (different wording)")
        else:
            print(f"    CLUE: (no matching content)")
            print(f"    VERDICT: CONTENT MISSING")
        print()

print("="*70)
print("THESIS: If most TF5 facts show 'CONTENT PRESENT', the scorer is the")
print("bottleneck, not the format. A real LLM would infer correctly.")
