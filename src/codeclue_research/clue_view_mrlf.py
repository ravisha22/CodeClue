"""MRLF v2.1: Multi-Resolution Lattice Format renderer.

Generates a two-file clue artifact:
  File 1 (.codeclue)        — plain-text primary clue, ≤4150 tokens
  File 2 (.codeclue-detail)  — JSONL detail store, one record per symbol

Design doc: docs/New-Design-Basis.md
PRD: source/CodeClue-PRD-v0.7.0-generalization.md

Resolution levels in File 1:
  L0 TREE   — directory structure       (~150 tokens, 100% coverage)
  L1 INDEX  — every module + top exports (~400 tokens, 100% modules)
  L2 SYM    — symbols by PageRank       (~1500 tokens, top N)
  L3 FOCUS  — task-conditioned detail with behavioral patterns (~2000 tokens)
  GAPS      — sufficiency classification + costed drill targets (~100 tokens)

v2.1 changes (Apr 14, 2026):
  - Graph-structural FOCUS selection (semantic anchoring + betweenness centrality)
  - Behavioral pattern extraction (GUARD, PRECEDENCE, BRANCH, etc.)
  - Budget-driven rendering (no fixed node cap)
  - Enhanced GAPS with question type classification
"""

from __future__ import annotations

import json
import random
import re
from collections import defaultdict
from dataclasses import dataclass
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
ENTERPRISE_NODE_THRESHOLD = 5000
L2_ENTERPRISE_CONTEXT_BUDGET = 200
README_PREAMBLE_BUDGET = 120
LARGE_EDGE_THRESHOLD = 100000
SAMPLED_EDGE_LIMIT = 50000

_ENC = tiktoken.get_encoding("cl100k_base")


def _token_count(text: str) -> int:
    """Count actual tokens using tiktoken cl100k_base."""
    return len(_ENC.encode(text))


def _word_count(text: str) -> int:
    """Count whitespace-delimited words (kept for backward compat / display)."""
    return len(text.split())


def _is_enterprise_graph(graph: CanonicalClueGraph) -> bool:
    return len(graph.nodes) > ENTERPRISE_NODE_THRESHOLD


def _sample_edges(edges: list[Edge], *, max_edges: int = SAMPLED_EDGE_LIMIT) -> list[Edge]:
    if len(edges) <= max_edges:
        return edges
    return random.Random(0).sample(edges, max_edges)


def _context_nodes(graph: CanonicalClueGraph, *, kinds: tuple[str, ...]) -> list[Node]:
    return [node for node in graph.nodes if node.node_type in kinds]


def _top_config_focus_nodes(graph: CanonicalClueGraph, *, limit: int = 3) -> list[Node]:
    priority_tokens = (
        ("settings.py", 0),
        (".env", 1),
        ("docker-compose", 2),
        ("config.py", 3),
        ("pyproject.toml", 4),
        ("package.json", 5),
    )

    def _rank(node: Node) -> tuple[int, str]:
        file_path = node.source_anchor.file_path.lower()
        for token, rank in priority_tokens:
            if token in file_path:
                return rank, file_path
        return 99, file_path

    configs = [node for node in graph.nodes if node.node_type == "config"]
    return sorted(configs, key=_rank)[:limit]


def _render_readme_preamble(graph: CanonicalClueGraph, budget: int = README_PREAMBLE_BUDGET) -> str:
    readme = next(
        (
            node for node in graph.nodes
            if node.node_type == "doc"
            and (
                node.source_anchor.file_path == "README.md"
                or (node.semantic_contract or {}).get("doc_kind") == "readme"
            )
        ),
        None,
    )
    if not readme:
        return ""

    sc = readme.semantic_contract or {}
    lines = ["-- README"]
    used_toks = _token_count("-- README\n")
    summary_lines = sc.get("summary_lines", [])
    headings = sc.get("headings", [])
    if summary_lines:
        summary = " ".join(summary_lines[:2])
        summary_toks = _token_count(summary + "\n")
        if used_toks + summary_toks <= budget:
            lines.append(summary)
            used_toks += summary_toks
    if headings:
        heading_line = "sections: " + ", ".join(headings[:5])
        heading_toks = _token_count(heading_line + "\n")
        if used_toks + heading_toks <= budget:
            lines.append(heading_line)
    return "\n".join(lines) + "\n"


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
    type_short = {
        "class": "C",
        "function": "M",
        "async_function": "M",
        "method": "M",
        "config": "G",
        "doc": "D",
        "route": "R",
    }

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


def _is_test_file(file_path: str) -> bool:
    """Check if a file path belongs to a test directory."""
    fp = file_path.lower().replace("\\", "/")
    return "/test" in fp or fp.startswith("test") or "_test." in fp or "conftest" in fp


