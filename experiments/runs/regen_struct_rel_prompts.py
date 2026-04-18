"""Generate prompts for structural/relational gold tasks."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GOLD_FILE = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "structural-relational-gold-tasks.json"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

PROMPT_TEMPLATE = """\
# Blind Evaluation Prompt - MRLF v2.1 (Structural/Relational)
# Task: {task_id}

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
{clue}
--- CLUE FILE END ---

QUESTION: {question}

Provide a detailed answer based solely on the clue file above.
For each claim, cite the specific clue entry that supports it.
"""

LANG_MAP = {"aiohttp": "python", "click": "python", "fiber": "go"}


def main():
    with open(GOLD_FILE) as f:
        tasks = json.load(f)

    for repo, lang in [("aiohttp", "python"), ("fiber", "go")]:
        repo_path = REPO_ROOT / "experiments" / "external-repos" / repo
        print(f"Extracting {repo}...", flush=True)
        graph = extract_graph(repo_path, language=lang)
        print(f"  {len(graph.nodes)} nodes", flush=True)

        repo_tasks = [t for t in tasks if t["repo"] == repo]
        for t in repo_tasks:
            clue = render_mrlf(graph, t["question"], repo_root=repo_path)
            prompt = PROMPT_TEMPLATE.format(
                task_id=t["task_id"], clue=clue, question=t["question"]
            )
            out = PROMPT_DIR / f"{t['task_id']}-answerer.prompt.md"
            out.write_text(prompt, encoding="utf-8")
            print(f"  {t['task_id']}: prompt written", flush=True)

        del graph
    print("Done.")


if __name__ == "__main__":
    main()
