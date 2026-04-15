"""Generate fiber struct/rel prompts from existing clue data."""
import json
import re
from pathlib import Path

base_clue = Path("experiments/runs/blind-eval/clues/blind-fiber-1.codeclue").read_text(encoding="utf-8")

with open("experiments/runs/blind-eval/structural-relational-gold-tasks.json") as f:
    tasks = json.load(f)

PROMPT_DIR = Path("experiments/runs/blind-eval/prompts")
CLUE_DIR = Path("experiments/runs/blind-eval/clues")

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

for t in tasks:
    if t["repo"] != "fiber":
        continue

    tid = t["task_id"]
    question = t["question"]

    clue = re.sub(r"^\? .+$", f"? {question}", base_clue, count=1, flags=re.MULTILINE)

    clue_path = CLUE_DIR / f"{tid}.codeclue"
    clue_path.write_text(clue, encoding="utf-8")

    prompt = PROMPT_HEADER.format(task_id=tid, clue=clue, question=question)
    prompt_path = PROMPT_DIR / f"{tid}-answerer.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    print(f"{tid}: generated ({len(clue)} chars clue, {len(prompt)} chars prompt)")

print("Done.")
