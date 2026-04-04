from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def _safe_div(num: float, den: float) -> float:
    if den == 0:
        return 0.0
    return num / den


def _load_probe(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_trace(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() in {".yaml", ".yml"}:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        return payload.get("events", [])
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        return payload.get("events", [])

    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        events.append(json.loads(line))
    return events


def run_cct_probe(probe_file: Path, trace_file: Path) -> dict[str, Any]:
    probe = _load_probe(probe_file)
    events = _load_trace(trace_file)

    expected_nodes = set(probe.get("expected_path", {}).get("nodes", []))
    expected_edges = set(probe.get("expected_path", {}).get("edges", []))

    observed_nodes = {event.get("node_id") for event in events if event.get("node_id")}
    observed_edges = {event.get("edge_id") for event in events if event.get("edge_id")}

    path_precision = _safe_div(
        len(expected_nodes & observed_nodes) + len(expected_edges & observed_edges),
        len(observed_nodes) + len(observed_edges),
    )
    path_recall = _safe_div(
        len(expected_nodes & observed_nodes) + len(expected_edges & observed_edges),
        len(expected_nodes) + len(expected_edges),
    )

    contradictions = probe.get("contradiction_injections", [])
    contradiction_count = len(contradictions)
    rejected = 0
    for event in events:
        for result in event.get("contradictions", []):
            if result.get("decision") == "reject":
                rejected += 1
    contradiction_rejection = 1.0 if contradiction_count == 0 else _safe_div(rejected, contradiction_count)

    ablation_targets = set(probe.get("ablation_targets", []))
    ablation_signals = {
        item.get("target")
        for event in events
        for item in event.get("ablation", [])
        if item.get("degraded")
    }
    causal_sensitivity = 1.0 if not ablation_targets else _safe_div(len(ablation_targets & ablation_signals), len(ablation_targets))

    path_drift_index = max(0.0, 1.0 - path_recall)

    thresholds = probe.get("thresholds", {})
    passed = (
        path_precision >= float(thresholds.get("path_precision_min", 0.0))
        and path_recall >= float(thresholds.get("path_recall_min", 0.0))
        and contradiction_rejection >= float(thresholds.get("contradiction_rejection_min", 0.0))
    )

    return {
        "probe_id": probe.get("probe_id", "unknown"),
        "task_id": probe.get("task_id", "unknown"),
        "passed": passed,
        "metrics": {
            "PP": round(path_precision, 6),
            "PR": round(path_recall, 6),
            "CS": round(causal_sensitivity, 6),
            "CRR": round(contradiction_rejection, 6),
            "PDI": round(path_drift_index, 6),
        },
        "counts": {
            "expected_nodes": len(expected_nodes),
            "expected_edges": len(expected_edges),
            "observed_nodes": len(observed_nodes),
            "observed_edges": len(observed_edges),
        },
    }
