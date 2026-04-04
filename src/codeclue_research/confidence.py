from __future__ import annotations

from collections import defaultdict
from statistics import mean, stdev
from typing import Any

from .models import CanonicalClueGraph


_TASK_FAMILY_THRESHOLDS: dict[str, float] = {
    "OF1": 0.80,
    "OF2": 0.90,
    "OF3": 0.85,
    "OF4": 0.95,
    "OF5": 0.95,
}

_TOOL_CALL_BUDGETS: dict[str, int] = {
    "OF1": 5,
    "OF2": 15,
    "OF3": 10,
    "OF4": 20,
    "OF5": 30,
}

_TIER1_CONFIDENCE_PENALTY = 0.15
_DENSITY_CONFIDENCE_PENALTY = 0.20
_FAN_OUT_Z_THRESHOLD = 2.0
_CROSS_FILE_RATIO_THRESHOLD = 0.60


def _safe_div(num: float, den: float) -> float:
    if den == 0:
        return 0.0
    return num / den


def _compute_fan_out_z_scores(
    graph: CanonicalClueGraph,
) -> dict[str, float]:
    type_fan_outs: dict[str, list[int]] = defaultdict(list)
    node_fan_out: dict[str, int] = {}

    for node in graph.nodes:
        count = sum(1 for e in graph.edges if e.from_node == node.node_id)
        node_fan_out[node.node_id] = count
        type_fan_outs[node.node_type].append(count)

    z_scores: dict[str, float] = {}
    for node in graph.nodes:
        fan_outs = type_fan_outs.get(node.node_type, [])
        if len(fan_outs) < 2:
            z_scores[node.node_id] = 0.0
            continue
        m = mean(fan_outs)
        s = stdev(fan_outs)
        if s == 0:
            z_scores[node.node_id] = 0.0
        else:
            z_scores[node.node_id] = (node_fan_out[node.node_id] - m) / s

    return z_scores


def detect_density_indicators(
    node_id: str,
    graph: CanonicalClueGraph,
    fan_out_z_scores: dict[str, float],
    projected_file_count: int,
    total_file_count: int,
) -> dict[str, Any]:
    node_map = {n.node_id: n for n in graph.nodes}
    node = node_map.get(node_id)
    if not node:
        return {"density_flag": False}

    contract = node.semantic_contract
    indicators = contract.get("complexity_indicators", {})

    uses_reflection = bool(indicators.get("uses_reflection", False))
    uses_dynamic_dispatch = bool(indicators.get("uses_dynamic_dispatch", False))
    uses_generics = bool(indicators.get("uses_generics", False))
    uses_metaprogramming = bool(indicators.get("uses_metaprogramming", False))
    decorator_depth = int(indicators.get("decorator_depth", 0))
    generic_type_param_count = int(indicators.get("generic_type_param_count", 0))

    fan_out = sum(1 for e in graph.edges if e.from_node == node_id)
    fan_out_z = fan_out_z_scores.get(node_id, 0.0)
    cross_file_ratio = _safe_div(projected_file_count, max(total_file_count, 1))

    density_flag = (
        uses_reflection
        or uses_dynamic_dispatch
        or uses_metaprogramming
        or fan_out_z > _FAN_OUT_Z_THRESHOLD
        or cross_file_ratio > _CROSS_FILE_RATIO_THRESHOLD
        or decorator_depth > 3
        or generic_type_param_count > 3
    )

    return {
        "uses_reflection": uses_reflection,
        "uses_dynamic_dispatch": uses_dynamic_dispatch,
        "uses_generics": uses_generics,
        "uses_metaprogramming": uses_metaprogramming,
        "decorator_depth": decorator_depth,
        "generic_type_param_count": generic_type_param_count,
        "fan_out": fan_out,
        "fan_out_z_score": round(fan_out_z, 3),
        "cross_file_span_ratio": round(cross_file_ratio, 3),
        "density_flag": density_flag,
    }


