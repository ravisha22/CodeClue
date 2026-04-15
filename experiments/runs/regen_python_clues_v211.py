"""Regenerate Python repo clues with improved GAPS drill targets (v2.1.1)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

with open(REPO_ROOT / "experiments/runs/blind-eval/blind-gold-tasks.json") as f:
    tasks = json.load(f)

CLUE_DIR = REPO_ROOT / "experiments/runs/blind-eval/clues"

for repo_name in ["aiohttp", "click"]:
    repo_path = REPO_ROOT / "experiments" / "external-repos" / repo_name
    print(f"Extracting {repo_name}...")
    graph = extract_graph(repo_path, language="python")
    print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges")

    detail_records = generate_detail_store(graph, repo_root=repo_path)
    detail_path = CLUE_DIR / f"{repo_name}.codeclue-detail"
    with open(detail_path, "w", encoding="utf-8") as f:
        for rec in detail_records:
            f.write(json.dumps(rec) + "\n")
    print(f"  Detail store: {len(detail_records)} records")

    repo_tasks = [t for t in tasks if t["repo"] == repo_name]
    for t in repo_tasks:
        clue = render_mrlf(graph, t["question"], repo_root=repo_path)
        clue_path = CLUE_DIR / f"{t['task_id']}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")
        gaps_idx = clue.find("-- GAPS")
        if gaps_idx >= 0:
            print(f"  {t['task_id']} GAPS:")
            for line in clue[gaps_idx:].splitlines()[:8]:
                print(f"    {line}")
        print()

print("Done regenerating Python clues.")
