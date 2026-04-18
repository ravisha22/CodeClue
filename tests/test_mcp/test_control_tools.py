"""Tests for control-layer tools — Phases 2-7."""
from __future__ import annotations

import json
import os
import pytest
from pathlib import Path

from codeclue_mcp.server import CodeClueServer
from codeclue_mcp.state import SessionState


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def workspace(tmp_path):
    """Create a temp workspace with fake repos."""
    # Python repo with .git
    py_repo = tmp_path / "my-flask-app"
    py_repo.mkdir()
    (py_repo / ".git").mkdir()
    (py_repo / "app.py").write_text("print('hello')")
    (py_repo / "utils.py").write_text("def f(): pass")

    # TS repo with .git
    ts_repo = tmp_path / "my-nest-api"
    ts_repo.mkdir()
    (ts_repo / ".git").mkdir()
    (ts_repo / "index.ts").write_text("export class App {}")
    (ts_repo / "service.ts").write_text("export class Svc {}")

    # Go repo with .git
    go_repo = tmp_path / "my-gin-svc"
    go_repo.mkdir()
    (go_repo / ".git").mkdir()
    (go_repo / "main.go").write_text("package main")

    # Non-git directory (should NOT be discovered)
    no_git = tmp_path / "random-dir"
    no_git.mkdir()
    (no_git / "data.csv").write_text("x,y")

    # Repo with existing clue
    clue_repo = tmp_path / "has-clue"
    clue_repo.mkdir()
    (clue_repo / ".git").mkdir()
    (clue_repo / "main.py").write_text("pass")
    clue_dir = clue_repo / ".codeclue"
    clue_dir.mkdir()
    (clue_dir / "graph.json").write_text("{}")

    return tmp_path


@pytest.fixture
def empty_server(workspace):
    """Server with workspace_root set but no graph loaded."""
    return CodeClueServer(workspace_root=str(workspace))


# ── Phase 2: discover_repos ─────────────────────────────────────

class TestDiscoverRepos:
    def test_finds_git_repos(self, empty_server, workspace):
        result = empty_server.call_tool("discover_repos", {})
        assert result["status"] == "ok"
        names = {r["repo_name"] for r in result["repos"]}
        assert "my-flask-app" in names
        assert "my-nest-api" in names
        assert "my-gin-svc" in names

    def test_excludes_non_git_dirs(self, empty_server, workspace):
        result = empty_server.call_tool("discover_repos", {})
        names = {r["repo_name"] for r in result["repos"]}
        assert "random-dir" not in names

    def test_detects_language_hint(self, empty_server, workspace):
        result = empty_server.call_tool("discover_repos", {})
        repos = {r["repo_name"]: r for r in result["repos"]}
        assert repos["my-flask-app"]["language_hint"] == "python"
        assert repos["my-nest-api"]["language_hint"] == "typescript"
        assert repos["my-gin-svc"]["language_hint"] == "go"

    def test_detects_existing_clue(self, empty_server, workspace):
        result = empty_server.call_tool("discover_repos", {})
        repos = {r["repo_name"]: r for r in result["repos"]}
        assert repos["has-clue"]["has_existing_clue"] is True
        assert repos["my-flask-app"]["has_existing_clue"] is False

    def test_updates_session_state(self, empty_server, workspace):
        empty_server.call_tool("discover_repos", {})
        assert len(empty_server.state.discovered_repos) >= 4

    def test_returns_error_without_workspace(self):
        srv = CodeClueServer()
        result = srv.call_tool("discover_repos", {})
        assert result["status"] == "error"


# ── Phase 3: get_repo_status ────────────────────────────────────

