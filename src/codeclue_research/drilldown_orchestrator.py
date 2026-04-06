"""Confidence-gated drill-down orchestrator.

Only triggers drill-down when confidence is below threshold.
Uses direct function calls to MCP tools (not protocol-level).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from codeclue_mcp.tools import code_slice, resolve_dependency, fetch_contract
from codeclue_mcp.budget import BudgetTracker
from .token_counter import count_tokens
from .models import CanonicalClueGraph


def _identify_gaps(clue: dict[str, Any], plan: str) -> list[dict[str, Any]]:
    """Identify gaps from the clue's uncertainty block."""
    gaps_info: list[dict[str, Any]] = []

    if plan == "a":
        # Plan A: entities with risks or low weight
        for entity in clue.get("entities", []):
            if entity.get("risks"):
                gaps_info.append({
                    "node_name": entity.get("name", ""),
                    "file": entity.get("file", ""),
                    "lines": entity.get("lines", [1, 50]),
                    "reason": f"Has risks: {', '.join(entity['risks'][:2])}",
                })
            elif entity.get("weight", 1.0) < 0.3:
                gaps_info.append({
                    "node_name": entity.get("name", ""),
                    "file": entity.get("file", ""),
                    "lines": entity.get("lines", [1, 50]),
                    "reason": "Low weight / low confidence",
                })
    elif plan == "b":
        # Plan B: nodes with risks or uncertain assertions
        for node in clue.get("nodes", []):
            if node.get("risks"):
                gaps_info.append({
                    "node_name": node.get("name", ""),
                    "file": node.get("file", ""),
                    "lines": node.get("lines", [1, 50]),
                    "reason": f"Has risks: {', '.join(node['risks'][:2])}",
                })

    # Also use uncertainty.gaps
    unc = clue.get("uncertainty", {})
    for gap_text in unc.get("gaps", unc.get("known_gaps", []))[:3]:
        gaps_info.append({
            "node_name": "",
            "file": "",
            "lines": [1, 50],
            "reason": gap_text,
        })

    return gaps_info[:5]  # Cap at 5 gaps


def run_gated_drilldown(
    clue: dict[str, Any],
    plan: str,
    graph: CanonicalClueGraph,
    repo_root: str | Path,
    confidence_threshold: float = 0.60,
    operation_family: str = "OF2",
) -> dict[str, Any]:
    """Execute confidence-gated drill-down on a clue artifact.

    Args:
        clue: Compact clue artifact (Plan A or Plan B).
        plan: "a" or "b".
        graph: Full canonical clue graph.
        repo_root: Path to repo root.
        confidence_threshold: Min confidence to skip drill-down.
        operation_family: For budget allocation.

    Returns:
        Dict with drill-down results and metrics.
    """
    # Check confidence
    unc = clue.get("uncertainty", {})
    confidence = unc.get("confidence", unc.get("overall_confidence", 0.5))

    if confidence >= confidence_threshold:
        return {
            "drilldown_triggered": False,
            "confidence": confidence,
            "tools_used": [],
            "drilldown_results": [],
            "drilldown_tokens": 0,
        }

    # Drill-down needed
    tracker = BudgetTracker(operation_family)
    gaps = _identify_gaps(clue, plan)
    repo_str = str(repo_root)

    tools_used: list[dict[str, Any]] = []
    drilldown_results: list[dict[str, Any]] = []

    for gap in gaps:
        if not tracker.can_call():
            break

        file_path = gap.get("file", "")
        lines = gap.get("lines", [1, 50])
        node_name = gap.get("node_name", "")

        # Strategy: prefer code_slice for source detail
        if file_path and lines:
            tracker.record_call("code_slice", node_name)
            result = code_slice(
                repo_root=repo_str,
                file_path=file_path,
                start_line=lines[0],
                end_line=min(lines[1], lines[0] + 50),  # Cap at 50 lines
            )
            tools_used.append({"tool": "code_slice", "file": file_path, "lines": lines})
            drilldown_results.append(result)

        # If we have a node_id match in the graph, try fetch_contract
        elif node_name and tracker.can_call():
            # Find matching node
            matching = [n for n in graph.nodes if node_name in n.node_id or
                        node_name == n.semantic_contract.get("symbol_name", "")]
            if matching:
                tracker.record_call("fetch_contract", matching[0].node_id)
                result = fetch_contract(graph, matching[0].node_id)
                tools_used.append({"tool": "fetch_contract", "node": matching[0].node_id})
                drilldown_results.append(result)

    total_tokens = sum(count_tokens(r) for r in drilldown_results)

    return {
        "drilldown_triggered": True,
        "confidence": confidence,
        "tools_used": tools_used,
        "drilldown_results": drilldown_results,
        "drilldown_tokens": total_tokens,
        "calls_made": len(tools_used),
        "budget_remaining": tracker.remaining(),
    }
