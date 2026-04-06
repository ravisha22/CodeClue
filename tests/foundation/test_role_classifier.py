"""Tests for role_classifier module."""

from __future__ import annotations

from codeclue_research.models import (
    CanonicalClueGraph,
    Edge,
    Node,
    SourceAnchor,
)
from codeclue_research.role_classifier import (
    ROLE_DISPATCHER,
    ROLE_ENTRYPOINT,
    ROLE_ERROR_HANDLER,
    ROLE_HANDLER,
    ROLE_MODULE,
    ROLE_UTILITY,
    ROLE_VALIDATOR,
    classify_projected_nodes,
)


def _anchor(path: str = "mod.py") -> SourceAnchor:
    return SourceAnchor(file_path=path, byte_start=0, byte_end=100, ast_path="", content_hash="abc")


def _node(nid: str, ntype: str = "function", name: str = "") -> Node:
    return Node(
        node_id=nid,
        node_type=ntype,
        source_anchor=_anchor(),
        semantic_contract={"symbol_name": name or nid},
        confidence=0.9,
    )


def _edge(etype: str, from_n: str, to_n: str) -> Edge:
    return Edge(edge_id=f"{etype}:{from_n}:{to_n}", edge_type=etype, from_node=from_n, to_node=to_n, evidence={})


class TestEntrypointDetection:
    def test_no_callers_with_callees(self) -> None:
        """Node with fan_in=0 and fan_out>0 → entrypoint."""
        graph = CanonicalClueGraph(
            metadata={}, repository={},
            nodes=[_node("entry"), _node("a"), _node("b")],
            edges=[_edge("calls", "entry", "a"), _edge("calls", "entry", "b")],
        )
        roles = classify_projected_nodes(graph, ["entry", "a", "b"])
        assert roles["entry"] == ROLE_ENTRYPOINT


class TestDispatcherDetection:
    def test_high_fan_out(self) -> None:
        """Node with fan_out >= 3 → dispatcher."""
        nodes = [_node("d"), _node("a"), _node("b"), _node("c"), _node("caller")]
        edges = [
            _edge("calls", "caller", "d"),
            _edge("calls", "d", "a"),
            _edge("calls", "d", "b"),
            _edge("calls", "d", "c"),
        ]
        graph = CanonicalClueGraph(metadata={}, repository={}, nodes=nodes, edges=edges)
        roles = classify_projected_nodes(graph, ["d", "a", "b", "c", "caller"])
        assert roles["d"] == ROLE_DISPATCHER


class TestHandlerDetection:
    def test_leaf_with_callers(self) -> None:
        """Node with fan_in>0 and fan_out=0 → handler."""
        graph = CanonicalClueGraph(
            metadata={}, repository={},
            nodes=[_node("caller"), _node("leaf")],
            edges=[_edge("calls", "caller", "leaf")],
        )
        roles = classify_projected_nodes(graph, ["caller", "leaf"])
        assert roles["leaf"] == ROLE_HANDLER


class TestErrorHandlerDetection:
    def test_by_name(self) -> None:
        """Node with exception-related name → error_handler."""
        graph = CanonicalClueGraph(
            metadata={}, repository={},
            nodes=[_node("handle_exception", name="handle_exception"), _node("caller")],
            edges=[_edge("calls", "caller", "handle_exception")],
        )
        roles = classify_projected_nodes(graph, ["handle_exception", "caller"])
        assert roles["handle_exception"] == ROLE_ERROR_HANDLER


class TestValidatorDetection:
    def test_by_security_markers(self) -> None:
        """Node with auth marker → validator."""
        graph = CanonicalClueGraph(
            metadata={}, repository={},
            nodes=[_node("check_auth", name="check_auth"), _node("caller")],
            edges=[_edge("calls", "caller", "check_auth")],
        )
        patterns = {"check_auth": {"risks": [], "security_markers": ["has_auth_decorator"], "sig": "", "patterns": ["has_auth_decorator"]}}
        roles = classify_projected_nodes(graph, ["check_auth", "caller"], source_patterns=patterns)
        assert roles["check_auth"] == ROLE_VALIDATOR


class TestModuleRoot:
    def test_module_type(self) -> None:
        """Module node → module_root."""
        graph = CanonicalClueGraph(
            metadata={}, repository={},
            nodes=[_node("mod", ntype="module"), _node("func")],
            edges=[_edge("contains", "mod", "func")],
        )
        roles = classify_projected_nodes(graph, ["mod", "func"])
        assert roles["mod"] == ROLE_MODULE


class TestUtilityFallback:
    def test_default_role(self) -> None:
        """Node that doesn't match any pattern → utility."""
        graph = CanonicalClueGraph(
            metadata={}, repository={},
            nodes=[_node("helper"), _node("a"), _node("b")],
            edges=[_edge("calls", "a", "helper"), _edge("calls", "helper", "b")],
        )
        roles = classify_projected_nodes(graph, ["helper", "a", "b"])
        # helper has fi=1, fo=1 → middleware or utility
        assert roles["helper"] in ("middleware", "utility")
