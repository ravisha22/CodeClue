"""MRLF: Multi-Resolution Lattice Format renderer.

Generates a two-file clue artifact:
  File 1 (.codeclue)        — plain-text primary clue, ≤4150 tokens
  File 2 (.codeclue-detail)  — JSONL detail store, one record per symbol

Design doc: docs/New-Design-Basis.md

Resolution levels in File 1:
  L0 TREE   — directory structure       (~150 tokens, 100% coverage)
  L1 INDEX  — every module + top exports (~400 tokens, 100% modules)
  L2 SYM    — symbols by PageRank       (~1500 tokens, top N)
  L3 FOCUS  — task-conditioned detail    (~2000 tokens, top K)
  GAPS      — missing info + drill hints (~100 tokens, 3-5 bullets)
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import tiktoken

from .models import CanonicalClueGraph, Node, Edge

# ---------------------------------------------------------------------------
# Budget caps (in actual tiktoken tokens, cl100k_base encoding)
# ---------------------------------------------------------------------------
BUDGET_L0 = 150
BUDGET_L1 = 400
BUDGET_L2 = 1500
BUDGET_L3 = 2000
BUDGET_GAPS = 100
BUDGET_TOTAL = 4150

_ENC = tiktoken.get_encoding("cl100k_base")


def _token_count(text: str) -> int:
    """Count actual tokens using tiktoken cl100k_base."""
    return len(_ENC.encode(text))


def _word_count(text: str) -> int:
    """Count whitespace-delimited words (kept for backward compat / display)."""
    return len(text.split())


# ---------------------------------------------------------------------------
# PageRank (pure-Python, no networkx dependency)
# ---------------------------------------------------------------------------

def _pagerank(
    nodes: list[str],
    edges: list[tuple[str, str]],
    damping: float = 0.85,
    iterations: int = 20,
) -> dict[str, float]:
    """Simple iterative PageRank on a directed graph.

    Returns a dict mapping node_id → PageRank score (sum ≈ 1.0).
    For large graphs (>10K nodes), uses fewer iterations for performance.
    """
    n = len(nodes)
    if n == 0:
        return {}

    # Adaptive iterations: fewer for large graphs (convergence is fast)
    if n > 10000:
        iterations = min(iterations, 10)
    elif n > 5000:
        iterations = min(iterations, 15)

    node_set = set(nodes)
    # Build adjacency: outgoing[from] = [to, ...]
    outgoing: dict[str, list[str]] = {nid: [] for nid in node_set}
    for src, dst in edges:
        if src in node_set and dst in node_set:
            outgoing[src].append(dst)

    rank = {nid: 1.0 / n for nid in node_set}
    teleport = (1.0 - damping) / n

    for _ in range(iterations):
        new_rank: dict[str, float] = {}
        # Collect dangling mass (nodes with no outgoing edges)
        dangling_mass = sum(rank[nid] for nid in node_set if not outgoing[nid])
        dangling_share = damping * dangling_mass / n

        for nid in node_set:
            new_rank[nid] = teleport + dangling_share

        for src in node_set:
            out_list = outgoing[src]
            if out_list:
                share = damping * rank[src] / len(out_list)
                for dst in out_list:
                    new_rank[dst] += share

        rank = new_rank

    return rank


# ---------------------------------------------------------------------------
# L0: TREE — directory structure
# ---------------------------------------------------------------------------

def _render_l0(graph: CanonicalClueGraph, budget: int = BUDGET_L0) -> str:
    """Render L0 TREE section: directory tree from file paths in the graph."""
    paths = sorted({n.source_anchor.file_path for n in graph.nodes})
    if not paths:
        return "-- TREE\n(empty)\n"

    # Build directory tree
    dirs: set[str] = set()
    file_by_dir: dict[str, list[str]] = defaultdict(list)
    for p in paths:
        parts = p.split("/")
        if len(parts) > 1:
            dir_path = "/".join(parts[:-1])
            dirs.add(dir_path)
            file_by_dir[dir_path].append(parts[-1])
        else:
            file_by_dir["."].append(parts[0])

    # Render as compact tree
    lines = ["-- TREE"]
    # Get top-level entries
    top_dirs: set[str] = set()
    top_files: list[str] = file_by_dir.get(".", [])
    for d in sorted(dirs):
        top = d.split("/")[0]
        top_dirs.add(top)

    for td in sorted(top_dirs):
        # Count files under this top dir
        sub_files = sum(
            len(v) for k, v in file_by_dir.items()
            if k == td or k.startswith(td + "/")
        )
        sub_dirs = sorted(
            d for d in dirs
            if d.startswith(td + "/") and d.count("/") == td.count("/") + 1
        )
        if sub_dirs:
            sub_names = "  ".join(d.split("/")[-1] + "/" for d in sub_dirs[:10])
            if len(sub_dirs) > 10:
                sub_names += f"  ...+{len(sub_dirs) - 10}"
            lines.append(f"{td}/  ({sub_files} files)")
            lines.append(f"  {sub_names}")
        else:
            lines.append(f"{td}/  ({sub_files} files)")

    if top_files:
        lines.append("  ".join(sorted(top_files)[:15]))

    # Trim to budget
    result = "\n".join(lines) + "\n"
    toks = _token_count(result)
    if toks > budget:
        # Collapse to just top-level dirs with counts
        lines = ["-- TREE"]
        for td in sorted(top_dirs):
            sub_files = sum(
                len(v) for k, v in file_by_dir.items()
                if k == td or k.startswith(td + "/")
            )
            lines.append(f"{td}/  ({sub_files} files)")
        result = "\n".join(lines) + "\n"

    return result


# ---------------------------------------------------------------------------
# L1: INDEX — every module with line count and top exports
# ---------------------------------------------------------------------------

def _render_l1(
    graph: CanonicalClueGraph,
    repo_root: str | Path = ".",
    budget: int = BUDGET_L1,
) -> str:
    """Render L1 INDEX: per-module line count + top exported symbol names."""
    modules: list[dict[str, Any]] = []
    # Build node lookup for O(1) access
    node_by_id = {n.node_id: n for n in graph.nodes}
    # Build containment: module -> symbols
    module_symbols: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        if edge.edge_type == "contains":
            from_id = edge.from_node
            to_node = node_by_id.get(edge.to_node)
            if to_node and to_node.node_type != "module":
                sym_name = to_node.semantic_contract.get("symbol_name", "")
                short = sym_name.rsplit(".", 1)[-1] if sym_name else ""
                if short and not short.startswith("_"):
                    module_symbols[from_id].append(short)

    # Compute import fan-in for ranking
    # Fan-in = how many call edges target symbols in this module
    node_to_module: dict[str, str] = {}
    for edge in graph.edges:
        if edge.edge_type == "contains":
            node_to_module[edge.to_node] = edge.from_node

    module_fanin: dict[str, int] = defaultdict(int)
    for edge in graph.edges:
        if edge.edge_type == "calls":
            target_module = node_to_module.get(edge.to_node, "")
            source_module = node_to_module.get(edge.from_node, "")
            if target_module and source_module and target_module != source_module:
                module_fanin[target_module] += 1

    for node in graph.nodes:
        if node.node_type != "module":
            continue
        fp = node.source_anchor.file_path
        # Use byte-span estimate for line count (fast, no file read)
        # Actual line count will be computed lazily below for rendered modules only
        byte_size = node.source_anchor.byte_end - node.source_anchor.byte_start
        line_est = max(1, byte_size // 40)

        exports = module_symbols.get(node.node_id, [])[:5]
        fanin = module_fanin.get(node.node_id, 0)
        modules.append({
            "file": fp,
            "lines": line_est,
            "exports": exports,
            "fanin": fanin,
        })

    # Sort by fan-in descending (most depended-on first)
    modules.sort(key=lambda m: m["fanin"], reverse=True)

    # Render — read actual line counts ONLY for modules within budget (lazy I/O)
    lines = ["-- INDEX"]
    used_toks = _token_count("-- INDEX\n")
    budget_exhausted = False
    for mod in modules:
        if budget_exhausted:
            break

        # Lazy file read: only read file for modules that might make it into the output
        fp = mod["file"]
        real_path = Path(repo_root) / fp
        if real_path.is_file():
            try:
                mod["lines"] = sum(1 for _ in real_path.open(encoding="utf-8", errors="replace"))
            except OSError:
                pass

        export_str = ", ".join(mod["exports"])
        entry = f"{mod['file']:<45s} {mod['lines']:>5d}L  {export_str}"
        entry_toks = _token_count(entry + "\n")
        if used_toks + entry_toks > budget:
            remaining = len(modules) - len(lines) + 1
            if remaining > 0:
                lines.append(f"  ...and {remaining} more modules")
            budget_exhausted = True
            break
        lines.append(entry)
        used_toks += entry_toks

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# L2: SYM — symbols ranked by PageRank
# ---------------------------------------------------------------------------

def _render_l2(
    graph: CanonicalClueGraph,
    repo_root: str | Path = ".",
    budget: int = BUDGET_L2,
) -> str:
    """Render L2 SYM: all non-module symbols ranked by PageRank."""
    # Collect non-module, non-test nodes
    def _is_test_path(fp: str) -> bool:
        fp_lower = fp.lower().replace("\\", "/")
        return ("/test" in fp_lower or fp_lower.startswith("test")
                or "_test." in fp_lower or "conftest" in fp_lower)

    symbol_nodes = [
        n for n in graph.nodes
        if n.node_type != "module" and not _is_test_path(n.source_anchor.file_path)
    ]
    if not symbol_nodes:
        # Fallback: include test files if no production code
        symbol_nodes = [n for n in graph.nodes if n.node_type != "module"]
    if not symbol_nodes:
        return "-- SYM\n(no symbols extracted)\n"

    # Build call graph for PageRank (production code only)
    prod_ids = {n.node_id for n in symbol_nodes}
    call_edges = [
        (e.from_node, e.to_node)
        for e in graph.edges
        if e.edge_type == "calls" and e.from_node in prod_ids and e.to_node in prod_ids
    ]
    all_sym_ids = [n.node_id for n in symbol_nodes]
    ranks = _pagerank(all_sym_ids, call_edges)

    # Fallback: if no call edges, use degree centrality
    if not call_edges:
        # degree = count of contains edges (as a proxy)
        for n in symbol_nodes:
            ranks[n.node_id] = 1.0 / len(symbol_nodes)

    # Sort by rank descending
    ranked = sorted(symbol_nodes, key=lambda n: ranks.get(n.node_id, 0), reverse=True)

    # Node type shorthand
    type_short = {"class": "C", "function": "M", "async_function": "M", "method": "M"}

    lines = ["-- SYM"]
    used_toks = _token_count("-- SYM\n")
    for node in ranked:
        sc = node.semantic_contract or {}
        sym_name = sc.get("symbol_name", node.node_id)
        short_name = sym_name.rsplit(".", 1)[-1] if "." in sym_name else sym_name
        ntype = type_short.get(node.node_type, node.node_type[0].upper())
        fp = node.source_anchor.file_path
        # Line number estimate
        byte_start = node.source_anchor.byte_start
        real_path = Path(repo_root) / fp
        line_no = "?"
        if real_path.is_file():
            try:
                source = real_path.read_text(encoding="utf-8", errors="replace")
                line_no = str(source[:byte_start].count("\n") + 1)
            except OSError:
                pass

        purpose = sc.get("purpose", "")
        # Compress purpose to first clause
        if purpose and len(purpose) > 50:
            purpose = purpose[:47] + "..."

        entry = f"{sym_name:<35s} {ntype} {fp}:{line_no:<6s} {purpose}"
        entry_toks = _token_count(entry + "\n")
        if used_toks + entry_toks > budget:
            remaining = len(ranked) - (len(lines) - 1)
            if remaining > 0:
                lines.append(f"  ...and {remaining} more symbols")
            break
        lines.append(entry)
        used_toks += entry_toks

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# L3: FOCUS — task-conditioned behavioural detail
# ---------------------------------------------------------------------------

def _extract_question_keywords(question: str) -> set[str]:
    """Extract meaningful keywords from a task question."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "of", "in", "to", "for",
        "with", "on", "at", "from", "by", "about", "as", "into", "through",
        "during", "before", "after", "above", "below", "between", "out",
        "up", "down", "and", "but", "or", "nor", "not", "so", "yet",
        "what", "which", "who", "whom", "this", "that", "these", "those",
        "how", "when", "where", "why", "all", "each", "every", "both",
        "few", "more", "most", "other", "some", "such", "no", "only",
        "same", "than", "too", "very", "just", "if", "it", "its",
    }
    words = set(re.findall(r"[a-zA-Z_]\w{2,}", question.lower()))
    return words - stop_words


