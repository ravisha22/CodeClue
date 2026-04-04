"""Tests for fetch_contract tool — retrieves full semantic contract for a node."""
import pytest
from pathlib import Path

from codeclue_mcp.tools import fetch_contract
from codeclue_research.io import load_graph


@pytest.fixture
def flask_graph():
    p = Path("experiments/runs/v2-lane-a-flask/graph.json")
    if not p.exists():
        pytest.skip("Flask v2 graph not available")
    return load_graph(p)


class TestFetchContract:
    def test_returns_full_contract(self, flask_graph):
        """fetch_contract returns the complete semantic_contract dict."""
        node_id = flask_graph.nodes[0].node_id
        result = fetch_contract(graph=flask_graph, node_id=node_id)
        assert result["status"] == "ok"
        assert "semantic_contract" in result
        assert isinstance(result["semantic_contract"], dict)

    def test_tier1_fields_present(self, flask_graph):
        """Tier 1 required fields are present in returned contract."""
        node_id = flask_graph.nodes[0].node_id
        result = fetch_contract(graph=flask_graph, node_id=node_id)
        contract = result["semantic_contract"]
        assert "purpose" in contract
        assert "language" in contract
        assert "symbol_name" in contract
        assert "symbol_type" in contract
        assert "tier" in contract

    def test_tier2_fields_when_present(self, flask_graph):
        """If a Tier 2 node exists, its contract includes behavioral fields."""
        tier2_nodes = [n for n in flask_graph.nodes if n.semantic_contract.get("tier") == 2]
        if not tier2_nodes:
            pytest.skip("No Tier 2 nodes in graph")
        result = fetch_contract(graph=flask_graph, node_id=tier2_nodes[0].node_id)
        contract = result["semantic_contract"]
        # Tier 2 function nodes should have these
        if contract.get("symbol_type") in ("function", "method", "async_function"):
            assert "preconditions" in contract
            assert "postconditions" in contract

    def test_complexity_indicators_included(self, flask_graph):
        """complexity_indicators are included in the contract."""
        node_id = flask_graph.nodes[0].node_id
        result = fetch_contract(graph=flask_graph, node_id=node_id)
        assert "complexity_indicators" in result["semantic_contract"]

    def test_unknown_node_returns_error(self, flask_graph):
        """Unknown node_id returns error."""
        result = fetch_contract(graph=flask_graph, node_id="nonexistent:node")
        assert result["status"] == "error"
