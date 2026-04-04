from __future__ import annotations

import argparse
import json
from pathlib import Path

from .cct import run_cct_probe
from .delta import apply_delta_patch
from .extractor import extract_graph
from .fidelity import evaluate_projection_fidelity
from .graph_analysis import analyze_graph_integrity
from .harness import run_pilot
from .io import load_data, load_graph, save_data, save_graph
from .operation_projection import project_operation  # pyright: ignore[reportMissingImports]
from .roundtrip import run_roundtrip
from .schema_validator import validate_graph


def _cmd_extract(args: argparse.Namespace) -> int:
    graph = extract_graph(
        Path(args.repo_root),
        commit_id=args.commit_id,
        language=args.language,
        generator_model=args.generator_model,
        generator_model_family=args.generator_model_family,
    )
    save_graph(Path(args.output), graph)
    print(json.dumps({"status": "ok", "output": args.output}, indent=2))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    graph = load_graph(Path(args.graph_file))
    errors = validate_graph(graph, Path(args.repo_root))
    payload = {"passed": len(errors) == 0, "errors": errors}
    print(json.dumps(payload, indent=2))
    return 0 if not errors else 1


def _cmd_roundtrip(args: argparse.Namespace) -> int:
    graph = load_graph(Path(args.graph_file))
    result = run_roundtrip(graph)
    print(json.dumps(result, indent=2))
    return 0 if result.get("passed") else 1


def _cmd_cct(args: argparse.Namespace) -> int:
    result = run_cct_probe(Path(args.probe_file), Path(args.trace_file))
    if args.output_file:
        save_data(Path(args.output_file), result)
    print(json.dumps(result, indent=2))
    return 0 if result.get("passed") else 1


def _cmd_integrity(args: argparse.Namespace) -> int:
    graph = load_graph(Path(args.graph_file))
    result = analyze_graph_integrity(graph)
    if args.output_file:
        save_data(Path(args.output_file), result)
    print(json.dumps(result, indent=2))
    checks = result.get("invariant_checks", {})
    passed = bool(
        checks.get("connectivity_invariant", False)
        and checks.get("no_gap_invariant", False)
    )
    return 0 if passed else 1


def _cmd_delta_apply(args: argparse.Namespace) -> int:
    base_graph = load_graph(Path(args.base_graph))
    patch = load_data(Path(args.delta_file))
    updated, report = apply_delta_patch(base_graph, patch, Path(args.repo_root))
    save_graph(Path(args.output_graph), updated)
    if args.output_report:
        save_data(Path(args.output_report), report)
    print(json.dumps(report, indent=2))
    return 0 if report.get("passed") else 1


