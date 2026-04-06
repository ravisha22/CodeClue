"""Tests for Plan B: flat-table clue view renderer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from codeclue_research.clue_view_plan_b import (
    FORBIDDEN_FIELDS,
    render_clue_plan_b,
    validate_clue_purity,
)
from codeclue_research.models import (
    CanonicalClueGraph,
    Edge,
    Node,
    SourceAnchor,
)
from codeclue_research.token_counter import count_tokens


# ---------------------------------------------------------------------------
# Fixtures (same graph structure as Plan A tests for fair comparison)
# ---------------------------------------------------------------------------

def _anchor(path: str = "src/app.py", start: int = 0, end: int = 200) -> SourceAnchor:
    return SourceAnchor(file_path=path, byte_start=start, byte_end=end, ast_path="function:test", content_hash="abc123")


def _node(nid: str, ntype: str = "function", name: str = "", path: str = "src/app.py", conf: float = 0.9) -> Node:
    return Node(
        node_id=nid, node_type=ntype,
        source_anchor=_anchor(path),
        semantic_contract={"symbol_name": name or nid, "language": "python", "tier": 1,
                           "complexity_indicators": {}, "calls": [], "called_by": []},
        confidence=conf,
    )


def _edge(etype: str, from_n: str, to_n: str, line: int = 10) -> Edge:
    eid = f"{etype}:{from_n}:{to_n}:{line}"
    return Edge(edge_id=eid, edge_type=etype, from_node=from_n, to_node=to_n,
                evidence={"line": line} if etype == "calls" else {})


def _make_graph_and_projection(tmp_path: Path) -> tuple[CanonicalClueGraph, dict[str, Any]]:
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "app.py").write_text(
        "def wsgi_app(self, environ):\n"
        "    try:\n"
        "        return self.dispatch()\n"
        "    finally:\n"
        "        self.cleanup()\n"
        "\n"
        "def dispatch(self):\n"
        "    return self.handle()\n"
        "\n"
        "def handle(self):\n"
        "    return 'ok'\n"
        "\n"
        "def cleanup(self):\n"
        "    pass\n",
        encoding="utf-8",
    )

    nodes = [
        _node("module:src/app.py", "module", "src/app.py"),
        _node("symbol:src/app.py:wsgi_app:1", "function", "wsgi_app", conf=0.95),
        _node("symbol:src/app.py:dispatch:7", "function", "dispatch", conf=0.88),
        _node("symbol:src/app.py:handle:10", "function", "handle", conf=0.82),
        _node("symbol:src/app.py:cleanup:13", "function", "cleanup", conf=0.75),
    ]
    edges = [
        _edge("contains", "module:src/app.py", "symbol:src/app.py:wsgi_app:1"),
        _edge("contains", "module:src/app.py", "symbol:src/app.py:dispatch:7"),
        _edge("contains", "module:src/app.py", "symbol:src/app.py:handle:10"),
        _edge("contains", "module:src/app.py", "symbol:src/app.py:cleanup:13"),
        _edge("calls", "symbol:src/app.py:wsgi_app:1", "symbol:src/app.py:dispatch:7"),
        _edge("calls", "symbol:src/app.py:dispatch:7", "symbol:src/app.py:handle:10"),
        _edge("calls", "symbol:src/app.py:wsgi_app:1", "symbol:src/app.py:cleanup:13"),
    ]

    graph = CanonicalClueGraph(
        metadata={"project": "test"}, repository={"url": "test"},
        nodes=nodes, edges=edges,
    )

    projection: dict[str, Any] = {
        "trace_id": "trace-test-001",
        "operation_family": "OF2",
        "prompt_profile": {"repo": "test/repo", "question": "What does wsgi_app do?"},
        "projected_nodes": [n.to_dict() for n in nodes],
        "projected_edges": [e.to_dict() for e in edges],
        "confidence": {
            "confidence_overall": 0.72,
            "lookup_decision_hint": "targeted_lookup",
            "per_node_confidence": [
                {"node_id": n.node_id, "confidence": n.confidence, "tier": 1,
                 "density_indicators": {}, "suggested_actions": []}
                for n in nodes
            ],
            "per_edge_confidence": [],
            "p_context_miss": 0.0,
            "p_dependency_miss": 0.2,
            "p_hallucination": 0.0,
            "code_density_risk": 0.1,
            "tool_call_budget": 15,
            "threshold": 0.9,
        },
        "reasoning_path": [],
        "validation": {"path_precision": 0.95},
        "stats": {"projected_node_count": 5},
        "policy": {"max_depth": 3},
    }

    return graph, projection


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSchemaB:
    def test_has_required_top_level_keys(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "What does wsgi_app do?", str(tmp_path))
        assert "task" in clue
        assert "clue_summary" in clue
        assert "nodes" in clue
        assert "relations" in clue
        assert "assertions" in clue
        assert "uncertainty" in clue

    def test_task_fields(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        task = clue["task"]
        assert "id" in task
        assert "family" in task
        assert "question" in task

    def test_clue_summary_structure(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        cs = clue["clue_summary"]
        assert "system_behavior" in cs
        assert "key_files" in cs
        assert "key_symbols" in cs
        assert isinstance(cs["system_behavior"], list)

    def test_uncertainty_structure(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        unc = clue["uncertainty"]
        assert "overall_confidence" in unc
        assert "lookup_hint" in unc
        assert "known_gaps" in unc
        assert len(unc["known_gaps"]) <= 3


class TestForbiddenFieldsB:
    def test_no_forbidden_fields(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        passed, violations = validate_clue_purity(clue)
        assert passed, f"Forbidden fields leaked: {violations}"

    def test_validate_catches_injected(self) -> None:
        bad = {"nodes": [{"reasoning_path": [1]}]}
        passed, violations = validate_clue_purity(bad)
        assert not passed


class TestRelationIntegrity:
    def test_all_from_to_exist_in_nodes(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        node_ids = {n["id"] for n in clue["nodes"]}
        for rel in clue["relations"]:
            assert rel["from"] in node_ids, f"Relation from {rel['from']} not in nodes"
            assert rel["to"] in node_ids, f"Relation to {rel['to']} not in nodes"

    def test_short_ids_in_relations(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        for rel in clue["relations"]:
            assert rel["from"].startswith("n"), f"Raw ID in relation: {rel['from']}"
            assert rel["to"].startswith("n"), f"Raw ID in relation: {rel['to']}"


class TestAssertionPaths:
    def test_assertion_paths_reference_valid_nodes(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        node_ids = {n["id"] for n in clue["nodes"]}
        for assertion in clue["assertions"]:
            for nid in assertion.get("path", []):
                assert nid in node_ids, f"Assertion path ref {nid} not in nodes"

    def test_assertions_have_fact(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        for assertion in clue["assertions"]:
            assert "fact" in assertion
            assert len(assertion["fact"]) > 0

    def test_assertions_capped(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        assert len(clue["assertions"]) <= 5


class TestNodeTable:
    def test_nodes_have_required_fields(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        required = {"id", "type", "name", "summary", "file", "lines", "importance", "role"}
        for node in clue["nodes"]:
            missing = required - set(node.keys())
            assert not missing, f"Node {node.get('id')} missing: {missing}"

    def test_short_ids_sequential(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        ids = [n["id"] for n in clue["nodes"]]
        for i, nid in enumerate(ids, 1):
            assert nid == f"n{i}"

    def test_total_clue_is_compact(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_b(proj, graph, "Test?", str(tmp_path))
        total = count_tokens(clue)
        assert total < 2000, f"Total clue is {total} tokens"
