"""Diagnostic: Check if L3 FOCUS now includes gold symbols via direct name-match.

Runs on Flask AND httpx to guard against single-repo overfitting.
"""
import json
from pathlib import Path
from collections import defaultdict
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _select_focus_nodes, _extract_question_keywords

TASKS = json.loads(Path("experiments/runs/mrlf-benchmark/gold-tasks.json").read_text())


def check_repo(repo_name: str):
    repo_tasks = [t for t in TASKS if t["repo"] == repo_name]
    if not repo_tasks:
        print(f"  {repo_name}: no tasks found")
        return

    repo_path = Path(repo_tasks[0]["repo_path"])
    graph = extract_graph(repo_path)

    # Build name lookup
    name_to_node = {}
    for n in graph.nodes:
        sc = n.semantic_contract or {}
        sym = sc.get("symbol_name", "")
        name_to_node[sym] = n
        short = sym.rsplit(".", 1)[-1] if "." in sym else sym
        if short != sym:
            name_to_node.setdefault(short, n)

    print(f"\n{'='*80}")
    print(f"  {repo_name}: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    print(f"{'='*80}")

    for task in repo_tasks:
        focus = _select_focus_nodes(graph, task["question"])
        focus_names = set()
        for fn in focus:
            sc = fn.semantic_contract or {}
            sym = sc.get("symbol_name", fn.node_id)
            focus_names.add(sym)
            short = sym.rsplit(".", 1)[-1] if "." in sym else sym
            focus_names.add(short)

        hits = 0
        total = len(task["gold_symbols"])
        for gs in task["gold_symbols"]:
            gs_short = gs.rsplit(".", 1)[-1] if "." in gs else gs
            found = gs in focus_names or gs_short in focus_names
            if found:
                hits += 1
            tag = "HIT" if found else "MISS"
            print(f"  {task['task_id']:40s} {gs:30s} {tag}")

        recall = hits / total if total > 0 else 0
        print(f"  {'':40s} Focus sym recall: {hits}/{total} = {recall:.2f}")
        print()


def main():
    for repo in ["flask", "httpx"]:
        check_repo(repo)


if __name__ == "__main__":
    main()
