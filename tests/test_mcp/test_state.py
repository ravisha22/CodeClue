"""Tests for SessionState and mutable server core — Phase 1."""
from __future__ import annotations

import pytest
from dataclasses import fields

from codeclue_mcp.state import SessionState, RepoInfo


class TestRepoInfo:
    def test_create_basic(self):
        info = RepoInfo(repo_name="flask", repo_path="/repos/flask", language_hint="python")
        assert info.repo_name == "flask"
        assert info.repo_path == "/repos/flask"
        assert info.language_hint == "python"
        assert info.has_existing_clue is False

    def test_with_existing_clue(self):
        info = RepoInfo(
            repo_name="django",
            repo_path="/repos/django",
            language_hint="python",
            has_existing_clue=True,
        )
        assert info.has_existing_clue is True


class TestSessionState:
    def test_default_empty(self):
        state = SessionState()
        assert state.workspace_root is None
        assert state.discovered_repos == []
        assert state.active_repo is None
        assert state.active_clue_path is None
        assert state.active_graph is None
        assert state.active_projection_path is None

    def test_with_workspace_root(self):
        state = SessionState(workspace_root="/workspace")
        assert state.workspace_root == "/workspace"

    def test_has_graph_false_when_empty(self):
        state = SessionState()
        assert state.has_graph is False

    def test_has_graph_true_when_loaded(self, tiny_graph):
        state = SessionState(active_graph=tiny_graph)
        assert state.has_graph is True


class TestServerSwapGraph:
    """Tests for CodeClueServer.swap_graph hot-loading."""

    def test_swap_replaces_graph(self, tiny_graph, tiny_graph_alt):
        from codeclue_mcp.server import CodeClueServer
        srv = CodeClueServer(graph=tiny_graph, repo_root="/old")
        srv.swap_graph(graph=tiny_graph_alt, repo_root="/new", graph_path="/new/graph.json")
        assert srv._graph is tiny_graph_alt
        assert srv._repo_root == "/new"
        assert srv._graph_path == "/new/graph.json"

    def test_swap_graph_old_remains_on_none(self, tiny_graph):
        """swap_graph rejects None graph (no half-swapped state)."""
        from codeclue_mcp.server import CodeClueServer
        srv = CodeClueServer(graph=tiny_graph, repo_root="/old")
        with pytest.raises((TypeError, ValueError)):
            srv.swap_graph(graph=None, repo_root="/new", graph_path="/new/graph.json")
        # Old graph must remain
        assert srv._graph is tiny_graph
        assert srv._repo_root == "/old"

    def test_tools_use_swapped_graph(self, tiny_graph, tiny_graph_alt):
        """After swap, drill-down tools operate on the new graph."""
        from codeclue_mcp.server import CodeClueServer
        srv = CodeClueServer(graph=tiny_graph, repo_root="/old")
        srv.swap_graph(graph=tiny_graph_alt, repo_root="/new", graph_path="/new/graph.json")
        result = srv.call_tool("fetch_contract", {"node_id": "alt.module"})
        assert result["status"] == "ok"
        assert result["node_id"] == "alt.module"


class TestServerEmptyState:
    """Tests for server starting without a graph loaded."""

    def test_empty_server_creation(self):
        from codeclue_mcp.server import CodeClueServer
        srv = CodeClueServer()
        assert srv._graph is None

    def test_drill_down_returns_error_when_empty(self):
        from codeclue_mcp.server import CodeClueServer
        srv = CodeClueServer()
        for tool_name in ["resolve_dependency", "check_freshness", "expand_projection", "fetch_contract"]:
            result = srv.call_tool(tool_name, {"node_id": "foo"})
            assert result["status"] == "error"
            assert "no clue loaded" in result["message"].lower() or "generate_clue" in result["message"].lower()

    def test_code_slice_returns_error_when_empty(self):
        from codeclue_mcp.server import CodeClueServer
        srv = CodeClueServer()
        result = srv.call_tool("code_slice", {"file_path": "x.py", "start_line": 1, "end_line": 5})
        assert result["status"] == "error"


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def tiny_graph():
    """Minimal CanonicalClueGraph with one node."""
    from codeclue_research.models import CanonicalClueGraph, Node, Edge, SourceAnchor
    node = Node(
        node_id="test.module",
        node_type="module",
        source_anchor=SourceAnchor(
            file_path="test.py",
            byte_start=0,
            byte_end=100,
            ast_path="test",
            content_hash="abc123",
        ),
        semantic_contract={"symbol_name": "test.module", "purpose": "test"},
        confidence=0.9,
    )
    return CanonicalClueGraph(
        nodes=[node],
        edges=[],
        metadata={"commit_id": "abc123", "language": "python"},
        repository={"root": "/test", "name": "test"},
    )


@pytest.fixture
def tiny_graph_alt():
    """A different minimal graph for swap testing."""
    from codeclue_research.models import CanonicalClueGraph, Node, SourceAnchor
    node = Node(
        node_id="alt.module",
        node_type="module",
        source_anchor=SourceAnchor(
            file_path="alt.py",
            byte_start=0,
            byte_end=50,
            ast_path="alt",
            content_hash="def456",
        ),
        semantic_contract={"symbol_name": "alt.module", "purpose": "alt test"},
        confidence=0.8,
    )
    return CanonicalClueGraph(
        nodes=[node],
        edges=[],
        metadata={"commit_id": "def456", "language": "python"},
        repository={"root": "/alt", "name": "alt"},
    )
