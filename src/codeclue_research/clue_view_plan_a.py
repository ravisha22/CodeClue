"""Plan A: Entity-centric clue view renderer.

Each entity is a self-contained object with class, weight, behavior,
inflow/outflow, risks, and invariants — zero cross-referencing needed.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .behavior_summary import generate_summary
from .role_classifier import classify_projected_nodes
from .source_patterns import scan_projected_nodes
from .models import CanonicalClueGraph


# Forbidden fields that must NEVER appear in the clue artifact
FORBIDDEN_FIELDS = frozenset({
    "per_node_confidence",
    "per_edge_confidence",
    "reasoning_path",
    "validation",
    "policy",
    "suggested_actions",
    "rationale",
    "density_indicators",
    "complexity_indicators",
    "ast_path",
    "byte_start",
    "byte_end",
    "content_hash",
    "tool_call_budget",
    "threshold",
    "p_context_miss",
    "p_dependency_miss",
    "p_hallucination",
    "code_density_risk",
    "stats",
    "prompt_profile",
})


def _byte_to_line(source: str, byte_offset: int) -> int:
    """Convert byte offset to 1-based line number."""
    return source[:byte_offset].count("\n") + 1


def _extract_task_info(projection: dict[str, Any], question: str | None) -> dict[str, Any]:
    """Build the task header from projection metadata."""
    pp = projection.get("prompt_profile", {}) or {}
    return {
        "id": projection.get("trace_id", "unknown"),
        "repo": pp.get("repo", ""),
        "family": projection.get("operation_family", ""),
        "operation_family": projection.get("operation_family", ""),
        "question": question or pp.get("question", ""),
    }


def _select_top_nodes(
    projected_nodes: list[dict[str, Any]],
    max_nodes: int = 15,
) -> list[dict[str, Any]]:
    """Select top projected nodes by confidence, capped adaptively.

    Filters out module nodes (low semantic value) and caps at min(max_nodes, projected).
    """
    # Prefer non-module nodes (modules add tokens but little semantic value for LLMs)
    non_module = [n for n in projected_nodes if n.get("node_type") != "module"]
    modules = [n for n in projected_nodes if n.get("node_type") == "module"]

    sorted_nodes = sorted(
        non_module,
        key=lambda n: n.get("confidence", 0),
        reverse=True,
    )
    # Include at most 1 module for context, only if we have room
    result = sorted_nodes[:max_nodes]
    if modules and len(result) < max_nodes:
        result.append(modules[0])
    return result


def _build_edge_index(
    projected_edges: list[dict[str, Any]],
    selected_ids: set[str],
) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
    """Build inflow/outflow indexes for selected nodes only."""
    inflow: dict[str, list[dict]] = {nid: [] for nid in selected_ids}
    outflow: dict[str, list[dict]] = {nid: [] for nid in selected_ids}

    for edge in projected_edges:
        from_n = edge.get("from_node", "")
        to_n = edge.get("to_node", "")
        etype = edge.get("edge_type", "calls")
        evidence = edge.get("evidence", {})

        if from_n in selected_ids and to_n in selected_ids:
            outflow[from_n].append({
                "to": to_n,  # Will be replaced with short ID later
                "via": etype,
                "_raw_to": to_n,
            })
            inflow[to_n].append({
                "from": from_n,  # Will be replaced with short ID later
                "via": etype,
                "_raw_from": from_n,
            })

    return inflow, outflow


def _derive_flow_details(
    node_id: str,
    flows: list[dict],
    source_patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Enrich flow entries with 'carries' and 'condition' from patterns."""
    enriched = []
    patterns = source_patterns.get(node_id, {})
    risks = patterns.get("risks", [])

    for flow in flows:
        entry: dict[str, Any] = {}
        # Copy direction fields
        if "from" in flow:
            entry["from"] = flow["from"]
        if "to" in flow:
            entry["to"] = flow["to"]
        entry["via"] = flow.get("via", "calls")

        # Derive condition from risks
        if "runs_in_finally" in risks:
            entry["condition"] = "unconditional"
        elif flow.get("via") == "calls":
            entry["condition"] = "normal"

        enriched.append(entry)
    return enriched


