import json, pathlib

results = pathlib.Path("experiments/cross-model-eval/results")
for f in sorted(results.glob("gpt54-flask-*.json"))[:3]:
    d = json.load(f.open())
    ab = d.get("arm_b", {})
    tid = d["task_id"]
    suff = ab.get("clue_sufficient", "?")
    gaps = len(ab.get("gaps_identified", []))
    print(f"{tid}: sufficient={suff}, gaps={gaps}")

# Count clue-sufficient tasks
all_files = sorted(results.glob("gpt54-*.json"))
sufficient_count = 0
total = 0
for f in all_files:
    if "COMPLETE" in f.name:
        continue
    d = json.load(f.open())
    ab = d.get("arm_b", {})
    if ab.get("clue_sufficient"):
        sufficient_count += 1
    total += 1
print(f"\nTotal: {total} tasks, {sufficient_count} clue-sufficient")
