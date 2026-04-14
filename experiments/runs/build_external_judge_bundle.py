from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent

from prepare_external_drilldown_packet import WORKSPACE_ROOT


def _load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_task_block(packet_dir: Path) -> dict:
    task = json.loads((packet_dir / "task.json").read_text(encoding="utf-8"))
    before = (packet_dir / "answers" / "pre-answer.md").read_text(encoding="utf-8").strip()
    after = (packet_dir / "answers" / "post-answer.md").read_text(encoding="utf-8").strip()
    return {
        "task_id": task["task_id"],
        "family": task["family"],
        "operation_family": task["operation_family"],
        "question": task["question"],
        "ground_truth_summary": task["ground_truth_summary"],
        "before_answer": before,
        "after_answer": after,
    }


def _bundle_prompt(batch_id: str, judge_result_path: str, tasks: list[dict]) -> str:
    parts = [
        "You are the independent judge for a batch CodeClue drill-down experiment.",
        "",
        "For each task, score the BEFORE answer and AFTER answer against the ground truth.",
        "The goal is to determine whether MCP drill-down materially improved the answer.",
        "",
        f"Batch ID: {batch_id}",
        "",
        f"Return only the JSON object, with no markdown fences and no extra commentary. The output must be suitable for saving verbatim into `{judge_result_path}`.",
        "",
        "Use this exact JSON shape:",
        "{",
        f'  "batch_id": "{batch_id}",',
        '  "tasks": [',
        "    {",
        '      "task_id": "example-task-id",',
        '      "before": {',
        '        "fidelity_score": 0.0,',
        '        "key_points_hit": [],',
        '        "key_points_missed": [],',
        '        "hallucinations": []',
        "      },",
        '      "after": {',
        '        "fidelity_score": 0.0,',
        '        "key_points_hit": [],',
        '        "key_points_missed": [],',
        '        "hallucinations": []',
        "      },",
        '      "delta": 0.0,',
        '      "did_drilldown_help": true,',
        '      "summary": "one short paragraph"',
        "    }",
        "  ],",
        '  "batch_summary": "one short paragraph"',
        "}",
        "",
        "Scoring rubric:",
        "- 1.0 = fully correct, covers the important causal/behavioral points",
        "- 0.75 = mostly correct, minor omissions",
        "- 0.50 = partially correct, important structure present but key implications missing",
        "- 0.25 = poor, mostly superficial",
        "- 0.0 = wrong or empty",
        "",
    ]

    for index, task in enumerate(tasks, start=1):
        parts.extend(
            [
                f"## Task {index}",
                f"Task ID: {task['task_id']}",
                f"Family: {task['family']}",
                f"Operation Family: {task['operation_family']}",
                "",
                "Question:",
                task["question"],
                "",
                "Ground Truth:",
                task["ground_truth_summary"],
                "",
                "BEFORE Answer:",
                task["before_answer"],
                "",
                "AFTER Answer:",
                task["after_answer"],
                "",
            ]
        )
    return "\n".join(parts) + "\n"


def _template(batch_id: str, tasks: list[dict]) -> dict:
    return {
        "batch_id": batch_id,
        "tasks": [
            {
                "task_id": task["task_id"],
                "before": {
                    "fidelity_score": 0.0,
                    "key_points_hit": [],
                    "key_points_missed": [],
                    "hallucinations": [],
                },
                "after": {
                    "fidelity_score": 0.0,
                    "key_points_hit": [],
                    "key_points_missed": [],
                    "hallucinations": [],
                },
                "delta": 0.0,
                "did_drilldown_help": True,
                "summary": "one short paragraph",
            }
            for task in tasks
        ],
        "batch_summary": "one short paragraph",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a single Gemini judge prompt for a prepared external drill-down batch")
    parser.add_argument(
        "--manifest",
        default="experiments/reports/external-drilldown/batch-20260405-subagents/batch-manifest.json",
        help="Path to batch manifest, relative to workspace root.",
    )
    args = parser.parse_args()

    manifest_path = WORKSPACE_ROOT / args.manifest
    manifest = _load_manifest(manifest_path)
    batch_root = manifest_path.parent

    completed: list[dict] = []
    missing: list[str] = []
    for task_entry in manifest.get("tasks", []):
        packet_dir = WORKSPACE_ROOT / task_entry["packet_dir"]
        pre_path = packet_dir / "answers" / "pre-answer.md"
        post_path = packet_dir / "answers" / "post-answer.md"
        if not pre_path.exists() or not post_path.exists():
            missing.append(task_entry["task_id"])
            continue
        completed.append(_build_task_block(packet_dir))

    if not completed:
        raise SystemExit("No tasks are ready for judging. Populate pre-answer.md and post-answer.md first.")

    judge_result_rel = str((batch_root / "judge-bundle.result.json").relative_to(WORKSPACE_ROOT))
    prompt = _bundle_prompt(manifest["batch_id"], judge_result_rel, completed)
    template = _template(manifest["batch_id"], completed)

    (batch_root / "judge-bundle.prompt.md").write_text(prompt, encoding="utf-8")
    (batch_root / "judge-bundle.template.json").write_text(json.dumps(template, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "ok",
                "batch_id": manifest["batch_id"],
                "ready_tasks": len(completed),
                "missing_tasks": missing,
                "prompt_file": str((batch_root / "judge-bundle.prompt.md").relative_to(WORKSPACE_ROOT)),
                "result_file": judge_result_rel,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())