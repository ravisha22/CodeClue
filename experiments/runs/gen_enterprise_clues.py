"""Generate clues for enterprise repos that have been extracted."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store
from regen_clues_with_drilldown import (
    _parse_gaps, _select_drill_snippets, _token_count,
    DRILLDOWN_PROMPT_TEMPLATE, PLAIN_PROMPT_TEMPLATE,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

with open(REPO_ROOT / "experiments/runs/blind-eval/enterprise-gold-tasks.json") as f:
    tasks = json.load(f)

LANG_MAP = {
    "saleor": "python", "netbox": "python",
    "maybe": "typescript", "calcom": "typescript", "supabase": "typescript",
    "mattermost": "go", "consul": "go", "grafana": "go",
}

# Only process repos passed as args (or all if no args)
import sys as _sys
target_repos = _sys.argv[1:] if len(_sys.argv) > 1 else list(LANG_MAP.keys())

for repo_name in target_repos:
    if repo_name not in LANG_MAP:
        continue
    repo_path = REPO_ROOT / "experiments" / "external-repos" / repo_name
    lang = LANG_MAP[repo_name]
    print(f"\n=== {repo_name} ({lang}) ===")

    start = time.time()
    graph = extract_graph(repo_path, language=lang)
    elapsed = time.time() - start
    print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges ({elapsed:.1f}s)")

    detail_records = generate_detail_store(graph, repo_root=repo_path)
    detail_path = CLUE_DIR / f"{repo_name}.codeclue-detail"
    with open(detail_path, "w", encoding="utf-8") as f:
        for rec in detail_records:
            f.write(json.dumps(rec) + "\n")
    print(f"  Detail store: {len(detail_records)} records")

    repo_tasks = [t for t in tasks if t["repo"] == repo_name]
    for t in repo_tasks:
        task_id = t["task_id"]
        question = t["question"]

        clue = render_mrlf(graph, question, repo_root=repo_path)
        clue_path = CLUE_DIR / f"{task_id}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")

        gaps_info = _parse_gaps(clue)
        q_type = gaps_info["question_type"]
        drill_targets = gaps_info["drill_targets"]

        if q_type == "MECHANISTIC" and drill_targets:
            snippets = _select_drill_snippets(
                drill_targets, detail_records, repo_path, clue_text=clue,
            )
            prompt = DRILLDOWN_PROMPT_TEMPLATE.format(
                task_id=task_id, clue=clue,
                drill_down_snippets=snippets, question=question,
            )
        else:
            prompt = PLAIN_PROMPT_TEMPLATE.format(
                task_id=task_id, clue=clue, question=question,
            )

        prompt_path = PROMPT_DIR / f"{task_id}-v23.prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"  {task_id}: {q_type} {_token_count(prompt)} tok")

    print(f"  Done {repo_name}")

print("\nAll done.")