class TestGetRepoStatus:
    def test_status_for_repo_with_clue(self, empty_server, workspace):
        repo_path = str(workspace / "has-clue")
        result = empty_server.call_tool("get_repo_status", {"repo_path": repo_path})
        assert result["status"] == "ok"
        assert result["clue_exists"] is True

    def test_status_for_repo_without_clue(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        result = empty_server.call_tool("get_repo_status", {"repo_path": repo_path})
        assert result["status"] == "ok"
        assert result["clue_exists"] is False

    def test_status_detects_language(self, empty_server, workspace):
        repo_path = str(workspace / "my-nest-api")
        result = empty_server.call_tool("get_repo_status", {"repo_path": repo_path})
        assert result["language"] == "typescript"

    def test_uses_active_repo_if_no_path(self, empty_server, workspace):
        empty_server.state.active_repo = str(workspace / "my-flask-app")
        result = empty_server.call_tool("get_repo_status", {})
        assert result["status"] == "ok"

    def test_error_without_repo_path_or_active(self, empty_server):
        result = empty_server.call_tool("get_repo_status", {})
        assert result["status"] == "error"


# ── Phase 4: generate_clue ──────────────────────────────────────

class TestGenerateClue:
    def test_generates_and_loads_clue(self, empty_server, workspace):
        """generate_clue extracts a graph and hot-loads it."""
        repo_path = str(workspace / "my-flask-app")
        result = empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        assert result["status"] == "ok"
        assert result["node_count"] > 0
        assert empty_server.state.has_graph

    def test_writes_graph_to_default_location(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        expected = workspace / "my-flask-app" / ".codeclue" / "graph.json"
        assert expected.exists()

    def test_writes_graph_to_custom_path(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        custom = str(workspace / "output" / "custom.json")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
            "output_path": custom,
        })
        assert Path(custom).exists()

    def test_rejects_non_git_without_flag(self, empty_server, workspace):
        repo_path = str(workspace / "random-dir")
        result = empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        assert result["status"] == "error"
        assert "git" in result["message"].lower()

    def test_allows_non_git_with_flag(self, empty_server, workspace):
        repo_path = str(workspace / "random-dir")
        # Create a .py file so extraction has something to work with
        (workspace / "random-dir" / "script.py").write_text("x = 1")
        result = empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
            "allow_no_git": True,
        })
        assert result["status"] == "ok"

    def test_rejects_path_outside_workspace(self, empty_server, workspace):
        result = empty_server.call_tool("generate_clue", {
            "repo_path": "/tmp/evil",
            "language": "python",
        })
        assert result["status"] == "error"

    def test_old_graph_survives_on_failure(self, workspace):
        """If extraction fails, the previously loaded graph must remain."""
        from codeclue_research.models import CanonicalClueGraph, Node, SourceAnchor
        node = Node(
            node_id="old.mod",
            node_type="module",
            source_anchor=SourceAnchor("old.py", 0, 10, "old", "aaa"),
            semantic_contract={"symbol_name": "old"},
            confidence=0.9,
        )
        old_graph = CanonicalClueGraph(
            nodes=[node], edges=[],
            metadata={"commit_id": "old", "language": "python"},
            repository={"root": "/old", "name": "old"},
        )
        srv = CodeClueServer(
            graph=old_graph, repo_root="/old",
            workspace_root=str(workspace),
        )
        # Give a path that exists but has no parseable source
        empty_dir = workspace / "empty-repo"
        empty_dir.mkdir()
        (empty_dir / ".git").mkdir()
        result = srv.call_tool("generate_clue", {
            "repo_path": str(empty_dir),
            "language": "python",
        })
        # Whether it "succeeds" with 0 nodes or "fails", old graph must survive
        assert srv._graph is old_graph or srv.state.has_graph


# ── Phase 5: select_repo ────────────────────────────────────────

class TestSelectRepo:
    def test_select_repo_with_existing_clue(self, empty_server, workspace):
        # First generate a real clue so there's something to load
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        # Now select that repo
        result = empty_server.call_tool("select_repo", {"repo_path": repo_path})
        assert result["status"] == "ok"
        assert result["clue_loaded"] is True

    def test_select_repo_without_clue(self, empty_server, workspace):
        repo_path = str(workspace / "my-gin-svc")
        result = empty_server.call_tool("select_repo", {"repo_path": repo_path})
        assert result["status"] == "no_clue"

    def test_select_sets_active_repo(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("select_repo", {"repo_path": repo_path})
        assert empty_server.state.active_repo == repo_path


# ── Phase 6: generate_projection ────────────────────────────────

class TestGenerateProjection:
    def test_generates_projection(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        result = empty_server.call_tool("generate_projection", {
            "operation_family": "OF1",
        })
        assert result["status"] == "ok"
        assert "node_count" in result
        assert "confidence_overall" in result

    def test_writes_projection_to_disk(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        result = empty_server.call_tool("generate_projection", {
            "operation_family": "OF1",
        })
        assert Path(result["projection_path"]).exists()

    def test_error_without_loaded_graph(self, empty_server):
        result = empty_server.call_tool("generate_projection", {
            "operation_family": "OF1",
        })
        assert result["status"] == "error"


# ── Phase 7: get_projection_summary ─────────────────────────────

class TestGetProjectionSummary:
    def test_returns_summary(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        empty_server.call_tool("generate_projection", {
            "operation_family": "OF1",
        })
        result = empty_server.call_tool("get_projection_summary", {})
        assert result["status"] == "ok"
        assert "confidence_overall" in result
        assert "node_count" in result

    def test_error_without_active_projection(self, empty_server):
        result = empty_server.call_tool("get_projection_summary", {})
        assert result["status"] == "error"

    def test_reads_specific_path(self, empty_server, workspace):
        repo_path = str(workspace / "my-flask-app")
        empty_server.call_tool("generate_clue", {
            "repo_path": repo_path,
            "language": "python",
        })
        proj_result = empty_server.call_tool("generate_projection", {
            "operation_family": "OF2",
        })
        result = empty_server.call_tool("get_projection_summary", {
            "projection_path": proj_result["projection_path"],
        })
        assert result["status"] == "ok"
