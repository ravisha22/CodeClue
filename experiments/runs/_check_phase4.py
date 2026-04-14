import json
data = json.load(open("experiments/runs/mrlf-benchmark/phase4-consumption-results.json"))
print("=== TF5 tasks ===")
for d in data:
    if "tf5" in d["task_id"]:
        print(f"  {d['task_id']}: fid={d['fidelity']}, A={d.get('exact_matches',0)}, P={d.get('partial_matches',0)}, M={d.get('misses',0)}, suff={d['sufficient']}")

print("\n=== Flask tasks ===")
for d in data:
    if "flask" in d["task_id"]:
        print(f"  {d['task_id']}: fid={d['fidelity']}, suff={d['sufficient']}")

print(f"\nOverall: {sum(1 for d in data if d['sufficient'])}/{len(data)} sufficient")
print(f"DFCR = {sum(1 for d in data if d['sufficient'])/len(data):.3f}")
