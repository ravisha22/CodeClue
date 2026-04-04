from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Any

from .models import CanonicalClueGraph


_ALLOWED_FAMILIES = {"OF1", "OF2", "OF3", "OF4", "OF5"}

_ENABLE_CONFIDENCE = True


def _policy_for(operation_family: str) -> dict[str, Any]:
    return {
        "OF1": {
            "max_depth": 1,
            "edge_types": ["contains"],
            "output_edge_types": ["contains"],
            "bidirectional": False,
            "seed_hops": 1,
        },
        "OF2": {
            "max_depth": 3,
            "edge_types": ["contains", "calls"],
            "output_edge_types": ["calls"],
            "include_only_edge_incident_nodes": True,
            "always_include_node_types": ["module"],
            "bidirectional": True,
            "seed_hops": 2,
        },
        "OF3": {
            "max_depth": 2,
            "edge_types": ["contains", "calls"],
            "output_edge_types": ["contains", "calls"],
            "bidirectional": True,
            "seed_hops": 2,
        },
        "OF4": {
            "max_depth": 4,
            "edge_types": ["calls", "contains"],
            "output_edge_types": ["calls", "contains"],
            "bidirectional": True,
            "seed_hops": 2,
        },
        "OF5": {
            "max_depth": 2,
            "edge_types": ["calls", "contains"],
            "output_edge_types": ["calls", "contains"],
            "bidirectional": True,
            "seed_hops": 2,
        },
    }[operation_family]


def _node_text(node: Any) -> str:
    symbol = node.semantic_contract.get("symbol_name", "")
    purpose = node.semantic_contract.get("purpose", "")
    symbol_type = node.semantic_contract.get("symbol_type", "")
    path = node.semantic_contract.get("path", "")
    return f"{node.node_id} {node.node_type} {symbol} {purpose} {symbol_type} {path}".lower()


def _context_level(prompt_profile: dict[str, Any]) -> str:
    constraints = prompt_profile.get("constraints", {}) or {}
    value = str(constraints.get("max_context", "balanced")).lower()
    if value not in {"focused", "balanced", "broad"}:
        return "balanced"
    return value


def _tuned_policy(base_policy: dict[str, Any], prompt_profile: dict[str, Any]) -> dict[str, Any]:
    level = _context_level(prompt_profile)
    depth_boost = {"focused": 0, "balanced": 1, "broad": 2}[level]
    budget = {"focused": 80, "balanced": 160, "broad": 320}[level]

    tuned = dict(base_policy)
    tuned["max_depth"] = int(base_policy["max_depth"]) + depth_boost
    tuned["node_budget"] = budget
    tuned["context_level"] = level
    return tuned


def _seed_nodes(
    graph: CanonicalClueGraph,
    operation_family: str,
    prompt_profile: dict[str, Any],
) -> set[str]:
    nodes = graph.nodes
    node_map = {node.node_id: node for node in nodes}
    seeds: set[str] = set()

    for node_id in prompt_profile.get("focus_node_ids", []) or []:
        if node_id in node_map:
            seeds.add(node_id)

    focus_symbols = {value.lower() for value in (prompt_profile.get("focus_symbols", []) or [])}
    if focus_symbols:
        for node in nodes:
            symbol = str(node.semantic_contract.get("symbol_name", "")).lower()
            if symbol and symbol in focus_symbols:
                seeds.add(node.node_id)

    focus_files = set(prompt_profile.get("focus_files", []) or [])
    if focus_files:
        for node in nodes:
            if node.source_anchor.file_path in focus_files:
                seeds.add(node.node_id)

    keywords = [kw.lower() for kw in (prompt_profile.get("focus_keywords", []) or [])]
    if keywords:
        for node in nodes:
            text = _node_text(node)
            if any(kw in text for kw in keywords):
                seeds.add(node.node_id)

    if operation_family == "OF5":
        security_terms = ["auth", "token", "secret", "encrypt", "password", "permission"]
        for node in nodes:
            text = _node_text(node)
            if any(term in text for term in security_terms):
                seeds.add(node.node_id)

    # Fix 2: Cap seed count to prevent projection explosion on large repos.
    # OF1/OF5 tend to seed on too many nodes (all modules, all security-keyword matches).
    # Cap seeds to keep projections focused. If focus_files or focus_symbols are set,
    # prefer those seeds; otherwise cap by family.
    _SEED_CAPS = {"OF1": 15, "OF2": 20, "OF3": 15, "OF4": 20, "OF5": 25}
    cap = _SEED_CAPS.get(operation_family, 20)
    if len(seeds) > cap:
        # Prefer seeds from focus_files/focus_symbols over keyword/security-term matches
        focused = set()
        for sid in seeds:
            n = node_map.get(sid)
            if not n:
                continue
            if focus_files and n.source_anchor.file_path in focus_files:
                focused.add(sid)
            elif focus_symbols and str(n.semantic_contract.get("symbol_name", "")).lower() in focus_symbols:
                focused.add(sid)
        if focused and len(focused) <= cap:
            seeds = focused
        else:
            seeds = set(sorted(seeds)[:cap])

    if seeds:
        return seeds

    if operation_family == "OF1":
        # Only seed on modules matching focus_files, or first 10 modules if no focus
        if focus_files:
            return {node.node_id for node in nodes if node.node_type == "module" and node.source_anchor.file_path in focus_files}
        module_ids = sorted(node.node_id for node in nodes if node.node_type == "module")
        return set(module_ids[:10])

    fallback = [node.node_id for node in nodes if node.node_type in {"function", "class", "struct"}]
    return set(fallback[:5])


