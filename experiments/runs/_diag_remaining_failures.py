"""Diagnose all 6 remaining keyword-failing tasks: what specific gold facts fail and why."""
import json
from pathlib import Path

data = json.load(open("experiments/runs/mrlf-benchmark/phase4-consumption-results.json"))

print("=== Remaining Failures: Root Cause Classification ===\n")
for task in data["per_task"]:
    if task["sufficient"]:
        continue
    print(f"TASK: {task['task_id']} (fidelity={task['fidelity']})")
    for fs in task["fact_scores"]:
        print(f"  [{fs['score']:7s}] {fs['fact'][:100]}")
    print()
