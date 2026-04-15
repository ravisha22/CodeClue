"""v2.3 Full regeneration: ALL clues for ALL repos, properly question-conditioned."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import tiktoken
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store

_ENC = tiktoken.get_encoding("cl100k_base")
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

sys.path.insert(0, str(REPO_ROOT / "experiments" / "runs"))
from regen_clues_with_drilldown import (
    _parse_gaps, _select_drill_snippets, _token_count,
    DRILLDOWN_PROMPT_TEMPLATE, PLAIN_PROMPT_TEMPLATE,
)

LANG_MAP = {
    "aiohttp": "python", "click": "python", "fiber": "go",
    "requests": "python", "echo": "go", "zod": "typescript",
}

# Load ALL gold tasks (dev + blind)
dev_tasks = json.loads((REPO_ROOT / "experiments/runs/blind-eval/blind-gold-tasks.json").read_text())
blind_tasks = json.loads((REPO_ROOT / "experiments/runs/blind-eval/blind-gold-tasks-v2.json").read_text())
struct_rel = json.loads((REPO_ROOT / "experiments/runs/blind-eval/structural-relational-gold-tasks.json").read_text())
all_tasks = dev_tasks + blind_tasks + struct_rel

# Group by repo
repos = {}
for t in all_tasks:
    repo = t["repo"]
    if repo not in repos:
        repos[repo] = {"path": t.get("repo_path", f"experiments/external-repos/{repo}"), "tasks": []}
    repos[repo]["tasks"].append(t)

stats = {"total": 0, "structural": 0, "relational": 0, "mechanistic": 0, "drill": 0}

for repo_name, info in repos.items():
    repo_path = REPO_ROOT / info["path"]
    lang = LANG_MAP.get(repo_name, "python")

    print(f"\n=== {repo_name} ({lang}) ===")
    start = time.time()
    graph = extract_graph(repo_path, language=lang)
    elapsed = time.time() - start
    print(f"  Graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges ({elapsed:.1f}s)")

    detail_records = generate_detail_store(graph, repo_root=repo_path)
    detail_path = CLUE_DIR / f"{repo_name}.codeclue-detail"
    with open(detail_path, "w", encoding="utf-8") as f:
        for rec in detail_records:
            f.write(json.dumps(rec) + "\n")
    print(f"  Detail store: {len(detail_records)} records")

    for t in info["tasks"]:
        task_id = t["task_id"]
        question = t["question"]
        stats["total"] += 1

        # Generate question-conditioned clue
        clue = render_mrlf(graph, question, repo_root=repo_path)
        clue_path = CLUE_DIR / f"{task_id}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")

        gaps_info = _parse_gaps(clue)
        q_type = gaps_info["question_type"]
        drill_targets = gaps_info["drill_targets"]

        if q_type == "MECHANISTIC" and drill_targets:
            stats["mechanistic"] += 1
            stats["drill"] += 1
            snippets = _select_drill_snippets(
                drill_targets, detail_records, repo_path, clue_text=clue,
            )
            prompt = DRILLDOWN_PROMPT_TEMPLATE.format(
                task_id=task_id, clue=clue,
                drill_down_snippets=snippets, question=question,
            )
            prompt_path = PROMPT_DIR / f"{task_id}-v23.prompt.md"
        else:
            key = q_type.lower()
            stats[key] = stats.get(key, 0) + 1
            prompt = PLAIN_PROMPT_TEMPLATE.format(
                task_id=task_id, clue=clue, question=question,
            )
            prompt_path = PROMPT_DIR / f"{task_id}-v23.prompt.md"

        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"  {task_id}: {q_type} {'[DRILL]' if drill_targets and q_type == 'MECHANISTIC' else ''} {_token_count(prompt)} tok")

print(f"\n{'='*60}")
print(f"DONE: {stats['total']} tasks")
print(f"  STRUCTURAL: {stats['structural']}")
print(f"  RELATIONAL: {stats['relational']}")
print(f"  MECHANISTIC: {stats['mechanistic']} ({stats['drill']} with drill-down)")
print(f"{'='*60}")