def _build_suggested_actions(
    node_id: str,
    node_confidence: float,
    threshold: float,
    graph: CanonicalClueGraph,
    projected_node_ids: set[str],
) -> list[dict[str, Any]]:
    if node_confidence >= threshold:
        return []

    actions: list[dict[str, Any]] = []
    node_map = {n.node_id: n for n in graph.nodes}
    node = node_map.get(node_id)
    if not node:
        return actions

    outgoing_outside = [
        e for e in graph.edges
        if e.from_node == node_id and e.to_node not in projected_node_ids
    ]
    if outgoing_outside:
        actions.append({
            "tool": "resolve_dependency",
            "args": {"node_id": node_id, "depth": 2},
            "rationale": (
                f"{len(outgoing_outside)} outgoing edge(s) point to nodes "
                f"outside this projection; dependency closure is incomplete"
            ),
        })

    anchor = node.source_anchor
    if anchor.file_path and anchor.byte_end - anchor.byte_start > 0:
        actions.append({
            "tool": "code_slice",
            "args": {
                "file_path": anchor.file_path,
                "start_line": 1,
                "end_line": 50,
            },
            "rationale": "Low confidence on this node; source verification recommended",
        })

    return actions


def compute_structural_confidence(
    projection: dict[str, Any],
    full_graph: CanonicalClueGraph,
    operation_family: str = "OF2",
) -> dict[str, Any]:
    projected_nodes_raw = projection.get("projected_nodes", [])
    projected_edges_raw = projection.get("projected_edges", [])
    prompt_profile = projection.get("prompt_profile", {})

    projected_node_ids = {
        n.get("node_id") for n in projected_nodes_raw
        if isinstance(n, dict) and n.get("node_id")
    }
    projected_edge_ids = {
        e.get("edge_id") for e in projected_edges_raw
        if isinstance(e, dict) and e.get("edge_id")
    }

    full_node_ids = {n.node_id for n in full_graph.nodes}
    full_edge_map = {e.edge_id: e for e in full_graph.edges}
    node_map = {n.node_id: n for n in full_graph.nodes}

    # Fix 1: Task-weighted dependency miss — only count external edges
    # from nodes that match the prompt profile's focus as "relevant misses".
    # Edges from incidental nodes (caught by BFS but not focus-aligned) are
    # discounted by a weight factor.
    focus_files = set(prompt_profile.get("focus_files", []) or [])
    focus_symbols = {s.lower() for s in (prompt_profile.get("focus_symbols", []) or [])}
    focus_keywords = [kw.lower() for kw in (prompt_profile.get("focus_keywords", []) or [])]

    def _is_focus_node(nid: str) -> bool:
        n = node_map.get(nid)
        if not n:
            return False
        if focus_files and n.source_anchor.file_path in focus_files:
            return True
        sym = str(n.semantic_contract.get("symbol_name", "")).lower()
        if focus_symbols and sym in focus_symbols:
            return True
        if focus_keywords:
            text = f"{n.node_id} {sym}".lower()
            if any(kw in text for kw in focus_keywords):
                return True
        return False

    # p_context_miss: weighted edges pointing outside projection
    weighted_outside = 0.0
    total_edge_weight = 0.0
    for edge_id in projected_edge_ids:
        edge = full_edge_map.get(edge_id)
        if not edge:
            continue
        # Focus-aligned edges get weight 1.0, others get 0.2
        from_focus = _is_focus_node(edge.from_node)
        to_focus = _is_focus_node(edge.to_node)
        weight = 1.0 if (from_focus or to_focus) else 0.2
        total_edge_weight += weight
        if edge.to_node not in projected_node_ids:
            weighted_outside += weight
        if edge.from_node not in projected_node_ids:
            weighted_outside += weight

    p_context_miss = _safe_div(weighted_outside, max(total_edge_weight * 2, 1))

    # p_dependency_miss: only count focus-aligned reachable nodes as "required"
    focus_reachable = set()
    other_reachable = set()
    for node_id in projected_node_ids:
        is_focus = _is_focus_node(node_id)
        for edge in full_graph.edges:
            if edge.from_node == node_id:
                if is_focus:
                    focus_reachable.add(edge.to_node)
                else:
                    other_reachable.add(edge.to_node)
            if edge.to_node == node_id:
                if is_focus:
                    focus_reachable.add(edge.from_node)
                else:
                    other_reachable.add(edge.from_node)

    # Focus closure gets full weight, other closure gets 0.2 weight
    focus_required = len(focus_reachable)
    focus_covered = len(focus_reachable & projected_node_ids)
    other_required = len(other_reachable - focus_reachable)
    other_covered = len((other_reachable - focus_reachable) & projected_node_ids)

    weighted_required = focus_required + 0.2 * other_required
    weighted_covered = focus_covered + 0.2 * other_covered
    p_dependency_miss = 1.0 - _safe_div(weighted_covered, max(weighted_required, 1))

    nodes_with_anchors = 0
    total_projected_nodes = len(projected_node_ids)
    for nid in projected_node_ids:
        node = node_map.get(nid)
        if node and node.source_anchor.file_path and node.source_anchor.content_hash:
            nodes_with_anchors += 1
    p_hallucination = 1.0 - _safe_div(nodes_with_anchors, max(total_projected_nodes, 1))

    projected_files = {
        node_map[nid].source_anchor.file_path
        for nid in projected_node_ids if nid in node_map
    }
    total_files = len({n.source_anchor.file_path for n in full_graph.nodes})

    fan_out_z_scores = _compute_fan_out_z_scores(full_graph)

    density_flags_count = 0
    per_node_confidence: list[dict[str, Any]] = []
    threshold = _TASK_FAMILY_THRESHOLDS.get(operation_family, 0.85)

    for nid in sorted(projected_node_ids):
        node = node_map.get(nid)
        if not node:
            continue

        density = detect_density_indicators(
            nid, full_graph, fan_out_z_scores,
            len(projected_files), total_files,
        )

        node_conf = node.confidence
        tier = node.semantic_contract.get("tier", 1)
        if tier < 2:
            node_conf -= _TIER1_CONFIDENCE_PENALTY
        if density["density_flag"]:
            node_conf -= _DENSITY_CONFIDENCE_PENALTY
            density_flags_count += 1
        node_conf = max(0.0, min(1.0, node_conf))

        suggested_actions = _build_suggested_actions(
            nid, node_conf, threshold, full_graph, projected_node_ids,
        )

        per_node_confidence.append({
            "node_id": nid,
            "confidence": round(node_conf, 6),
            "tier": tier,
            "density_indicators": density,
            "suggested_actions": suggested_actions,
        })

    per_edge_confidence: list[dict[str, Any]] = []
    for eid in sorted(projected_edge_ids):
        edge = full_edge_map.get(eid)
        if not edge:
            continue

        from_in = edge.from_node in projected_node_ids
        to_in = edge.to_node in projected_node_ids
        edge_conf = 1.0 if (from_in and to_in) else 0.5
        actions: list[dict[str, Any]] = []
        if edge_conf < threshold:
            target = edge.to_node if not to_in else edge.from_node
            actions.append({
                "tool": "fetch_contract",
                "args": {"node_id": target},
                "rationale": "Edge endpoint is outside projection; contract missing",
            })

        per_edge_confidence.append({
            "edge_id": eid,
            "confidence": round(edge_conf, 6),
            "suggested_actions": actions,
        })

    code_density_risk = _safe_div(density_flags_count, max(total_projected_nodes, 1))
    confidence_overall = (
        (1 - p_context_miss)
        * (1 - p_dependency_miss)
        * (1 - p_hallucination)
        * (1 - code_density_risk)
    )
    confidence_overall = max(0.0, min(1.0, confidence_overall))

    if confidence_overall >= 0.85:
        lookup_hint = "clue_only"
    elif confidence_overall >= 0.60:
        lookup_hint = "targeted_lookup"
    else:
        lookup_hint = "expanded_lookup"

    return {
        "p_context_miss": round(p_context_miss, 6),
        "p_dependency_miss": round(p_dependency_miss, 6),
        "p_hallucination": round(p_hallucination, 6),
        "code_density_risk": round(code_density_risk, 6),
        "confidence_overall": round(confidence_overall, 6),
        "lookup_decision_hint": lookup_hint,
        "operation_family": operation_family,
        "threshold": threshold,
        "tool_call_budget": _TOOL_CALL_BUDGETS.get(operation_family, 15),
        "per_node_confidence": per_node_confidence,
        "per_edge_confidence": per_edge_confidence,
    }
