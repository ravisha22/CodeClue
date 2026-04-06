"""Hybrid clue view renderer: Plan A entity structure + restored semantic content.

Combines:
- Plan A: entity-centric format, role classification, source patterns, risk detection
- Original: calls/called_by (compacted to short IDs), purpose, per-node confidence
- Strips: hashes, bytes, AST paths, density arrays, per-edge arrays, policy/validation metadata
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .behavior_summary import generate_summary
from .role_classifier import classify_projected_nodes
from .source_patterns import scan_projected_nodes
from .models import CanonicalClueGraph


FORBIDDEN_FIELDS = frozenset({
    "per_node_confidence", "per_edge_confidence", "reasoning_path",
    "validation", "policy", "density_indicators", "complexity_indicators",
    "ast_path", "byte_start", "byte_end", "content_hash",
    "tool_call_budget", "threshold", "p_context_miss",
    "p_dependency_miss", "p_hallucination", "code_density_risk",
    "stats", "prompt_profile",
})


def _byte_to_line(source: str, byte_offset: int) -> int:
    return source[:byte_offset].count("\n") + 1


def _select_top_nodes(
    projected_nodes: list[dict[str, Any]],
    max_nodes: int = 15,
) -> list[dict[str, Any]]:
    non_module = [n for n in projected_nodes if n.get("node_type") != "module"]
    modules = [n for n in projected_nodes if n.get("node_type") == "module"]
    sorted_nodes = sorted(non_module, key=lambda n: n.get("confidence", 0), reverse=True)
    result = sorted_nodes[:max_nodes]
    if modules and len(result) < max_nodes:
        result.append(modules[0])
    return result


def render_clue_hybrid(
    projection: dict[str, Any],
    graph: CanonicalClueGraph,
    question: str | None = None,
    repo_root: str | Path = ".",
) -> dict[str, Any]:
    """Render a hybrid clue: Plan A entities + restored semantic content."""
    projected_nodes = projection.get("projected_nodes", [])
    projected_edges = projection.get("projected_edges", [])
    confidence_data = projection.get("confidence", {})
    per_node_conf = {
        pn["node_id"]: pn.get("confidence", 0.5)
        for pn in confidence_data.get("per_node_confidence", [])
    }

    # Select top nodes
    selected = _select_top_nodes(projected_nodes)
    selected_ids = {n["node_id"] for n in selected}

    # Short ID mapping
    id_map: dict[str, str] = {}
    for i, node in enumerate(selected, 1):
        id_map[node["node_id"]] = f"n{i}"

    # Source patterns + role classification
    patterns = scan_projected_nodes(selected, str(repo_root))
    projected_ids = [n["node_id"] for n in selected]
    roles = classify_projected_nodes(graph, projected_ids, source_patterns=patterns)

    # Node name mapping
    node_names: dict[str, str] = {}
    for node in selected:
        sc = node.get("semantic_contract", {})
        node_names[node["node_id"]] = sc.get("symbol_name", node["node_id"])

    # Build entities with RESTORED semantic content
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

        # Behavioral summary (Plan A enrichment)
        behavior = generate_summary(
            node_id=nid, node_type=node.get("node_type", ""),
            symbol_name=sc.get("symbol_name", nid), role=role,
            risks=risks, security_markers=security, sig=sig,
            projected_edges=projected_edges, node_names=node_names,
        )

        # RESTORED: calls/called_by compacted to short IDs
        calls_raw = sc.get("calls", [])
        called_by_raw = sc.get("called_by", [])
        calls = []
        for c in calls_raw:
            target = c.get("target", "") if isinstance(c, dict) else str(c)
            if target in id_map:
                calls.append(id_map[target])
            else:
                # Include the symbol name even if not in selected set
                target_name = ""
                for n2 in projected_nodes:
                    if n2["node_id"] == target:
                        target_name = n2.get("semantic_contract", {}).get("symbol_name", "")
                        break
                if target_name:
                    calls.append(target_name)

        called_by = []
        for c in called_by_raw:
            source = c.get("source", "") if isinstance(c, dict) else str(c)
            if source in id_map:
                called_by.append(id_map[source])
            else:
                for n2 in projected_nodes:
                    if n2["node_id"] == source:
                        source_name = n2.get("semantic_contract", {}).get("symbol_name", "")
                        if source_name:
                            called_by.append(source_name)
                        break

        # RESTORED: purpose from semantic contract
        purpose = sc.get("purpose", "")

        # RESTORED: per-node confidence (real value, not derived weight)
        confidence = per_node_conf.get(nid, node.get("confidence", 0.5))

        # Compute line numbers
        file_path = anchor.get("file_path", "")
        byte_start = anchor.get("byte_start", 0)
        byte_end = anchor.get("byte_end", 0)
        full_source = None
        if file_path:
            fp = Path(repo_root) / file_path
            if fp.is_file():
                try:
                    full_source = fp.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    pass
        if full_source:
            start_line = _byte_to_line(full_source, byte_start)
            end_line = _byte_to_line(full_source, byte_end)
        else:
            start_line, end_line = 1, 1

        entity: dict[str, Any] = {
            "id": short_id,
            "class": role,
            "name": sc.get("symbol_name", nid),
            "file": file_path,
            "lines": [start_line, end_line],
            "confidence": round(confidence, 2),
            "purpose": purpose,
            "behavior": behavior,
        }
        if sig:
            entity["sig"] = sig
        if calls:
            entity["calls"] = calls
        if called_by:
            entity["called_by"] = called_by
        if risks:
            entity["risks"] = risks
        entities.append(entity)

    # Task info
    pp = projection.get("prompt_profile", {}) or {}
    task = {
        "id": projection.get("trace_id", "unknown"),
        "repo": pp.get("repo", ""),
        "family": projection.get("operation_family", ""),
        "question": question or pp.get("question", ""),
    }

    # Summary
    sorted_ents = sorted(entities, key=lambda e: e.get("confidence", 0), reverse=True)
    summary_parts = []
    for ent in sorted_ents[:5]:
        if ent.get("behavior"):
            summary_parts.append(f"{ent['name']}: {ent['behavior']}")
    summary = " ".join(summary_parts[:3]) if summary_parts else ""

    # Uncertainty (RESTORED: real confidence signal)
    overall_conf = confidence_data.get("confidence_overall", 0.5)
    hint = confidence_data.get("lookup_decision_hint", "targeted_lookup")
    uncertainty = {
        "confidence": round(overall_conf, 2),
        "hint": hint,
        "gaps": [],
    }
    # Top 3 gaps from low-confidence entities
    low_ents = [e for e in entities if e.get("confidence", 1) < 0.6]
    for le in low_ents[:3]:
        uncertainty["gaps"].append(f"Low confidence on {le['name']} ({le['confidence']})")

    return {
        "task": task,
        "summary": summary,
        "entities": entities,
        "uncertainty": uncertainty,
    }


def validate_clue_purity(clue: dict[str, Any]) -> tuple[bool, list[str]]:
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
