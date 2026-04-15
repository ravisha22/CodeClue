"""Generate clues and drill-down prompts for blind-eval v2 repos (requests, echo, zod).

Uses the frozen v2.1.1 selector. Only processes Python and TypeScript repos
(Go extraction hangs on large repos — echo will use summary-only clue approach).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import tiktoken
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store

_ENC = tiktoken.get_encoding("cl100k_base")
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

with open(REPO_ROOT / "experiments/runs/blind-eval/blind-gold-tasks-v2.json") as f:
    tasks = json.load(f)

CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"
CLUE_DIR.mkdir(exist_ok=True)
PROMPT_DIR.mkdir(exist_ok=True)

LANG_MAP = {"requests": "python", "echo": "go", "zod": "typescript"}

DRILLDOWN_TOKEN_BUDGET = 2000

# Import drill-down helpers from the existing script
sys.path.insert(0, str(REPO_ROOT / "experiments" / "runs"))
from regen_clues_with_drilldown import (
    _parse_gaps, _select_drill_snippets, _token_count, _load_detail_store,
    DRILLDOWN_PROMPT_TEMPLATE, PLAIN_PROMPT_TEMPLATE,
)


def process_repo(repo_name: str):
    repo_path = REPO_ROOT / "experiments" / "external-repos" / repo_name
    lang = LANG_MAP[repo_name]

    print(f"\n=== Processing {repo_name} ({lang}) ===")
    print(f"Extracting graph...")
    graph = extract_graph(repo_path, language=lang)
    print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges")

    # Generate detail store
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

        # Generate clue
        clue = render_mrlf(graph, question, repo_root=repo_path)
        clue_path = CLUE_DIR / f"{task_id}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")

        # Parse GAPS
        gaps_info = _parse_gaps(clue)
        q_type = gaps_info["question_type"]
        drill_targets = gaps_info["drill_targets"]

        if q_type == "MECHANISTIC" and drill_targets:
            snippets = _select_drill_snippets(
                drill_targets, detail_records, repo_path,
                clue_text=clue,
            )
            prompt = DRILLDOWN_PROMPT_TEMPLATE.format(
                task_id=task_id, clue=clue,
                drill_down_snippets=snippets, question=question,
            )
            prompt_path = PROMPT_DIR / f"{task_id}-drilldown.prompt.md"
        else:
            prompt = PLAIN_PROMPT_TEMPLATE.format(
                task_id=task_id, clue=clue, question=question,
            )
            prompt_path = PROMPT_DIR / f"{task_id}-answerer.prompt.md"

        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"  {task_id}: {q_type} — {_token_count(prompt)} tok")
        if drill_targets:
            print(f"    drill: {[d['symbol'] for d in drill_targets]}")


if __name__ == "__main__":
    # Process repos in order; skip Go if it hangs
    for repo in ["requests", "zod", "echo"]:
        try:
            process_repo(repo)
        except Exception as e:
            print(f"  ERROR processing {repo}: {e}")
            import traceback
            traceback.print_exc()
