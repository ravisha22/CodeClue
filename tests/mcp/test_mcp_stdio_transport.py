"""Protocol-level MCP smoke test over stdio transport."""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import anyio
import pytest

from codeclue_research.io import load_graph


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = WORKSPACE_ROOT / "experiments/runs/v2-lane-a-flask/graph.json"
SOURCE_ROOT = WORKSPACE_ROOT / "experiments/external-repos/flask"
TESTS_ROOT = WORKSPACE_ROOT / "tests"
SITE_PACKAGES = WORKSPACE_ROOT / ".venv/Lib/site-packages"

if str(TESTS_ROOT) in sys.path:
    sys.path.remove(str(TESTS_ROOT))

loaded_mcp = sys.modules.get("mcp")
loaded_mcp_path = str(getattr(loaded_mcp, "__file__", ""))
if loaded_mcp_path.endswith("tests\\mcp\\__init__.py") or loaded_mcp_path.endswith("tests/mcp/__init__.py"):
    del sys.modules["mcp"]

sys.path.insert(0, str(SITE_PACKAGES))
mcp_sdk = importlib.import_module("mcp")

ClientSession = mcp_sdk.ClientSession
StdioServerParameters = mcp_sdk.StdioServerParameters
stdio_client = mcp_sdk.stdio_client


def _pythonpath_for_subprocess() -> str:
    src_path = str(WORKSPACE_ROOT / "src")
    existing = os.environ.get("PYTHONPATH")
    if existing:
        return os.pathsep.join([src_path, existing])
    return src_path


def _sample_source_path() -> str:
    graph = load_graph(GRAPH_PATH)
    for node in graph.nodes:
        if node.source_anchor is not None and node.source_anchor.file_path:
            return node.source_anchor.file_path
    raise AssertionError("No source-anchored nodes found in the sample graph")


@pytest.mark.skipif(not GRAPH_PATH.exists(), reason="Flask v2 graph not available")
def test_stdio_transport_initializes_lists_tools_and_calls_tool() -> None:
    source_path = _sample_source_path()

    async def scenario() -> None:
        server = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "codeclue_mcp",
                "--graph-path",
                str(GRAPH_PATH),
                "--repo-root",
                str(SOURCE_ROOT),
            ],
            cwd=WORKSPACE_ROOT,
            env={"PYTHONPATH": _pythonpath_for_subprocess()},
        )

        async with stdio_client(server) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                initialize_result = await session.initialize()
                assert initialize_result.serverInfo.name == "CodeClue"
                assert initialize_result.capabilities.tools is not None

                tools = await session.list_tools()
                tool_names = {tool.name for tool in tools.tools}
                assert tool_names == {
                    "code_slice",
                    "resolve_dependency",
                    "check_freshness",
                    "expand_projection",
                    "fetch_contract",
                }

                result = await session.call_tool(
                    "code_slice",
                    {
                        "file_path": source_path,
                        "start_line": 1,
                        "end_line": 5,
                    },
                )
                assert result.isError is False
                assert result.structuredContent is not None
                assert result.structuredContent["status"] == "ok"
                assert result.structuredContent["file_path"] == source_path
                assert result.structuredContent["start_line"] == 1
                assert result.structuredContent["end_line"] == 5

    anyio.run(scenario)