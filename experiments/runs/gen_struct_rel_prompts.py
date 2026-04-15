"""Generate structural/relational prompts for fiber tasks."""
import json, sys
sys.path.insert(0, "src")
from pathlib import Path
from codeclue_research.clue_view_mrlf import render_mrlf
from codeclue_research.extractor import extract_graph

with open("experiments/runs/blind-eval/structural-relational-gold-tasks.json") as f:
    tasks = json.load(f)

CLUE_DIR = Path("experiments/runs/blind-eval/clues")
PROMPT_DIR = Path("experiments/runs/blind-eval/prompts")

PROMPT_TEMPLATE = (
    "# Blind Evaluation Prompt - MRLF v2.1 (Structural/Relational)\n"
    "# Task: {task_id}\n\n"
    "You are a senior software engineer. You have been given a codebase\n"
    "comprehension artifact (a \"clue file\") that summarises a repository's\n"
    "structure, symbols, and behavior. This is NOT the full source code - it is\n"
    "a compressed representation.\n\n"
    "Answer the question below using ONLY the information in the clue file.\n"
    "Do not use any external knowledge about the framework or library.\n\n"
    "--- CLUE FILE START ---\n{clue}\n--- CLUE FILE END ---\n\n"
    "QUESTION: {question}\n\n"
    "Provide a detailed answer based solely on the clue file above.\n"
    "For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.\n"
)

repo_root = Path("experiments/external-repos/fiber")
print("Extracting fiber graph...")
fiber_graph = extract_graph(repo_root, language="go")
print(f"  {len(fiber_graph.nodes)} nodes, {len(fiber_graph.edges)} edges")

for t in tasks:
    tid = t["task_id"]
    repo = t["repo"]
    question = t["question"]

    prompt_path = PROMPT_DIR / f"{tid}-answerer.prompt.md"
    clue_path = CLUE_DIR / f"{tid}.codeclue"

    if prompt_path.exists():
        print(f"  {tid}: prompt exists, skipping")
        continue

    if repo != "fiber":
        print(f"  {tid}: not fiber, skipping")
        continue

    clue = render_mrlf(fiber_graph, question, repo_root=repo_root)
    clue_path.write_text(clue, encoding="utf-8")
    prompt = PROMPT_TEMPLATE.format(task_id=tid, clue=clue, question=question)
    prompt_path.write_text(prompt, encoding="utf-8")
    print(f"  {tid}: generated ({len(clue)} chars)")

print("Done.")