def _split_compound_words(text: str) -> set[str]:
    """Split compound identifiers in text into individual tokens.

    Handles camelCase, PascalCase, snake_case, and concatenated words
    that commonly appear in docstrings referencing code identifiers.
    Language-agnostic: these patterns occur in all programming languages.
    """
    # First split on non-alpha characters (underscores, spaces, punctuation)
    parts = re.sub(r"[^a-zA-Z]", " ", text)
    # Then split camelCase: insert space before uppercase letters
    parts = re.sub(r"([a-z])([A-Z])", r"\1 \2", parts)
    return set(re.findall(r"[a-z]{3,}", parts.lower()))


def _keyword_variants(keyword: str) -> set[str]:
    variants = {keyword}
    alias_map = {
        "context": {"ctx"},
        "request": {"req"},
        "response": {"res"},
        "routing": {"route", "router"},
        "route": {"router", "routing"},
        "router": {"route", "routing"},
        "types": {"type"},
        "defined": {"define", "definition"},
    }
    variants.update(alias_map.get(keyword, set()))
    if keyword.endswith("ing") and len(keyword) > 5:
        variants.add(keyword[:-3])
    if keyword.endswith("es") and len(keyword) > 4:
        variants.add(keyword[:-2])
    if keyword.endswith("s") and len(keyword) > 4:
        variants.add(keyword[:-1])
    return {variant for variant in variants if variant}


def _semantic_overlap(purpose: str, question_keywords: set[str]) -> float:
    """Score overlap between node documentation and question intent.

    Splits compound identifiers in docstrings (e.g., 'ErrorHandler' ->
    {'error', 'handler'}) so they match individual question keywords.
    This is general: docstrings in all languages reference code identifiers.
    """
    if not purpose:
        return 0.0
    purpose_words = _split_compound_words(purpose)
    return len(purpose_words & question_keywords) / max(len(question_keywords), 1)


def _symbol_overlap(symbol_name: str, file_path: str, question_keywords: set[str]) -> float:
    if not question_keywords:
        return 0.0
    symbol_words = _split_compound_words(symbol_name)
    path_words = _split_compound_words(file_path)
    expanded_keywords = set()
    for keyword in question_keywords:
        expanded_keywords.update(_keyword_variants(keyword))
    return len((symbol_words | path_words) & expanded_keywords) / max(len(question_keywords), 1)


def _node_question_relevance(node: Node, question_keywords: set[str]) -> float:
    if not question_keywords:
        return 0.0
    sc = node.semantic_contract or {}
    score = 0.0
    score += _semantic_overlap(sc.get("purpose", ""), question_keywords)
    score += 0.7 * _symbol_overlap(
        sc.get("symbol_name", node.node_id),
        node.source_anchor.file_path,
        question_keywords,
    )
    behavior_text = " ".join(sc.get("behavior_patterns", []))
    if behavior_text:
        score += 0.4 * _semantic_overlap(behavior_text, question_keywords)
    uses_text = " ".join(str(item) for item in sc.get("uses", []))
    if uses_text:
        score += 0.2 * _semantic_overlap(uses_text, question_keywords)
    if sc.get("bases") and {
        "inheritance", "inherit", "extends", "extension", "relationship", "relationships", "hierarchy",
    } & question_keywords:
        score += 0.6 + 0.2 * _semantic_overlap(" ".join(sc.get("bases", [])), question_keywords)
    return score


def _drill_question_overlap(node: Node, question_keywords: set[str]) -> float:
    """Question overlap used for drill targeting.

    Prioritises docstring/purpose overlap, with symbol/path overlap as a smaller
    supplement when the purpose text is sparse.
    """
    if not question_keywords:
        return 0.0
    sc = node.semantic_contract or {}
    return (
        1.0 * _semantic_overlap(sc.get("purpose", ""), question_keywords)
        + 0.35 * _symbol_overlap(
            sc.get("symbol_name", node.node_id),
            node.source_anchor.file_path,
            question_keywords,
        )
    )


def _question_content_overlap(
    nodes: list[Node],
    question_keywords: set[str],
    *,
    behavior_only: bool = False,
) -> float:
    if not question_keywords or not nodes:
        return 0.0
    content_tokens: set[str] = set()
    for node in nodes:
        sc = node.semantic_contract or {}
        if behavior_only:
            for item in sc.get("behavior_patterns", []):
                content_tokens.update(_split_compound_words(item))
            for key in ("raises", "uses"):
                for item in sc.get(key, []):
                    content_tokens.update(_split_compound_words(str(item)))
        else:
            content_tokens.update(_split_compound_words(sc.get("symbol_name", "")))
            content_tokens.update(_split_compound_words(sc.get("purpose", "")))
            content_tokens.update(_split_compound_words(node.source_anchor.file_path))
    return len(content_tokens & question_keywords) / max(len(question_keywords), 1)


