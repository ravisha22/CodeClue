"""Check gold symbol coverage in FOCUS after the fix, for ALL 6 blind tasks."""
import json
import re
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _select_focus_nodes

TASKS_PATH = Path("experiments/runs/blind-eval/blind-gold-tasks.json")
with open(TASKS_PATH) as f:
    tasks = json.load(f)

REPO_MAP = {
    "aiohttp": Path("experiments/external-repos/aiohttp"),
    "fiber": Path("experiments/external-repos/fiber"),
    "click": Path("experiments/external-repos/click"),
}

# Cache graphs
graphs = {}
for repo_name, repo_path in REPO_MAP.items():
    print(f"Extracting graph for {repo_name}...")
    graphs[repo_name] = extract_graph(repo_path)

print("\n" + "=" * 60)
print("GOLD SYMBOL COVERAGE IN FOCUS (post-fix)")
print("=" * 60)

total_gold = 0
total_in_focus = 0

for t in tasks:
    tid = t["task_id"]
    repo = t["repo"]
    question = t["question"]
    gold_syms = t.get("gold_symbols", [])

    graph = graphs[repo]
    focus_nodes = _select_focus_nodes(graph, question)
    focus_names = {n.semantic_contract.get("symbol_name", "") for n in focus_nodes}

    print(f"\n--- {tid} ({repo}) ---")
    print(f"  Q: {question[:70]}...")
    print(f"  FOCUS nodes: {len(focus_nodes)}")

    task_in = 0
    for sym in gold_syms:
        # Check exact match and partial match (bare name)
        bare = sym.split(".")[-1]
        in_focus = bare in focus_names or sym in focus_names
        # Also check if any focus node's file+name matches
        if not in_focus:
            for fn in focus_nodes:
                sn = fn.semantic_contract.get("symbol_name", "")
                if bare == sn:
                    in_focus = True
                    break
        status = "IN FOCUS" if in_focus else "MISSING"
        if in_focus:
            task_in += 1
        print(f"  [{status:9s}] {sym}")

    total_gold += len(gold_syms)
    total_in_focus += task_in
    print(f"  Score: {task_in}/{len(gold_syms)}")

print(f"\n{'=' * 60}")
print(f"TOTAL: {total_in_focus}/{total_gold} gold symbols in FOCUS ({100*total_in_focus/total_gold:.0f}%)")
print(f"{'=' * 60}")
