"""Definitive root cause analysis: trace FOCUS selection for blind-click-2."""
import json
import re
from collections import defaultdict
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _extract_question_keywords, _select_focus_nodes

repo_path = Path("experiments/external-repos/click")
question = "When an option or argument value is not provided directly on the command line, how does Click decide what value to use, and what extra work do file and path types perform during conversion?"

GOLD = ["consume_value", "type_cast_value", "Choice", "convert", "File", "Path", "LazyFile", "normalize_choice"]

# Extract graph
graph = extract_graph(repo_path)
print(f"Graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

# Check keywords
keywords = _extract_question_keywords(question)
print(f"\nKeywords from question: {sorted(keywords)}")

# Stem them (same logic as _select_focus_nodes)
stemmed_kw = set()
for kw in keywords:
    stemmed_kw.add(kw)
    if kw.endswith("s") and len(kw) > 4:
        stemmed_kw.add(kw[:-1])
    if kw.endswith("ing") and len(kw) > 5:
        stemmed_kw.add(kw[:-3])
    if kw.endswith("ed") and len(kw) > 4:
        stemmed_kw.add(kw[:-2])
print(f"Stemmed keywords: {sorted(stemmed_kw)}")

# Select focus nodes
focus_nodes = _select_focus_nodes(graph, question)
print(f"\nFOCUS selected: {len(focus_nodes)} nodes")

# Check each gold symbol
print("\n=== GOLD SYMBOL STATUS ===")
for gold_name in GOLD:
    # Find in graph
    graph_matches = [n for n in graph.nodes
                    if gold_name == n.semantic_contract.get("symbol_name", "")
                    and n.node_type != "module"
                    and "/test" not in n.source_anchor.file_path.lower()]
    # Find in focus
    focus_matches = [n for n in focus_nodes
                    if gold_name == n.semantic_contract.get("symbol_name", "")]

    in_graph = len(graph_matches) > 0
    in_focus = len(focus_matches) > 0

    if in_focus:
        status = "IN FOCUS"
    elif in_graph:
        status = "IN GRAPH BUT NOT FOCUS"
    else:
        status = "NOT IN GRAPH"

    print(f"  [{status:25s}] {gold_name}", end="")
    if graph_matches and not focus_matches:
        # Why wasn't it selected? Check keyword overlap
        for n in graph_matches[:1]:
            sn = n.semantic_contract.get("symbol_name", "").lower()
            name_parts = set(re.findall(r"[a-z_]\w{2,}", sn))
            overlap = stemmed_kw & name_parts
            print(f"  (name_parts={name_parts}, kw_overlap={overlap}, "
                  f"file={n.source_anchor.file_path})", end="")
    elif focus_matches:
        print(f"  (file={focus_matches[0].source_anchor.file_path})", end="")
    print()

# Show what IS in focus (first 20 entries)
print(f"\n=== FOCUS ENTRIES (first 20 of {len(focus_nodes)}) ===")
for n in focus_nodes[:20]:
    sn = n.semantic_contract.get("symbol_name", "")
    fp = n.source_anchor.file_path
    print(f"  {sn:40s} {n.node_type:10s} {fp}")

# Check how many symbols have "value" in name (to understand the noise)
value_syms = [n for n in graph.nodes
              if "value" in n.semantic_contract.get("symbol_name", "").lower()
              and n.node_type != "module"
              and "/test" not in n.source_anchor.file_path.lower()]
print(f"\n=== Symbols containing 'value' in name: {len(value_syms)} ===")
for n in value_syms[:10]:
    sn = n.semantic_contract.get("symbol_name", "")
    in_f = "YES" if n in focus_nodes else "NO"
    print(f"  [{in_f}] {sn:40s} {n.source_anchor.file_path}")
if len(value_syms) > 10:
    print(f"  ... and {len(value_syms) - 10} more")

# Check convert symbols
convert_syms = [n for n in graph.nodes
                if "convert" in n.semantic_contract.get("symbol_name", "").lower()
                and n.node_type != "module"
                and "/test" not in n.source_anchor.file_path.lower()]
print(f"\n=== Symbols containing 'convert' in name: {len(convert_syms)} ===")
for n in convert_syms:
    sn = n.semantic_contract.get("symbol_name", "")
    in_f = "YES" if n in focus_nodes else "NO"
    print(f"  [{in_f}] {sn:40s} {n.source_anchor.file_path}")