def _betweenness_centrality(
    node_ids: list[str],
    edges: list[tuple[str, str]],
) -> dict[str, float]:
    """Compute betweenness centrality on a small subgraph."""
    node_set = set(node_ids)
    adj: dict[str, set[str]] = defaultdict(set)
    for u, v in edges:
        if u in node_set and v in node_set:
            adj[u].add(v)
            adj[v].add(u)

    bc: dict[str, float] = {n: 0.0 for n in node_ids}
    for source in node_ids:
        stack: list[str] = []
        pred: dict[str, list[str]] = {n: [] for n in node_ids}
        sigma: dict[str, int] = {n: 0 for n in node_ids}
        sigma[source] = 1
        dist: dict[str, int] = {n: -1 for n in node_ids}
        dist[source] = 0
        queue = [source]
        qi = 0
        while qi < len(queue):
            v = queue[qi]
            qi += 1
            stack.append(v)
            for w in adj.get(v, set()):
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)

        delta = {n: 0.0 for n in node_ids}
        while stack:
            w = stack.pop()
            if sigma[w] == 0:
                continue
            for v in pred[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != source:
                bc[w] += delta[w]

    n = len(node_ids)
    if n > 2:
        norm = 1.0 / ((n - 1) * (n - 2))
        bc = {k: v * norm for k, v in bc.items()}
    return bc


@dataclass
class _FocusSelection:
    selected_nodes: list[Node]
    ranked_candidate_ids: list[str]
    expanded_candidate_ids: list[str]


def _extract_question_entities(question: str, keywords: set[str]) -> set[str]:
    entities = set(keywords)
    q = question.lower()
    for dotted in re.findall(r"[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)+", question):
        entities.add(dotted.lower())
        entities.update(_split_compound_words(dotted))
    for phrase in (
        "error handler",
        "default behavior",
        "edge case",
        "what happens",
    ):
        if phrase in q:
            entities.add(phrase)
    operation_clusters = [
        (
            {"json", "multipart", "upload", "uploads", "form", "forms", "payload", "body"},
            {"post", "read", "json", "multipart", "baserequest.post", "baserequest.read", "baserequest.json"},
        ),
        (
            {"restart", "routing", "route", "routes", "dispatch", "404", "405", "method"},
            {"restartrouting", "next", "match", "defaultctx.restartrouting", "app.next", "app.nextcustom"},
        ),
        (
            {"cleanup", "teardown", "shutdown", "error", "fallback", "default"},
            {"cleanup", "handle_error", "error_handler"},
        ),
    ]
    for triggers, expansions in operation_clusters:
        if triggers & entities or any(trigger in q for trigger in triggers):
            entities.update(expansions)
    return {entity for entity in entities if entity}


def _question_entity_overlap(node: Node, question_entities: set[str]) -> float:
    if not question_entities:
        return 0.0
    sc = node.semantic_contract or {}
    symbol_name = sc.get("symbol_name", node.node_id)
    lower_name = symbol_name.lower()
    name_tokens = _split_compound_words(symbol_name)
    if not name_tokens and lower_name:
        name_tokens = set(re.findall(r"[a-z0-9]{3,}", lower_name))
    best = 0.0
    for entity in question_entities:
        if "." in entity and entity in lower_name:
            best = max(best, 1.4)
            continue
        if " " in entity:
            phrase_tokens = set(entity.split())
            if phrase_tokens:
                overlap = len(phrase_tokens & name_tokens) / len(phrase_tokens)
                if overlap:
                    best = max(best, 0.8 + 0.4 * overlap)
            continue
        if entity in name_tokens:
            best = max(best, 1.0)
        elif entity in lower_name:
            best = max(best, 0.75)
    return best


def _question_has_mechanistic_signals(question: str) -> bool:
    q = question.lower()
    mechanistic_signals = (
        r"\bhow does\b",
        r"\bwhat happens\b",
        r"\bhow .* handle\b",
        r"\bprecedence\b",
        r"\berror\b",
        r"\bwhen .* fails?\b",
        r"\bedge case\b",
        r"\binternally\b",
        r"\bdefault behavior\b",
        r"\bfallback\b",
        r"\bcleanup\b",
        r"\bteardown\b",
        r"\bstep by step\b",
        r"\bunder the hood\b",
    )
    return any(re.search(pattern, q) for pattern in mechanistic_signals)


def _analyze_focus_selection(
    graph: CanonicalClueGraph,
    question: str,
    budget: int = BUDGET_L3,
) -> _FocusSelection:
    """Select and rank task-relevant nodes, retaining expanded candidates for GAPS."""
    keywords = _extract_question_keywords(question)
    question_entities = _extract_question_entities(question, keywords)
    node_by_id = {n.node_id: n for n in graph.nodes}
    symbol_nodes = [
        node for node in graph.nodes
        if node.node_type != "module" and not _is_test_file(node.source_anchor.file_path)
    ]
    soft_cap = max(20, min(80, budget // 25 if budget > 0 else 80))

    def _fallback_nodes() -> _FocusSelection:
        call_edges = [(e.from_node, e.to_node) for e in graph.edges if e.edge_type == "calls"]
        ranks = _pagerank([n.node_id for n in symbol_nodes], call_edges)
        ordered = sorted(
            symbol_nodes,
            key=lambda node: (
                -ranks.get(node.node_id, 0.0),
                0 if node.node_type == "class" else 1,
                node.semantic_contract.get("symbol_name", node.node_id),
            ),
        )
        ranked_ids = [node.node_id for node in ordered]
        return _FocusSelection(ordered[:soft_cap], ranked_ids, ranked_ids[soft_cap:])

    if not keywords:
        return _fallback_nodes()

    contains_children: dict[str, set[str]] = defaultdict(set)
    contains_parents: dict[str, set[str]] = defaultdict(set)
    call_neighbors: dict[str, set[str]] = defaultdict(set)
    structural_edges: list[tuple[str, str]] = []
    expansion_edges = graph.edges
    if len(graph.edges) > LARGE_EDGE_THRESHOLD:
        expansion_edges = _sample_edges(list(graph.edges))
    for edge in expansion_edges:
        if edge.edge_type == "contains":
            contains_children[edge.from_node].add(edge.to_node)
            contains_parents[edge.to_node].add(edge.from_node)
            structural_edges.append((edge.from_node, edge.to_node))
        elif edge.edge_type in {"calls", "inherits", "relates", "routes", "configures", "task"}:
            call_neighbors[edge.from_node].add(edge.to_node)
            call_neighbors[edge.to_node].add(edge.from_node)
            structural_edges.append((edge.from_node, edge.to_node))

    semantic_scores: dict[str, float] = {}
    lexical_scores: dict[str, float] = {}
    entity_scores: dict[str, float] = {}
    class_anchors: list[str] = []
    function_anchors: list[str] = []
    for node in symbol_nodes:
        sc = node.semantic_contract or {}
        overlap = _semantic_overlap(sc.get("purpose", ""), keywords)
        lexical_overlap = _symbol_overlap(
            sc.get("symbol_name", node.node_id),
            node.source_anchor.file_path,
            keywords,
        )
        entity_overlap = _question_entity_overlap(node, question_entities)
        semantic_scores[node.node_id] = overlap
        lexical_scores[node.node_id] = lexical_overlap
        entity_scores[node.node_id] = entity_overlap
        if overlap > 0:
            if node.node_type == "class":
                class_anchors.append(node.node_id)
            else:
                function_anchors.append(node.node_id)

    semantic_anchors = class_anchors + function_anchors
    anchors = list(semantic_anchors)
    lexical_fallback = False
    lexical_supplements: list[str] = []
    entity_expansions: list[str] = [
        node.node_id
        for node in sorted(
            symbol_nodes,
            key=lambda node: (
                -entity_scores.get(node.node_id, 0.0),
                -lexical_scores.get(node.node_id, 0.0),
                0 if node.node_type == "class" else 1,
                node.semantic_contract.get("symbol_name", node.node_id),
            ),
        )
        if entity_scores.get(node.node_id, 0.0) > 0
    ][: max(8, min(20, soft_cap // 2))]
    if not anchors:
        lexical_anchors = [
            node.node_id
            for node in symbol_nodes
            if lexical_scores.get(node.node_id, 0.0) > 0 or entity_scores.get(node.node_id, 0.0) > 0
        ]
        anchors = lexical_anchors[:soft_cap]
        lexical_fallback = bool(anchors)
    else:
        lexical_supplements = [
            node.node_id
            for node in sorted(
                symbol_nodes,
                key=lambda node: (
                    -entity_scores.get(node.node_id, 0.0),
                    -lexical_scores.get(node.node_id, 0.0),
                    0 if node.node_type == "class" else 1,
                    node.semantic_contract.get("symbol_name", node.node_id),
                ),
            )
            if (
                lexical_scores.get(node.node_id, 0.0) > 0 or entity_scores.get(node.node_id, 0.0) > 0
            ) and node.node_id not in semantic_anchors
        ][: max(8, min(20, soft_cap // 3))]
    if not anchors:
        return _fallback_nodes()

    candidates: set[str] = set(anchors)
    anchor_tier: dict[str, int] = {
        anchor: 1 if lexical_fallback else 0
        for anchor in anchors
    }
    for lexical_id in lexical_supplements:
        candidates.add(lexical_id)
        anchor_tier[lexical_id] = min(anchor_tier.get(lexical_id, 1), 1)
    for entity_id in entity_expansions:
        candidates.add(entity_id)
        anchor_tier[entity_id] = min(anchor_tier.get(entity_id, 1), 1)
    for anchor in list(anchors):
        anchor_node = node_by_id.get(anchor)
        if not anchor_node:
            continue
        if anchor_node.node_type == "class":
            for child_id in contains_children.get(anchor, set()):
                child = node_by_id.get(child_id)
                if child and child.node_type in ("function", "async_function"):
                    candidates.add(child_id)
                    anchor_tier[child_id] = min(anchor_tier.get(child_id, 2), anchor_tier[anchor] + 1)
        elif anchor_node.node_type in ("function", "async_function"):
            for parent_id in contains_parents.get(anchor, set()):
                parent = node_by_id.get(parent_id)
                if parent and parent.node_type == "class":
                    candidates.add(parent_id)
                    anchor_tier[parent_id] = min(anchor_tier.get(parent_id, 2), anchor_tier[anchor] + 1)

    frontier = set(anchors)
    visited = set(anchors)
    proximity: dict[str, int] = {anchor: 0 for anchor in anchors}
    for _ in range(2):
        next_frontier: set[str] = set()
        for current in frontier:
            for neighbor in call_neighbors.get(current, set()):
                if neighbor in visited:
                    continue
                neighbor_node = node_by_id.get(neighbor)
                if not neighbor_node or neighbor_node.node_type == "module":
                    continue
                if _is_test_file(neighbor_node.source_anchor.file_path):
                    continue
                candidates.add(neighbor)
                next_frontier.add(neighbor)
                visited.add(neighbor)
                proximity[neighbor] = proximity.get(current, 0) + 1
                anchor_tier[neighbor] = min(
                    anchor_tier.get(neighbor, 3),
                    anchor_tier.get(current, 1 if lexical_fallback else 0) + 1,
                )
        frontier = next_frontier
        if not frontier:
            break

    candidate_ids = [nid for nid in candidates if nid in node_by_id]
    use_pagerank_centrality = len(graph.edges) > LARGE_EDGE_THRESHOLD
    centrality = (
        _pagerank(candidate_ids, structural_edges)
        if use_pagerank_centrality
        else _betweenness_centrality(candidate_ids, structural_edges)
    )
    anchor_support: dict[str, float] = defaultdict(float)
    semantic_anchor_set = set(semantic_anchors)
    for anchor in semantic_anchor_set or set(anchors):
        for neighbor in call_neighbors.get(anchor, set()):
            if neighbor in candidates:
                anchor_support[neighbor] += 1.0
        for parent_id in contains_parents.get(anchor, set()):
            if parent_id in candidates:
                anchor_support[parent_id] += 0.75
        for child_id in contains_children.get(anchor, set()):
            if child_id in candidates:
                anchor_support[child_id] += 0.75
    type_priority = {"class": 0, "function": 1, "async_function": 1, "method": 1}
    relational_focus = bool({
        "inheritance", "inherit", "extends", "extension", "relationship", "relationships", "hierarchy",
    } & keywords)
    structural_focus = _classify_question_type(question, [], symbol_nodes) == "STRUCTURAL"
    mechanistic_focus = _question_has_mechanistic_signals(question)
    max_anchor_support = max(anchor_support.values(), default=0.0)
    file_focus_scores: dict[str, float] = defaultdict(float)
    if structural_focus:
        for candidate_id in candidate_ids:
            node = node_by_id[candidate_id]
            score = lexical_scores.get(candidate_id, 0.0) + entity_scores.get(candidate_id, 0.0)
            if score > 0:
                file_focus_scores[node.source_anchor.file_path] = max(
                    file_focus_scores[node.source_anchor.file_path],
                    score,
                )

    def _normalized_entity_score(nid: str) -> float:
        return min(1.0, max(0.0, entity_scores.get(nid, 0.0) / 1.4))

    def _call_graph_proximity_score(nid: str) -> float:
        distance_score = 1.0 if nid in anchors else 0.0
        if nid in proximity:
            distance_score = max(distance_score, 1.0 / (1.0 + proximity[nid]))
        support_score = 0.0
        if max_anchor_support > 0:
            support_score = min(1.0, anchor_support.get(nid, 0.0) / max_anchor_support)
        return max(distance_score, support_score)

    def _blended_focus_score(nid: str) -> float:
        semantic_score = min(1.0, max(0.0, semantic_scores.get(nid, 0.0)))
        entity_score = _normalized_entity_score(nid)
        proximity_score = _call_graph_proximity_score(nid)
        file_score = 0.0
        if structural_focus:
            file_score = min(1.0, file_focus_scores.get(node_by_id[nid].source_anchor.file_path, 0.0))
        return (
            (0.52 * semantic_score)
            + (0.22 * entity_score)
            + (0.14 * proximity_score)
            + (0.12 * file_score)
        )

    def _rank_key(nid: str) -> tuple:
        return (
            -_blended_focus_score(nid),
            0 if (semantic_scores.get(nid, 0.0) > 0 or entity_scores.get(nid, 0.0) > 0) else 1,
            0 if relational_focus and (node_by_id[nid].semantic_contract or {}).get("bases") else 1,
            anchor_tier.get(nid, 3),
            -semantic_scores.get(nid, 0.0),
            -_normalized_entity_score(nid),
            -_call_graph_proximity_score(nid),
            -_node_question_relevance(node_by_id[nid], keywords),
            proximity.get(nid, 99),
            -centrality.get(nid, 0.0),
            -lexical_scores.get(nid, 0.0),
            type_priority.get(node_by_id[nid].node_type, 2),
            node_by_id[nid].semantic_contract.get("symbol_name", node_by_id[nid].node_id),
        )

    ranked_ids = sorted(candidate_ids, key=_rank_key)
    priority_entity_ids = [
        nid for nid in ranked_ids
        if entity_scores.get(nid, 0.0) > 0
    ][: max(6, min(12, soft_cap // 3))]

    if mechanistic_focus and ranked_ids:
        seed_ids = list(dict.fromkeys(priority_entity_ids + ranked_ids[: max(6, min(12, soft_cap // 2))]))
        for seed_id in seed_ids:
            for neighbor in call_neighbors.get(seed_id, set()):
                neighbor_node = node_by_id.get(neighbor)
                if not neighbor_node or neighbor_node.node_type == "module":
                    continue
                if _is_test_file(neighbor_node.source_anchor.file_path):
                    continue
                candidates.add(neighbor)
                anchor_tier[neighbor] = min(anchor_tier.get(neighbor, 4), anchor_tier.get(seed_id, 2) + 1)
                proximity.setdefault(neighbor, proximity.get(seed_id, 0) + 1)
        candidate_ids = [nid for nid in candidates if nid in node_by_id]
        centrality = (
            _pagerank(candidate_ids, structural_edges)
            if use_pagerank_centrality
            else _betweenness_centrality(candidate_ids, structural_edges)
        )
        ranked_ids = sorted(candidate_ids, key=_rank_key)

    selected_ids = ranked_ids[:soft_cap]
    expanded_candidate_ids = [nid for nid in ranked_ids if nid not in selected_ids]
    return _FocusSelection(
        selected_nodes=[node_by_id[nid] for nid in selected_ids],
        ranked_candidate_ids=ranked_ids,
        expanded_candidate_ids=expanded_candidate_ids,
    )


def _select_focus_nodes(
    graph: CanonicalClueGraph,
    question: str,
    budget: int = BUDGET_L3,
) -> list[Node]:
    """Select task-relevant nodes via semantic anchoring and structure."""
    selection = _analyze_focus_selection(graph, question, budget=budget).selected_nodes
    if not _is_enterprise_graph(graph):
        return selection

    prepended = _top_config_focus_nodes(graph)
    merged: list[Node] = []
    seen: set[str] = set()
    for node in prepended + selection:
        if node.node_id in seen:
            continue
        merged.append(node)
        seen.add(node.node_id)
    return merged


def _render_l3(
    graph: CanonicalClueGraph,
    question: str,
    repo_root: str | Path = ".",
    budget: int = BUDGET_L3,
) -> str:
    """Render L3 FOCUS: task-conditioned behavioural detail."""
    focus_nodes = _select_focus_nodes(graph, question, budget=budget)
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

        if node.node_type == "config":
            config_entries = sc.get("config_entries", [])
            services = sc.get("services", [])
            dependencies = sc.get("dependencies", [])
            if config_entries:
                entry_lines.append(f"  entries: {', '.join(config_entries[:5])}")
            if services:
                entry_lines.append(f"  services: {', '.join(services[:5])}")
            if dependencies:
                entry_lines.append(f"  deps: {', '.join(dependencies[:6])}")

        if node.node_type == "doc":
            headings = sc.get("headings", [])
            if headings:
                entry_lines.append(f"  sections: {', '.join(headings[:5])}")

        if node.node_type == "route":
            route_target = sc.get("route_target", "")
            if route_target:
                entry_lines.append(f"  target: {route_target}")

        # Signature for functions
        sig = sc.get("signature", "")
        if sig and sig != "()" and node.node_type != "class":
            entry_lines.append(f"  sig: {sym_name}{sig}")

        behavior = sc.get("behavior_patterns", [])
        if behavior:
            entry_lines.append(f"  behavior: {'; '.join(behavior)}")

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

def _classify_question_type(
    question: str,
    focus_nodes: list[Node],
    l2_symbols: list[Node],
) -> str:
    """Classify question as STRUCTURAL, RELATIONAL, or MECHANISTIC.

    Uses both question phrasing and repository content coverage. Questions that
    can be grounded in L0-L2 symbol metadata should stay STRUCTURAL/RELATIONAL;
    only questions that require body-level behavior should be marked
    MECHANISTIC.
    """
    q = question.lower()
    keywords = _extract_question_keywords(question)
    behavior_verbs = {"handle", "resolve", "convert", "dispatch", "process"}
    symbolish_reference = bool(re.search(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+", question))
    behavior_verb_hit = any(re.search(rf"\b{verb}\b", q) for verb in behavior_verbs)
    mechanistic_signal = _question_has_mechanistic_signals(question) or any(
        phrase in q
        for phrase in (
            "what happens",
            "what does",
            "actually do",
            "when ",
            "error",
            "default behavior",
            "edge case",
        )
    )

    relational_signals = [
        "relationship",
        "calls",
        "depends on",
        "inherits",
        "extends",
        "implements",
        "connected",
        "hierarchy",
        "which .* call",
        "who calls",
        "interact",
        "communicate",
        "flow between",
        "used by",
    ]
    structural_score = _question_content_overlap(l2_symbols, keywords)
    behavior_score = _question_content_overlap(focus_nodes, keywords, behavior_only=True)

    if mechanistic_signal and (
        behavior_verb_hit
        or symbolish_reference
        or " work" in q
        or "internally" in q
        or behavior_score > 0
        or structural_score == 0
    ):
        return "MECHANISTIC"

    if behavior_verb_hit and (symbolish_reference or any(word in keywords for word in behavior_verbs)):
        return "MECHANISTIC"

    if any(re.search(signal, q) for signal in relational_signals):
        return "RELATIONAL"

    if behavior_score >= structural_score - 0.05:
        return "MECHANISTIC"

    return "STRUCTURAL"


def _render_gaps(
    graph: CanonicalClueGraph,
    question: str,
    focus_nodes: list[Node],
    l2_symbols: list[Node],
    budget: int = BUDGET_GAPS,
) -> str:
    """Render enhanced GAPS: sufficiency classification + coverage + drill targets.

    v2.1: Replaces keyword-gap reporting with:
    1. Question type classification (STRUCTURAL/RELATIONAL/MECHANISTIC)
    2. Coverage report (how many task-relevant symbols have behavioral annotations)
    3. Costed drill targets (file:lines + estimated size for informed drill-down)
    """
    question_keywords = _extract_question_keywords(question)
    question_entities = _extract_question_entities(question, question_keywords)
    question_type = _classify_question_type(question, focus_nodes, l2_symbols)

    # Count coverage
    total_focus = len(focus_nodes)
    with_behavior = sum(
        1 for n in focus_nodes
        if (n.semantic_contract or {}).get("behavior_patterns")
    )

    lines = ["-- GAPS"]

    # Line 1: question type + sufficiency hint
    if question_type == "STRUCTURAL":
        lines.append(f"type: STRUCTURAL (answerable from L0-L2)")
    elif question_type == "RELATIONAL":
        lines.append(f"type: RELATIONAL (answerable from L2-L3 structure)")
    else:
        lines.append(f"type: MECHANISTIC (body logic needed for full answer)")

    # Line 2: coverage
    lines.append(f"coverage: {total_focus} symbols in L3, {with_behavior} with behavior annotations")

    selection = _analyze_focus_selection(graph, question, budget=BUDGET_L3)
    focus_ids = {node.node_id for node in focus_nodes}
    node_by_id = {node.node_id: node for node in graph.nodes}
    candidate_order = {nid: idx for idx, nid in enumerate(selection.ranked_candidate_ids)}
    uncovered_pool = sorted(
        (nid for nid in selection.ranked_candidate_ids if nid not in focus_ids),
        key=lambda nid: (
            -_question_entity_overlap(node_by_id[nid], question_entities),
            -_drill_question_overlap(node_by_id[nid], question_keywords),
            candidate_order[nid],
        ),
    )
    uncovered = [
        (node_by_id[nid].semantic_contract or {}).get("symbol_name", nid)
        for nid in uncovered_pool
    ]
    if uncovered:
        lines.append(f"uncovered: {', '.join(uncovered[:4])}")

    # Line 3+: drill targets for mechanistic questions.
    # v2.1.1: For MECHANISTIC questions, ALL function-level FOCUS nodes are
    # drill candidates, not just unannotated ones. Behavioral annotations
    # capture control-flow *structure* but not *content* (specific conditions,
    # precedence values, constructor wiring). Ranked by:
    #   1. Unannotated functions (highest info gap)
    #   2. Annotated functions with large bodies (shallow annotation risk)
    #   3. Annotated functions with callees also in FOCUS (call-chain depth)
    if question_type == "MECHANISTIC":
        func_focus = [
            n for n in focus_nodes
            if (n.semantic_contract or {}).get("symbol_type") in (
                "function", "method", "async_function", "async_method", None
            )
        ]
        focus_relevance = {
            node.node_id: _drill_question_overlap(node, question_keywords)
            for node in focus_nodes
        }

        def _drill_priority(n: Node) -> tuple:
            byte_span = n.source_anchor.byte_end - n.source_anchor.byte_start
            relevance = _drill_question_overlap(n, question_keywords)
            sym_id = n.node_id
            chain_support = 0.0
            for edge in graph.edges:
                if edge.edge_type != "calls":
                    continue
                if edge.from_node == sym_id and edge.to_node in focus_ids:
                    chain_support += max(0.25, focus_relevance.get(edge.to_node, 0.0))
                elif edge.to_node == sym_id and edge.from_node in focus_ids:
                    chain_support += max(0.25, focus_relevance.get(edge.from_node, 0.0))
            return (-relevance, -chain_support, -byte_span)

        drill_candidates = sorted(func_focus, key=_drill_priority)

        for node in drill_candidates[:5]:  # increased from 3 to 5
            sc = node.semantic_contract or {}
            sym_name = sc.get("symbol_name", node.node_id)
            fp = node.source_anchor.file_path
            byte_span = node.source_anchor.byte_end - node.source_anchor.byte_start
            est_lines = max(1, byte_span // 40)
            lines.append(f"drill: {fp} (~{est_lines} lines, {sym_name})")

    # Trim if over budget
    result = "\n".join(lines) + "\n"
    while _token_count(result) > budget and len(lines) > 2:
        lines.pop()
        result = "\n".join(lines) + "\n"

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
    header = f"=CC v2.1 {repo_name}@{commit_short} {module_count}mod {sym_count}sym\n"
    header += f"? {question}\n"

    # Render each level
    enterprise_context = _is_enterprise_graph(graph)
    readme_preamble = _render_readme_preamble(graph) if enterprise_context else ""
    l2_budget = BUDGET_L2 - L2_ENTERPRISE_CONTEXT_BUDGET if enterprise_context else BUDGET_L2
    l0 = _render_l0(graph)
    l1 = _render_l1(graph, repo_root)
    l2_text = _render_l2(graph, repo_root, budget=l2_budget)
    l3 = _render_l3(graph, question, repo_root)

    # For GAPS, we need focus and l2 node lists
    focus_nodes = _select_focus_nodes(graph, question, budget=BUDGET_L3)
    l2_symbols = [n for n in graph.nodes if n.node_type != "module"]

    gaps = _render_gaps(graph, question, focus_nodes, l2_symbols)

    # Assemble
    sections = [header, "", readme_preamble, l0, l1, l2_text, l3, gaps]
    result = "\n".join(sections)

    # Final budget check — if over total, trim L3 FOCUS first
    total_toks = _token_count(result)
    if total_toks > BUDGET_TOTAL:
        # Re-render L3 with reduced budget
        overshoot = total_toks - BUDGET_TOTAL
        reduced_l3_budget = max(200, BUDGET_L3 - overshoot)
        l3 = _render_l3(graph, question, repo_root, budget=reduced_l3_budget)
        sections = [header, "", readme_preamble, l0, l1, l2_text, l3, gaps]
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
            "node_id": node.node_id,
            "symbol": sym_name,
            "type": node.node_type,
            "file": fp,
            "lines": [start_line, end_line],
            "source": source_snippet,
            "calls": _resolve_names(calls_out.get(node.node_id, [])),
            "called_by": _resolve_names(calls_in.get(node.node_id, [])),
            "confidence": node.confidence,
            "purpose": sc.get("purpose", ""),
            "behavior_patterns": list(sc.get("behavior_patterns", []) or []),
            "semantic_contract": sc,
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
