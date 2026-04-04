"""Collate cross-model evaluation results after all three models have run.
Run this in the main Claude session to collect and analyze all outputs."""
import json
import math
from pathlib import Path

results_dir = Path("experiments/cross-model-eval/results")

# Check prerequisites
gpt_complete = results_dir / "gpt54-COMPLETE.json"
gemini_summary = results_dir / "gemini-judge-SUMMARY.json"
tier2_comparison = Path("experiments/reports/tier2-flask-comparison.json")

print("=== PREREQUISITE CHECK ===")
print(f"GPT 5.4 complete:  {'YES' if gpt_complete.exists() else 'NO — run GPT 5.4 tab first'}")
print(f"Gemini summary:    {'YES' if gemini_summary.exists() else 'NO — run Gemini tab first'}")
print(f"Tier 2 comparison: {'YES' if tier2_comparison.exists() else 'NO — run Claude tab first'}")

if not gpt_complete.exists() or not gemini_summary.exists():
    print("\nNot all models have completed. Run missing tabs first.")
    exit(1)

# Load all GPT 5.4 results
gpt_results = {}
for f in sorted(results_dir.glob("gpt54-*.json")):
    if "COMPLETE" in f.name:
        continue
    d = json.loads(f.read_text())
    gpt_results[d["task_id"]] = d

# Load all Gemini judge results
judge_results = {}
for f in sorted(results_dir.glob("gemini-judge-*.json")):
    if "SUMMARY" in f.name:
        continue
    d = json.loads(f.read_text())
    judge_results[d["task_id"]] = d

# Load Claude baseline
claude_data = json.loads(Path("experiments/reports/v2-benchmark-all-23.json").read_text())
claude_scores = {}
for t in claude_data.get("existing_15_tasks_v2", []) + claude_data.get("new_8_tasks_v2", []):
    claude_scores[t["task_id"]] = {"arm_b": t["arm_b_fs"], "arm_a": t["arm_a_fs"]}

# Load Gemini summary
gemini_sum = json.loads(gemini_summary.read_text())

print(f"\n=== RESULTS ===")
print(f"GPT 5.4 tasks: {len(gpt_results)}")
print(f"Gemini-judged tasks: {len(judge_results)}")
print(f"Claude baseline tasks: {len(claude_scores)}")

# Collated report
report = {
    "timestamp": "auto",
    "models": {
        "generator": "claude-opus-4.6 (Tier 2 contracts)",
        "consumer": "gpt-5.4 (Arm B/A execution)",
        "judge": "gemini-3.1-pro (independent scoring)",
        "baseline": "claude-opus-4.6 (original v2 self-evaluation)"
    },
    "gemini_summary": gemini_sum,
    "per_task": [],
}

for task_id in sorted(claude_scores.keys()):
    entry = {
        "task_id": task_id,
        "claude_arm_b": claude_scores[task_id]["arm_b"],
        "claude_arm_a": claude_scores[task_id]["arm_a"],
    }
    if task_id in judge_results:
        j = judge_results[task_id]
        arm_b_key = [k for k in j.keys() if "arm_b" in k and isinstance(j[k], dict)]
        arm_a_key = [k for k in j.keys() if "arm_a" in k and isinstance(j[k], dict)]
        if arm_b_key:
            entry["gpt54_arm_b_judged"] = j[arm_b_key[0]].get("score", -1)
        if arm_a_key:
            entry["gpt54_arm_a_judged"] = j[arm_a_key[0]].get("score", -1)

    report["per_task"].append(entry)

out_path = Path("experiments/reports/cross-model-collated-final.json")
out_path.write_text(json.dumps(report, indent=2, sort_keys=True))
print(f"\nCollated report saved to {out_path}")
print(f"\nGemini verdict: {gemini_sum.get('verdict', 'unknown')}")

# Tier 2 results if available
if tier2_comparison.exists():
    t2 = json.loads(tier2_comparison.read_text())
    print(f"\n=== TIER 2 COMPARISON (Flask) ===")
    print(f"Tier 2 enriched nodes: {t2.get('tier2_enriched_nodes', 0)} / {t2.get('total_nodes', 0)}")
    for t in t2.get("tasks", []):
        print(f"  {t['task_id']}: T1 conf={t.get('tier1_conf','?')} → T2 conf={t.get('tier2_conf','?')} (Δ={t.get('conf_delta','?')})")