def _tokenize_symbol(name: str) -> set[str]:
    """Split a symbol name into keyword-matchable tokens.

    Splits on underscores and camelCase boundaries, lowercases, keeps tokens >= 3 chars.
    'type_cast_value' -> {'type', 'cast', 'value'}
    'LazyFile' -> {'lazy', 'file'}
    'normalize_choice' -> {'normalize', 'choice'}
    """
    # Split on underscores first
    parts = name.replace("_", " ").replace(".", " ")
    # Split camelCase: insert space before uppercase letters
    parts = re.sub(r"([a-z])([A-Z])", r"\1 \2", parts)
    tokens = set(re.findall(r"[a-z]{3,}", parts.lower()))
    return tokens


def _is_test_file(file_path: str) -> bool:
    """Check if a file path belongs to a test directory."""
    fp = file_path.lower().replace("\\", "/")
    return "/test" in fp or fp.startswith("test") or "_test." in fp or "conftest" in fp


def _is_src_file(file_path: str) -> bool:
    """Check if a file path belongs to src/ (not examples/, docs/, etc.)."""
    fp = file_path.lower().replace("\\", "/")
    return fp.startswith("src/") or (
        not fp.startswith("examples/")
        and not fp.startswith("docs/")
        and not fp.startswith("test")
    )


