"""Typed drill-down tools for the CodeClue MCP server."""
from __future__ import annotations

import hashlib
import json
import re
from collections import deque
from pathlib import Path
from typing import Any

from codeclue_research.clue_view_mrlf import render_mrlf
from codeclue_research.models import CanonicalClueGraph, Node


def load_detail_records(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    detail_path = Path(path)
    if not detail_path.exists():
        return records
    for line in detail_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


def _safe_resolve(repo_root: str, file_path: str) -> Path | None:
    """Resolve file_path within repo_root, rejecting path traversal."""
    root = Path(repo_root).resolve()
    target = (root / file_path).resolve()
    if not str(target).startswith(str(root)):
        return None
    if not target.exists():
        return None
    return target


def _hashes_match(current_hash: str, stored_hash: str) -> bool:
    if not current_hash or not stored_hash:
        return False
    return current_hash.startswith(stored_hash) or stored_hash.startswith(current_hash)


def _with_confidence(
    payload: dict[str, Any],
    confidence: float,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    payload["confidence"] = round(float(confidence), 4)
    if confidence_threshold is not None and confidence < confidence_threshold:
        payload["warning"] = (
            f"confidence {confidence:.2f} below session threshold {confidence_threshold:.2f}"
        )
    return payload


def _detail_index(detail_records: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for record in detail_records or []:
        symbol = str(record.get("symbol", "")).strip()
        node_id = str(record.get("node_id", "")).strip()
        if symbol:
            index[symbol] = record
            index[symbol.lower()] = record
        if node_id:
            index[node_id] = record
    return index


def _node_maps(graph: CanonicalClueGraph | None) -> tuple[dict[str, Node], dict[str, Node]]:
    node_by_id: dict[str, Node] = {}
    node_by_symbol: dict[str, Node] = {}
    if graph is None:
        return node_by_id, node_by_symbol
    for node in graph.nodes:
        node_by_id[node.node_id] = node
        symbol = str((node.semantic_contract or {}).get("symbol_name", "")).strip()
        if symbol:
            node_by_symbol[symbol] = node
            node_by_symbol[symbol.lower()] = node
    return node_by_id, node_by_symbol


def _line_range_from_bytes(file_text: str, byte_start: int, byte_end: int) -> tuple[int, int]:
    start_line = file_text[:byte_start].count("\n") + 1
    end_line = file_text[:byte_end].count("\n") + 1
    return max(1, start_line), max(start_line, end_line)


def _slice_from_lines(file_path: str, all_lines: list[str], start_line: int, end_line: int) -> dict[str, Any]:
    start = max(1, start_line)
    end = min(len(all_lines), end_line)
    lines = [{"line_number": i, "content": all_lines[i - 1]} for i in range(start, end + 1)]
    return {
        "status": "ok",
        "file_path": file_path,
        "start_line": start,
        "end_line": end,
        "total_lines_in_file": len(all_lines),
        "lines": lines,
    }


def code_slice(
    repo_root: str,
    file_path: str | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
    *,
    symbol_name: str | None = None,
    graph: CanonicalClueGraph | None = None,
    detail_records: list[dict[str, Any]] | None = None,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Fetch raw source lines for a specific file range or symbol."""
    if symbol_name:
        indexed_detail = _detail_index(detail_records)
        node_by_id, node_by_symbol = _node_maps(graph)
        detail = indexed_detail.get(symbol_name) or indexed_detail.get(symbol_name.lower())
        node = node_by_symbol.get(symbol_name) or node_by_symbol.get(symbol_name.lower()) or node_by_id.get(symbol_name)
        if detail:
            file_path = str(detail.get("file") or file_path or "")
            line_range = detail.get("lines") or [start_line or 1, end_line or 1]
            if isinstance(line_range, list) and len(line_range) >= 2:
                start_line = int(line_range[0] or 1)
                end_line = int(line_range[1] or start_line or 1)
        elif node:
            file_path = node.source_anchor.file_path
        else:
            return {"status": "error", "message": f"Unknown symbol: {symbol_name}"}

    if not file_path:
        return {"status": "error", "message": "file_path or symbol_name is required"}

    target = _safe_resolve(repo_root, file_path)
    if target is not None:
        try:
            text = target.read_text(encoding="utf-8")
            all_lines = text.splitlines()
        except Exception as exc:  # pragma: no cover - filesystem failure
            return {"status": "error", "message": str(exc)}

        if symbol_name and graph is not None:
            node_by_id, node_by_symbol = _node_maps(graph)
            node = node_by_symbol.get(symbol_name) or node_by_symbol.get(symbol_name.lower()) or node_by_id.get(symbol_name)
            if node and node.source_anchor.file_path == file_path:
                start_line, end_line = _line_range_from_bytes(
                    text,
                    node.source_anchor.byte_start,
                    node.source_anchor.byte_end,
                )

        if start_line is None or end_line is None:
            indexed_detail = _detail_index(detail_records)
            detail = indexed_detail.get(symbol_name) if symbol_name else None
            if detail and isinstance(detail.get("lines"), list) and len(detail["lines"]) >= 2:
                start_line = int(detail["lines"][0] or 1)
                end_line = int(detail["lines"][1] or start_line or 1)
            else:
                start_line = start_line or 1
                end_line = end_line or start_line

        result = _slice_from_lines(file_path, all_lines, start_line, end_line)
        if symbol_name:
            result["symbol_name"] = symbol_name
        return _with_confidence(result, 1.0, confidence_threshold)

    indexed_detail = _detail_index(detail_records)
    detail = indexed_detail.get(symbol_name) if symbol_name else None
    if detail and detail.get("source"):
        snippet_lines = str(detail["source"]).splitlines()
        start = int((detail.get("lines") or [1])[0] or 1)
        result = {
            "status": "ok",
            "file_path": str(detail.get("file", file_path)),
            "start_line": start,
            "end_line": start + max(len(snippet_lines) - 1, 0),
            "total_lines_in_file": max(start + len(snippet_lines) - 1, start),
            "lines": [
                {"line_number": start + idx, "content": line}
                for idx, line in enumerate(snippet_lines)
            ],
            "symbol_name": symbol_name,
            "source": "detail_store",
        }
        return _with_confidence(result, 0.82, confidence_threshold)

    return {"status": "error", "message": f"File not found or path traversal: {file_path}"}


def resolve_dependency(
    graph: CanonicalClueGraph,
    node_id: str,
    depth: int = 2,
    *,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """BFS from node_id to expand dependency subgraph."""
    node_map = {n.node_id: n for n in graph.nodes}
    if node_id not in node_map:
        return {"status": "error", "message": f"Unknown node: {node_id}"}

    adjacency: dict[str, list[tuple[str, str]]] = {n.node_id: [] for n in graph.nodes}
    reverse: dict[str, list[tuple[str, str]]] = {n.node_id: [] for n in graph.nodes}
    for edge in graph.edges:
        adjacency.setdefault(edge.from_node, []).append((edge.to_node, edge.edge_id))
        reverse.setdefault(edge.to_node, []).append((edge.from_node, edge.edge_id))

    visited: set[str] = set()
    collected_edges: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(node_id, 0)])

    while queue:
        nid, current_depth = queue.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        if current_depth >= depth:
            continue
        for neighbor, edge_id in adjacency.get(nid, []):
            collected_edges.add(edge_id)
            if neighbor not in visited:
                queue.append((neighbor, current_depth + 1))
        for neighbor, edge_id in reverse.get(nid, []):
            collected_edges.add(edge_id)
            if neighbor not in visited:
                queue.append((neighbor, current_depth + 1))

    edge_map = {e.edge_id: e for e in graph.edges}
    result = {
        "status": "ok",
        "seed_node": node_id,
        "depth": depth,
        "nodes": [node_map[nid].to_dict() for nid in sorted(visited) if nid in node_map],
        "edges": [edge_map[eid].to_dict() for eid in sorted(collected_edges) if eid in edge_map],
    }
    return _with_confidence(result, node_map[node_id].confidence, confidence_threshold)


def check_freshness(
    graph: CanonicalClueGraph,
    repo_root: str,
    module_id: str,
    override_hash: str | None = None,
    *,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Check if a module's clue is stale relative to source."""
    node_map = {n.node_id: n for n in graph.nodes}
    node = node_map.get(module_id)
    if node is None:
        return {"status": "error", "message": f"Unknown module: {module_id}"}

    anchor = node.source_anchor
    target = _safe_resolve(repo_root, anchor.file_path)
    if target is None:
        return _with_confidence(
            {
                "status": "ok",
                "module_id": module_id,
                "stale": True,
                "change_summary": f"Source file not found: {anchor.file_path}",
            },
            1.0,
            confidence_threshold,
        )

    current_hash = override_hash
    if current_hash is None:
        content = target.read_text(encoding="utf-8")
        current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    stale = not _hashes_match(current_hash, anchor.content_hash)
    result = {
        "status": "ok",
        "module_id": module_id,
        "file_path": anchor.file_path,
        "stale": stale,
        "clue_hash": anchor.content_hash,
        "current_hash": current_hash,
        "change_summary": "File content changed since clue generation" if stale else "File unchanged",
    }
    return _with_confidence(result, 1.0, confidence_threshold)


def expand_projection(
    graph: CanonicalClueGraph,
    node_id: str,
    additional_hops: int = 1,
    edge_types: list[str] | None = None,
    *,
    confidence_threshold: float | None = None,
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
        nid, current_depth = queue.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        if current_depth >= additional_hops:
            continue
        for edge in graph.edges:
            if edge.edge_type not in allowed_types:
                continue
            if edge.from_node == nid:
                collected_edges.add(edge.edge_id)
                if edge.to_node not in visited:
                    queue.append((edge.to_node, current_depth + 1))
            if edge.to_node == nid:
                collected_edges.add(edge.edge_id)
                if edge.from_node not in visited:
                    queue.append((edge.from_node, current_depth + 1))

    edge_map = {e.edge_id: e for e in graph.edges}
    result = {
        "status": "ok",
        "seed_node": node_id,
        "additional_hops": additional_hops,
        "edge_types": list(allowed_types),
        "projected_nodes": [node_map[nid].to_dict() for nid in sorted(visited) if nid in node_map],
        "projected_edges": [edge_map[eid].to_dict() for eid in sorted(collected_edges) if eid in edge_map],
    }
    return _with_confidence(result, node_map[node_id].confidence, confidence_threshold)


def fetch_contract(
    graph: CanonicalClueGraph,
    node_id: str,
    *,
    detail_records: list[dict[str, Any]] | None = None,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Retrieve the semantic contract for a specific node."""
    node_map = {n.node_id: n for n in graph.nodes}
    node = node_map.get(node_id)
    if node is None:
        return {"status": "error", "message": f"Unknown node: {node_id}"}

    detail = _detail_index(detail_records).get(node_id)
    semantic_contract = dict(node.semantic_contract or {})
    if detail:
        semantic_contract.setdefault("calls", detail.get("calls", []))
        semantic_contract.setdefault("called_by", detail.get("called_by", []))
        semantic_contract.setdefault("source", detail.get("source", ""))
        if detail.get("behavior_patterns"):
            semantic_contract["behavior_patterns"] = detail["behavior_patterns"]

    behavior_patterns = semantic_contract.get("behavior_patterns", []) or []
    confidence = 0.95 if behavior_patterns else 0.72
    result = {
        "status": "ok",
        "node_id": node_id,
        "node_type": node.node_type,
        "source_anchor": node.source_anchor.to_dict(),
        "semantic_contract": semantic_contract,
    }
    if detail:
        result["detail_record"] = detail
    return _with_confidence(result, confidence, confidence_threshold)


def get_clue(
    graph: CanonicalClueGraph,
    repo_root: str,
    *,
    question: str | None = None,
    clue_text: str | None = None,
    commit_id: str = "",
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Return a pre-generated clue or render one for a question."""
    rendered = False
    active_question = ""
    if clue_text:
        for line in clue_text.splitlines():
            if line.startswith("? "):
                active_question = line[2:].strip()
                break
    if clue_text and (question is None or question.strip() == active_question):
        text = clue_text
    else:
        rendered = True
        question = question or active_question or "What are the key structures and behaviors in this repository?"
        text = render_mrlf(graph, question, repo_root=repo_root, commit_id=commit_id)
        active_question = question
    result = {
        "status": "ok",
        "question": active_question,
        "clue": text,
        "rendered": rendered,
    }
    return _with_confidence(result, 0.9 if rendered else 0.94, confidence_threshold)


def get_drill_targets(
    *,
    clue_text: str,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Parse the GAPS section from a clue and return drill targets."""
    in_gaps = False
    question_type = ""
    coverage = ""
    uncovered = ""
    targets: list[dict[str, Any]] = []
    pattern = re.compile(r"^drill:\s+(.+?)\s+\(~(\d+)\s+lines,\s+(.+?)\)$")

    for raw_line in clue_text.splitlines():
        line = raw_line.strip()
        if line == "-- GAPS":
            in_gaps = True
            continue
        if in_gaps and line.startswith("-- "):
            break
        if not in_gaps or not line:
            continue
        if line.startswith("type:"):
            question_type = line[5:].strip()
        elif line.startswith("coverage:"):
            coverage = line[9:].strip()
        elif line.startswith("uncovered:"):
            uncovered = line[10:].strip()
        elif line.startswith("drill:"):
            match = pattern.match(line)
            if match:
                targets.append(
                    {
                        "file_path": match.group(1),
                        "estimated_lines": int(match.group(2)),
                        "symbol_name": match.group(3),
                    }
                )
            else:
                targets.append({"raw": line[6:].strip()})

    result = {
        "status": "ok",
        "question_type": question_type,
        "coverage": coverage,
        "uncovered": uncovered,
        "targets": targets,
    }
    return _with_confidence(result, 0.92, confidence_threshold)
