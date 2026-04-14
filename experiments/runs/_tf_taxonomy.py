import json

golds = json.loads(open("experiments/runs/mrlf-benchmark/gold-tasks.json").read())

print("=" * 70)
print("TF5 FACT TAXONOMY — What kind of knowledge does each fact require?")
print("=" * 70)

for g in golds:
    if g["family"] == "TF5":
        print(f"\n--- {g['task_id']} ---")
        print(f"Q: {g['question']}")
        for i, f in enumerate(g["gold_facts"], 1):
            print(f"  FACT {i}: {f}")
        print()

# Also show TF2 and TF4 for comparison — what kind of facts do PASSING TFs need?
print("=" * 70)
print("TF2 FACTS (PASSING — 4/4) — What kind of knowledge do these need?")
print("=" * 70)
for g in golds:
    if g["family"] == "TF2":
        print(f"\n--- {g['task_id']} ---")
        for i, f in enumerate(g["gold_facts"], 1):
            print(f"  FACT {i}: {f}")

print()
print("=" * 70)
print("TF3 FACTS (PASSING — 4/4) — What kind of knowledge do these need?")
print("=" * 70)
for g in golds:
    if g["family"] == "TF3":
        print(f"\n--- {g['task_id']} ---")
        for i, f in enumerate(g["gold_facts"], 1):
            print(f"  FACT {i}: {f}")
