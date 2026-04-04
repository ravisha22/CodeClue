"""Tests for MCP protocol handshake and tool discovery."""
import pytest

# This test requires the mcp SDK — will be installed in GREEN phase.
# For RED phase, this import will fail, confirming the tests are real.
from codeclue_mcp.server import create_server


class TestMCPProtocol:
    def test_server_creates(self):
        """MCP server instance can be created."""
        server = create_server(
            graph_path="experiments/runs/v2-lane-a-flask/graph.json",
            repo_root="experiments/external-repos/flask",
        )
        assert server is not None

    def test_server_lists_five_tools(self):
        """Server exposes exactly 5 tools."""
        server = create_server(
            graph_path="experiments/runs/v2-lane-a-flask/graph.json",
            repo_root="experiments/external-repos/flask",
        )
        tools = server.list_tools()
        tool_names = {t["name"] for t in tools}
        assert tool_names == {"code_slice", "resolve_dependency", "check_freshness",
                              "expand_projection", "fetch_contract"}

    def test_tool_schemas_have_required_fields(self):
        """Each tool has input_schema with required parameters."""
        server = create_server(
            graph_path="experiments/runs/v2-lane-a-flask/graph.json",
            repo_root="experiments/external-repos/flask",
        )
        tools = server.list_tools()
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "input_schema" in tool
            assert "properties" in tool["input_schema"]

    def test_code_slice_schema(self):
        """code_slice tool has file_path, start_line, end_line parameters."""
        server = create_server(
            graph_path="experiments/runs/v2-lane-a-flask/graph.json",
            repo_root="experiments/external-repos/flask",
        )
        tools = {t["name"]: t for t in server.list_tools()}
        cs = tools["code_slice"]
        props = cs["input_schema"]["properties"]
        assert "file_path" in props
        assert "start_line" in props
        assert "end_line" in props

    def test_resolve_dependency_schema(self):
        """resolve_dependency tool has node_id and depth parameters."""
        server = create_server(
            graph_path="experiments/runs/v2-lane-a-flask/graph.json",
            repo_root="experiments/external-repos/flask",
        )
        tools = {t["name"]: t for t in server.list_tools()}
        rd = tools["resolve_dependency"]
        props = rd["input_schema"]["properties"]
        assert "node_id" in props
        assert "depth" in props
