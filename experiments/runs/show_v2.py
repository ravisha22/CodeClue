import json
d = json.load(open("experiments/reports/v2-existing-projections.json"))
for t in d["tasks"]:
    print(f"{t['task_id']:25s} conf={t['conf']:7.4f}  hint={t['hint']:20s}  nodes={t['nodes']}")
