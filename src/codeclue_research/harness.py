from __future__ import annotations

from pathlib import Path
from typing import Any

from .cct import run_cct_probe
from .extractor import extract_graph
from .fidelity import evaluate_projection_fidelity
from .graph_analysis import analyze_graph_integrity
from .io import save_data, save_graph
from .operation_projection import project_operation  # pyright: ignore[reportMissingImports]
from .roundtrip import run_roundtrip
from .schema_validator import validate_graph


def run_pilot(
    repo_root: Path,
    run_dir: Path,
    commit_id: str,
    language: str = "auto",
    probe_file: Path | None = None,
    trace_file: Path | None = None,
    operation_family: str | None = None,
    prompt_profile: dict[str, Any] | None = None,
    gold_spec: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)

    graph = extract_graph(repo_root=repo_root, commit_id=commit_id, language=language)
    graph_path = run_dir / "graph.json"
    save_graph(graph_path, graph)

    validation_errors = validate_graph(graph, repo_root)
    roundtrip_result = run_roundtrip(graph)
    integrity_result = analyze_graph_integrity(graph)

    cct_result: dict[str, Any] | None = None
    if probe_file and trace_file:
        cct_result = run_cct_probe(probe_file, trace_file)

    projection_result: dict[str, Any] | None = None
    if operation_family:
        projection_result = project_operation(
            graph=graph,
            operation_family=operation_family,
            prompt_profile=prompt_profile,
        )
        save_data(run_dir / "projection-trace.json", projection_result)

    fidelity_result: dict[str, Any] | None = None
    if projection_result is not None and gold_spec is not None:
        fidelity_result = evaluate_projection_fidelity(projection_result, gold_spec)
        save_data(run_dir / "projection-fidelity.json", fidelity_result)

    integrity_checks = integrity_result.get("invariant_checks", {})
    integrity_passed = bool(
        integrity_checks.get("connectivity_invariant", False)
        and integrity_checks.get("no_gap_invariant", False)
    )

    summary = {
        "run_dir": run_dir.as_posix(),
        "graph_file": graph_path.as_posix(),
        "validation_passed": len(validation_errors) == 0,
        "validation_errors": validation_errors,
        "roundtrip": roundtrip_result,
        "integrity": integrity_result,
        "integrity_passed": integrity_passed,
        "cct": cct_result,
        "projection": projection_result,
        "fidelity": fidelity_result,
        "passed": (
            len(validation_errors) == 0
            and roundtrip_result.get("passed", False)
            and integrity_passed
        ),
    }

    if cct_result is not None:
        summary["passed"] = bool(summary["passed"] and cct_result.get("passed", False))

    if fidelity_result is not None:
        summary["passed"] = bool(summary["passed"] and fidelity_result.get("passed", False))

    save_data(run_dir / "run-summary.json", summary)
    return summary
