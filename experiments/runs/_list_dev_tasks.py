"""List development gold tasks to ensure held-out set is distinct."""
import json
data = json.load(open("experiments/runs/mrlf-benchmark/gold-tasks.json"))
repos = set(d["repo"] for d in data)
print(f"Dev repos: {repos}")
print(f"Dev tasks: {len(data)}")
for d in data:
    print(f"  {d['task_id']:45s} {d['family']}")
