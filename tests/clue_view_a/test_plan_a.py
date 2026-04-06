"""Tests for Plan A: entity-centric clue view renderer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from codeclue_research.clue_view_plan_a import (
    FORBIDDEN_FIELDS,
    render_clue_plan_a,
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
# Fixtures
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
    """Create a minimal graph + projection for testing."""
    # Write a minimal source file
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


class TestSchemaA:
    def test_has_required_top_level_keys(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "What does wsgi_app do?", str(tmp_path))
        assert "task" in clue
        assert "summary" in clue
        assert "entities" in clue
        assert "uncertainty" in clue

    def test_task_has_required_fields(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        task = clue["task"]
        assert "id" in task
        assert "family" in task
        assert "question" in task

    def test_uncertainty_structure(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        unc = clue["uncertainty"]
        assert "confidence" in unc
        assert "hint" in unc
        assert "gaps" in unc
        assert isinstance(unc["gaps"], list)
        assert len(unc["gaps"]) <= 3


class TestEntityCompleteness:
    def test_entities_have_all_dimensions(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        required = {"id", "class", "name", "file", "lines", "weight", "behavior"}
        optional = {"sig", "inflow", "outflow", "risks", "invariants"}
        for entity in clue["entities"]:
            missing = required - set(entity.keys())
            assert not missing, f"Entity {entity.get('id')} missing required: {missing}"
            # Optional fields must be valid types if present
            for opt in optional:
                if opt in entity:
                    assert isinstance(entity[opt], (str, list)), f"Bad type for {opt}"

    def test_entities_not_empty(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        assert len(clue["entities"]) > 0

    def test_short_ids_sequential(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        ids = [e["id"] for e in clue["entities"]]
        for i, eid in enumerate(ids, 1):
            assert eid == f"n{i}", f"Expected n{i}, got {eid}"


class TestNoCrossReferenceNeeded:
    def test_inflow_outflow_use_short_ids(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        valid_ids = {e["id"] for e in clue["entities"]}
        for entity in clue["entities"]:
            for flow in entity.get("inflow", []):
                assert flow["from"] in valid_ids, f"Inflow ref {flow['from']} not in entities"
            for flow in entity.get("outflow", []):
                assert flow["to"] in valid_ids, f"Outflow ref {flow['to']} not in entities"

    def test_no_raw_node_ids_in_flows(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        for entity in clue["entities"]:
            for flow in entity.get("inflow", []) + entity.get("outflow", []):
                for key in ("from", "to"):
                    if key in flow:
                        assert flow[key].startswith("n"), f"Flow has raw ID: {flow[key]}"


class TestForbiddenFieldsA:
    def test_no_forbidden_fields(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        passed, violations = validate_clue_purity(clue)
        assert passed, f"Forbidden fields leaked: {violations}"

    def test_validate_catches_injected_field(self) -> None:
        bad_clue = {"entities": [{"per_node_confidence": [1, 2, 3]}]}
        passed, violations = validate_clue_purity(bad_clue)
        assert not passed
        assert any("per_node_confidence" in v for v in violations)

    def test_no_internal_underscore_fields(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        raw = json.dumps(clue)
        assert "_raw_from" not in raw
        assert "_raw_to" not in raw


class TestEntityTokenBudget:
    def test_no_entity_exceeds_200_tokens(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        for entity in clue["entities"]:
            tokens = count_tokens(entity)
            assert tokens <= 200, f"Entity {entity['id']} has {tokens} tokens (max 200)"

    def test_total_clue_is_compact(self, tmp_path: Path) -> None:
        graph, proj = _make_graph_and_projection(tmp_path)
        clue = render_clue_plan_a(proj, graph, "Test?", str(tmp_path))
        total = count_tokens(clue)
        # For 5 nodes, should be well under 2000 tokens
        assert total < 2000, f"Total clue is {total} tokens"
