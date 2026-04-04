"""Tests for check_freshness tool — detects stale clue modules."""
import json
import pytest
import tempfile
import shutil
from pathlib import Path

from codeclue_mcp.tools import check_freshness
from codeclue_research.io import load_graph


@pytest.fixture
def flask_graph():
    p = Path("experiments/runs/v2-lane-a-flask/graph.json")
    if not p.exists():
        pytest.skip("Flask v2 graph not available")
    return load_graph(p)


@pytest.fixture
def flask_repo():
    p = Path("experiments/external-repos/flask")
    if not p.exists():
        pytest.skip("Flask repo not cloned")
    return p


class TestCheckFreshness:
    def test_unmodified_module_is_fresh(self, flask_graph, flask_repo):
        """A module whose source hasn't changed since extraction is fresh."""
        module_id = [n.node_id for n in flask_graph.nodes if n.node_type == "module"][0]
        result = check_freshness(
            graph=flask_graph,
            repo_root=str(flask_repo),
            module_id=module_id,
        )
        assert result["status"] == "ok"
        assert result["stale"] is False

    def test_modified_module_is_stale(self, flask_graph, flask_repo, tmp_path):
        """A module detected as stale when source file content hash differs."""
        # Copy flask to temp, modify a file
        temp_repo = tmp_path / "flask_copy"
        # We won't actually copy the whole repo — just test the hash comparison logic
        module_node = [n for n in flask_graph.nodes if n.node_type == "module"][0]
        result = check_freshness(
            graph=flask_graph,
            repo_root=str(flask_repo),
            module_id=module_node.node_id,
            override_hash="fake_hash_that_wont_match",
        )
        assert result["status"] == "ok"
        assert result["stale"] is True

    def test_unknown_module_returns_error(self, flask_graph, flask_repo):
        """Unknown module_id returns error."""
        result = check_freshness(
            graph=flask_graph,
            repo_root=str(flask_repo),
            module_id="module:nonexistent.py",
        )
        assert result["status"] == "error"

    def test_returns_change_summary(self, flask_graph, flask_repo):
        """Result includes a change_summary field."""
        module_id = [n.node_id for n in flask_graph.nodes if n.node_type == "module"][0]
        result = check_freshness(
            graph=flask_graph,
            repo_root=str(flask_repo),
            module_id=module_id,
        )
        assert "change_summary" in result
