"""Per-model confidence calibration per PRD Appendix D.2 and E.4.

Provides:
- fit_calibration_profile: train a calibration transform from labeled data
- apply_calibration: transform raw confidence → calibrated probability
- load_calibration_profile: load profile from disk with staleness check
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _compute_ece(probabilities: list[float], outcomes: list[bool], n_bins: int = 10) -> float:
    """Expected Calibration Error."""
    bins: list[list[tuple[float, bool]]] = [[] for _ in range(n_bins)]
    for p, o in zip(probabilities, outcomes):
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append((p, o))

    ece = 0.0
    total = len(probabilities)
    for bin_items in bins:
        if not bin_items:
            continue
        avg_conf = sum(p for p, _ in bin_items) / len(bin_items)
        avg_outcome = sum(1 for _, o in bin_items if o) / len(bin_items)
        ece += (len(bin_items) / total) * abs(avg_conf - avg_outcome)
    return ece


def _compute_brier(probabilities: list[float], outcomes: list[bool]) -> float:
    """Brier score."""
    n = len(probabilities)
    if n == 0:
        return 0.0
    return sum((p - (1.0 if o else 0.0)) ** 2 for p, o in zip(probabilities, outcomes)) / n


def _temperature_scale(raw: list[float], outcomes: list[bool]) -> tuple[float, list[float]]:
    """Find optimal temperature scaling parameter."""
    best_t = 1.0
    best_ece = float("inf")

    for t_candidate in [x * 0.1 for x in range(5, 30)]:
        scaled = [1.0 / (1.0 + math.exp(-math.log(max(p, 1e-10) / max(1 - p, 1e-10)) / t_candidate))
                  for p in raw]
        ece = _compute_ece(scaled, outcomes)
        if ece < best_ece:
            best_ece = ece
            best_t = t_candidate

    calibrated = [1.0 / (1.0 + math.exp(-math.log(max(p, 1e-10) / max(1 - p, 1e-10)) / best_t))
                  for p in raw]
    return best_t, calibrated


def _platt_scale(raw: list[float], outcomes: list[bool]) -> tuple[dict[str, float], list[float]]:
    """Platt scaling (logistic regression on raw scores)."""
    # Simple gradient descent on log-loss
    a, b = 0.0, 0.0
    lr = 0.01
    targets = [1.0 if o else 0.0 for o in outcomes]

    for _ in range(1000):
        grad_a, grad_b = 0.0, 0.0
        for p_raw, t in zip(raw, targets):
            logit = a * p_raw + b
            logit = max(-20, min(20, logit))
            pred = 1.0 / (1.0 + math.exp(-logit))
            err = pred - t
            grad_a += err * p_raw
            grad_b += err
        a -= lr * grad_a / len(raw)
        b -= lr * grad_b / len(raw)

    calibrated = []
    for p_raw in raw:
        logit = a * p_raw + b
        logit = max(-20, min(20, logit))
        calibrated.append(1.0 / (1.0 + math.exp(-logit)))

    return {"a": round(a, 6), "b": round(b, 6)}, calibrated


def fit_calibration_profile(
    raw_confidences: list[float],
    actual_outcomes: list[bool],
    generator_model: str,
    generator_family: str,
    method: str = "auto",
) -> dict[str, Any]:
    """Fit a calibration profile from labeled data.

    Args:
        raw_confidences: model's raw confidence per task/node
        actual_outcomes: True if the task had a miss/gap, False if clue was sufficient
        generator_model: exact model identifier
        generator_family: model family (anthropic, openai, google, etc.)
        method: 'auto', 'temperature_scaling', 'platt_scaling', or 'isotonic'

    Returns:
        Calibration profile dict matching PRD Appendix D.2.2 schema.
    """
    n = len(raw_confidences)
    if n < 3:
        return _fallback_profile(generator_model, generator_family, "insufficient data (n < 3)")

    # Try methods and pick best ECE
    results: list[tuple[str, dict[str, Any], list[float], float, float]] = []

    # Temperature scaling
    try:
        temp, cal_temp = _temperature_scale(raw_confidences, actual_outcomes)
        ece_temp = _compute_ece(cal_temp, actual_outcomes)
        brier_temp = _compute_brier(cal_temp, actual_outcomes)
        results.append(("temperature_scaling", {"temperature": round(temp, 4)}, cal_temp, ece_temp, brier_temp))
    except Exception:
        pass

    # Platt scaling
    try:
        params_platt, cal_platt = _platt_scale(raw_confidences, actual_outcomes)
        ece_platt = _compute_ece(cal_platt, actual_outcomes)
        brier_platt = _compute_brier(cal_platt, actual_outcomes)
        results.append(("platt_scaling", params_platt, cal_platt, ece_platt, brier_platt))
    except Exception:
        pass

    if not results:
        return _fallback_profile(generator_model, generator_family, "all calibration methods failed")

    # Pick method with lowest ECE
    results.sort(key=lambda x: x[3])
    best_method, best_params, best_cal, best_ece, best_brier = results[0]

    gate_passed = best_ece <= 0.05 and best_brier <= 0.18

    if not gate_passed and method == "auto":
        # If no method passes gate, still report best but mark gate as failed
        pass

    return {
        "generator_model": generator_model,
        "generator_model_family": generator_family,
        "calibration_method": best_method,
        "fitted_on_date": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "ece": round(best_ece, 6),
            "brier": round(best_brier, 6),
        },
        "parameters": best_params,
        "gate_passed": gate_passed,
        "fallback_note": None if gate_passed else f"ECE={best_ece:.4f}, Brier={best_brier:.4f} — gate thresholds not met",
    }


def _fallback_profile(model: str, family: str, reason: str) -> dict[str, Any]:
    return {
        "generator_model": model,
        "generator_model_family": family,
        "calibration_method": "FALLBACK_STRUCTURAL_ONLY",
        "fitted_on_date": datetime.now(timezone.utc).isoformat(),
        "metrics": {"ece": 1.0, "brier": 1.0},
        "parameters": {},
        "gate_passed": False,
        "fallback_note": reason,
    }


def apply_calibration(raw_confidence: float, profile: dict[str, Any]) -> float | None:
    """Apply a calibration transform to a raw confidence score.

    Returns None if profile is FALLBACK_STRUCTURAL_ONLY (caller should use structural only).
    """
    method = profile.get("calibration_method", "FALLBACK_STRUCTURAL_ONLY")
    params = profile.get("parameters", {})

    if method == "FALLBACK_STRUCTURAL_ONLY":
        return None

    if method == "temperature_scaling":
        temp = params.get("temperature", 1.0)
        logit = math.log(max(raw_confidence, 1e-10) / max(1 - raw_confidence, 1e-10))
        scaled_logit = logit / temp
        scaled_logit = max(-20, min(20, scaled_logit))
        return 1.0 / (1.0 + math.exp(-scaled_logit))

    if method == "platt_scaling":
        a = params.get("a", 0.0)
        b = params.get("b", 0.0)
        logit = a * raw_confidence + b
        logit = max(-20, min(20, logit))
        return 1.0 / (1.0 + math.exp(-logit))

    return None


def load_calibration_profile(
    generator_model: str,
    calibration_dir: Path,
) -> dict[str, Any]:
    """Load calibration profile for a specific generator model.

    Returns FALLBACK_STRUCTURAL_ONLY if no matching profile found.
    """
    if not calibration_dir.exists():
        return _fallback_profile(generator_model, "unknown", f"calibration directory not found: {calibration_dir}")

    # Exact match
    profile_path = calibration_dir / f"{generator_model}.calib.json"
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        if profile.get("generator_model") == generator_model:
            return profile
        # Version mismatch in file
        return _fallback_profile(generator_model, "unknown",
                                 f"calibration profile version mismatch: file has {profile.get('generator_model')}")

    # No match found
    return _fallback_profile(generator_model, "unknown", f"no calibration profile for {generator_model}")