def _select_focus_nodes(
    graph: CanonicalClueGraph,
    question: str,
    max_nodes: int = 80,
) -> list[Node]:
    """Two-stage focus selection: keyword anchoring + graph walk.

    Fixes applied (Step 3, Apr 14):
    - Tokenize symbol names on _ and camelCase for keyword matching
    - Seeds always keep dist=0 (never overwritten by graph walk)
    - Prioritize src/ over examples/ in cap sorting
    """
    keywords = _extract_question_keywords(question)
    if not keywords:
        # Fallback: return top PageRank nodes
        symbol_nodes = [n for n in graph.nodes if n.node_type != "module"]
        call_edges = [(e.from_node, e.to_node) for e in graph.edges if e.edge_type == "calls"]
        ranks = _pagerank([n.node_id for n in symbol_nodes], call_edges)
        symbol_nodes.sort(key=lambda n: ranks.get(n.node_id, 0), reverse=True)
        return symbol_nodes[:max_nodes]

    node_by_id = {n.node_id: n for n in graph.nodes}

    # Stem keywords for fuzzy matching
    stemmed_kw = set()
    for kw in keywords:
        stemmed_kw.add(kw)
        if kw.endswith("s") and len(kw) > 4:
            stemmed_kw.add(kw[:-1])
        if kw.endswith("ing") and len(kw) > 5:
            stemmed_kw.add(kw[:-3])
        if kw.endswith("ed") and len(kw) > 4:
            stemmed_kw.add(kw[:-2])

    # Stage 1: keyword anchoring — find seed nodes
    # Use _tokenize_symbol to split on _ and camelCase for matching
    class_seeds: list[str] = []
    func_seeds: list[str] = []
    for node in graph.nodes:
        if node.node_type == "module":
            continue
        if _is_test_file(node.source_anchor.file_path):
            continue
        sc = node.semantic_contract or {}
        sym_name = sc.get("symbol_name", node.node_id)
        file_path = node.source_anchor.file_path.lower()
        # Tokenize symbol name on _ and camelCase boundaries
        name_tokens = _tokenize_symbol(sym_name)
        path_tokens = _tokenize_symbol(file_path)
        overlap = stemmed_kw & (name_tokens | path_tokens)
        if overlap:
            if node.node_type == "class":
                class_seeds.append(node.node_id)
            else:
                func_seeds.append(node.node_id)

    # Prioritise: class seeds first (architectural), then function seeds
    seeds = class_seeds + func_seeds
    seed_set = set(seeds)

    if not seeds:
        # No keyword matches — fall back to top PageRank
        symbol_nodes = [n for n in graph.nodes if n.node_type != "module"]
        call_edges = [(e.from_node, e.to_node) for e in graph.edges if e.edge_type == "calls"]
        ranks = _pagerank([n.node_id for n in symbol_nodes], call_edges)
        symbol_nodes.sort(key=lambda n: ranks.get(n.node_id, 0), reverse=True)
        return symbol_nodes[:max_nodes]

    # Stage 2: graph walk — expand 1-2 hops from seeds
    # Build adjacency (both directions for calls edges)
    neighbors: dict[str, set[str]] = defaultdict(set)
    for edge in graph.edges:
        if edge.edge_type == "calls":
            neighbors[edge.from_node].add(edge.to_node)
            neighbors[edge.to_node].add(edge.from_node)

    collected: dict[str, int] = {}  # node_id -> distance from seed
    # Pre-register ALL seeds as dist=0 so graph walk can't overwrite them
    for seed in seeds:
        collected[seed] = 0
    # Now do the walk — only assign dist to NON-seed nodes
    for seed in seeds:
        # Hop 1
        for neighbor in neighbors.get(seed, set()):
            if neighbor in seed_set:
                continue  # never overwrite a seed
            if neighbor not in collected or collected[neighbor] > 1:
                collected[neighbor] = 1
            # Hop 2
            for n2 in neighbors.get(neighbor, set()):
                if n2 in seed_set:
                    continue  # never overwrite a seed
                if n2 not in collected or collected[n2] > 2:
                    collected[n2] = 2

    # Sort by distance (closer to seed = higher priority), filter modules
    # Within same distance: (1) more keyword matches first, (2) classes before functions
    type_priority = {"class": 0, "function": 1, "async_function": 1, "method": 1}

    def _kw_overlap(nid: str) -> int:
        """Count stemmed keywords matching this symbol's tokenized name."""
        nd = node_by_id.get(nid)
        if not nd:
            return 0
        sc = nd.semantic_contract or {}
        sym_name = sc.get("symbol_name", "")
        tokens = _tokenize_symbol(sym_name)
        return len(stemmed_kw & tokens)

    def _src_priority(nid: str) -> int:
        """0 for src/ files, 1 for others (lower = better)."""
        nd = node_by_id.get(nid)
        if not nd:
            return 1
        return 0 if _is_src_file(nd.source_anchor.file_path) else 1

    focus_ids = sorted(
        (nid for nid in collected if nid in node_by_id and node_by_id[nid].node_type != "module"),
        key=lambda nid: (
            collected[nid],                                          # dist: 0 first
            -_kw_overlap(nid),                                       # more kw matches first
            _src_priority(nid),                                      # src/ before examples/
            type_priority.get(node_by_id[nid].node_type, 2),         # classes before functions
        ),
    )

    # Stage 3: Direct name-match inclusion
    # If a keyword matches part of a symbol's tokenized name, include it
    # even if graph walk didn't reach it (handles disconnected classes)
    direct_matches: list[str] = []
    for node in graph.nodes:
        if node.node_type == "module":
            continue
        if node.node_id in collected:
            continue  # already included via graph walk
        if _is_test_file(node.source_anchor.file_path):
            continue
        sc = node.semantic_contract or {}
        sym_name = sc.get("symbol_name", "")
        tokens = _tokenize_symbol(sym_name)
        # Match if any stemmed keyword (>=4 chars) matches a token
        if any(kw in tokens for kw in stemmed_kw if len(kw) >= 4):
            direct_matches.append(node.node_id)

    # Merge: direct matches FIRST (they're the most relevant — user asked about
    # these exact concepts), then graph-walk results by distance
    all_focus_ids: list[str] = []
    seen: set[str] = set()
    # Direct matches first
    for nid in direct_matches:
        if nid not in seen:
            all_focus_ids.append(nid)
            seen.add(nid)
    # Then graph-walk results
    for nid in focus_ids:
        if nid not in seen:
            all_focus_ids.append(nid)
            seen.add(nid)

    return [node_by_id[nid] for nid in all_focus_ids[:max_nodes]]


