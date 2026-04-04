from __future__ import annotations

from copy import deepcopy
from typing import Any

from .graph_analysis import analyze_graph_integrity, compare_operational_paths
from .models import CanonicalClueGraph, Edge, Node, SourceAnchor
from .schema_validator import validate_graph


SUPPORTED_OPS = {
    "add_node",
    "remove_node",
    "update_node_contract",
    "add_edge",
    "remove_edge",
}


def _node_from_payload(payload: dict[str, Any]) -> Node:
    return Node(
        node_id=payload["node_id"],
        node_type=payload["node_type"],
        source_anchor=SourceAnchor(**payload["source_anchor"]),
        semantic_contract=payload["semantic_contract"],
        confidence=float(payload["confidence"]),
    )


def _edge_from_payload(payload: dict[str, Any]) -> Edge:
    return Edge(
        edge_id=payload["edge_id"],
        edge_type=payload["edge_type"],
        from_node=payload["from_node"],
        to_node=payload["to_node"],
        evidence=payload["evidence"],
    )


def apply_delta_patch(
    base_graph: CanonicalClueGraph,
    delta_patch: dict[str, Any],
    repo_root,
) -> tuple[CanonicalClueGraph, dict[str, Any]]:
    updated = CanonicalClueGraph.from_dict(deepcopy(base_graph.to_dict()))
    nodes = {node.node_id: node for node in updated.nodes}
    edges = {edge.edge_id: edge for edge in updated.edges}

    applied_ops: list[dict[str, Any]] = []
    errors: list[str] = []

    for index, operation in enumerate(delta_patch.get("operations", []), start=1):
        op = operation.get("op")
        if op not in SUPPORTED_OPS:
            errors.append(f"Unsupported op at index {index}: {op}")
            continue

        if op == "add_node":
            node = _node_from_payload(operation["node"])
            nodes[node.node_id] = node
            applied_ops.append({"index": index, "op": op, "node_id": node.node_id})

        elif op == "remove_node":
            node_id = operation["node_id"]
            nodes.pop(node_id, None)
            edges = {
                edge_id: edge
                for edge_id, edge in edges.items()
                if edge.from_node != node_id and edge.to_node != node_id
            }
            applied_ops.append({"index": index, "op": op, "node_id": node_id})

        elif op == "update_node_contract":
            node_id = operation["node_id"]
            node = nodes.get(node_id)
            if not node:
                errors.append(f"Node not found for update_node_contract: {node_id}")
                continue
            if "semantic_contract" in operation:
                node.semantic_contract = operation["semantic_contract"]
            if "confidence" in operation:
                node.confidence = float(operation["confidence"])
            applied_ops.append({"index": index, "op": op, "node_id": node_id})

        elif op == "add_edge":
            edge = _edge_from_payload(operation["edge"])
            edges[edge.edge_id] = edge
            applied_ops.append({"index": index, "op": op, "edge_id": edge.edge_id})

        elif op == "remove_edge":
            edge_id = operation["edge_id"]
            edges.pop(edge_id, None)
            applied_ops.append({"index": index, "op": op, "edge_id": edge_id})

    updated.nodes = sorted(nodes.values(), key=lambda item: item.node_id)
    updated.edges = sorted(edges.values(), key=lambda item: item.edge_id)

    path_report = compare_operational_paths(base_graph, updated)
    integrity_report = analyze_graph_integrity(updated)
    validation_errors = validate_graph(updated, repo_root)

    no_gap = integrity_report["invariant_checks"].get("no_gap_invariant", False)
    connectivity = integrity_report["invariant_checks"].get(
        "connectivity_invariant", False
    )

    report = {
        "patch_id": delta_patch.get("patch_id", "unknown"),
        "applied_operation_count": len(applied_ops),
        "applied_operations": applied_ops,
        "operation_errors": errors,
        "validation_errors": validation_errors,
        "path_report": path_report,
        "integrity_report": integrity_report,
        "proofs": {
            "no_gap_proof": no_gap,
            "connectivity_proof": connectivity,
            "path_coverage": path_report.get("path_coverage", 0.0),
        },
        "passed": not errors and not validation_errors and no_gap and connectivity,
    }
    return updated, report
