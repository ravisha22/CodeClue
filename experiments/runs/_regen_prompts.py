"""Regenerate ONLY the prompt files from existing clues + gold tasks."""
import json
from pathlib import Path

GOLD_PATH = Path("experiments/runs/blind-eval/blind-gold-tasks.json")
CLUE_DIR = Path("experiments/runs/blind-eval/clues")
PROMPT_DIR = Path("experiments/runs/blind-eval/prompts")
TEMPLATE_PATH = Path("experiments/runs/blind-eval/step3-answerer-template.md")

PROMPT_DIR.mkdir(parents=True, exist_ok=True)

golds = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
template = TEMPLATE_PATH.read_text(encoding="utf-8")

for gold in golds:
    task_id = gold["task_id"]
    question = gold["question"]

    clue_path = CLUE_DIR / f"{task_id}.codeclue"
    if not clue_path.exists():
        print(f"  {task_id}: SKIP (no clue file)")
        continue

    clue = clue_path.read_text(encoding="utf-8")
    gold_facts = gold.get("gold_facts", [])

    facts_block = ""
    scoring_lines = ""
    scoring_json_parts = []
    for i, fact in enumerate(gold_facts, 1):
        facts_block += f"FACT {i}: {fact}\n"
        scoring_lines += f"FACT {i}: [COVERED or MISSED] - [brief justification]\n"
        scoring_json_parts.append(f'{{"fact": {i}, "verdict": "COVERED_or_MISSED", "reason": "..."}}')
    scoring_json_template = ", ".join(scoring_json_parts)

    prompt = template.replace("{CLUE_CONTENT}", clue)
    prompt = prompt.replace("{QUESTION}", question)
    prompt = prompt.replace("{TASK_ID}", task_id)
    prompt = prompt.replace("{GOLD_FACTS_BLOCK}", facts_block.strip())
    prompt = prompt.replace("{SCORING_LINES}", scoring_lines.strip())
    prompt = prompt.replace("{SCORING_JSON_TEMPLATE}", scoring_json_template)

    prompt_path = PROMPT_DIR / f"{task_id}-answerer.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    print(f"  {task_id}: prompt regenerated ({len(gold_facts)} facts)")

print(f"\nAll prompts saved to {PROMPT_DIR}")
