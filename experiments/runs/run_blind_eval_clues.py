"""Step 2: Generate clue files for blind evaluation tasks.

Usage:
  1. Save the Creator LLM's output as blind-eval/blind-gold-tasks.json
  2. Run: python experiments/runs/run_blind_eval_clues.py
  3. Clue files will be generated in blind-eval/clues/
"""

import json
import time
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import (
    render_mrlf, generate_detail_store, write_detail_store, _token_count
)

GOLD_PATH = Path("experiments/runs/blind-eval/blind-gold-tasks.json")
OUT_DIR = Path("experiments/runs/blind-eval/clues")
PROMPT_DIR = Path("experiments/runs/blind-eval/prompts")


def main():
    if not GOLD_PATH.exists():
        print(f"ERROR: {GOLD_PATH} not found.")
        print("Run Step 1 first: paste step1-creator-prompt.md into GPT-5.4 or Gemini,")
        print("save the JSON output as blind-gold-tasks.json")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)

    golds = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(golds)} blind evaluation tasks")
    print("=" * 70)

    # Group by repo
    repos = {}
    for g in golds:
        repos.setdefault(g["repo"], []).append(g)

    # Read answerer template
    template_path = Path("experiments/runs/blind-eval/step3-answerer-template.md")
    answerer_template = template_path.read_text(encoding="utf-8")

    for repo_name, tasks in sorted(repos.items()):
        repo_path = Path(tasks[0].get("repo_path", f"experiments/external-repos/{repo_name}"))
        if not repo_path.exists():
            print(f"\n  {repo_name}: SKIP (repo not found at {repo_path})")
            continue

        print(f"\n  {repo_name}: extracting...", end=" ", flush=True)
        t0 = time.time()
        graph = extract_graph(repo_path)
        n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
        n_sym = len(graph.nodes) - n_mod
        print(f"{n_mod} mod, {n_sym} sym ({time.time()-t0:.1f}s)")

        # Generate detail store once per repo
        detail = generate_detail_store(graph, repo_root=str(repo_path))
        detail_path = OUT_DIR / f"{repo_name}.codeclue-detail"
        write_detail_store(detail, detail_path)
        print(f"    Detail store: {len(detail)} records")

        for gold in tasks:
            task_id = gold["task_id"]
            question = gold["question"]

            # Generate File 1
            clue = render_mrlf(graph, question, repo_root=str(repo_path))
            toks = _token_count(clue)
            clue_path = OUT_DIR / f"{task_id}.codeclue"
            clue_path.write_text(clue, encoding="utf-8")

            # Build gold facts block
            gold_facts = gold.get("gold_facts", [])
            facts_block = ""
            scoring_lines = ""
            scoring_json_parts = []
            for i, fact in enumerate(gold_facts, 1):
                facts_block += f"FACT {i}: {fact}\n"
                scoring_lines += f"FACT {i}: [COVERED or MISSED] - [brief justification]\n"
                scoring_json_parts.append(f'{{"fact": {i}, "verdict": "COVERED_or_MISSED", "reason": "..."}}')
            scoring_json_template = ", ".join(scoring_json_parts)

            # Build combined answerer+scorer prompt
            prompt = answerer_template.replace("{CLUE_CONTENT}", clue)
            prompt = prompt.replace("{QUESTION}", question)
            prompt = prompt.replace("{TASK_ID}", task_id)
            prompt = prompt.replace("{GOLD_FACTS_BLOCK}", facts_block.strip())
            prompt = prompt.replace("{SCORING_LINES}", scoring_lines.strip())
            prompt = prompt.replace("{SCORING_JSON_TEMPLATE}", scoring_json_template)
            prompt = prompt.replace("{TASK_ID}", task_id)
            prompt = prompt.replace("{GOLD_FACTS_BLOCK}", facts_block.strip())
            prompt = prompt.replace("{SCORING_LINES}", scoring_lines.strip())
            prompt_path = PROMPT_DIR / f"{task_id}-answerer.prompt.md"
            prompt_path.write_text(prompt, encoding="utf-8")

            print(f"    {task_id}: {toks} tokens, {len(gold_facts)} facts, prompt saved")

    print(f"\n{'=' * 70}")
    print(f"Clue files saved to: {OUT_DIR}")
    print(f"Answerer prompts saved to: {PROMPT_DIR}")
    print(f"\nNext: Open each prompt in {PROMPT_DIR} and paste into a different LLM")
    print(f"than the one that created the gold tasks.")


if __name__ == "__main__":
    main()
