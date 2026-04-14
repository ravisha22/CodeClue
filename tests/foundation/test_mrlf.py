"""Tests for MRLF renderer (clue_view_mrlf.py).

Tests cover:
  - PageRank implementation
  - L0 TREE rendering
  - L1 INDEX rendering
  - L2 SYM rendering
  - L3 FOCUS keyword anchoring + graph walk
  - GAPS generation
  - Full render_mrlf integration
  - Detail store generation
  - Budget enforcement
"""

from __future__ import annotations

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from codeclue_research.models import CanonicalClueGraph, Node, Edge, SourceAnchor
from codeclue_research.clue_view_mrlf import (
    _pagerank,
    _render_l0,
    _render_l1,
    _render_l2,
    _render_l3,
    _render_gaps,
    _extract_question_keywords,
    _select_focus_nodes,
    _word_count,
    render_mrlf,
    generate_detail_store,
    write_detail_store,
    BUDGET_TOTAL,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_anchor(file_path: str, byte_start: int = 0, byte_end: int = 100) -> SourceAnchor:
    return SourceAnchor(
        file_path=file_path,
        byte_start=byte_start,
        byte_end=byte_end,
        ast_path="test",
        content_hash="abc123",
    )


def _make_node(
    node_id: str,
    node_type: str,
    file_path: str,
    symbol_name: str | None = None,
    confidence: float = 0.9,
    purpose: str = "",
) -> Node:
    sname = symbol_name or node_id.split(":")[-1]
    return Node(
        node_id=node_id,
        node_type=node_type,
        source_anchor=_make_anchor(file_path),
        semantic_contract={
            "symbol_name": sname,
            "symbol_type": node_type,
            "purpose": purpose or f"{node_type} {sname}",
            "language": "python",
            "tier": 1,
            "calls": [],
            "called_by": [],
            "complexity_indicators": {"decorator_depth": 0, "generic_type_param_count": 0},
        },
        confidence=confidence,
    )


def _make_edge(edge_type: str, from_node: str, to_node: str) -> Edge:
    return Edge(
        edge_id=f"{edge_type}:{from_node}:{to_node}",
        edge_type=edge_type,
        from_node=from_node,
        to_node=to_node,
        evidence={"line": 1} if edge_type == "calls" else {"rel": "ast_containment"},
    )


def _make_small_graph() -> CanonicalClueGraph:
    """Small graph: 2 modules, 5 symbols, call chain A->B->C."""
    nodes = [
        _make_node("module:src/app.py", "module", "src/app.py", symbol_name="src/app.py"),
        _make_node("module:src/config.py", "module", "src/config.py", symbol_name="src/config.py"),
        _make_node("sym:app:Flask", "class", "src/app.py", symbol_name="Flask", purpose="Main application class"),
        _make_node("sym:app:wsgi_app", "function", "src/app.py", symbol_name="wsgi_app", purpose="WSGI entrypoint"),
        _make_node("sym:app:dispatch", "function", "src/app.py", symbol_name="dispatch_request"),
        _make_node("sym:config:Config", "class", "src/config.py", symbol_name="Config", purpose="Configuration dict subclass"),
        _make_node("sym:config:from_file", "function", "src/config.py", symbol_name="from_file", confidence=0.6),
    ]
    edges = [
        _make_edge("contains", "module:src/app.py", "sym:app:Flask"),
        _make_edge("contains", "module:src/app.py", "sym:app:wsgi_app"),
        _make_edge("contains", "module:src/app.py", "sym:app:dispatch"),
        _make_edge("contains", "module:src/config.py", "sym:config:Config"),
        _make_edge("contains", "module:src/config.py", "sym:config:from_file"),
        _make_edge("calls", "sym:app:wsgi_app", "sym:app:dispatch"),
        _make_edge("calls", "sym:app:Flask", "sym:config:Config"),
        _make_edge("calls", "sym:config:Config", "sym:config:from_file"),
    ]
    return CanonicalClueGraph(
        metadata={"schema_version": "2.0", "generator": "test"},
        repository={"name": "test-repo", "root_path": "."},
        nodes=nodes,
        edges=edges,
    )


def _make_large_graph(n_modules: int = 50, symbols_per_module: int = 10) -> CanonicalClueGraph:
    """Larger graph for budget testing."""
    nodes: list[Node] = []
    edges: list[Edge] = []
    all_sym_ids: list[str] = []

    for m in range(n_modules):
        mod_id = f"module:src/mod{m:03d}.py"
        nodes.append(_make_node(mod_id, "module", f"src/mod{m:03d}.py", symbol_name=f"src/mod{m:03d}.py"))
        for s in range(symbols_per_module):
            sym_id = f"sym:mod{m:03d}:func{s:03d}"
            nodes.append(_make_node(sym_id, "function", f"src/mod{m:03d}.py", symbol_name=f"func{s:03d}"))
            edges.append(_make_edge("contains", mod_id, sym_id))
            all_sym_ids.append(sym_id)

    # Add some call edges (chain within each module)
    for m in range(n_modules):
        for s in range(symbols_per_module - 1):
            edges.append(_make_edge("calls", f"sym:mod{m:03d}:func{s:03d}", f"sym:mod{m:03d}:func{s + 1:03d}"))
        # Cross-module calls
        if m > 0:
            edges.append(_make_edge("calls", f"sym:mod{m:03d}:func000", f"sym:mod{m - 1:03d}:func000"))

    return CanonicalClueGraph(
        metadata={"schema_version": "2.0", "generator": "test"},
        repository={"name": "large-test", "root_path": "."},
        nodes=nodes,
        edges=edges,
    )


# ---------------------------------------------------------------------------
# PageRank tests
# ---------------------------------------------------------------------------

class TestPageRank:
    def test_empty_graph(self):
        result = _pagerank([], [])
        assert result == {}

    def test_single_node(self):
        result = _pagerank(["a"], [])
        assert "a" in result
        assert abs(result["a"] - 1.0) < 0.01

    def test_two_node_chain(self):
        result = _pagerank(["a", "b"], [("a", "b")])
        # b should have higher rank (receives link from a)
        assert result["b"] > result["a"]

    def test_cycle(self):
        result = _pagerank(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
        # Equal ranks in a cycle
        assert abs(result["a"] - result["b"]) < 0.01
        assert abs(result["b"] - result["c"]) < 0.01

    def test_star_topology(self):
        # Many nodes point to one hub
        nodes = ["hub"] + [f"n{i}" for i in range(10)]
        edges = [(f"n{i}", "hub") for i in range(10)]
        result = _pagerank(nodes, edges)
        assert result["hub"] > max(result[f"n{i}"] for i in range(10))

    def test_sum_approximately_one(self):
        nodes = ["a", "b", "c", "d"]
        edges = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")]
        result = _pagerank(nodes, edges)
        assert abs(sum(result.values()) - 1.0) < 0.01


# ---------------------------------------------------------------------------
# Keyword extraction tests
# ---------------------------------------------------------------------------

class TestKeywordExtraction:
    def test_basic_extraction(self):
        kw = _extract_question_keywords("What is the impact of modifying Flask.wsgi_app?")
        assert "flask" in kw
        assert "wsgi_app" in kw
        assert "impact" in kw
        assert "modifying" in kw
        assert "the" not in kw
        assert "of" not in kw

    def test_empty_question(self):
        kw = _extract_question_keywords("")
        assert kw == set()

    def test_code_identifiers(self):
        kw = _extract_question_keywords("Where is Config.from_file defined?")
        assert "config" in kw
        assert "from_file" in kw


# ---------------------------------------------------------------------------
# L0 TREE tests
# ---------------------------------------------------------------------------

class TestL0:
    def test_renders_tree_header(self):
        graph = _make_small_graph()
        result = _render_l0(graph)
        assert result.startswith("-- TREE")

    def test_contains_directories(self):
        graph = _make_small_graph()
        result = _render_l0(graph)
        assert "src/" in result

    def test_empty_graph(self):
        graph = CanonicalClueGraph(
            metadata={}, repository={}, nodes=[], edges=[],
        )
        result = _render_l0(graph)
        assert "-- TREE" in result


# ---------------------------------------------------------------------------
# L1 INDEX tests
# ---------------------------------------------------------------------------

class TestL1:
    def test_renders_index_header(self):
        graph = _make_small_graph()
        result = _render_l1(graph)
        assert result.startswith("-- INDEX")

    def test_contains_module_files(self):
        graph = _make_small_graph()
        result = _render_l1(graph)
        assert "src/app.py" in result
        assert "src/config.py" in result

    def test_budget_enforced(self):
        graph = _make_large_graph(n_modules=200)
        result = _render_l1(graph, budget=50)
        words = _word_count(result)
        # Should be under or near budget (with the "...and N more" line)
        assert words < 80  # generous margin


# ---------------------------------------------------------------------------
# L2 SYM tests
# ---------------------------------------------------------------------------

class TestL2:
    def test_renders_sym_header(self):
        graph = _make_small_graph()
        result = _render_l2(graph)
        assert result.startswith("-- SYM")

    def test_contains_symbol_names(self):
        graph = _make_small_graph()
        result = _render_l2(graph)
        assert "Flask" in result or "wsgi_app" in result or "Config" in result

    def test_modules_excluded(self):
        graph = _make_small_graph()
        result = _render_l2(graph)
        lines = result.strip().split("\n")
        for line in lines[1:]:  # skip header
            if line.startswith("  ..."):
                continue
            assert "module:" not in line.lower() or "src/" not in line[:10]

    def test_budget_enforced_large(self):
        graph = _make_large_graph(n_modules=50, symbols_per_module=20)
        result = _render_l2(graph, budget=200)
        words = _word_count(result)
        assert words < 250  # generous margin


# ---------------------------------------------------------------------------
# L3 FOCUS tests
# ---------------------------------------------------------------------------

class TestL3:
    def test_renders_focus_header(self):
        graph = _make_small_graph()
        result = _render_l3(graph, "What does wsgi_app do?")
        assert result.startswith("-- FOCUS")

    def test_keyword_anchoring(self):
        graph = _make_small_graph()
        focus = _select_focus_nodes(graph, "What does wsgi_app do?")
        focus_names = {
            n.semantic_contract.get("symbol_name", "") for n in focus
        }
        assert "wsgi_app" in focus_names

    def test_graph_walk_includes_neighbors(self):
        graph = _make_small_graph()
        # wsgi_app calls dispatch_request, so dispatch should be in focus
        focus = _select_focus_nodes(graph, "What does wsgi_app do?")
        focus_names = {
            n.semantic_contract.get("symbol_name", "") for n in focus
        }
        assert "dispatch_request" in focus_names

    def test_no_question_falls_back_to_pagerank(self):
        graph = _make_small_graph()
        focus = _select_focus_nodes(graph, "")
        assert len(focus) > 0

    def test_budget_enforced(self):
        graph = _make_large_graph()
        result = _render_l3(graph, "What does func000 do?", budget=100)
        words = _word_count(result)
        assert words < 150  # generous margin


# ---------------------------------------------------------------------------
# GAPS tests
# ---------------------------------------------------------------------------

class TestGaps:
    def test_renders_gaps_header(self):
        graph = _make_small_graph()
        focus = _select_focus_nodes(graph, "What about sessions?")
        l2 = [n for n in graph.nodes if n.node_type != "module"]
        result = _render_gaps(graph, "What about sessions?", focus, l2)
        assert result.startswith("-- GAPS")

    def test_uncovered_keyword_flagged(self):
        graph = _make_small_graph()
        focus = _select_focus_nodes(graph, "What about sessions module?")
        l2 = [n for n in graph.nodes if n.node_type != "module"]
        result = _render_gaps(graph, "What about sessions module?", focus, l2)
        assert "sessions" in result.lower()

    def test_low_confidence_flagged(self):
        graph = _make_small_graph()
        # from_file has confidence 0.6
        focus = _select_focus_nodes(graph, "How does Config.from_file work?")
        l2 = [n for n in graph.nodes if n.node_type != "module"]
        result = _render_gaps(graph, "How does Config.from_file work?", focus, l2)
        assert "confidence" in result.lower() or "from_file" in result

    def test_max_5_bullets(self):
        graph = _make_small_graph()
        focus = []
        l2 = []
        result = _render_gaps(
            graph,
            "sessions templates blueprints signals helpers logging views wrappers",
            focus, l2,
        )
        bullet_count = result.count("\n- ")
        assert bullet_count <= 5


# ---------------------------------------------------------------------------
# Full render_mrlf tests
# ---------------------------------------------------------------------------

class TestRenderMRLF:
    def test_renders_all_sections(self):
        graph = _make_small_graph()
        result = render_mrlf(graph, "What does wsgi_app do?")
        assert "=CC v2" in result
        assert "-- TREE" in result
        assert "-- INDEX" in result
        assert "-- SYM" in result
        assert "-- FOCUS" in result
        assert "-- GAPS" in result

    def test_header_contains_question(self):
        graph = _make_small_graph()
        result = render_mrlf(graph, "What does wsgi_app do?")
        assert "? What does wsgi_app do?" in result

    def test_header_contains_counts(self):
        graph = _make_small_graph()
        result = render_mrlf(graph, "test question")
        assert "2mod" in result  # 2 modules
        assert "5sym" in result  # 5 symbols

    def test_total_budget_respected(self):
        graph = _make_large_graph(n_modules=50, symbols_per_module=20)
        result = render_mrlf(graph, "What does func000 do?")
        words = _word_count(result)
        # Allow generous margin — budget is ~3190 words
        assert words < BUDGET_TOTAL + 200

    def test_small_graph_output_reasonable(self):
        graph = _make_small_graph()
        result = render_mrlf(graph, "Impact of modifying Config?")
        words = _word_count(result)
        # Small graph should produce compact output
        assert words < 500


# ---------------------------------------------------------------------------
# Detail store tests
# ---------------------------------------------------------------------------

class TestDetailStore:
    def test_generates_records_for_symbols(self):
        graph = _make_small_graph()
        records = generate_detail_store(graph)
        assert len(records) == 5  # 5 non-module symbols

    def test_each_record_has_required_fields(self):
        graph = _make_small_graph()
        records = generate_detail_store(graph)
        required = {"symbol", "type", "file", "lines", "source", "calls", "called_by", "confidence", "purpose"}
        for rec in records:
            assert required.issubset(rec.keys()), f"Missing fields: {required - rec.keys()}"

    def test_modules_excluded(self):
        graph = _make_small_graph()
        records = generate_detail_store(graph)
        for rec in records:
            assert rec["type"] != "module"

    def test_call_graph_populated(self):
        graph = _make_small_graph()
        records = generate_detail_store(graph)
        wsgi_rec = next(r for r in records if r["symbol"] == "wsgi_app")
        assert "dispatch_request" in wsgi_rec["calls"]

    def test_write_jsonl(self, tmp_path):
        graph = _make_small_graph()
        records = generate_detail_store(graph)
        out = tmp_path / "test.codeclue-detail"
        write_detail_store(records, out)
        assert out.exists()
        lines = out.read_text().strip().split("\n")
        assert len(lines) == 5
        # Each line should be valid JSON
        for line in lines:
            parsed = json.loads(line)
            assert "symbol" in parsed
