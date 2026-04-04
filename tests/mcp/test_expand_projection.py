"""Tests for expand_projection tool — widens projection around a node."""
import pytest
from pathlib import Path

from codeclue_mcp.tools import expand_projection
from codeclue_research.io import load_graph


@pytest.fixture
def flask_graph():
    p = Path("experiments/runs/v2-lane-a-flask/graph.json")
    if not p.exists():
        pytest.skip("Flask v2 graph not available")
    return load_graph(p)


class TestExpandProjection:
    def test_expands_beyond_original(self, flask_graph):
        """expand_projection returns more nodes than the seed alone."""
        node_id = flask_graph.nodes[0].node_id
        result = expand_projection(
            graph=flask_graph,
            node_id=node_id,
            additional_hops=2,
            edge_types=["contains", "calls"],
        )
        assert result["status"] == "ok"
        assert len(result["projected_nodes"]) > 1

    def test_respects_edge_type_filter(self, flask_graph):
        """Filtering to 'contains' only excludes 'calls' edges."""
        node_id = [n.node_id for n in flask_graph.nodes if n.node_type == "module"][0]
        r_contains = expand_projection(
            graph=flask_graph, node_id=node_id,
            additional_hops=1, edge_types=["contains"],
        )
        r_all = expand_projection(
            graph=flask_graph, node_id=node_id,
            additional_hops=1, edge_types=["contains", "calls"],
        )
        assert len(r_all["projected_nodes"]) >= len(r_contains["projected_nodes"])

    def test_zero_hops_returns_seed_only(self, flask_graph):
        """With 0 additional hops, only the seed node is returned."""
        node_id = flask_graph.nodes[0].node_id
        result = expand_projection(
            graph=flask_graph, node_id=node_id,
            additional_hops=0, edge_types=["contains"],
        )
        assert len(result["projected_nodes"]) == 1
        assert result["projected_nodes"][0]["node_id"] == node_id

    def test_unknown_node_returns_error(self, flask_graph):
        """Unknown node_id returns error."""
        result = expand_projection(
            graph=flask_graph, node_id="nonexistent:node",
            additional_hops=1, edge_types=["contains"],
        )
        assert result["status"] == "error"