def _render_l3(
    graph: CanonicalClueGraph,
    question: str,
    repo_root: str | Path = ".",
    budget: int = BUDGET_L3,
) -> str:
    """Render L3 FOCUS: task-conditioned behavioural detail."""
    focus_nodes = _select_focus_nodes(graph, question)
    if not focus_nodes:
        return "-- FOCUS\n(no focus nodes selected)\n"

    # Build call edges for context
    calls_out: dict[str, list[str]] = defaultdict(list)
    calls_in: dict[str, list[str]] = defaultdict(list)
    node_by_id = {n.node_id: n for n in graph.nodes}
    for edge in graph.edges:
        if edge.edge_type == "calls":
            from_name = (node_by_id.get(edge.from_node, None) or Node.__new__(Node))
            to_name = (node_by_id.get(edge.to_node, None) or Node.__new__(Node))
            from_sym = ""
            to_sym = ""
            if hasattr(from_name, "semantic_contract") and from_name.semantic_contract:
                from_sym = from_name.semantic_contract.get("symbol_name", "")
            if hasattr(to_name, "semantic_contract") and to_name.semantic_contract:
                to_sym = to_name.semantic_contract.get("symbol_name", "")
            if from_sym:
                calls_out[edge.from_node].append(to_sym or edge.to_node)
            if to_sym:
                calls_in[edge.to_node].append(from_sym or edge.from_node)

    lines = ["-- FOCUS"]
    used_toks = _token_count("-- FOCUS\n")
    for node in focus_nodes:
        sc = node.semantic_contract or {}
        sym_name = sc.get("symbol_name", node.node_id)
        fp = node.source_anchor.file_path
        purpose = sc.get("purpose", "")

        # Line numbers
        byte_start = node.source_anchor.byte_start
        byte_end = node.source_anchor.byte_end
        real_path = Path(repo_root) / fp
        start_line, end_line = "?", "?"
        if real_path.is_file():
            try:
                source = real_path.read_text(encoding="utf-8", errors="replace")
                start_line = str(source[:byte_start].count("\n") + 1)
                end_line = str(source[:byte_end].count("\n") + 1)
            except OSError:
                pass

        # Build compact focus entry
        entry_lines = [f"{sym_name} ({fp}:{start_line}-{end_line})"]
        if purpose and purpose != f"{node.node_type} {sym_name}":
            entry_lines.append(f"  {purpose}")

        # Signature for functions
        sig = sc.get("signature", "")
        if sig and sig != "()" and node.node_type != "class":
            entry_lines.append(f"  sig: {sym_name}{sig}")

        # For classes: show parent classes, key attrs, and methods
        if node.node_type == "class":
            bases = sc.get("bases", [])
            if bases:
                entry_lines.append(f"  extends: {', '.join(bases[:3])}")

            class_attrs = sc.get("class_attrs", {})
            if class_attrs:
                attr_strs = [f"{k}={v}" for k, v in list(class_attrs.items())[:4]]
                entry_lines.append(f"  attrs: {', '.join(attr_strs)}")

            child_methods = []
            for edge in graph.edges:
                if edge.edge_type == "contains" and edge.from_node == node.node_id:
                    child = node_by_id.get(edge.to_node)
                    if child and child.node_type in ("function", "async_function"):
                        child_sc = child.semantic_contract or {}
                        child_name = child_sc.get("symbol_name", "").rsplit(".", 1)[-1]
                        if child_name and not child_name.startswith("_"):
                            child_methods.append(child_name)
            if child_methods:
                entry_lines.append(f"  methods: {', '.join(child_methods[:6])}")

            # Show file-level imports (from containing module) for security context
            for edge in graph.edges:
                if edge.edge_type == "contains" and edge.to_node == node.node_id:
                    module_node = node_by_id.get(edge.from_node)
                    if module_node and module_node.node_type == "module":
                        mod_imports = module_node.semantic_contract.get("imports", [])
                        if mod_imports:
                            entry_lines.append(f"  imports: {', '.join(mod_imports[:5])}")
                    break

        # Calls out (deduplicate, preserve order)
        out = calls_out.get(node.node_id, [])
        if out:
            seen = set()
            deduped = []
            for s in out:
                short = s.rsplit(".", 1)[-1]
                if short not in seen:
                    seen.add(short)
                    deduped.append(short)
            entry_lines.append(f"  calls: {', '.join(deduped[:8])}")

        # Called by (deduplicate, preserve order)
        inc = calls_in.get(node.node_id, [])
        if inc:
            seen = set()
            deduped = []
            for s in inc:
                short = s.rsplit(".", 1)[-1]
                if short not in seen:
                    seen.add(short)
                    deduped.append(short)
            entry_lines.append(f"  called_by: {', '.join(deduped[:8])}")

        # Raises/panics (invariant knowledge)
        raises = sc.get("raises", [])
        if raises:
            entry_lines.append(f"  raises: {', '.join(raises[:4])}")

        # Uses: external class instantiation (mechanistic knowledge)
        uses = sc.get("uses", [])
        # For classes: aggregate uses from child methods
        if node.node_type == "class" and not uses:
            child_uses: list[str] = []
            for edge in graph.edges:
                if edge.from_node == node.node_id and edge.edge_type in ("contains", "calls"):
                    child = node_by_id.get(edge.to_node)
                    if child and child.node_type in ("function", "async_function"):
                        child_sc = child.semantic_contract or {}
                        child_uses.extend(child_sc.get("uses", []))
            if child_uses:
                uses = list(dict.fromkeys(child_uses))[:4]
        if uses:
            entry_lines.append(f"  uses: {', '.join(uses[:4])}")

        entry = "\n".join(entry_lines)
        entry_toks = _token_count(entry + "\n")
        if used_toks + entry_toks > budget:
            break
        lines.append(entry)
        lines.append("")  # blank line separator
        used_toks += entry_toks

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# GAPS — missing information + drill hints
# ---------------------------------------------------------------------------

