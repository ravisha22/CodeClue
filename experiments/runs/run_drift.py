"""Run drift protocol on Flask and save results."""
from pathlib import Path
from codeclue_research.drift import run_drift_protocol
import json

result = run_drift_protocol(
    repo_root=Path("experiments/external-repos/flask"),
    n_commits=10,
    operation_family="OF2",
    language="python",
)
print(f"Steps: {result['steps_completed']}")
print(f"Slope: {result['slope']}")
print(f"Floor maintained: {result['floor_maintained']}")
print(f"Reset triggered: {result['reset_triggered']}")
for s in result["steps"]:
    idx = s.get("index", "?")
    fc = s.get("from_commit", "?")
    tc = s.get("to_commit", "?")
    fid = s.get("fidelity", 0)
    dng = s.get("dng", 0)
    cf = s.get("changed_files", 0)
    err = s.get("error", "")
    if err:
        print(f"  Step {idx}: {fc}->{tc} ERROR: {err}")
    else:
        print(f"  Step {idx}: {fc}->{tc} fidelity={fid:.4f} dng={dng:.4f} files={cf}")

Path("experiments/reports/drift-flask-10step.json").write_text(
    json.dumps(result, indent=2, default=str)
)
print("Saved to experiments/reports/drift-flask-10step.json")
