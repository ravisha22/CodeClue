"""Cross-repo durability check: Run Phase 3 on Nest, Django, Chi with the new sorting code.
These repos were NOT used during the keyword relevance fix development."""

import json
import time
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, _token_count

# Nest tasks (TypeScript)
NEST_TASKS = [
    {"task_id": "nest-tf1-module-refactor", "question": "If I refactor the module system to use dynamic imports, what breaks?",
     "gold_files": ["packages/core/injector/module.ts", "packages/core/injector/module-ref.ts"],
     "gold_symbols": ["Module", "ModuleRef", "DynamicModule"]},
    {"task_id": "nest-tf5-auth-security", "question": "What security mechanisms protect authentication and authorization?",
     "gold_files": ["packages/core/guards/guards-consumer.ts", "packages/common/decorators/core/set-metadata.decorator.ts"],
     "gold_symbols": ["GuardsConsumer", "SetMetadata", "AuthGuard"]},
]

# Chi tasks (Go)
CHI_TASKS = [
    {"task_id": "chi-tf1-router-refactor", "question": "How would you refactor the router tree to support versioned APIs?",
     "gold_files": ["mux.go", "tree.go"],
     "gold_symbols": ["Mux", "node", "addRoute"]},
    {"task_id": "chi-tf2-middleware-impact", "question": "What is the downstream impact of modifying the middleware chain?",
     "gold_files": ["mux.go", "middleware.go"],
     "gold_symbols": ["Middlewares", "Handler", "Use"]},
]

REPOS = {
    "nest": ("experiments/external-repos/nest", NEST_TASKS),
    "chi": ("experiments/external-repos/chi", CHI_TASKS),
}

import re

def extract_mentioned_symbols(clue_text):
    symbols = set()
    in_sym = False
    for line in clue_text.split("\n"):
        if line.strip() == "-- SYM":
            in_sym = True
            continue
        if line.startswith("-- ") and in_sym:
            in_sym = False
            continue
        if in_sym and line.strip() and not line.strip().startswith("..."):
            first_token = line.split()[0] if line.split() else ""
            if first_token and len(first_token) > 1:
                symbols.add(first_token)
                if "." in first_token:
                    symbols.add(first_token.rsplit(".", 1)[-1])
    in_focus = False
    for line in clue_text.split("\n"):
        if line.strip() == "-- FOCUS":
            in_focus = True
            continue
        if line.startswith("-- ") and in_focus:
            in_focus = False
            continue
        if in_focus and line.strip() and not line.startswith("  "):
            paren_pos = line.find(" (")
            if paren_pos > 0:
                sym = line[:paren_pos].strip()
                if sym:
                    symbols.add(sym)
    for match in re.finditer(r'\b([A-Z]\w+)\b', clue_text):
        symbols.add(match.group(1))
    for match in re.finditer(r'\b([a-z_]\w{2,})\b', clue_text):
        name = match.group(1)
        if name not in {'the', 'and', 'for', 'not', 'function', 'class', 'module',
                       'extends', 'imports', 'calls', 'called_by', 'raises', 'attrs',
                       'files', 'symbols', 'more', 'modules', 'async_function'}:
            symbols.add(name)
    return symbols

def score_task(clue_text, gold):
    mentioned = extract_mentioned_symbols(clue_text)
    gold_syms = set(gold["gold_symbols"])
    if gold_syms:
        hits = sum(1 for gs in gold_syms if gs in mentioned or gs.rsplit(".", 1)[-1] in mentioned
                   or any(gs.lower() == ms.lower() for ms in mentioned))
        sym_recall = hits / len(gold_syms)
    else:
        sym_recall = 1.0
    
    gold_files = set(gold["gold_files"])
    mentioned_files = set(re.findall(r'[\w./\-]+\.\w{1,4}', clue_text))
    if gold_files:
        fhits = sum(1 for gf in gold_files if any(gf.split("/")[-1] == mf.split("/")[-1] for mf in mentioned_files))
        file_recall = fhits / len(gold_files)
    else:
        file_recall = 1.0
    
    loc = 0.4 * file_recall + 0.6 * sym_recall
    return {"task_id": gold["task_id"], "loc": round(loc, 3), "sym_recall": round(sym_recall, 3),
            "file_recall": round(file_recall, 3), "sufficient": loc >= 0.60}

print("Cross-Repo Durability Check")
print("=" * 70)

for repo_name, (repo_path_str, tasks) in REPOS.items():
    repo_path = Path(repo_path_str)
    if not repo_path.exists():
        print(f"\n  {repo_name}: SKIP (not found)")
        continue
    
    print(f"\n  {repo_name}: extracting...", end=" ", flush=True)
    t0 = time.time()
    graph = extract_graph(repo_path)
    print(f"({time.time()-t0:.1f}s)")
    
    for task in tasks:
        clue = render_mrlf(graph, task["question"], repo_root=str(repo_path))
        toks = _token_count(clue)
        result = score_task(clue, task)
        status = "PASS" if result["sufficient"] else "FAIL"
        print(f"    {result['task_id']:40s} loc={result['loc']:.3f} "
              f"sym={result['sym_recall']:.3f} file={result['file_recall']:.3f} "
              f"tok={toks:>5d} {status}")

print("\nDone.")
