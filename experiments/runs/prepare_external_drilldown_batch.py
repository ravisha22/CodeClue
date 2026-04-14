from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import yaml

from codeclue_mcp.budget import BudgetTracker
from codeclue_mcp.server import CodeClueServer
from codeclue_mcp.tracer import InvocationTracer, hash_output
from codeclue_research.io import load_graph
from codeclue_research.operation_projection import project_operation

from prepare_external_drilldown_packet import REPO_DIR_BY_SLUG, TASK_FILES, WORKSPACE_ROOT, build_packet


def _normalize_task(task: dict, task_file: Path) -> dict:
    selected = dict(task)
    repo_dir = selected.get("repo_dir")
    if not repo_dir:
        repo_dir = REPO_DIR_BY_SLUG.get(selected.get("repo"), "flask")
        selected["repo_dir"] = repo_dir
    if "repo" not in selected and repo_dir == "flask":
        selected["repo"] = "pallets/flask"
    selected["task_file"] = str(task_file.relative_to(WORKSPACE_ROOT))
    return selected


def _load_all_tasks() -> list[dict]:
    tasks: list[dict] = []
    for task_file in TASK_FILES:
        if not task_file.exists():
            continue
        payload = yaml.safe_load(task_file.read_text(encoding="utf-8")) or {}
        for task in payload.get("tasks", []):
            tasks.append(_normalize_task(task, task_file))
    return tasks


def _select_tasks(
    tasks: list[dict],
    task_ids: list[str] | None,
    repos: list[str] | None,
    families: list[str] | None,
    limit: int | None,
) -> list[dict]:
    selected: list[dict] = []
    task_id_filter = set(task_ids or [])
    repo_filter = set(repos or [])
    family_filter = set(families or [])

    for task in tasks:
        if task_id_filter and task["task_id"] not in task_id_filter:
            continue
        if repo_filter and task.get("repo_dir") not in repo_filter and task.get("repo") not in repo_filter:
            continue
        if family_filter and task.get("family") not in family_filter:
            continue
        selected.append(task)
        if limit is not None and len(selected) >= limit:
            break
    return selected


def _estimate_raw_tokens(graph, repo_root: Path) -> int:
    raw_token_estimate = 0
    seen_files: set[str] = set()
    for node in graph.nodes:
        file_path = node.source_anchor.file_path
        if file_path in seen_files:
            continue
        seen_files.add(file_path)
        full_path = repo_root / file_path
        if full_path.exists():
            raw_token_estimate += full_path.stat().st_size // 4
    return raw_token_estimate


def _build_automated_post_prompt(task: dict, projection: dict, tool_results: dict) -> str:
    parts = [
        "You are running the AFTER pass of a CodeClue drill-down evaluation.",
        "",
        "Rules:",
        "- Start from the same clue projection below.",
        "- Use the automated MCP drill-down evidence below as your only post-clue evidence.",
        "- Do NOT inspect any other source beyond what is included in this prompt.",
        "- Produce a revised answer that clearly reflects what the drill-down changed.",
        "",
        f"Task ID: {task['task_id']}",
        f"Family: {task['family']}",
        f"Operation Family: {task['operation_family']}",
        "",
        "Question:",
        task["question"],
        "",
        "Return your answer in this format:",
        "",
        "1. Revised answer",
        "2. Tool evidence used:",
        "   - tool name + what it contributed",
        "3. What changed after drill-down:",
        "   - ...",
        "4. Remaining uncertainty:",
        "   - ...",
        "5. Final confidence: low|medium|high",
        "",
        "## Confidence Block",
        json.dumps(projection.get("confidence", {}), indent=2, ensure_ascii=True),
        "",
        "## Projection Stats",
        json.dumps(projection.get("stats", {}), indent=2, ensure_ascii=True),
        "",
        "## Projected Nodes",
        json.dumps(projection.get("projected_nodes", []), indent=2, ensure_ascii=True),
        "",
        "## Projected Edges",
        json.dumps(projection.get("projected_edges", []), indent=2, ensure_ascii=True),
        "",
        "## Automated MCP Drill-Down Results",
        json.dumps(tool_results, indent=2, ensure_ascii=True),
    ]
    return "\n".join(parts) + "\n"


