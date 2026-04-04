"""Run Lane B on all v2 projections across all 7 repos."""
import json
import glob
from pathlib import Path
from codeclue_research.lane_b import generate_lane_b_report

# Collect ALL v2 projections
traces = []
for pattern in [
    "experiments/runs/v2-lane-a-flask/v2-proj-*.json",
    "experiments/runs/v2-lane-a-fastapi/v2-proj-*.json",
    "experiments/runs/v2-lane-a-nest/v2-proj-*.json",
    "experiments/runs/v2-lane-a-httpx/v2-proj-*.json",
    "experiments/runs/v2-lane-a-express/v2-proj-*.json",
    "experiments/runs/v2-lane-a-typeorm/v2-proj-*.json",
    "experiments/runs/v2-lane-a-gin/v2-proj-*.json",
]:
    for f in sorted(glob.glob(pattern)):
        traces.append(json.load(open(f)))

print(f"Total projection traces: {len(traces)}")

report = generate_lane_b_report(
    traces,
    output_path=Path("experiments/reports/v2-lane-b-all-repos.json"),
)

print(json.dumps({
    "ift_alignment": report["ift_scent_alignment"]["ift_scent_alignment"],
    "spearman": report["ift_scent_alignment"]["spearman_correlation"],
    "kl_divergence": report["callback_distribution_agreement"]["kl_divergence"],
    "observed_dist": report["callback_distribution_agreement"]["observed_distribution"],
    "g7_passed": report["gate_g7"]["passed"],
    "data_points": report["ift_scent_alignment"]["data_points"],
}, indent=2))