def _generate_invariants(
    node_id: str,
    role: str,
    risks: list[str],
    outflow: list[dict],
    node_names: dict[str, str],
) -> list[str]:
    """Generate behavioral invariants from patterns and topology."""
    invariants: list[str] = []

    if "runs_in_finally" in risks:
        invariants.append("Executes unconditionally (in finally block).")

    if "exception_swallowed" in risks or "bare_except" in risks:
        invariants.append("May suppress exceptions silently.")

    if "broad_exception_handler" in risks:
        invariants.append("Catches broad exceptions; specific errors may be masked.")

    if role == "entrypoint" and outflow:
        targets = [node_names.get(f.get("_raw_to", ""), "") for f in outflow if f.get("_raw_to")]
        if targets:
            invariants.append(f"Entry point; all request paths flow through here.")

    if "state_mutation_outside_init" in risks:
        invariants.append("Mutates instance state outside constructor.")

    if "mutable_default_arg" in risks:
        invariants.append("Uses mutable default argument (shared across calls).")

    return invariants[:3]  # Cap at 3


def _generate_task_summary(
    entities: list[dict[str, Any]],
    question: str,
) -> str:
    """Generate a task-level behavioral narrative from entities."""
    # Find key entities by weight
    sorted_ents = sorted(entities, key=lambda e: e.get("weight", 0), reverse=True)
    top = sorted_ents[:5]

    parts = []
    for ent in top:
        behavior = ent.get("behavior", "")
        name = ent.get("name", "")
        if behavior:
            parts.append(f"{name}: {behavior}")

    if not parts:
        return "Insufficient entity data for summary."

    # Join the top behaviors into a concise narrative
    return " ".join(parts[:3])


