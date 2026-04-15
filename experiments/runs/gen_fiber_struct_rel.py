"""Generate question-conditioned fiber structural/relational clues and prompts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from codeclue_research.clue_view_mrlf import render_mrlf
from codeclue_research.extractor import extract_graph

TASKS_PATH = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "structural-relational-gold-tasks.json"
CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"
FIBER_ROOT = REPO_ROOT / "experiments" / "external-repos" / "fiber"

PROMPT_HEADER = (
    "# Blind Evaluation Prompt - MRLF v2.1 (Structural/Relational)\n"
    "# Task: {task_id}\n\n"
    "You are a senior software engineer. You have been given a codebase\n"
    "comprehension artifact (a 'clue file') that summarises a repository's\n"
    "structure, symbols, and behavior. This is NOT the full source code - it is\n"
    "a compressed representation.\n\n"
    "Answer the question below using ONLY the information in the clue file.\n"
    "Do not use any external knowledge about the framework or library.\n\n"
    "--- CLUE FILE START ---\n{clue}\n--- CLUE FILE END ---\n\n"
    "QUESTION: {question}\n\n"
    "Provide a detailed answer based solely on the clue file above.\n"
    "For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.\n"
)


def main() -> None:
    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    fiber_tasks = [task for task in tasks if task.get("repo") == "fiber"]

    print("Extracting fiber graph...")
    graph = extract_graph(FIBER_ROOT, language="go")
    print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges")

    for task in fiber_tasks:
        task_id = task["task_id"]
        question = task["question"]
        clue = render_mrlf(graph, question, repo_root=FIBER_ROOT)

        clue_path = CLUE_DIR / f"{task_id}.codeclue"
        prompt_path = PROMPT_DIR / f"{task_id}-answerer.prompt.md"
        clue_path.write_text(clue, encoding="utf-8")

        prompt = PROMPT_HEADER.format(task_id=task_id, clue=clue, question=question)
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"  {task_id}: generated ({len(clue)} chars clue)")

    print("Done.")


if __name__ == "__main__":
    main()
