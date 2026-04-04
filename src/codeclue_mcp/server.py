"""CodeClue MCP Server — exposes 5 drill-down tools via MCP protocol."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from codeclue_research.io import load_graph
from codeclue_research.models import CanonicalClueGraph

from .tools import code_slice, resolve_dependency, check_freshness, expand_projection, fetch_contract


_TOOL_DEFINITIONS = [
    {
        "name": "code_slice",
        "description": "Fetch raw source lines for a specific file range. Use when clue confidence is low and you need to verify source detail.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Relative path to source file within the repository"},
                "start_line": {"type": "integer", "description": "First line to fetch (1-based)"},
                "end_line": {"type": "integer", "description": "Last line to fetch (1-based, inclusive)"},
            },
            "required": ["file_path", "start_line", "end_line"],
        },
    },
    {
        "name": "resolve_dependency",
        "description": "Expand a compressed edge to its full dependency subgraph via BFS from a node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "The node_id to expand from"},
                "depth": {"type": "integer", "description": "BFS depth (default 2)", "default": 2},
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "check_freshness",
        "description": "Verify whether a clue module is stale relative to the current source.",
        "input_schema": {
            "type": "object",
            "properties": {
                "module_id": {"type": "string", "description": "The module node_id to check"},
            },
            "required": ["module_id"],
        },
    },
    {
        "name": "expand_projection",
        "description": "Widen the projected subgraph around a seed node by additional hops.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "The seed node_id"},
                "additional_hops": {"type": "integer", "description": "Number of additional BFS hops", "default": 1},
                "edge_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Edge types to follow (default: contains, calls)",
                },
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "fetch_contract",
        "description": "Retrieve the full semantic contract for a specific node, including complexity indicators.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "The node_id to fetch the contract for"},
            },
            "required": ["node_id"],
        },
    },
]


class CodeClueServer:
    """Lightweight MCP-compatible server wrapping the 5 CodeClue tools."""

    def __init__(self, graph: CanonicalClueGraph, repo_root: str) -> None:
        self._graph = graph
        self._repo_root = repo_root

    def list_tools(self) -> list[dict[str, Any]]:
        return list(_TOOL_DEFINITIONS)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "code_slice":
            return code_slice(
                repo_root=self._repo_root,
                file_path=arguments["file_path"],
                start_line=arguments["start_line"],
                end_line=arguments["end_line"],
            )
        elif name == "resolve_dependency":
            return resolve_dependency(
                graph=self._graph,
                node_id=arguments["node_id"],
                depth=arguments.get("depth", 2),
            )
        elif name == "check_freshness":
            return check_freshness(
                graph=self._graph,
                repo_root=self._repo_root,
                module_id=arguments["module_id"],
            )
        elif name == "expand_projection":
            return expand_projection(
                graph=self._graph,
                node_id=arguments["node_id"],
                additional_hops=arguments.get("additional_hops", 1),
                edge_types=arguments.get("edge_types"),
            )
        elif name == "fetch_contract":
            return fetch_contract(
                graph=self._graph,
                node_id=arguments["node_id"],
            )
        else:
            return {"status": "error", "message": f"Unknown tool: {name}"}


def create_server(graph_path: str, repo_root: str) -> CodeClueServer:
    """Create a CodeClueServer from a graph file path and repo root."""
    graph = load_graph(Path(graph_path))
    return CodeClueServer(graph=graph, repo_root=repo_root)
