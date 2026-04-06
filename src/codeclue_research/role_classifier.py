"""Topology-based role classification for projected nodes.

Uses graph structure (fan-in, fan-out, dominator sets, reachability)
to assign semantic roles without LLM calls.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import CanonicalClueGraph


# Role definitions (priority order — first match wins)
ROLE_ENTRYPOINT = "entrypoint"
ROLE_HUB = "hub"
ROLE_DISPATCHER = "dispatcher"
ROLE_ERROR_HANDLER = "error_handler"
ROLE_VALIDATOR = "validator"
ROLE_DATA_ACCESSOR = "data_accessor"
ROLE_MIDDLEWARE = "middleware"
ROLE_HANDLER = "handler"
ROLE_UTILITY = "utility"
ROLE_MODULE = "module_root"

ALL_ROLES = [
    ROLE_ENTRYPOINT,
    ROLE_HUB,
    ROLE_DISPATCHER,
    ROLE_ERROR_HANDLER,
    ROLE_VALIDATOR,
    ROLE_DATA_ACCESSOR,
    ROLE_MIDDLEWARE,
    ROLE_HANDLER,
    ROLE_UTILITY,
    ROLE_MODULE,
]

# Patterns for name-based classification hints
_ERROR_NAMES = {"handle_exception", "handle_error", "error_handler", "on_error",
                "handle_user_exception", "handle_http_exception", "exception_handler"}
_VALIDATOR_NAMES = {"validate", "sanitize", "check", "verify", "clean", "is_valid"}
_DATA_NAMES = {"query", "execute", "fetch", "insert", "update", "delete", "save",
               "find", "get_db", "session", "cursor", "commit", "rollback"}


def _compute_fan(
    graph: CanonicalClueGraph,
    projected_ids: set[str],
) -> tuple[dict[str, int], dict[str, int]]:
    """Compute fan-in and fan-out for projected nodes within the projection subgraph."""
    fan_in: dict[str, int] = defaultdict(int)
    fan_out: dict[str, int] = defaultdict(int)

    for edge in graph.edges:
        if edge.from_node in projected_ids and edge.to_node in projected_ids:
            fan_out[edge.from_node] += 1
            fan_in[edge.to_node] += 1

    # Ensure all projected nodes have entries
    for nid in projected_ids:
        fan_in.setdefault(nid, 0)
        fan_out.setdefault(nid, 0)

    return dict(fan_in), dict(fan_out)


def _name_hint(symbol_name: str) -> str | None:
    """Return a role hint based on naming conventions."""
    lower = symbol_name.lower()
    parts = set(lower.replace(".", "_").replace("-", "_").split("_"))

    if parts & _ERROR_NAMES or "exception" in lower or "error" in lower:
        return ROLE_ERROR_HANDLER
    if parts & _VALIDATOR_NAMES:
        return ROLE_VALIDATOR
    if parts & _DATA_NAMES:
        return ROLE_DATA_ACCESSOR
    return None


def classify_projected_nodes(
    graph: CanonicalClueGraph,
    projected_node_ids: list[str],
    source_patterns: dict[str, dict[str, Any]] | None = None,
) -> dict[str, str]:
    """Classify each projected node into a semantic role.

    Args:
        graph: Full canonical clue graph.
        projected_node_ids: Node IDs in the projection.
        source_patterns: Optional output from source_patterns.scan_projected_nodes().

    Returns:
        Dict mapping node_id → role label.
    """
    projected_set = set(projected_node_ids)
    node_map = {n.node_id: n for n in graph.nodes}
    fan_in, fan_out = _compute_fan(graph, projected_set)
    source_patterns = source_patterns or {}

    roles: dict[str, str] = {}

    for nid in projected_node_ids:
        node = node_map.get(nid)
        if node is None:
            roles[nid] = ROLE_UTILITY
            continue

        # Module roots
        if node.node_type == "module":
            roles[nid] = ROLE_MODULE
            continue

        fi = fan_in.get(nid, 0)
        fo = fan_out.get(nid, 0)
        symbol_name = node.semantic_contract.get("symbol_name", "")
        patterns = source_patterns.get(nid, {})
        risks = patterns.get("risks", [])
        security = patterns.get("security_markers", [])

        # Name-based hint (strong signal)
        name_role = _name_hint(symbol_name)

        # Classification logic (priority order)
        if name_role == ROLE_ERROR_HANDLER or any("exception" in r for r in risks):
            roles[nid] = ROLE_ERROR_HANDLER
        elif name_role == ROLE_VALIDATOR or "has_input_validation" in security or "has_auth_decorator" in security:
            roles[nid] = ROLE_VALIDATOR
        elif name_role == ROLE_DATA_ACCESSOR:
            roles[nid] = ROLE_DATA_ACCESSOR
        elif fi == 0 and fo > 0:
            # No callers in projection, has callees → entrypoint
            roles[nid] = ROLE_ENTRYPOINT
        elif fo >= 3:
            # High fan-out → dispatcher
            roles[nid] = ROLE_DISPATCHER
        elif fi >= 5:
            # High fan-in → hub (many callers)
            roles[nid] = ROLE_HUB
        elif fi > 0 and fo == 0:
            # Has callers, no callees → leaf handler
            roles[nid] = ROLE_HANDLER
        elif fi > 0 and fo > 0 and fi <= 2 and fo <= 2:
            # On a path, moderate connectivity → middleware
            roles[nid] = ROLE_MIDDLEWARE
        else:
            roles[nid] = ROLE_UTILITY

    return roles
