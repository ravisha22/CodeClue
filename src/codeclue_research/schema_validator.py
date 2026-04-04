from __future__ import annotations

from pathlib import Path
from typing import Any

from .graph_analysis import analyze_graph_integrity
from .models import CanonicalClueGraph


REQUIRED_TOP_LEVEL = {
    "metadata",
    "repository",
    "nodes",
    "edges",
    "operations",
    "invariants",
}


def validate_graph(graph: CanonicalClueGraph, repo_root: Path) -> list[str]:
    errors: list[str] = []
    repo_root = repo_root.resolve()
    payload = graph.to_dict()

    missing = REQUIRED_TOP_LEVEL - set(payload.keys())
    if missing:
        errors.append(f"Missing top-level fields: {sorted(missing)}")

    node_ids = [node.node_id for node in graph.nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("Duplicate node_id values detected")

    edge_ids = [edge.edge_id for edge in graph.edges]
    if len(edge_ids) != len(set(edge_ids)):
        errors.append("Duplicate edge_id values detected")

    node_id_set = set(node_ids)
    for edge in graph.edges:
        if edge.from_node not in node_id_set:
            errors.append(f"Edge {edge.edge_id} has unknown from_node: {edge.from_node}")
        if edge.to_node not in node_id_set:
            errors.append(f"Edge {edge.edge_id} has unknown to_node: {edge.to_node}")

    for node in graph.nodes:
        anchor = node.source_anchor
        if anchor.byte_start < 0 or anchor.byte_end < 0:
            errors.append(f"Node {node.node_id} has negative byte offsets")
        if anchor.byte_start > anchor.byte_end:
            errors.append(f"Node {node.node_id} has byte_start > byte_end")
        if not anchor.file_path:
            errors.append(f"Node {node.node_id} has empty file_path")
            continue
        source_path = repo_root / anchor.file_path
        if not source_path.exists():
            errors.append(
                f"Node {node.node_id} anchor path not found in repo: {anchor.file_path}"
            )

        if not isinstance(node.semantic_contract, dict) or not node.semantic_contract:
            errors.append(f"Node {node.node_id} semantic_contract is empty")

    if not isinstance(graph.operations, dict) or not graph.operations:
        errors.append("operations section is missing or empty")

    if not isinstance(graph.invariants, dict) or not graph.invariants:
        errors.append("invariants section is missing or empty")

    for invariant in (
        "connectivity_invariant",
        "anchor_invariant",
        "no_gap_invariant",
        "round_trip_invariant",
    ):
        if invariant not in graph.invariants:
            errors.append(f"Missing invariant: {invariant}")

    integrity = analyze_graph_integrity(graph)
    checks = integrity.get("invariant_checks", {})
    if not checks.get("connectivity_invariant", False):
        errors.append("Graph integrity failed connectivity invariant")
    if not checks.get("no_gap_invariant", False):
        errors.append("Graph integrity failed no-gap invariant")
    if integrity.get("module_roots", 0) == 0:
        errors.append("Graph has no module roots")

    return errors


def validate_payload(payload: dict[str, Any], repo_root: Path) -> list[str]:
    return validate_graph(CanonicalClueGraph.from_dict(payload), repo_root)
