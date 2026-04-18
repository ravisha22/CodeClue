"""Build full-stack enterprise prompts: arch summary + deep context + clue + drill-down."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

# Load contexts
arch = (REPO_ROOT / "experiments/runs/blind-eval/arch-summaries.md").read_text(encoding="utf-8")
saleor_arch = arch[arch.index("Saleor"):arch.index("NetBox")].strip()
deep_ctx = (REPO_ROOT / "experiments/runs/blind-eval/saleor-deep-context.md").read_text(encoding="utf-8")

FULL_STACK_INJECT = """
--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
{arch}
--- END ARCHITECTURAL CONTEXT ---

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
{deep}
--- END DEEP DOMAIN CONTEXT ---

"""

with open(REPO_ROOT / "experiments/runs/blind-eval/enterprise-gold-tasks-v2.json") as f:
    tasks = json.load(f)

for t in tasks:
    if t["repo"] != "saleor":
        continue
    task_id = t["task_id"]

    prompt_path = PROMPT_DIR / f"{task_id}-v23.prompt.md"
    if not prompt_path.exists():
        print(f"  SKIP {task_id}")
        continue

    prompt = prompt_path.read_text(encoding="utf-8")

    inject_point = prompt.find("--- CLUE FILE")
    if inject_point == -1:
        inject_point = prompt.find("--- CLUE")
    if inject_point == -1:
        print(f"  SKIP {task_id}: no marker")
        continue

    enhanced = prompt[:inject_point] + FULL_STACK_INJECT.format(arch=saleor_arch, deep=deep_ctx) + prompt[inject_point:]

    out_path = PROMPT_DIR / f"{task_id}-v4-fullstack.prompt.md"
    out_path.write_text(enhanced, encoding="utf-8")
    print(f"  {task_id}: {len(enhanced)} chars")

print("Done.")
