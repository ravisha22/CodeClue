"""Generate File-1-only (no drill-down) prompts for ALL mechanistic tasks.

This is for the ablation study: comparing File 1 only vs File 1 + drill-down.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

PLAIN_TEMPLATE = (
    "# Blind Evaluation Prompt - MRLF v2.3 (File 1 Only — No Drill-Down)\n"
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
    "For each claim you make, cite the specific clue entry that supports it.\n"
)

# Load all gold tasks
dev_tasks = json.loads((REPO_ROOT / "experiments/runs/blind-eval/blind-gold-tasks.json").read_text())
blind_tasks = json.loads((REPO_ROOT / "experiments/runs/blind-eval/blind-gold-tasks-v2.json").read_text())
all_tasks = dev_tasks + blind_tasks

count = 0
for t in all_tasks:
    task_id = t["task_id"]
    question = t["question"]

    # Only mechanistic tasks (the ones that normally get drill-down)
    clue_path = CLUE_DIR / f"{task_id}.codeclue"
    if not clue_path.exists():
        continue

    clue = clue_path.read_text(encoding="utf-8")
    prompt = PLAIN_TEMPLATE.format(task_id=task_id, clue=clue, question=question)
    prompt_path = PROMPT_DIR / f"{task_id}-v23-file1only.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    count += 1
    print(f"  {task_id}: file1-only prompt generated")

print(f"\nDone: {count} file1-only prompts generated.")