def _render_gaps(
    graph: CanonicalClueGraph,
    question: str,
    focus_nodes: list[Node],
    l2_symbols: list[Node],
    budget: int = BUDGET_GAPS,
) -> str:
    """Render GAPS section: what's missing, where to drill."""
    keywords = _extract_question_keywords(question)
    gaps: list[str] = []

    # Signal 1: uncovered question keywords
    covered_names: set[str] = set()
    for node in focus_nodes + l2_symbols:
        sc = node.semantic_contract or {}
        sym_name = sc.get("symbol_name", node.node_id).lower()
        covered_names.update(re.findall(r"[a-z_]\w{2,}", sym_name))
        covered_names.update(re.findall(r"[a-z_]\w{2,}", node.source_anchor.file_path.lower()))

    uncovered = keywords - covered_names
    if uncovered:
        uncovered_str = ", ".join(sorted(uncovered)[:5])
        gaps.append(f"- Question mentions [{uncovered_str}] — not found in focus or symbol index")

    # Signal 2: low-confidence focus nodes
    for node in focus_nodes[:20]:
        if node.confidence < 0.70:
            sc = node.semantic_contract or {}
            sym_name = sc.get("symbol_name", node.node_id)
            fp = node.source_anchor.file_path
            gaps.append(f"- {sym_name} has low structural confidence ({node.confidence:.2f})")
            gaps.append(f"  > drill: {fp}")
            if len(gaps) >= 4:
                break

    # Signal 3: modules mentioned in question but not detailed
    module_files = {n.source_anchor.file_path.lower() for n in graph.nodes if n.node_type == "module"}
    focus_files = {n.source_anchor.file_path.lower() for n in focus_nodes}
    for kw in keywords:
        for mf in module_files:
            if kw in mf and mf not in focus_files:
                gaps.append(f"- Module {mf} matches question but has no focus detail")
                gaps.append(f"  > drill: {mf}")
                break
        if len(gaps) >= 5:
            break

    if not gaps:
        gaps.append("- No significant gaps detected for this question")

    lines = ["-- GAPS"] + gaps[:5]  # Max 5 bullets
    result = "\n".join(lines) + "\n"

    # Trim if over budget
    while _token_count(result) > budget and len(gaps) > 1:
        gaps.pop()
        result = "\n".join(["-- GAPS"] + gaps) + "\n"

    return result


