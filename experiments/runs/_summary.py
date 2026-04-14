import json
data = json.loads(open("experiments/runs/mrlf-benchmark/phase3-localization-results.json").read())
repos = {}
for r in data:
    repos.setdefault(r["repo"], []).append(r)
for repo, rs in sorted(repos.items()):
    ml = sum(r["localization_accuracy"] for r in rs) / len(rs)
    su = sum(1 for r in rs if r["sufficient"])
    print(f"{repo:12s} loc={ml:.3f} suff={su}/{len(rs)}")
overall = sum(r["localization_accuracy"] for r in data) / len(data)
suff = sum(1 for r in data if r["sufficient"])
print(f"OVERALL      loc={overall:.3f} suff={suff}/{len(data)}")

# Also run Phase 4
print("\n--- Phase 4 ---")
import subprocess, sys
subprocess.run([sys.executable, "experiments/runs/run_phase4_consumption.py"])
