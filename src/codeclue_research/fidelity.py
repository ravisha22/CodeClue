from __future__ import annotations

from typing import Any


def _safe_div(num: float, den: float) -> float:
    if den == 0:
        return 0.0
    return num / den


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _extract_projection_sets(projection_trace: dict[str, Any]) -> tuple[set[str], set[str]]:
    observed_nodes = {
        node.get("node_id")
        for node in projection_trace.get("projected_nodes", [])
        if isinstance(node, dict) and node.get("node_id")
    }
    observed_edges = {
        edge.get("edge_id")
        for edge in projection_trace.get("projected_edges", [])
        if isinstance(edge, dict) and edge.get("edge_id")
    }
    return observed_nodes, observed_edges


def _extract_gold_sets(gold_spec: dict[str, Any]) -> tuple[set[str], set[str]]:
    if "gold_path" in gold_spec:
        path = gold_spec.get("gold_path", {}) or {}
        expected_nodes = set(path.get("nodes", []) or [])
        expected_edges = set(path.get("edges", []) or [])
    else:
        expected_nodes = set(gold_spec.get("expected_nodes", []) or [])
        expected_edges = set(gold_spec.get("expected_edges", []) or [])
    return expected_nodes, expected_edges


def evaluate_projection_fidelity(
    projection_trace: dict[str, Any],
    gold_spec: dict[str, Any],
) -> dict[str, Any]:
    observed_nodes, observed_edges = _extract_projection_sets(projection_trace)
    expected_nodes, expected_edges = _extract_gold_sets(gold_spec)

    node_tp = len(observed_nodes & expected_nodes)
    edge_tp = len(observed_edges & expected_edges)

    node_precision = _safe_div(node_tp, len(observed_nodes))
    node_recall = _safe_div(node_tp, len(expected_nodes))
    node_f1 = _f1(node_precision, node_recall)

    edge_precision = _safe_div(edge_tp, len(observed_edges))
    edge_recall = _safe_div(edge_tp, len(expected_edges))
    edge_f1 = _f1(edge_precision, edge_recall)

    path_fidelity = (node_f1 + edge_f1) / 2.0

    thresholds = gold_spec.get("thresholds", {}) or {}
    node_f1_min = float(thresholds.get("node_f1_min", 0.0))
    edge_f1_min = float(thresholds.get("edge_f1_min", 0.0))
    path_fidelity_min = float(thresholds.get("path_fidelity_min", 0.0))

    passed = (
        node_f1 >= node_f1_min
        and edge_f1 >= edge_f1_min
        and path_fidelity >= path_fidelity_min
    )

    return {
        "gold_id": gold_spec.get("gold_id", "unknown"),
        "operation_family": projection_trace.get("operation_family", "unknown"),
        "projection_trace_id": projection_trace.get("trace_id", "unknown"),
        "passed": passed,
        "metrics": {
            "node_precision": round(node_precision, 6),
            "node_recall": round(node_recall, 6),
            "node_f1": round(node_f1, 6),
            "edge_precision": round(edge_precision, 6),
            "edge_recall": round(edge_recall, 6),
            "edge_f1": round(edge_f1, 6),
            "path_fidelity": round(path_fidelity, 6),
        },
        "thresholds": {
            "node_f1_min": node_f1_min,
            "edge_f1_min": edge_f1_min,
            "path_fidelity_min": path_fidelity_min,
        },
        "counts": {
            "expected_nodes": len(expected_nodes),
            "observed_nodes": len(observed_nodes),
            "expected_edges": len(expected_edges),
            "observed_edges": len(observed_edges),
            "node_true_positives": node_tp,
            "edge_true_positives": edge_tp,
        },
        "diff": {
            "missing_nodes": sorted(expected_nodes - observed_nodes),
            "extra_nodes": sorted(observed_nodes - expected_nodes),
            "missing_edges": sorted(expected_edges - observed_edges),
            "extra_edges": sorted(observed_edges - expected_edges),
        },
    }
