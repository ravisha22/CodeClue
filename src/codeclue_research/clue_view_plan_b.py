"""Plan B: Flat table clue view renderer with separate relations and assertions.

Nodes, relations, and assertions are in separate arrays.
The consumer LLM must cross-reference node IDs across tables.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .behavior_summary import generate_summary
from .role_classifier import classify_projected_nodes
from .source_patterns import scan_projected_nodes
from .models import CanonicalClueGraph


# Same forbidden fields as Plan A
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
    return source[:byte_offset].count("\n") + 1


def _extract_task_info(projection: dict[str, Any], question: str | None) -> dict[str, Any]:
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
    """Select top projected nodes by confidence, capped adaptively."""
    non_module = [n for n in projected_nodes if n.get("node_type") != "module"]
    modules = [n for n in projected_nodes if n.get("node_type") == "module"]
    sorted_nodes = sorted(
        non_module,
        key=lambda n: n.get("confidence", 0),
        reverse=True,
    )
    result = sorted_nodes[:max_nodes]
    if modules and len(result) < max_nodes:
        result.append(modules[0])
    return result


def _generate_system_behavior(
    nodes_table: list[dict[str, Any]],
    relations_table: list[dict[str, Any]],
    question: str,
) -> list[str]:
    """Generate 3-5 system behavior sentences from nodes and relations."""
    sentences: list[str] = []
    # Describe top 3-5 nodes by importance
    sorted_nodes = sorted(nodes_table, key=lambda n: n.get("importance", 99))
    for node in sorted_nodes[:5]:
        name = node.get("name", "")
        behavior = node.get("summary", "")
        if behavior:
            sentences.append(f"{name}: {behavior}")
    return sentences[:5]


def _generate_assertions(
    nodes_table: list[dict[str, Any]],
    relations_table: list[dict[str, Any]],
    node_risks: dict[str, list[str]],
) -> list[dict[str, Any]]:
    """Generate path-based behavioral assertions from topology + risks."""
    assertions: list[dict[str, Any]] = []
    node_name_map = {n["id"]: n["name"] for n in nodes_table}

    # Build path chains from relations
    outgoing: dict[str, list[str]] = {}
    for rel in relations_table:
        src = rel.get("from", "")
        tgt = rel.get("to", "")
        outgoing.setdefault(src, []).append(tgt)

    # Generate assertions for paths involving risky nodes
    for node in nodes_table:
        nid = node["id"]
        risks = node_risks.get(nid, [])

        if "runs_in_finally" in risks:
            # Find who calls this node
            callers = [r["from"] for r in relations_table if r.get("to") == nid]
            for caller in callers[:1]:
                assertions.append({
                    "path": [caller, nid],
                    "fact": f"{node_name_map.get(nid, nid)} runs unconditionally (in finally block) regardless of success/failure in {node_name_map.get(caller, caller)}.",
                })

        if "exception_swallowed" in risks or "bare_except" in risks:
            assertions.append({
                "path": [nid],
                "fact": f"{node_name_map.get(nid, nid)} may suppress exceptions silently.",
            })

        if "broad_exception_handler" in risks:
            assertions.append({
                "path": [nid],
                "fact": f"{node_name_map.get(nid, nid)} catches broad exceptions; specific errors may be masked.",
            })

    # Generate assertions for call chains (top 2 longest paths)
    for node in sorted(nodes_table, key=lambda n: n.get("importance", 99))[:2]:
        nid = node["id"]
        targets = outgoing.get(nid, [])
        if len(targets) >= 2:
            path = [nid] + targets[:3]
            names = [node_name_map.get(p, p) for p in path]
            assertions.append({
                "path": path,
                "fact": f"Call chain: {' → '.join(names)}.",
            })

    return assertions[:5]  # Cap at 5


def render_clue_plan_b(
    projection: dict[str, Any],
    graph: CanonicalClueGraph,
    question: str | None = None,
    repo_root: str | Path = ".",
) -> dict[str, Any]:
    """Render a flat-table clue view with separate nodes, relations, and assertions.

    Args:
        projection: Output of project_operation().
        graph: Full canonical clue graph.
        question: The task question text.
        repo_root: Path to the repo root.

    Returns:
        Flat-table clue artifact (Plan B schema).
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

    # Step 5: Node name mapping
    node_names: dict[str, str] = {}
    for node in selected:
        nid = node["node_id"]
        sc = node.get("semantic_contract", {})
        node_names[nid] = sc.get("symbol_name", nid)

    # Step 6: Build nodes table
    nodes_table: list[dict[str, Any]] = []
    node_risks: dict[str, list[str]] = {}  # short_id → risks

    for i, node in enumerate(selected):
        nid = node["node_id"]
        short_id = id_map[nid]
        sc = node.get("semantic_contract", {})
        anchor = node.get("source_anchor", {})
        pat = patterns.get(nid, {})
        role = roles.get(nid, "utility")
        risks = pat.get("risks", [])
        security = pat.get("security_markers", [])
        sig = pat.get("sig", "")

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

        # Compute line numbers
        file_path = anchor.get("file_path", "")
        byte_start = anchor.get("byte_start", 0)
        byte_end = anchor.get("byte_end", 0)
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

        node_entry: dict[str, Any] = {
            "id": short_id,
            "type": node.get("node_type", ""),
            "name": sc.get("symbol_name", nid),
            "summary": behavior,
            "file": file_path,
            "lines": [start_line, end_line],
            "importance": i + 1,
            "role": role,
        }
        if sig:
            node_entry["sig"] = sig
        if risks:
            node_entry["risks"] = risks
        nodes_table.append(node_entry)
        node_risks[short_id] = risks

    # Step 7: Build relations table
    relations_table: list[dict[str, Any]] = []
    for edge in projected_edges:
        from_n = edge.get("from_node", "")
        to_n = edge.get("to_node", "")
        if from_n in selected_ids and to_n in selected_ids:
            etype = edge.get("edge_type", "calls")
            rel: dict[str, Any] = {
                "type": etype,
                "from": id_map[from_n],
                "to": id_map[to_n],
            }
            # Add note for important relations
            if etype == "calls":
                from_name = node_names.get(from_n, "")
                to_name = node_names.get(to_n, "")
                if from_name and to_name:
                    rel["note"] = f"{from_name.rsplit('.', 1)[-1]} calls {to_name.rsplit('.', 1)[-1]}"
            relations_table.append(rel)

    # Step 8: Generate assertions
    assertions = _generate_assertions(nodes_table, relations_table, node_risks)

    # Step 9: Clue summary
    q = question or ""
    system_behavior = _generate_system_behavior(nodes_table, relations_table, q)
    key_files = sorted({n["file"] for n in nodes_table if n["file"]})
    key_symbols = [n["name"] for n in sorted(nodes_table, key=lambda n: n["importance"])[:5]
                   if n["type"] != "module"]

    # Risk summary for TF4/TF5
    all_risks = [r for n in nodes_table for r in n.get("risks", [])]
    risk_summary = ""
    if all_risks:
        unique_risks = list(dict.fromkeys(all_risks))[:3]
        risk_summary = f"Detected risks: {', '.join(unique_risks)}."

    clue_summary = {
        "system_behavior": system_behavior,
        "key_files": key_files,
        "key_symbols": key_symbols,
    }
    if risk_summary:
        clue_summary["risk_summary"] = risk_summary

    # Step 10: Uncertainty
    overall_conf = confidence_data.get("confidence_overall", 0.5)
    hint = confidence_data.get("lookup_decision_hint", "targeted_lookup")
    per_node = confidence_data.get("per_node_confidence", [])
    low_conf = sorted(
        [n for n in per_node if n.get("confidence", 1.0) < 0.6],
        key=lambda n: n.get("confidence", 1.0),
    )
    gaps = []
    for lcn in low_conf[:3]:
        actions = lcn.get("suggested_actions", [])
        if actions:
            gaps.append(actions[0].get("rationale", "Low confidence node.")[:100])
        else:
            gaps.append(f"Low confidence on {lcn.get('node_id', 'unknown')[:50]}.")

    uncertainty = {
        "overall_confidence": round(overall_conf, 2),
        "lookup_hint": hint,
        "known_gaps": gaps,
    }

    return {
        "task": _extract_task_info(projection, question),
        "clue_summary": clue_summary,
        "nodes": nodes_table,
        "relations": relations_table,
        "assertions": assertions,
        "uncertainty": uncertainty,
    }


def validate_clue_purity(clue: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate that no forbidden fields leaked into the clue artifact."""
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
