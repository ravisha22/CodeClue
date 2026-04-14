"""Rebuild LLM consumer prompts with self-scoring.

The prompt now has TWO sections:
  PART 1: Answer the question from the clue (same as before)
  PART 2: Self-score against gold facts and output a structured scoring block

The LLM outputs its answer AND the scoring in one response.
"""
import json
from pathlib import Path

GOLD_PATH = Path("experiments/runs/mrlf-benchmark/gold-tasks.json")
CLUE_DIR = Path("experiments/runs/mrlf-benchmark")
PROMPT_DIR = CLUE_DIR / "llm-prompts"
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

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
        continue

    clue_path = CLUE_DIR / f"{task_id}.codeclue"
    if not clue_path.exists():
        continue

    clue = clue_path.read_text(encoding="utf-8")

    # Build gold facts block for self-scoring
    facts_block = ""
    for i, fact in enumerate(gold.get("gold_facts", []), 1):
        facts_block += f"FACT {i}: {fact}\n"

    prompt = f"""You have TWO tasks to complete. Read carefully.

=== TASK 1: ANSWER THE QUESTION ===

You are a senior software engineer reading a codebase comprehension artifact (a "clue file") that summarises a repository's structure and behavior. Answer the question below using ONLY the information in the clue file. Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
{clue}
--- CLUE FILE END ---

QUESTION: {gold["question"]}

Provide a detailed answer covering:
1. Which specific files and symbols are involved
2. How the mechanism works (based on what the clue tells you)
3. Any security properties, error handling, or invariants mentioned in the clue
4. What risks or gaps you can identify from the clue

=== TASK 2: SELF-SCORE YOUR ANSWER ===

After writing your answer above, score it against these gold facts.
For EACH fact below, state whether your answer COVERS it (the information is present or can be inferred from your answer) or MISSES it (the information is not in your answer).

{facts_block}
Output your scoring in this EXACT format at the end of your response:

```
=== SCORING ===
Task: {task_id}
Model: [state which model you are, e.g. Claude Opus 4.6, GPT-5.4, Gemini 3.4]
FACT 1: [COVERS or MISSES] - [brief justification]
FACT 2: [COVERS or MISSES] - [brief justification]
FACT 3: [COVERS or MISSES] - [brief justification]
FACT 4: [COVERS or MISSES] - [brief justification]
Score: [count of COVERS]/[total facts]
Sufficient: [YES if score >= 60%, NO otherwise]
```
"""

    prompt_path = PROMPT_DIR / f"{task_id}.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    print(f"  {task_id}: {len(prompt)} chars ({len(gold.get('gold_facts', []))} facts)")

print(f"\nAll prompts saved to {PROMPT_DIR}")
print(f"\nSuggested model split for cross-model validation:")
print(f"  GPT-5.4:   flask-tf1, flask-tf5, httpx-tf5, fastapi-tf5")
print(f"  Gemini 3.4: gin-tf5, fastapi-tf1, fastapi-tf4")
print(f"\nFor each prompt:")
print(f"  1. Open the .prompt.md file")
print(f"  2. Copy ALL content into a fresh chat with the assigned model")
print(f"  3. The model will answer AND self-score")
print(f"  4. Copy the === SCORING === block from the response")
print(f"  5. Paste it back to me for tabulation")
