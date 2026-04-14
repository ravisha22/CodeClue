"""Build LLM consumer prompts for the 7 failing Phase 4 tasks.

Generates one prompt file per task containing:
  - System instruction (answer from clue only)
  - The MRLF clue content
  - The gold question
  - Gold facts (hidden from LLM, shown to human scorer)

Output: experiments/runs/mrlf-benchmark/llm-prompts/
"""
import json
from pathlib import Path

GOLD_PATH = Path("experiments/runs/mrlf-benchmark/gold-tasks.json")
CLUE_DIR = Path("experiments/runs/mrlf-benchmark")
PROMPT_DIR = CLUE_DIR / "llm-prompts"
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

# The 7 failing tasks from Phase 4
FAILING_TASKS = [
    "flask-tf1-refactor-sessions",
    "flask-tf5-session-security",
    "httpx-tf5-redirect-security",
    "gin-tf5-credential-handling",
    "fastapi-tf1-dependency-injection",
    "fastapi-tf4-form-parsing",
    "fastapi-tf5-input-validation",
]

golds = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
gold_by_id = {g["task_id"]: g for g in golds}

for task_id in FAILING_TASKS:
    gold = gold_by_id.get(task_id)
    if not gold:
        print(f"SKIP: {task_id} not in gold tasks")
        continue

    clue_path = CLUE_DIR / f"{task_id}.codeclue"
    if not clue_path.exists():
        print(f"SKIP: {task_id} no clue file")
        continue

    clue = clue_path.read_text(encoding="utf-8")

    # Build consumer prompt
    prompt = f"""You are a senior software engineer reading a codebase comprehension artifact (a "clue file") that summarises a repository's structure and behavior. Your task is to answer the question below using ONLY the information in the clue file. Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
{clue}
--- CLUE FILE END ---

QUESTION: {gold["question"]}

Please provide a detailed answer covering:
1. Which specific files and symbols are involved
2. How the mechanism works (based on what the clue tells you)
3. Any security properties, error handling, or invariants mentioned in the clue
4. What risks or gaps you can identify from the clue

Answer thoroughly, citing specific information from the clue file.
"""

    # Build scoring guide (for the human scorer, NOT sent to LLM)
    scoring = f"""
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: {task_id}
Repo: {gold["repo"]}
Family: {gold["family"]}

Gold Facts to check in the LLM's answer:
"""
    for i, fact in enumerate(gold.get("gold_facts", []), 1):
        scoring += f"  FACT {i}: {fact}\n"
        scoring += f"    [ ] PRESENT — LLM's answer contains or implies this fact\n"
        scoring += f"    [ ] ABSENT  — LLM's answer does not mention this\n\n"

    scoring += f"""
Scoring:
  Count PRESENT facts: ___/{len(gold.get('gold_facts', []))}
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
"""

    # Save prompt and scoring guide
    prompt_path = PROMPT_DIR / f"{task_id}.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    score_path = PROMPT_DIR / f"{task_id}.scoring.md"
    score_path.write_text(scoring, encoding="utf-8")

    print(f"  {task_id}: prompt={len(prompt)} chars, clue={len(clue)} chars")

print(f"\nPrompts saved to {PROMPT_DIR}")
print(f"\nINSTRUCTIONS:")
print(f"1. Open each .prompt.md file")
print(f"2. Copy the ENTIRE content into a fresh Copilot Chat / Claude / GPT session")
print(f"3. Read the LLM's response")
print(f"4. Open the matching .scoring.md file")
print(f"5. Check each gold fact against the response: PRESENT or ABSENT")
print(f"6. Record the fidelity score")