def _expand_seed_set(
    seeds: set[str],
    graph: CanonicalClueGraph,
    policy: dict[str, Any],
) -> set[str]:
    node_map = {node.node_id: node for node in graph.nodes}
    file_modules: dict[str, str] = {}
    file_nodes: dict[str, set[str]] = {}
    for node in graph.nodes:
        file_nodes.setdefault(node.source_anchor.file_path, set()).add(node.node_id)
        if node.node_type == "module":
            file_modules[node.source_anchor.file_path] = node.node_id

    expanded = set(seeds)
    for seed in list(seeds):
        node = node_map.get(seed)
        if not node:
            continue
        file_path = node.source_anchor.file_path
        module_id = file_modules.get(file_path)
        if module_id:
            expanded.add(module_id)
        if node.node_type == "module":
            expanded.update(file_nodes.get(file_path, set()))

    return expanded


def _candidate_universe(
    seeds: set[str],
    adjacency: dict[str, list[tuple[str, str]]],
    reverse: dict[str, list[tuple[str, str]]],
    max_depth: int,
    bidirectional: bool,
) -> tuple[set[str], set[str]]:
    candidate_nodes: set[str] = set()
    candidate_edges: set[str] = set()

    queue: deque[tuple[str, int]] = deque((seed, 0) for seed in sorted(seeds))
    while queue:
        node_id, depth = queue.popleft()
        if node_id in candidate_nodes and depth > max_depth:
            continue
        candidate_nodes.add(node_id)
        if depth >= max_depth:
            continue

        neighbors = list(adjacency.get(node_id, []))
        if bidirectional:
            neighbors.extend(reverse.get(node_id, []))

        for neighbor, edge_id in neighbors:
            candidate_edges.add(edge_id)
            if neighbor not in candidate_nodes:
                queue.append((neighbor, depth + 1))

    return candidate_nodes, candidate_edges


