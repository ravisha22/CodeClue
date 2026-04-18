import json
import yaml
import sys
from pathlib import Path

tasks = yaml.safe_load(Path("tests/fixtures/lane_a_extended_tasks.yaml").read_text())["tasks"]

repo_graph_map = {
    "pallets/flask": "experiments/runs/lane-a-flask/graph.json",
    "fastapi/fastapi": "experiments/runs/lane-a-fastapi/graph.json",
    "nestjs/nest": "experiments/runs/lane-a-nest/graph.json",
}

repo_run_dir = {
    "pallets/flask": "experiments/runs/lane-a-flask",
    "fastapi/fastapi": "experiments/runs/lane-a-fastapi",
    "nestjs/nest": "experiments/runs/lane-a-nest",
}

for t in tasks:
    tid = t["task_id"]
    repo = t["repo"]
    pp = t["prompt_profile"]
    run_dir = repo_run_dir[repo]
    pp_path = f"{run_dir}/pp-{tid}.yaml"
    Path(pp_path).write_text(yaml.safe_dump(pp, sort_keys=False))
    print(f"Created: {pp_path}")

print(f"\nTotal: {len(tasks)} prompt profiles created")
