"""Deterministic one-line behavioral summary generation per node.

Template-based: uses role + signature + source patterns + graph context
to compose a meaningful summary without LLM calls.
"""

from __future__ import annotations

from typing import Any


def _short_name(symbol_name: str) -> str:
    """Get the short name from a qualified symbol name."""
    parts = symbol_name.rsplit(".", 1)
    return parts[-1] if parts else symbol_name


def _callee_names(
    node_id: str,
    projected_edges: list[dict[str, Any]],
    node_names: dict[str, str],
    limit: int = 3,
) -> list[str]:
    """Get short names of callees within the projection."""
    names = []
    for edge in projected_edges:
        if edge.get("edge_type") == "calls" and edge.get("from_node") == node_id:
            target = edge.get("to_node", "")
            name = node_names.get(target, "")
            if name:
                names.append(_short_name(name))
    return names[:limit]


def _caller_names(
    node_id: str,
    projected_edges: list[dict[str, Any]],
    node_names: dict[str, str],
    limit: int = 2,
) -> list[str]:
    """Get short names of callers within the projection."""
    names = []
    for edge in projected_edges:
        if edge.get("edge_type") == "calls" and edge.get("to_node") == node_id:
            source = edge.get("from_node", "")
            name = node_names.get(source, "")
            if name:
                names.append(_short_name(name))
    return names[:limit]


def _risk_clause(risks: list[str]) -> str:
    """Generate a brief risk clause from detected risks."""
    if not risks:
        return ""
    risk_phrases = {
        "exception_swallowed": "exceptions are swallowed",
        "bare_except": "uses bare except",
        "broad_exception_handler": "catches broad exceptions",
        "mutable_default_arg": "has mutable default argument",
        "runs_in_finally": "runs in finally block",
        "implicit_none_return": "may return None implicitly",
        "state_mutation_outside_init": "mutates state outside __init__",
        "sql_injection_risk": "potential SQL injection",
        "path_traversal_risk": "potential path traversal",
    }
    phrases = [risk_phrases.get(r, r) for r in risks[:2]]
    return "; ".join(phrases)


# Role-based summary templates
_ROLE_TEMPLATES: dict[str, str] = {
    "entrypoint": "{action}Entrypoint that {delegates}.",
    "hub": "{action}Hub called by {callers}; delegates to {callees}.",
    "dispatcher": "{action}Dispatcher that routes to {callees}.",
    "error_handler": "{action}Error handler that {handles}.",
    "validator": "{action}Validates {validates}.",
    "data_accessor": "{action}Accesses data via {pattern}.",
    "middleware": "{action}Middleware between {callers} and {callees}.",
    "handler": "{action}Handles {handles}.",
    "utility": "{action}{purpose}.",
    "module_root": "Module containing {children}.",
}


def generate_summary(
    node_id: str,
    node_type: str,
    symbol_name: str,
    role: str,
    risks: list[str],
    security_markers: list[str],
    sig: str,
    projected_edges: list[dict[str, Any]],
    node_names: dict[str, str],
) -> str:
    """Generate a one-line behavioral summary for a node.

    Args:
        node_id: Full node identifier.
        node_type: "function", "class", "module", etc.
        symbol_name: Human-readable name (e.g., "Flask.wsgi_app").
        role: Role from role_classifier (e.g., "entrypoint").
        risks: Risk tags from source_patterns.
        security_markers: Security tags from source_patterns.
        sig: Function signature string.
        projected_edges: Edges in the projection (for callee/caller lookup).
        node_names: Map of node_id → symbol_name for all projected nodes.

    Returns:
        One-line summary string, max ~30 words.
    """
    short = _short_name(symbol_name)
    callees = _callee_names(node_id, projected_edges, node_names)
    callers = _caller_names(node_id, projected_edges, node_names)
    risk_text = _risk_clause(risks)

    # Build action prefix from signature hints
    action = ""
    if "async" in sig.lower():
        action = "Async "

    # Security prefix
    if "has_auth_decorator" in security_markers:
        action += "Auth-protected "

    # Role-specific content
    if role == "entrypoint":
        delegates = ", ".join(callees) if callees else "downstream handlers"
        summary = f"{action}Entrypoint that delegates to {delegates}."

    elif role == "hub":
        caller_str = ", ".join(callers) if callers else "multiple callers"
        callee_str = ", ".join(callees) if callees else "multiple targets"
        summary = f"{action}Hub called by {caller_str}; routes to {callee_str}."

    elif role == "dispatcher":
        callee_str = ", ".join(callees) if callees else "registered handlers"
        summary = f"{action}Dispatcher that routes to {callee_str}."

    elif role == "error_handler":
        callee_str = ", ".join(callees) if callees else "error response"
        summary = f"{action}Error handler; produces {callee_str}."

    elif role == "validator":
        summary = f"{action}Validates input before processing."

    elif role == "data_accessor":
        summary = f"{action}Accesses data store."

    elif role == "middleware":
        caller_str = ", ".join(callers) if callers else "upstream"
        callee_str = ", ".join(callees) if callees else "downstream"
        summary = f"{action}Middleware between {caller_str} and {callee_str}."

    elif role == "handler":
        caller_str = ", ".join(callers) if callers else "dispatcher"
        summary = f"{action}Leaf handler invoked by {caller_str}."

    elif role == "module_root":
        child_count = sum(
            1 for e in projected_edges
            if e.get("edge_type") == "contains" and e.get("from_node") == node_id
        )
        summary = f"Module containing {child_count} projected symbol(s)."

    else:
        # utility / fallback
        summary = f"{action}{node_type.capitalize()} {short}."

    # Append risk clause if present
    if risk_text:
        summary = summary.rstrip(".") + f"; {risk_text}."

    # Truncate to ~40 words max
    words = summary.split()
    if len(words) > 40:
        summary = " ".join(words[:40]) + "..."

    return summary
