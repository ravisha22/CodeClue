from __future__ import annotations

import argparse
import os

from .server import serve_mcp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the CodeClue MCP server over a real MCP transport.",
    )
    parser.add_argument("--graph-path", default=None, help="Path to a pre-built clue graph JSON file (optional)")
    parser.add_argument("--repo-root", default=None, help="Repository root for source access (optional)")
    parser.add_argument("--workspace-root", default=None, help="Workspace root for repo discovery (defaults to cwd)")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "sse", "streamable-http"],
        help="Transport to run the MCP server on",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    workspace_root = args.workspace_root or os.getcwd()
    serve_mcp(
        graph_path=args.graph_path,
        repo_root=args.repo_root,
        transport=args.transport,
        workspace_root=workspace_root,
    )
