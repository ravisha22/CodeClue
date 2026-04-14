from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean

from prepare_external_drilldown_packet import WORKSPACE_ROOT


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _format_num(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def _load_bundle_results(path: Path) -> dict[str, dict]:
    payload = _load_json(path)
    tasks = payload.get("tasks", [])
    return {task["task_id"]: task for task in tasks}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collate Gemini-judged external drill-down batch results")
    parser.add_argument(
        "--manifest",
        default="experiments/reports/external-drilldown/batch-20260405-subagents/batch-manifest.json",
        help="Path to batch manifest, relative to workspace root.",
    )
    parser.add_argument(
        "--judge-results",
        default="experiments/reports/external-drilldown/batch-20260405-subagents/judge-bundle.result.json",
        help="Path to the Gemini judge result bundle, relative to workspace root.",
    )
    parser.add_argument("--consumer-model", default="GPT-5.4")
    parser.add_argument("--judge-model", default="Gemini 3.1 Pro")
    parser.add_argument("--judge-mode", default="independent-cross-family")
    parser.add_argument("--evidence-tier", default="cross-model-subagent-pilot")
    args = parser.parse_args()

    manifest_path = WORKSPACE_ROOT / args.manifest
    judge_path = WORKSPACE_ROOT / args.judge_results
    manifest = _load_json(manifest_path)
    judge_results = _load_bundle_results(judge_path)
    batch_root = manifest_path.parent

    summary_rows: list[dict] = []
    for task_entry in manifest.get("tasks", []):
        task_id = task_entry["task_id"]
        if task_id not in judge_results:
            continue

        packet_dir = WORKSPACE_ROOT / task_entry["packet_dir"]
        judge_result = judge_results[task_id]
        (packet_dir / "answers" / "judge-result.json").write_text(
            json.dumps(judge_result, indent=2),
            encoding="utf-8",
        )

        result_template_path = packet_dir / "result-template.json"
        result_template = _load_json(result_template_path)
        metrics = result_template.setdefault("metrics", {})
        metrics["before_fidelity"] = judge_result["before"]["fidelity_score"]
        metrics["after_fidelity"] = judge_result["after"]["fidelity_score"]
        metrics["delta"] = judge_result["delta"]
        metrics["h5_pass"] = judge_result["delta"] >= 0.10
        if metrics.get("etrr") is not None:
            metrics["h7_pass"] = metrics["etrr"] >= 0.65

        result_template["consumer_model_before"] = args.consumer_model
        result_template["consumer_model_after"] = args.consumer_model
        result_template["judge_model"] = args.judge_model
        result_template["judge_mode"] = args.judge_mode
        result_template["evidence_tier"] = args.evidence_tier

        result_template_path.write_text(json.dumps(result_template, indent=2), encoding="utf-8")

        summary_rows.append(
            {
                "task_id": task_id,
                "repo_dir": task_entry["repo_dir"],
                "family": task_entry["family"],
                "operation_family": task_entry["operation_family"],
                "before_fidelity": metrics["before_fidelity"],
                "after_fidelity": metrics["after_fidelity"],
                "delta": metrics["delta"],
                "did_drilldown_help": judge_result["did_drilldown_help"],
                "clue_tokens": metrics.get("clue_tokens"),
                "drill_down_tokens": metrics.get("drill_down_tokens"),
                "total_tokens": metrics.get("total_tokens"),
                "raw_estimate_tokens": metrics.get("raw_estimate_tokens"),
                "etrr": metrics.get("etrr"),
                "h5_pass": metrics.get("h5_pass"),
                "h7_pass": metrics.get("h7_pass"),
                "summary": judge_result.get("summary"),
            }
        )

    if not summary_rows:
        raise SystemExit("No judge results matched the manifest tasks.")

    aggregate = {
        "task_count": len(summary_rows),
        "mean_before_fidelity": mean(row["before_fidelity"] for row in summary_rows),
        "mean_after_fidelity": mean(row["after_fidelity"] for row in summary_rows),
        "mean_delta": mean(row["delta"] for row in summary_rows),
        "h5_pass_count": sum(1 for row in summary_rows if row["h5_pass"]),
        "h7_pass_count": sum(1 for row in summary_rows if row["h7_pass"]),
    }

    summary_json = {
        "batch_id": manifest["batch_id"],
        "consumer_model": args.consumer_model,
        "judge_model": args.judge_model,
        "judge_mode": args.judge_mode,
        "evidence_tier": args.evidence_tier,
        "aggregate": aggregate,
        "tasks": summary_rows,
    }
    (batch_root / "external-drilldown-summary.json").write_text(
        json.dumps(summary_json, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# External Drill-Down Summary",
        "",
        f"- Batch ID: `{manifest['batch_id']}`",
        f"- Consumer model: `{args.consumer_model}`",
        f"- Judge model: `{args.judge_model}`",
        f"- Judge mode: `{args.judge_mode}`",
        f"- Evidence tier: `{args.evidence_tier}`",
        "",
        "## Aggregate",
        "",
        f"- Tasks judged: {aggregate['task_count']}",
        f"- Mean before fidelity: {_format_num(aggregate['mean_before_fidelity'])}",
        f"- Mean after fidelity: {_format_num(aggregate['mean_after_fidelity'])}",
        f"- Mean delta: {_format_num(aggregate['mean_delta'])}",
        f"- H5 pass count: {aggregate['h5_pass_count']}/{aggregate['task_count']}",
        f"- H7 pass count: {aggregate['h7_pass_count']}/{aggregate['task_count']}",
        "",
        "## Per-Task",
        "",
        "| Task ID | Repo | Family | Before | After | Delta | H5 | H7 | ETRR |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {task_id} | {repo_dir} | {family} | {before} | {after} | {delta} | {h5} | {h7} | {etrr} |".format(
                task_id=row["task_id"],
                repo_dir=row["repo_dir"],
                family=row["family"],
                before=_format_num(row["before_fidelity"]),
                after=_format_num(row["after_fidelity"]),
                delta=_format_num(row["delta"]),
                h5="pass" if row["h5_pass"] else "fail",
                h7="pass" if row["h7_pass"] else "fail",
                etrr=_format_num(row["etrr"], digits=4),
            )
        )
    (batch_root / "external-drilldown-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    paper_lines = [
        "# Paper Summary Snippet",
        "",
        "Use this only after verifying the judged tasks remain representative and the batch size is stated honestly.",
        "",
        (
            "In an externally judged subagent-automated drill-down pilot spanning {count} tasks, {consumer} improved "
            "from mean fidelity {before} to {after} after drill-down (mean Δ = {delta}). H5 passed on {h5}/{count} tasks; "
            "H7 passed on {h7}/{count} tasks under a {judge_mode} setup with {judge}."
        ).format(
            count=aggregate["task_count"],
            consumer=args.consumer_model,
            before=_format_num(aggregate["mean_before_fidelity"]),
            after=_format_num(aggregate["mean_after_fidelity"]),
            delta=_format_num(aggregate["mean_delta"]),
            h5=aggregate["h5_pass_count"],
            h7=aggregate["h7_pass_count"],
            judge_mode=args.judge_mode,
            judge=args.judge_model,
        ),
        "",
        "| Task ID | Before | After | Delta | H5 | H7 |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in summary_rows:
        paper_lines.append(
            "| {task_id} | {before} | {after} | {delta} | {h5} | {h7} |".format(
                task_id=row["task_id"],
                before=_format_num(row["before_fidelity"]),
                after=_format_num(row["after_fidelity"]),
                delta=_format_num(row["delta"]),
                h5="pass" if row["h5_pass"] else "fail",
                h7="pass" if row["h7_pass"] else "fail",
            )
        )
    (batch_root / "paper-summary-snippet.md").write_text("\n".join(paper_lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "ok",
                "batch_id": manifest["batch_id"],
                "summary_file": str((batch_root / "external-drilldown-summary.md").relative_to(WORKSPACE_ROOT)),
                "paper_snippet_file": str((batch_root / "paper-summary-snippet.md").relative_to(WORKSPACE_ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())