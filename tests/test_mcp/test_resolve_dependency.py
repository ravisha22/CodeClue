"""Tests for resolve_dependency tool — BFS expansion from a node."""
import json
import pytest
from pathlib import Path

from codeclue_mcp.tools import resolve_dependency
from codeclue_research.io import load_graph


@pytest.fixture
def flask_graph():
    p = Path("experiments/runs/v2-lane-a-flask/graph.json")
    if not p.exists():
        pytest.skip("Flask v2 graph not available")
    return load_graph(p)


class TestResolveDependency:
    def test_returns_subgraph(self, flask_graph):
        """resolve_dependency returns a subgraph dict with nodes and edges."""
        # Pick a known node from flask
        node_id = flask_graph.nodes[0].node_id
        result = resolve_dependency(graph=flask_graph, node_id=node_id, depth=1)
        assert result["status"] == "ok"
        assert "nodes" in result
        assert "edges" in result
        assert len(result["nodes"]) >= 1  # at least the seed node

    def test_depth_1_includes_neighbors(self, flask_graph):
        """At depth 1, includes direct call targets."""
        # Find a node that has calls edges
        callers = set()
        for e in flask_graph.edges:
            if e.edge_type == "calls":
                callers.add(e.from_node)
        if not callers:
            pytest.skip("No calls edges in graph")

        caller_id = sorted(callers)[0]
        result = resolve_dependency(graph=flask_graph, node_id=caller_id, depth=1)
        assert len(result["nodes"]) > 1

    def test_depth_2_expands_further(self, flask_graph):
        """Depth 2 returns more nodes than depth 1."""
        node_id = flask_graph.nodes[0].node_id
        r1 = resolve_dependency(graph=flask_graph, node_id=node_id, depth=1)
        r2 = resolve_dependency(graph=flask_graph, node_id=node_id, depth=2)
        assert len(r2["nodes"]) >= len(r1["nodes"])

    def test_unknown_node_returns_error(self, flask_graph):
        """Unknown node_id returns error status."""
        result = resolve_dependency(graph=flask_graph, node_id="nonexistent:node", depth=1)
        assert result["status"] == "error"

    def test_returned_nodes_have_ids(self, flask_graph):
        """Each returned node has a node_id field."""
        node_id = flask_graph.nodes[0].node_id
        result = resolve_dependency(graph=flask_graph, node_id=node_id, depth=1)
        for n in result["nodes"]:
            assert "node_id" in n