def _execute_automated_drilldown(task: dict, packet_dir: Path) -> dict:
    repo_dir = task["repo_dir"]
    graph_path = WORKSPACE_ROOT / f"experiments/runs/v2-lane-a-{repo_dir}/graph.json"
    repo_root = WORKSPACE_ROOT / f"experiments/external-repos/{repo_dir}"

    graph = load_graph(graph_path)
    server = CodeClueServer(
        graph=graph,
        repo_root=str(repo_root),
        graph_path=str(graph_path),
        workspace_root=str(WORKSPACE_ROOT),
    )
    tracer = InvocationTracer(trace_dir=packet_dir / "traces")
    tracker = BudgetTracker(operation_family=task["operation_family"])

    projection = project_operation(
        graph=graph,
        operation_family=task["operation_family"],
        prompt_profile=task["prompt_profile"],
    )
    confidence = projection.get("confidence", {})

    clue_token_estimate = len(
        json.dumps(
            {
                "confidence": projection.get("confidence", {}),
                "stats": projection.get("stats", {}),
                "projected_nodes": projection.get("projected_nodes", []),
                "projected_edges": projection.get("projected_edges", []),
            },
            sort_keys=True,
        )
    ) // 4

    raw_token_estimate = _estimate_raw_tokens(graph, repo_root)
    tool_results: list[dict] = []
    drill_down_tokens = 0

    for node_confidence in confidence.get("per_node_confidence", []):
        if not tracker.can_call():
            break
        for action in node_confidence.get("suggested_actions", []):
            if not tracker.can_call():
                break
            result = server.call_tool(action["tool"], action.get("args", {}))
            if result.get("status") != "ok":
                tool_results.append(
                    {
                        "tool": action["tool"],
                        "args": action.get("args", {}),
                        "node_id": node_confidence["node_id"],
                        "confidence_trigger": node_confidence.get("confidence", 0),
                        "result": result,
                    }
                )
                continue

            tracker.record_call(tool=action["tool"], node_id=node_confidence["node_id"])
            tracer.log(
                tool=action["tool"],
                args=action.get("args", {}),
                output_hash=hash_output(result),
                source_anchor=node_confidence["node_id"],
                confidence_trigger=node_confidence.get("confidence", 0),
                session_id=task["task_id"],
            )
            result_blob = json.dumps(result, sort_keys=True)
            output_tokens = len(result_blob) // 4
            drill_down_tokens += output_tokens
            tool_results.append(
                {
                    "tool": action["tool"],
                    "args": action.get("args", {}),
                    "node_id": node_confidence["node_id"],
                    "confidence_trigger": node_confidence.get("confidence", 0),
                    "output_size_tokens": output_tokens,
                    "result": result,
                }
            )

    total_tokens = clue_token_estimate + drill_down_tokens
    etrr = 1.0 - (total_tokens / max(raw_token_estimate, 1))

    summary = {
        "task_id": task["task_id"],
        "repo_dir": repo_dir,
        "operation_family": task["operation_family"],
        "confidence_overall": confidence.get("confidence_overall"),
        "lookup_hint": confidence.get("lookup_decision_hint"),
        "projected_nodes": projection.get("stats", {}).get("projected_node_count"),
        "actions_executed": len([entry for entry in tool_results if entry.get("result", {}).get("status") == "ok"]),
        "budget": tracker.get_escalation(),
        "tokens": {
            "clue": clue_token_estimate,
            "drill_down": drill_down_tokens,
            "total": total_tokens,
            "raw_estimate": raw_token_estimate,
        },
        "etrr": round(etrr, 4),
        "h7_pass": etrr >= 0.65,
        "tool_results": tool_results,
        "trace_file": str(tracer.trace_path.relative_to(WORKSPACE_ROOT)),
    }

    (packet_dir / "drilldown-tool-results.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    (packet_dir / "consumer-post-automated.prompt.md").write_text(
        _build_automated_post_prompt(task, projection, summary),
        encoding="utf-8",
    )

    result_template_path = packet_dir / "result-template.json"
    if result_template_path.exists():
        result_template = json.loads(result_template_path.read_text(encoding="utf-8"))
        metrics = result_template.setdefault("metrics", {})
        metrics["clue_tokens"] = clue_token_estimate
        metrics["drill_down_tokens"] = drill_down_tokens
        metrics["total_tokens"] = total_tokens
        metrics["raw_estimate_tokens"] = raw_token_estimate
        metrics["etrr"] = round(etrr, 4)
        metrics["h7_pass"] = etrr >= 0.65
        result_template_path.write_text(json.dumps(result_template, indent=2), encoding="utf-8")

    return {
        "task_id": task["task_id"],
        "packet_dir": str(packet_dir.relative_to(WORKSPACE_ROOT)),
        "graph_path": str(graph_path.relative_to(WORKSPACE_ROOT)),
        "repo_root": str(repo_root.relative_to(WORKSPACE_ROOT)),
        "projection_path": f"experiments/runs/v2-lane-a-{repo_dir}/v2-proj-{task['task_id']}.json",
        "status": {
            "packet_prepared": True,
            "tool_results_generated": True,
            "pre_answer": False,
            "post_answer": False,
            "judged": False,
        },
        "metrics": {
            "confidence_overall": confidence.get("confidence_overall"),
            "actions_executed": summary["actions_executed"],
            "clue_tokens": clue_token_estimate,
            "drill_down_tokens": drill_down_tokens,
            "total_tokens": total_tokens,
            "raw_estimate_tokens": raw_token_estimate,
            "etrr": round(etrr, 4),
            "h7_pass": etrr >= 0.65,
        },
    }


