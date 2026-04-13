"""Trace exactly why File and Path aren't in FOCUS despite keyword match."""
import re
from collections import defaultdict
from pathlib import Path as PyPath

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import _extract_question_keywords

repo_path = PyPath("experiments/external-repos/click")
question = "When an option or argument value is not provided directly on the command line, how does Click decide what value to use, and what extra work do file and path types perform during conversion?"

graph = extract_graph(repo_path)
keywords = _extract_question_keywords(question)

# Reproduce _select_focus_nodes logic step by step
stemmed_kw = set()
for kw in keywords:
    stemmed_kw.add(kw)
    if kw.endswith("s") and len(kw) > 4:
        stemmed_kw.add(kw[:-1])
    if kw.endswith("ing") and len(kw) > 5:
        stemmed_kw.add(kw[:-3])
    if kw.endswith("ed") and len(kw) > 4:
        stemmed_kw.add(kw[:-2])

node_by_id = {n.node_id: n for n in graph.nodes}

# Stage 1: keyword anchoring (seeds)
class_seeds = []
func_seeds = []
for node in graph.nodes:
    if node.node_type == "module":
        continue
    fp = node.source_anchor.file_path.lower().replace("\\", "/")
    if "/test" in fp or fp.startswith("test") or "_test." in fp or "conftest" in fp:
        continue
    sc = node.semantic_contract or {}
    sym_name = sc.get("symbol_name", node.node_id).lower()
    file_path = node.source_anchor.file_path.lower()
    name_parts = set(re.findall(r"[a-z_]\w{2,}", sym_name))
    path_parts = set(re.findall(r"[a-z_]\w{2,}", file_path))
    overlap = stemmed_kw & (name_parts | path_parts)
    if overlap:
        if node.node_type == "class":
            class_seeds.append(node.node_id)
        else:
            func_seeds.append(node.node_id)

seeds = class_seeds + func_seeds
print(f"Seeds: {len(seeds)} ({len(class_seeds)} class, {len(func_seeds)} func)")

# Check if File and Path are seeds
for nid in seeds:
    n = node_by_id[nid]
    sn = n.semantic_contract.get("symbol_name", "")
    if sn in ("File", "Path", "Choice", "LazyFile"):
        print(f"  SEED: {sn} ({n.source_anchor.file_path})")

# Stage 2: graph walk
neighbors = defaultdict(set)
for edge in graph.edges:
    if edge.edge_type == "calls":
        neighbors[edge.from_node].add(edge.to_node)
        neighbors[edge.to_node].add(edge.from_node)

collected = {}
for seed in seeds:
    if seed not in collected:
        collected[seed] = 0
    for neighbor in neighbors.get(seed, set()):
        if neighbor not in collected or collected[neighbor] > 1:
            collected[neighbor] = 1
        for n2 in neighbors.get(neighbor, set()):
            if n2 not in collected or collected[n2] > 2:
                collected[n2] = 2

print(f"\nGraph walk collected: {len(collected)} nodes")

# Check if File/Path are in collected
for nid, dist in collected.items():
    n = node_by_id.get(nid)
    if n:
        sn = n.semantic_contract.get("symbol_name", "")
        if sn in ("File", "Path", "Choice", "LazyFile", "type_cast_value", "convert"):
            print(f"  COLLECTED (dist={dist}): {sn} ({n.source_anchor.file_path})")

# Stage 3: direct matches
stemmed_keywords = set()
for kw in keywords:
    stemmed_keywords.add(kw)
    if kw.endswith("s") and len(kw) > 4:
        stemmed_keywords.add(kw[:-1])
    if kw.endswith("ing") and len(kw) > 5:
        stemmed_keywords.add(kw[:-3])
    if kw.endswith("ed") and len(kw) > 4:
        stemmed_keywords.add(kw[:-2])

direct_matches = []
for node in graph.nodes:
    if node.node_type == "module":
        continue
    if node.node_id in collected:
        continue  # already in graph walk
    fp = node.source_anchor.file_path.lower().replace("\\", "/")
    if "/test" in fp or fp.startswith("test") or "_test." in fp or "conftest" in fp:
        continue
    sc = node.semantic_contract or {}
    sym_name = sc.get("symbol_name", "").lower()
    for kw in stemmed_keywords:
        if len(kw) >= 4 and kw in sym_name:
            direct_matches.append(node.node_id)
            break

print(f"\nDirect matches (not in graph walk): {len(direct_matches)}")
for nid in direct_matches:
    n = node_by_id[nid]
    sn = n.semantic_contract.get("symbol_name", "")
    if sn in ("File", "Path", "Choice", "LazyFile", "type_cast_value", "convert",
              "normalize_choice", "consume_value"):
        print(f"  DIRECT: {sn} ({n.source_anchor.file_path})")

# Final merge
all_focus = []
seen = set()
for nid in direct_matches:
    if nid not in seen:
        all_focus.append(nid)
        seen.add(nid)

type_priority = {"class": 0, "function": 1, "async_function": 1, "method": 1}
focus_ids = sorted(
    (nid for nid in collected if nid in node_by_id and node_by_id[nid].node_type != "module"),
    key=lambda nid: (collected[nid], type_priority.get(node_by_id[nid].node_type, 2)),
)
for nid in focus_ids:
    if nid not in seen:
        all_focus.append(nid)
        seen.add(nid)

# Cap at 80
print(f"\nTotal before cap: {len(all_focus)}")
all_focus = all_focus[:80]

# Check what's in and out
for nid in all_focus:
    n = node_by_id[nid]
    sn = n.semantic_contract.get("symbol_name", "")
    if sn in ("File", "Path", "Choice", "LazyFile", "type_cast_value", "convert",
              "normalize_choice", "consume_value"):
        idx = all_focus.index(nid)
        print(f"  IN FOCUS (pos={idx}): {sn}")

# Check File specifically
file_nodes = [n for n in graph.nodes if n.semantic_contract.get("symbol_name") == "File"
              and "/test" not in n.source_anchor.file_path.lower()]
for fn in file_nodes:
    in_seeds = fn.node_id in seeds
    in_collected = fn.node_id in collected
    in_direct = fn.node_id in [d for d in direct_matches]
    print(f"\nFile node: {fn.node_id}")
    print(f"  In seeds: {in_seeds}")
    print(f"  In collected (graph walk): {in_collected} (dist={collected.get(fn.node_id, 'N/A')})")
    print(f"  In direct matches: {in_direct}")

    # Why not a seed?
    sym_name = fn.semantic_contract.get("symbol_name", "").lower()
    name_parts = set(re.findall(r"[a-z_]\w{2,}", sym_name))
    print(f"  name_parts from regex: {name_parts}")
    print(f"  stemmed_kw: 'file' in stemmed_kw = {'file' in stemmed_kw}")
    print(f"  overlap: {stemmed_kw & name_parts}")