# ---------------------------------------------------------------------------
# Public API: render File 1 (primary clue)
# ---------------------------------------------------------------------------

def render_mrlf(
    graph: CanonicalClueGraph,
    question: str,
    repo_root: str | Path = ".",
    commit_id: str = "",
) -> str:
    """Render File 1: complete MRLF primary clue.

    Args:
        graph: The canonical clue graph.
        question: The task question to condition L3 on.
        repo_root: Path to the repository root (for line number extraction).
        commit_id: Optional commit hash for the header.

    Returns:
        Plain-text MRLF clue string.
    """
    repo_name = graph.repository.get("name", "unknown")
    node_count = len(graph.nodes)
    module_count = sum(1 for n in graph.nodes if n.node_type == "module")
    sym_count = node_count - module_count

    # Header
    commit_short = commit_id[:8] if commit_id else "HEAD"
    header = f"=CC v2 {repo_name}@{commit_short} {module_count}mod {sym_count}sym\n"
    header += f"? {question}\n"

    # Render each level
    l0 = _render_l0(graph)
    l1 = _render_l1(graph, repo_root)
    l2_text = _render_l2(graph, repo_root)
    l3 = _render_l3(graph, question, repo_root)

    # For GAPS, we need focus and l2 node lists
    focus_nodes = _select_focus_nodes(graph, question)
    l2_symbols = [n for n in graph.nodes if n.node_type != "module"]

    gaps = _render_gaps(graph, question, focus_nodes, l2_symbols)

    # Assemble
    sections = [header, "", l0, l1, l2_text, l3, gaps]
    result = "\n".join(sections)

    # Final budget check — if over total, trim L3 FOCUS first
    total_toks = _token_count(result)
    if total_toks > BUDGET_TOTAL:
        # Re-render L3 with reduced budget
        overshoot = total_toks - BUDGET_TOTAL
        reduced_l3_budget = max(200, BUDGET_L3 - overshoot)
        l3 = _render_l3(graph, question, repo_root, budget=reduced_l3_budget)
        sections = [header, "", l0, l1, l2_text, l3, gaps]
        result = "\n".join(sections)

    return result


