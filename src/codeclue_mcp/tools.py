"""Five typed drill-down tools for the CodeClue MCP server."""
from __future__ import annotations

import hashlib
from collections import deque
from pathlib import Path
from typing import Any

from codeclue_research.models import CanonicalClueGraph


def _safe_resolve(repo_root: str, file_path: str) -> Path | None:
    """Resolve file_path within repo_root, rejecting path traversal."""
    root = Path(repo_root).resolve()
    target = (root / file_path).resolve()
    if not str(target).startswith(str(root)):
        return None
    if not target.exists():
        return None
    return target


def code_slice(
    repo_root: str,
    file_path: str,
    start_line: int,
    end_line: int,
) -> dict[str, Any]:
    """Fetch raw source lines for a specific file range."""
    target = _safe_resolve(repo_root, file_path)
    if target is None:
        return {"status": "error", "message": f"File not found or path traversal: {file_path}"}

    try:
        all_lines = target.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    start = max(1, start_line)
    end = min(len(all_lines), end_line)

    lines = []
    for i in range(start, end + 1):
        lines.append({"line_number": i, "content": all_lines[i - 1]})

    return {
        "status": "ok",
        "file_path": file_path,
        "start_line": start,
        "end_line": end,
        "total_lines_in_file": len(all_lines),
        "lines": lines,
    }


def resolve_dependency(
    graph: CanonicalClueGraph,
    node_id: str,
    depth: int = 2,
) -> dict[str, Any]:
    """BFS from node_id to expand dependency subgraph."""
    node_map = {n.node_id: n for n in graph.nodes}
    if node_id not in node_map:
        return {"status": "error", "message": f"Unknown node: {node_id}"}

    adjacency: dict[str, list[tuple[str, str]]] = {n.node_id: [] for n in graph.nodes}
    reverse: dict[str, list[tuple[str, str]]] = {n.node_id: [] for n in graph.nodes}
    for e in graph.edges:
        adjacency.setdefault(e.from_node, []).append((e.to_node, e.edge_id))
        reverse.setdefault(e.to_node, []).append((e.from_node, e.edge_id))

    visited: set[str] = set()
    collected_edges: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(node_id, 0)])

    while queue:
        nid, d = queue.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        if d >= depth:
            continue
        for neighbor, eid in adjacency.get(nid, []):
            collected_edges.add(eid)
            if neighbor not in visited:
                queue.append((neighbor, d + 1))
        for neighbor, eid in reverse.get(nid, []):
            collected_edges.add(eid)
            if neighbor not in visited:
                queue.append((neighbor, d + 1))

    edge_map = {e.edge_id: e for e in graph.edges}
    return {
        "status": "ok",
        "seed_node": node_id,
        "depth": depth,
        "nodes": [node_map[nid].to_dict() for nid in sorted(visited) if nid in node_map],
        "edges": [edge_map[eid].to_dict() for eid in sorted(collected_edges) if eid in edge_map],
    }


def check_freshness(
    graph: CanonicalClueGraph,
    repo_root: str,
    module_id: str,
    override_hash: str | None = None,
) -> dict[str, Any]:
    """Check if a module's clue is stale relative to source."""
    node_map = {n.node_id: n for n in graph.nodes}
    node = node_map.get(module_id)
    if node is None:
        return {"status": "error", "message": f"Unknown module: {module_id}"}

    anchor = node.source_anchor
    target = _safe_resolve(repo_root, anchor.file_path)

    if target is None:
        return {
            "status": "ok",
            "module_id": module_id,
            "stale": True,
            "change_summary": f"Source file not found: {anchor.file_path}",
        }

    current_hash = override_hash
    if current_hash is None:
        content = target.read_text(encoding="utf-8")
        current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    stale = current_hash != anchor.content_hash

    return {
        "status": "ok",
        "module_id": module_id,
        "file_path": anchor.file_path,
        "stale": stale,
        "clue_hash": anchor.content_hash,
        "current_hash": current_hash,
        "change_summary": "File content changed since clue generation" if stale else "File unchanged",
    }


def expand_projection(
    graph: CanonicalClueGraph,
    node_id: str,
    additional_hops: int = 1,
    edge_types: list[str] | None = None,
) -> dict[str, Any]:
    """Widen the projected subgraph around a seed node."""
    node_map = {n.node_id: n for n in graph.nodes}
    if node_id not in node_map:
        return {"status": "error", "message": f"Unknown node: {node_id}"}

    allowed_types = set(edge_types) if edge_types else {"contains", "calls"}

    visited: set[str] = set()
    collected_edges: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(node_id, 0)])

    while queue:
        nid, d = queue.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        if d >= additional_hops:
            continue
        for e in graph.edges:
            if e.edge_type not in allowed_types:
                continue
            if e.from_node == nid:
                collected_edges.add(e.edge_id)
                if e.to_node not in visited:
                    queue.append((e.to_node, d + 1))
            if e.to_node == nid:
                collected_edges.add(e.edge_id)
                if e.from_node not in visited:
                    queue.append((e.from_node, d + 1))

    edge_map = {e.edge_id: e for e in graph.edges}
    return {
        "status": "ok",
        "seed_node": node_id,
        "additional_hops": additional_hops,
        "edge_types": list(allowed_types),
        "projected_nodes": [node_map[nid].to_dict() for nid in sorted(visited) if nid in node_map],
        "projected_edges": [edge_map[eid].to_dict() for eid in sorted(collected_edges) if eid in edge_map],
    }


def fetch_contract(
    graph: CanonicalClueGraph,
    node_id: str,
) -> dict[str, Any]:
    """Retrieve the full semantic contract for a specific node."""
    node_map = {n.node_id: n for n in graph.nodes}
    node = node_map.get(node_id)
    if node is None:
        return {"status": "error", "message": f"Unknown node: {node_id}"}

    return {
        "status": "ok",
        "node_id": node_id,
        "node_type": node.node_type,
        "source_anchor": node.source_anchor.to_dict(),
        "semantic_contract": node.semantic_contract,
        "confidence": node.confidence,
    }