def _cmd_run_pilot(args: argparse.Namespace) -> int:
    prompt_profile = None
    if args.prompt_profile_file:
        prompt_profile = load_data(Path(args.prompt_profile_file))

    gold_spec = None
    if args.gold_file:
        gold_spec = load_data(Path(args.gold_file))

    summary = run_pilot(
        repo_root=Path(args.repo_root),
        run_dir=Path(args.run_dir),
        commit_id=args.commit_id,
        language=args.language,
        probe_file=Path(args.probe_file) if args.probe_file else None,
        trace_file=Path(args.trace_file) if args.trace_file else None,
        operation_family=args.operation_family,
        prompt_profile=prompt_profile,
        gold_spec=gold_spec,
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary.get("passed") else 1


def _cmd_project(args: argparse.Namespace) -> int:
    graph = load_graph(Path(args.graph_file))
    prompt_profile = None
    if args.prompt_profile_file:
        prompt_profile = load_data(Path(args.prompt_profile_file))

    trace = project_operation(
        graph=graph,
        operation_family=args.operation_family,
        prompt_profile=prompt_profile,
    )
    if args.output_file:
        save_data(Path(args.output_file), trace)
    print(json.dumps(trace, indent=2))
    return 0


def _cmd_fidelity_eval(args: argparse.Namespace) -> int:
    projection_trace = load_data(Path(args.projection_file))
    gold_spec = load_data(Path(args.gold_file))
    result = evaluate_projection_fidelity(projection_trace, gold_spec)
    if args.output_file:
        save_data(Path(args.output_file), result)
    print(json.dumps(result, indent=2))
    return 0 if result.get("passed") else 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codeclue", description="CodeClue research CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="Extract canonical clue graph from repository")
    extract.add_argument("--repo-root", required=True)
    extract.add_argument("--output", required=True)
    extract.add_argument("--commit-id", default="unknown")
    extract.add_argument(
        "--language",
        default="auto",
        choices=["auto", "python", "typescript", "go"],
    )
    extract.add_argument(
        "--generator-model",
        default="codeclue-structural-v1",
        help="Generator model identifier for provenance tagging",
    )
    extract.add_argument(
        "--generator-model-family",
        default="codeclue",
        help="Generator model family (e.g., anthropic, openai, codeclue)",
    )
    extract.set_defaults(func=_cmd_extract)

    validate = sub.add_parser("validate", help="Validate canonical clue graph invariants")
    validate.add_argument("--graph-file", required=True)
    validate.add_argument("--repo-root", required=True)
    validate.set_defaults(func=_cmd_validate)

    roundtrip = sub.add_parser("roundtrip", help="Run lossless round-trip checks")
    roundtrip.add_argument("--graph-file", required=True)
    roundtrip.set_defaults(func=_cmd_roundtrip)

    cct = sub.add_parser("cct", help="Run Comprehension Circuit Tracing probe")
    cct.add_argument("--probe-file", required=True)
    cct.add_argument("--trace-file", required=True)
    cct.add_argument("--output-file")
    cct.set_defaults(func=_cmd_cct)

    project = sub.add_parser(
        "project",
        help="Generate OF1-OF5 task-conditioned projection from canonical graph",
    )
    project.add_argument("--graph-file", required=True)
    project.add_argument(
        "--operation-family",
        required=True,
        choices=["OF1", "OF2", "OF3", "OF4", "OF5"],
    )
    project.add_argument("--prompt-profile-file")
    project.add_argument("--output-file")
    project.set_defaults(func=_cmd_project)

    fidelity = sub.add_parser(
        "fidelity-eval",
        help="Evaluate projection against gold path specification",
    )
    fidelity.add_argument("--projection-file", required=True)
    fidelity.add_argument("--gold-file", required=True)
    fidelity.add_argument("--output-file")
    fidelity.set_defaults(func=_cmd_fidelity_eval)

    integrity = sub.add_parser(
        "integrity",
        help="Run graph-theoretic integrity checks",
    )
    integrity.add_argument("--graph-file", required=True)
    integrity.add_argument("--output-file")
    integrity.set_defaults(func=_cmd_integrity)

    delta_apply = sub.add_parser(
        "delta-apply",
        help="Apply delta patch and verify no-gap/connectivity proofs",
    )
    delta_apply.add_argument("--base-graph", required=True)
    delta_apply.add_argument("--delta-file", required=True)
    delta_apply.add_argument("--repo-root", required=True)
    delta_apply.add_argument("--output-graph", required=True)
    delta_apply.add_argument("--output-report")
    delta_apply.set_defaults(func=_cmd_delta_apply)

    pilot = sub.add_parser(
        "run-pilot",
        help="Execute extract/validate/roundtrip/integrity/CCT in one run",
    )
    pilot.add_argument("--repo-root", required=True)
    pilot.add_argument("--run-dir", required=True)
    pilot.add_argument("--commit-id", default="unknown")
    pilot.add_argument(
        "--language",
        default="auto",
        choices=["auto", "python", "typescript", "go"],
    )
    pilot.add_argument("--probe-file")
    pilot.add_argument("--trace-file")
    pilot.add_argument(
        "--operation-family",
        choices=["OF1", "OF2", "OF3", "OF4", "OF5"],
    )
    pilot.add_argument("--prompt-profile-file")
    pilot.add_argument("--gold-file")
    pilot.set_defaults(func=_cmd_run_pilot)

    # Lane A batch
    lane_a = sub.add_parser(
        "lane-a",
        help="Run Lane A extraction batch across external repos from replay set",
    )
    lane_a.add_argument("--replay-set", required=True, help="Path to pr-replay-set JSON")
    lane_a.add_argument("--repos-dir", required=True, help="Directory containing cloned repos")
    lane_a.add_argument("--runs-dir", required=True, help="Output directory for run artifacts")
    lane_a.set_defaults(func=_cmd_lane_a)

    # Lane B report
    lane_b = sub.add_parser(
        "lane-b",
        help="Generate Lane B ecological validity report from projection traces",
    )
    lane_b.add_argument("--traces-dir", required=True, help="Directory containing projection-*.json files")
    lane_b.add_argument("--output-file", required=True, help="Path for Lane B report JSON")
    lane_b.set_defaults(func=_cmd_lane_b)

    return parser


def _cmd_lane_a(args: argparse.Namespace) -> int:
    from .lane_a import run_lane_a_batch

    result = run_lane_a_batch(
        replay_set_path=Path(args.replay_set),
        external_repos_dir=Path(args.repos_dir),
        runs_base_dir=Path(args.runs_dir),
    )
    print(json.dumps(result, indent=2))
    return 0 if result.get("repos_succeeded", 0) > 0 else 1


def _cmd_lane_b(args: argparse.Namespace) -> int:
    from .lane_b import generate_lane_b_report
    from .io import load_data

    traces_dir = Path(args.traces_dir)
    projection_traces = []
    for f in sorted(traces_dir.glob("projection-*.json")):
        projection_traces.append(load_data(f))

    if not projection_traces:
        print(json.dumps({"error": "No projection traces found"}))
        return 1

    report = generate_lane_b_report(
        projection_traces=projection_traces,
        output_path=Path(args.output_file),
    )
    print(json.dumps(report, indent=2))
    return 0 if report.get("gate_g7", {}).get("passed", False) else 1


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    return int(args.func(args))