def _write_batch_summary(batch_root: Path, manifest: dict) -> None:
    lines = [
        "# External Drill-Down Batch",
        "",
        f"- Batch ID: `{manifest['batch_id']}`",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Task count: {len(manifest['tasks'])}",
        "",
        "| Task ID | Repo | Family | OF | Confidence | Tool Calls | ETRR | H7 |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]

    for task in manifest["tasks"]:
        metrics = task.get("metrics", {})
        lines.append(
            "| {task_id} | {repo_dir} | {family} | {operation_family} | {confidence:.2f} | {calls} | {etrr:.4f} | {h7} |".format(
                task_id=task["task_id"],
                repo_dir=task["repo_dir"],
                family=task["family"],
                operation_family=task["operation_family"],
                confidence=metrics.get("confidence_overall") or 0.0,
                calls=metrics.get("actions_executed") or 0,
                etrr=metrics.get("etrr") or 0.0,
                h7="pass" if metrics.get("h7_pass") else "fail",
            )
        )

    (batch_root / "batch-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a batch of external drill-down experiment packets")
    parser.add_argument("--task-id", action="append", dest="task_ids", help="Task ID to include. Repeat for multiple tasks.")
    parser.add_argument("--repo", action="append", dest="repos", help="Repo slug or repo_dir to include. Repeat for multiple repos.")
    parser.add_argument("--family", action="append", dest="families", help="Task family to include. Repeat for multiple families.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of tasks to include after filtering.")
    parser.add_argument(
        "--output-dir",
        default="experiments/reports/external-drilldown/batch-20260405-subagents",
        help="Batch output directory, relative to workspace root.",
    )
    args = parser.parse_args()

    tasks = _select_tasks(
        tasks=_load_all_tasks(),
        task_ids=args.task_ids,
        repos=args.repos,
        families=args.families,
        limit=args.limit,
    )
    if not tasks:
        raise SystemExit("No tasks matched the selected filters.")

    batch_root = WORKSPACE_ROOT / args.output_dir
    batch_root.mkdir(parents=True, exist_ok=True)

    manifest = {
        "batch_id": batch_root.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tasks": [],
    }

    for task in tasks:
        packet_dir = batch_root / task["task_id"]
        build_packet(task_id=task["task_id"], output_dir=packet_dir)
        packet_record = _execute_automated_drilldown(task, packet_dir)
        packet_record["family"] = task["family"]
        packet_record["operation_family"] = task["operation_family"]
        packet_record["repo_dir"] = task["repo_dir"]
        manifest["tasks"].append(packet_record)

    (batch_root / "batch-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _write_batch_summary(batch_root, manifest)

    print(
        json.dumps(
            {
                "status": "ok",
                "batch_id": manifest["batch_id"],
                "output_dir": str(batch_root.relative_to(WORKSPACE_ROOT)),
                "task_count": len(manifest["tasks"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())