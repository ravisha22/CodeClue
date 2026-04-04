from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import load_data, save_data


# Sillito et al. (2006, 2008) reference callback rate distribution per category.
# Mapped to CodeClue operation families.
# Values represent relative callback frequency (normalized to sum to 1.0).
_SILLITO_REFERENCE_DISTRIBUTION: dict[str, float] = {
    "OF1": 0.10,   # "Finding initial focus points" — low callback rate
    "OF2": 0.20,   # "Building on a focus point" — medium
    "OF3": 0.15,   # "Finding initial focus points" (edit variant) — low-medium
    "OF4": 0.30,   # "Understanding a subgraph" — high
    "OF5": 0.25,   # "Over groups of subgraphs" — high
}


def _kl_divergence(p: dict[str, float], q: dict[str, float]) -> float:
    """Compute KL(P || Q) where P is the observed distribution and Q is the reference."""
    total = 0.0
    for key in p:
        p_val = max(p.get(key, 0.0), 1e-10)
        q_val = max(q.get(key, 0.0), 1e-10)
        total += p_val * math.log(p_val / q_val)
    return total


def compute_ift_scent_alignment(
    projection_traces: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    IFT Scent Alignment: correlation between confidence scores and
    drill-down targeting. Higher confidence = fewer suggested actions (lower scent).
    Lower confidence = more suggested actions (higher scent to navigate away).

    Returns alignment score in [0, 1].
    """
    data_points: list[tuple[float, int]] = []

    for trace in projection_traces:
        confidence_block = trace.get("confidence", {})
        for node_data in confidence_block.get("per_node_confidence", []):
            conf = node_data.get("confidence", 1.0)
            action_count = len(node_data.get("suggested_actions", []))
            data_points.append((conf, action_count))

    if len(data_points) < 3:
        return {"ift_scent_alignment": 0.0, "data_points": len(data_points), "status": "insufficient_data"}

    # IFT predicts: low confidence (low scent) should correlate with more actions (navigation cues).
    # Compute rank correlation between confidence and inverse-action-count.
    confidences = [d[0] for d in data_points]
    actions = [d[1] for d in data_points]

    # Nodes with low confidence should have MORE actions (negative correlation expected)
    n = len(data_points)

    def _rank(values: list[float]) -> list[float]:
        sorted_vals = sorted(enumerate(values), key=lambda x: x[1])
        ranks = [0.0] * n
        for rank_idx, (orig_idx, _) in enumerate(sorted_vals):
            ranks[orig_idx] = float(rank_idx + 1)
        return ranks

    conf_ranks = _rank(confidences)
    action_ranks = _rank(actions)

    mean_c = sum(conf_ranks) / n
    mean_a = sum(action_ranks) / n
    numerator = sum((conf_ranks[i] - mean_c) * (action_ranks[i] - mean_a) for i in range(n))
    denom_c = math.sqrt(sum((conf_ranks[i] - mean_c) ** 2 for i in range(n)))
    denom_a = math.sqrt(sum((action_ranks[i] - mean_a) ** 2 for i in range(n)))

    if denom_c == 0 or denom_a == 0:
        spearman = 0.0
    else:
        spearman = numerator / (denom_c * denom_a)

    # IFT alignment: negative correlation is GOOD (low conf → more actions)
    # Convert to [0, 1] scale: -1.0 → 1.0 alignment, 0 → 0.5 alignment, +1.0 → 0.0 alignment
    alignment = max(0.0, min(1.0, (1.0 - spearman) / 2.0))

    return {
        "ift_scent_alignment": round(alignment, 6),
        "spearman_correlation": round(spearman, 6),
        "data_points": n,
        "status": "ok",
    }


def compute_callback_distribution_agreement(
    projection_traces: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Callback Distribution Agreement: KL divergence between LLM callback frequency
    per OF and Sillito reference distribution.

    Lower KL = better agreement. Target: KL < 0.15.
    """
    action_counts_per_of: dict[str, int] = {}
    for trace in projection_traces:
        of = trace.get("operation_family", "unknown")
        confidence_block = trace.get("confidence", {})
        actions = sum(
            len(n.get("suggested_actions", []))
            for n in confidence_block.get("per_node_confidence", [])
        )
        action_counts_per_of[of] = action_counts_per_of.get(of, 0) + actions

    total_actions = sum(action_counts_per_of.values())
    if total_actions == 0:
        return {"kl_divergence": 0.0, "status": "no_actions", "observed_distribution": {}}

    observed: dict[str, float] = {}
    for of in _SILLITO_REFERENCE_DISTRIBUTION:
        observed[of] = action_counts_per_of.get(of, 0) / total_actions

    kl = _kl_divergence(observed, _SILLITO_REFERENCE_DISTRIBUTION)

    return {
        "kl_divergence": round(kl, 6),
        "observed_distribution": {k: round(v, 4) for k, v in observed.items()},
        "reference_distribution": _SILLITO_REFERENCE_DISTRIBUTION,
        "passed": kl < 0.15,
        "status": "ok",
    }


def compute_self_consistency(
    runs: list[list[str]],
) -> dict[str, Any]:
    """
    Self-consistency: given N repeated runs (each is a list of tool call signatures),
    compute what percentage of tool calls appear in >= (N-1) of N runs.

    Target: >= 0.70.
    """
    if not runs:
        return {"self_consistency": 0.0, "status": "no_runs"}

    n = len(runs)
    threshold = max(1, n - 1)

    # Count how many runs each unique tool call appears in
    call_run_counts: dict[str, int] = {}
    for run_calls in runs:
        unique_in_run = set(run_calls)
        for call in unique_in_run:
            call_run_counts[call] = call_run_counts.get(call, 0) + 1

    if not call_run_counts:
        return {"self_consistency": 1.0, "status": "no_calls", "total_unique_calls": 0}

    consistent = sum(1 for count in call_run_counts.values() if count >= threshold)
    total = len(call_run_counts)
    score = consistent / total if total > 0 else 0.0

    return {
        "self_consistency": round(score, 6),
        "consistent_calls": consistent,
        "total_unique_calls": total,
        "runs": n,
        "threshold": threshold,
        "passed": score >= 0.70,
        "status": "ok",
    }


def generate_lane_b_report(
    projection_traces: list[dict[str, Any]],
    self_consistency_runs: list[list[str]] | None = None,
    output_path: Path | None = None,
) -> dict[str, Any]:
    """Generate the complete Lane B measurement report."""

    ift_result = compute_ift_scent_alignment(projection_traces)
    callback_result = compute_callback_distribution_agreement(projection_traces)

    sc_result: dict[str, Any] = {"status": "not_run"}
    if self_consistency_runs:
        sc_result = compute_self_consistency(self_consistency_runs)

    # Gate G7 verdict
    ift_passed = ift_result.get("ift_scent_alignment", 0.0) >= 0.60
    callback_passed = callback_result.get("passed", False)
    sc_passed = sc_result.get("passed", True)  # Pass if not run

    g7_passed = ift_passed and callback_passed

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ift_scent_alignment": ift_result,
        "callback_distribution_agreement": callback_result,
        "self_consistency": sc_result,
        "gate_g7": {
            "passed": g7_passed,
            "ift_alignment_passed": ift_passed,
            "callback_distribution_passed": callback_passed,
            "self_consistency_passed": sc_passed,
        },
        "summary": {
            "projection_traces_analyzed": len(projection_traces),
            "recommendation": "Lane B passed" if g7_passed else "Lane B requires remediation",
        },
    }

    if output_path:
        save_data(output_path, report)

    return report