def project_operation(
    graph: CanonicalClueGraph,
    operation_family: str,
    prompt_profile: dict[str, Any] | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    if operation_family not in _ALLOWED_FAMILIES:
        raise ValueError(f"Unsupported operation family: {operation_family}")

    profile = prompt_profile or {
        "profile_id": "default",
        "intent": "generic",
        "constraints": {"max_context": "balanced"},
    }

    base_policy = _policy_for(operation_family)
    policy = _tuned_policy(base_policy, profile)
    initial_seeds = _seed_nodes(graph, operation_family, profile)
    seeds = _expand_seed_set(initial_seeds, graph, policy)
    node_map = {node.node_id: node for node in graph.nodes}
    edge_types = set(policy["edge_types"])
    output_edge_types = set(policy.get("output_edge_types", policy["edge_types"]))
    edge_map = {edge.edge_id: edge for edge in graph.edges}

    adjacency: dict[str, list[tuple[str, str]]] = {node.node_id: [] for node in graph.nodes}
    reverse: dict[str, list[tuple[str, str]]] = {node.node_id: [] for node in graph.nodes}

    for edge in graph.edges:
        if edge.edge_type not in edge_types:
            continue
        adjacency.setdefault(edge.from_node, []).append((edge.to_node, edge.edge_id))
        reverse.setdefault(edge.to_node, []).append((edge.from_node, edge.edge_id))

    max_depth = int(policy["max_depth"])
    bidirectional = bool(policy.get("bidirectional", False))
    node_budget = int(policy.get("node_budget", 160))

    candidate_nodes, candidate_edges = _candidate_universe(
        seeds=seeds,
        adjacency=adjacency,
        reverse=reverse,
        max_depth=max_depth,
        bidirectional=bidirectional,
    )

    queue: deque[tuple[str, int, str | None]] = deque((seed, 0, None) for seed in sorted(seeds))
    visited: set[str] = set()
    selected_nodes: set[str] = set()
    selected_edges: set[str] = set()
    reasoning_path: list[dict[str, Any]] = []
    traversed_edge_ids: set[str] = set()

    while queue:
        if len(selected_nodes) >= node_budget:
            break

        node_id, depth, via_edge = queue.popleft()
        if node_id in visited:
            continue
        visited.add(node_id)

        if node_id not in node_map:
            continue
        selected_nodes.add(node_id)
        reasoning_path.append(
            {
                "step": len(reasoning_path) + 1,
                "node_id": node_id,
                "depth": depth,
                "via_edge": via_edge,
            }
        )

        if depth >= max_depth:
            continue

        neighbors = list(adjacency.get(node_id, []))
        if bidirectional:
            neighbors.extend(reverse.get(node_id, []))

        for neighbor, edge_id in neighbors:
            edge_obj = edge_map.get(edge_id)
            if edge_obj and edge_obj.edge_type in output_edge_types:
                traversed_edge_ids.add(edge_id)
                selected_edges.add(edge_id)
            if neighbor not in visited:
                queue.append((neighbor, depth + 1, edge_id))

    projected_edges = [edge_map[edge_id].to_dict() for edge_id in sorted(selected_edges) if edge_id in edge_map]

    projected_node_ids = set(selected_nodes)
    if bool(policy.get("include_only_edge_incident_nodes", False)):
        incident_node_ids: set[str] = set()
        for edge_id in selected_edges:
            edge_obj = edge_map.get(edge_id)
            if not edge_obj:
                continue
            incident_node_ids.add(edge_obj.from_node)
            incident_node_ids.add(edge_obj.to_node)

        always_include_node_types = set(policy.get("always_include_node_types", []))
        projected_node_ids = {
            node_id
            for node_id in projected_node_ids
            if node_id in incident_node_ids
            or node_map[node_id].node_type in always_include_node_types
        }

    projected_nodes = [node_map[node_id].to_dict() for node_id in sorted(projected_node_ids)]

    traversed_edges = len(traversed_edge_ids)
    path_precision = 1.0 if traversed_edges == 0 else min(1.0, len(projected_edges) / traversed_edges)
    path_recall_local = (
        1.0 if not candidate_nodes else min(1.0, len(selected_nodes) / len(candidate_nodes))
    )
    path_recall_global = 0.0 if not graph.nodes else min(1.0, len(projected_nodes) / len(graph.nodes))
    contradiction_rejection = 1.0 if profile.get("strict_mode", True) else 0.75
    path_drift_index = max(0.0, 1.0 - path_recall_local)

    result = {
        "trace_id": trace_id or f"trace-{operation_family}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "operation_family": operation_family,
        "prompt_profile": profile,
        "policy": policy,
        "projected_nodes": projected_nodes,
        "projected_edges": projected_edges,
        "reasoning_path": reasoning_path,
        "validation": {
            "path_precision": round(path_precision, 6),
            "path_recall": round(path_recall_local, 6),
            "path_recall_global": round(path_recall_global, 6),
            "contradiction_rejection": round(contradiction_rejection, 6),
            "path_drift_index": round(path_drift_index, 6),
            "candidate_edge_count": len(candidate_edges),
            "candidate_node_count": len(candidate_nodes),
            "traversed_edge_count": traversed_edges,
        },
        "stats": {
            "seed_count": len(seeds),
            "initial_seed_count": len(initial_seeds),
            "projected_node_count": len(projected_nodes),
            "projected_edge_count": len(projected_edges),
            "graph_node_count": len(graph.nodes),
            "graph_edge_count": len(graph.edges),
        },
    }

    if _ENABLE_CONFIDENCE:
        from .confidence import compute_structural_confidence

        confidence_block = compute_structural_confidence(
            projection=result,
            full_graph=graph,
            operation_family=operation_family,
        )
        result["confidence"] = confidence_block

    return result
