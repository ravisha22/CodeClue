"""Regenerate all blind-eval clue files and prompts with MRLF v2.1."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GOLD_TASKS = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "blind-gold-tasks.json"
CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

LANG_MAP = {
    "aiohttp": "python",
    "click": "python",
    "flask": "python",
    "httpx": "python",
    "fastapi": "python",
    "django": "python",
    "fiber": "go",
    "gin": "go",
    "chi": "go",
    "echo": "go",
    "express": "typescript",
    "nest": "typescript",
    "typeorm": "typescript",
}

PROMPT_TEMPLATE = """\
# Blind Evaluation Prompt - MRLF v2.1
# Run this in a SEPARATE session (fresh chat, no prior context).
# Task: {task_id}

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.
If the clue does not contain enough information to fully answer, say what
you CAN determine and what you CANNOT.

--- CLUE FILE START ---
{clue}
--- CLUE FILE END ---

QUESTION: {question}

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
"""


def main():
    with open(GOLD_TASKS) as f:
        tasks = json.load(f)

    # Group tasks by repo
    repos: dict[str, dict] = {}
    for t in tasks:
        repo = t["repo"]
        if repo not in repos:
            repos[repo] = {"path": t["repo_path"], "tasks": []}
        repos[repo]["tasks"].append(t)

    for repo, info in repos.items():
        print(f"--- Extracting {repo} ---")
        repo_path = REPO_ROOT / info["path"]
        lang = LANG_MAP.get(repo, "python")

        graph = extract_graph(repo_path, language=lang)
        print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges")

        # Generate detail store (one per repo)
        detail_records = generate_detail_store(graph, repo_root=repo_path)
        detail_path = CLUE_DIR / f"{repo}.codeclue-detail"
        with open(detail_path, "w", encoding="utf-8") as f:
            for rec in detail_records:
                f.write(json.dumps(rec) + "\n")
        print(f"  Detail store: {len(detail_records)} records -> {detail_path.name}")

        # Generate clue + prompt per task
        for t in info["tasks"]:
            task_id = t["task_id"]
            question = t["question"]

            clue = render_mrlf(graph, question, repo_root=repo_path)
            clue_path = CLUE_DIR / f"{task_id}.codeclue"
            clue_path.write_text(clue, encoding="utf-8")

            behavior_count = clue.count("behavior:")
            print(f"  {task_id}: clue ({len(clue)} chars, {behavior_count} behavior annotations)")

            prompt = PROMPT_TEMPLATE.format(
                task_id=task_id,
                clue=clue,
                question=question,
            )
            prompt_path = PROMPT_DIR / f"{task_id}-answerer.prompt.md"
            prompt_path.write_text(prompt, encoding="utf-8")

    print()
    print("=== DONE: All clue files and prompts regenerated with MRLF v2.1 ===")


if __name__ == "__main__":
    main()