def render_clue_plan_a(
    projection: dict[str, Any],
    graph: CanonicalClueGraph,
    question: str | None = None,
    repo_root: str | Path = ".",
) -> dict[str, Any]:
    """Render an entity-centric clue view from a projection result.

    Args:
        projection: Output of project_operation() (the verbose projection dict).
        graph: Full canonical clue graph.
        question: The task question text.
        repo_root: Path to the repo root for source file reading.

    Returns:
        Entity-centric clue artifact (Plan A schema).
    """
    projected_nodes = projection.get("projected_nodes", [])
    projected_edges = projection.get("projected_edges", [])
    confidence_data = projection.get("confidence", {})

    # Step 1: Select top nodes
    selected = _select_top_nodes(projected_nodes)
    selected_ids = {n["node_id"] for n in selected}

    # Step 2: Short ID mapping
    id_map: dict[str, str] = {}
    for i, node in enumerate(selected, 1):
        id_map[node["node_id"]] = f"n{i}"

    # Step 3: Source pattern scanning
    patterns = scan_projected_nodes(selected, str(repo_root))

    # Step 4: Role classification
    projected_ids = [n["node_id"] for n in selected]
    roles = classify_projected_nodes(graph, projected_ids, source_patterns=patterns)

    # Step 5: Build edge indexes
    inflow_idx, outflow_idx = _build_edge_index(projected_edges, selected_ids)

    # Step 6: Node name mapping for summary generation
    node_names: dict[str, str] = {}
    for node in selected:
        nid = node["node_id"]
        sc = node.get("semantic_contract", {})
        node_names[nid] = sc.get("symbol_name", nid)

    # Step 7: Build entities
    entities: list[dict[str, Any]] = []
    for node in selected:
        nid = node["node_id"]
        short_id = id_map[nid]
        sc = node.get("semantic_contract", {})
        anchor = node.get("source_anchor", {})
        pat = patterns.get(nid, {})
        role = roles.get(nid, "utility")
        risks = pat.get("risks", [])
        security = pat.get("security_markers", [])
        sig = pat.get("sig", "")

        # Generate behavioral summary
        behavior = generate_summary(
            node_id=nid,
            node_type=node.get("node_type", ""),
            symbol_name=sc.get("symbol_name", nid),
            role=role,
            risks=risks,
            security_markers=security,
            sig=sig,
            projected_edges=projected_edges,
            node_names=node_names,
        )

        # Build inflow/outflow with short IDs
        raw_inflow = inflow_idx.get(nid, [])
        raw_outflow = outflow_idx.get(nid, [])

        inflow_enriched = _derive_flow_details(nid, raw_inflow, patterns)
        outflow_enriched = _derive_flow_details(nid, raw_outflow, patterns)

        # Replace raw IDs with short IDs
        for flow in inflow_enriched:
            raw_from = flow.pop("_raw_from", flow.get("from", ""))
            flow["from"] = id_map.get(raw_from, raw_from)

        for flow in outflow_enriched:
            raw_to = flow.pop("_raw_to", flow.get("to", ""))
            flow["to"] = id_map.get(raw_to, raw_to)

        # Generate invariants
        invariants = _generate_invariants(
            nid, role, risks, raw_outflow, node_names,
        )

        # Compute weight: confidence × importance rank
        conf = node.get("confidence", 0.5)
        importance_rank = selected.index(node) + 1
        weight = round(conf * (1.0 - (importance_rank - 1) / max(len(selected), 1)), 2)

        # Compute line numbers from byte offsets
        file_path = anchor.get("file_path", "")
        byte_start = anchor.get("byte_start", 0)
        byte_end = anchor.get("byte_end", 0)

        # Approximate lines
        full_source = None
        if file_path:
            full_path = Path(repo_root) / file_path
            if full_path.is_file():
                try:
                    full_source = full_path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    pass

        if full_source:
            start_line = _byte_to_line(full_source, byte_start)
            end_line = _byte_to_line(full_source, byte_end)
        else:
            start_line = 1
            end_line = 1

        entity: dict[str, Any] = {
            "id": short_id,
            "class": role,
            "name": sc.get("symbol_name", nid),
            "file": file_path,
            "lines": [start_line, end_line],
            "weight": weight,
            "behavior": behavior,
        }
        # Only include non-empty optional fields to save tokens
        if sig:
            entity["sig"] = sig
        if inflow_enriched:
            entity["inflow"] = inflow_enriched
        if outflow_enriched:
            entity["outflow"] = outflow_enriched
        if risks:
            entity["risks"] = risks
        if invariants:
            entity["invariants"] = invariants
        entities.append(entity)

    # Step 8: Task info and summary
    task = _extract_task_info(projection, question)
    summary = _generate_task_summary(entities, question or "")

    # Step 9: Uncertainty
    overall_conf = confidence_data.get("confidence_overall", 0.5)
    hint = confidence_data.get("lookup_decision_hint", "targeted_lookup")
    # Extract top 3 gaps from per_node_confidence (low-conf nodes)
    per_node = confidence_data.get("per_node_confidence", [])
    low_conf_nodes = sorted(
        [n for n in per_node if n.get("confidence", 1.0) < 0.6],
        key=lambda n: n.get("confidence", 1.0),
    )
    gaps = []
    for lcn in low_conf_nodes[:3]:
        actions = lcn.get("suggested_actions", [])
        if actions:
            gaps.append(actions[0].get("rationale", "Low confidence node.")[:100])
        else:
            gaps.append(f"Low confidence on {lcn.get('node_id', 'unknown')[:50]}.")

    uncertainty = {
        "confidence": round(overall_conf, 2),
        "hint": hint,
        "gaps": gaps,
    }

    return {
        "task": task,
        "summary": summary,
        "entities": entities,
        "uncertainty": uncertainty,
    }


def validate_clue_purity(clue: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate that no forbidden fields leaked into the clue artifact.

    Returns:
        (passed, violations) — passed is True if no violations found.
    """
    violations: list[str] = []

    def _check(obj: Any, path: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_path = f"{path}.{key}" if path else key
                if key in FORBIDDEN_FIELDS:
                    violations.append(f"Forbidden field '{key}' at {full_path}")
                _check(value, full_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _check(item, f"{path}[{i}]")

    _check(clue)
    return (len(violations) == 0, violations)
