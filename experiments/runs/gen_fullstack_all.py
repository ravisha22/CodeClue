"""Build full-stack enterprise prompts for all repos with deep context files."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

# Load arch summaries
arch_text = (REPO_ROOT / "experiments/runs/blind-eval/arch-summaries.md").read_text(encoding="utf-8")
saleor_arch = arch_text[arch_text.index("Saleor"):arch_text.index("NetBox")].strip()
netbox_arch = arch_text[arch_text.index("NetBox"):].strip()

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

# Map repos to their context files
REPO_CONTEXTS = {}
for repo in ["netbox", "consul", "mattermost", "calcom", "maybe", "grafana", "supabase"]:
    deep_path = REPO_ROOT / f"experiments/runs/blind-eval/{repo}-deep-context.md"
    if deep_path.exists():
        REPO_CONTEXTS[repo] = {
            "deep": deep_path.read_text(encoding="utf-8"),
            "arch": netbox_arch if repo == "netbox" else f"(See deep context below for {repo} architecture)",
        }

count = 0
for t in tasks:
    repo = t["repo"]
    task_id = t["task_id"]

    if repo == "saleor":  # Already done in v4
        continue
    if repo not in REPO_CONTEXTS:
        continue

    prompt_path = PROMPT_DIR / f"{task_id}-v23.prompt.md"
    if not prompt_path.exists():
        print(f"  SKIP {task_id}: no base prompt")
        continue

    prompt = prompt_path.read_text(encoding="utf-8")
    inject_point = prompt.find("--- CLUE FILE")
    if inject_point == -1:
        inject_point = prompt.find("--- CLUE")
    if inject_point == -1:
        print(f"  SKIP {task_id}: no marker")
        continue

    ctx = REPO_CONTEXTS[repo]
    enhanced = prompt[:inject_point] + FULL_STACK_INJECT.format(
        arch=ctx["arch"], deep=ctx["deep"]
    ) + prompt[inject_point:]

    out_path = PROMPT_DIR / f"{task_id}-v4-fullstack.prompt.md"
    out_path.write_text(enhanced, encoding="utf-8")
    count += 1
    print(f"  {task_id}: {len(enhanced)} chars")

print(f"\nDone: {count} prompts generated.")
