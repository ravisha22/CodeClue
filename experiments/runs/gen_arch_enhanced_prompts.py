"""Prepend architectural summary to enterprise clue prompts and regenerate."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"
RESPONSE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "responses" / "enterprise-v3"
RESPONSE_DIR.mkdir(exist_ok=True)

# Load arch summaries
summaries_text = (REPO_ROOT / "experiments/runs/blind-eval/arch-summaries.md").read_text(encoding="utf-8")

# Split into per-repo summaries
saleor_summary = summaries_text[summaries_text.index("Saleor"):summaries_text.index("NetBox")].strip()
netbox_summary = summaries_text[summaries_text.index("NetBox"):].strip()

ARCH_INJECT = """
--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
{summary}
--- END ARCHITECTURAL CONTEXT ---

"""

# Load gold tasks
with open(REPO_ROOT / "experiments/runs/blind-eval/enterprise-gold-tasks-v2.json") as f:
    tasks = json.load(f)

for t in tasks:
    repo = t["repo"]
    task_id = t["task_id"]

    if repo not in ("saleor", "netbox"):
        continue

    summary = saleor_summary if repo == "saleor" else netbox_summary

    # Read existing prompt
    prompt_path = PROMPT_DIR / f"{task_id}-v23.prompt.md"
    if not prompt_path.exists():
        print(f"  SKIP {task_id}: no prompt")
        continue

    prompt = prompt_path.read_text(encoding="utf-8")

    # Inject arch summary BEFORE the clue file
    inject_point = prompt.find("--- CLUE FILE")
    if inject_point == -1:
        inject_point = prompt.find("--- CLUE")
    if inject_point == -1:
        print(f"  SKIP {task_id}: no clue marker found")
        continue

    enhanced_prompt = prompt[:inject_point] + ARCH_INJECT.format(summary=summary) + prompt[inject_point:]

    # Write enhanced prompt
    enhanced_path = PROMPT_DIR / f"{task_id}-v3.prompt.md"
    enhanced_path.write_text(enhanced_prompt, encoding="utf-8")
    print(f"  {task_id}: enhanced ({len(enhanced_prompt)} chars)")

print("\nDone.")