# ---------------------------------------------------------------------------
# Public API: generate File 2 (detail store)
# ---------------------------------------------------------------------------

def generate_detail_store(
    graph: CanonicalClueGraph,
    repo_root: str | Path = ".",
) -> list[dict[str, Any]]:
    """Generate File 2 detail records (one per non-module symbol).

    Returns a list of dicts, each serialisable as one JSONL line.
    """
    node_by_id = {n.node_id: n for n in graph.nodes}

    # Build call graph
    calls_out: dict[str, list[str]] = defaultdict(list)
    calls_in: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        if edge.edge_type == "calls":
            calls_out[edge.from_node].append(edge.to_node)
            calls_in[edge.to_node].append(edge.from_node)

    records: list[dict[str, Any]] = []
    for node in graph.nodes:
        if node.node_type == "module":
            continue

        sc = node.semantic_contract or {}
        sym_name = sc.get("symbol_name", node.node_id)
        fp = node.source_anchor.file_path

        # Read source snippet
        source_snippet = ""
        start_line, end_line = 0, 0
        real_path = Path(repo_root) / fp
        if real_path.is_file():
            try:
                full_source = real_path.read_text(encoding="utf-8", errors="replace")
                byte_start = node.source_anchor.byte_start
                byte_end = node.source_anchor.byte_end
                start_line = full_source[:byte_start].count("\n") + 1
                end_line = full_source[:byte_end].count("\n") + 1
                # Extract source lines
                source_lines = full_source.splitlines()
                snippet_lines = source_lines[start_line - 1:end_line]
                source_snippet = "\n".join(snippet_lines)
            except OSError:
                pass

        # Resolve call symbols to names
        def _resolve_names(node_ids: list[str]) -> list[str]:
            names = []
            for nid in node_ids:
                n = node_by_id.get(nid)
                if n:
                    nsc = n.semantic_contract or {}
                    names.append(nsc.get("symbol_name", nid))
                else:
                    names.append(nid)
            return names

        record = {
            "symbol": sym_name,
            "type": node.node_type,
            "file": fp,
            "lines": [start_line, end_line],
            "source": source_snippet,
            "calls": _resolve_names(calls_out.get(node.node_id, [])),
            "called_by": _resolve_names(calls_in.get(node.node_id, [])),
            "confidence": node.confidence,
            "purpose": sc.get("purpose", ""),
        }
        records.append(record)

    return records


def write_detail_store(records: list[dict[str, Any]], output_path: str | Path) -> None:
    """Write detail store records to a JSONL file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
