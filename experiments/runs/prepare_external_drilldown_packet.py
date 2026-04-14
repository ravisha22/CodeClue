from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent

import yaml


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
TASK_FILES = [
    WORKSPACE_ROOT / "tests/fixtures/lane_a_flask_tasks.yaml",
    WORKSPACE_ROOT / "tests/fixtures/lane_a_extended_tasks.yaml",
    WORKSPACE_ROOT / "tests/fixtures/lane_a_newrepo_tasks.yaml",
]
REPO_DIR_BY_SLUG = {
    "pallets/flask": "flask",
    "fastapi/fastapi": "fastapi",
    "nestjs/nest": "nest",
}


def _load_task(task_id: str) -> dict:
    for task_file in TASK_FILES:
        if not task_file.exists():
            continue
        payload = yaml.safe_load(task_file.read_text(encoding="utf-8")) or {}
        for task in payload.get("tasks", []):
            if task.get("task_id") != task_id:
                continue
            selected = dict(task)
            repo_dir = selected.get("repo_dir")
            if not repo_dir:
                repo_dir = REPO_DIR_BY_SLUG.get(selected.get("repo"), "flask")
                selected["repo_dir"] = repo_dir
            if "repo" not in selected and repo_dir == "flask":
                selected["repo"] = "pallets/flask"
            selected["task_file"] = str(task_file.relative_to(WORKSPACE_ROOT))
            return selected
    raise FileNotFoundError(f"Task not found: {task_id}")


def _load_projection(task_id: str, repo_dir: str) -> tuple[Path, dict]:
    projection_path = WORKSPACE_ROOT / f"experiments/runs/v2-lane-a-{repo_dir}/v2-proj-{task_id}.json"
    if not projection_path.exists():
        raise FileNotFoundError(f"Projection not found: {projection_path}")
    return projection_path, json.loads(projection_path.read_text(encoding="utf-8"))


def _server_command(task: dict) -> str:
    repo_dir = task["repo_dir"]
    return (
        ".\\.venv\\Scripts\\codeclue-mcp.exe "
        f"--graph-path experiments/runs/v2-lane-a-{repo_dir}/graph.json "
        f"--repo-root experiments/external-repos/{repo_dir}"
    )


def _consumer_pre_prompt(task: dict, projection: dict) -> str:
    parts = [
        "You are running the BEFORE pass of a CodeClue drill-down evaluation.",
        "",
        "Rules:",
        "- Use ONLY the clue projection below.",
        "- Do NOT use raw source code.",
        "- Do NOT call MCP tools.",
        "- If the clue is insufficient, say exactly what is missing.",
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
        "1. Answer",
        "2. Clue sufficient: yes|no",
        "3. Missing information:",
        "   - ...",
        "4. Confidence in your answer: low|medium|high",
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
    ]
    return "\n".join(parts) + "\n"


def _consumer_post_prompt(task: dict, projection: dict) -> str:
    parts = [
        "You are running the AFTER pass of a CodeClue drill-down evaluation.",
        "",
        "Rules:",
        "- Start from the same clue projection below.",
        "- You MAY use the configured CodeClue MCP tools if needed.",
        "- Use tool calls only where the clue is insufficient.",
        "- After any tool usage, produce a revised answer.",
        "- Be explicit about what changed because of the tools.",
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
        "2. Tools used:",
        "   - tool name + why you used it",
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
    ]
    return "\n".join(parts) + "\n"


def _judge_prompt(task: dict) -> str:
    return dedent(
        f"""
        You are the independent judge for a CodeClue drill-down experiment.

        Score the BEFORE answer and AFTER answer against the ground truth.
        The goal is to determine whether MCP drill-down materially improved the answer.

        Task ID: {task['task_id']}
        Family: {task['family']}
        Operation Family: {task['operation_family']}

        Question:
        {task['question']}

        Ground Truth:
        {task['ground_truth_summary']}

        BEFORE Answer:
        {{PASTE_BEFORE_ANSWER_HERE}}

        AFTER Answer:
        {{PASTE_AFTER_ANSWER_HERE}}

                Return only the JSON object, with no markdown fences and no extra commentary. The output must be suitable for saving verbatim into `answers/judge-result.json`.

                Use this exact JSON shape:
        {{
          "task_id": "{task['task_id']}",
          "before": {{
            "fidelity_score": 0.0,
            "key_points_hit": [],
            "key_points_missed": [],
            "hallucinations": []
          }},
          "after": {{
            "fidelity_score": 0.0,
            "key_points_hit": [],
            "key_points_missed": [],
            "hallucinations": []
          }},
          "delta": 0.0,
          "did_drilldown_help": true,
          "summary": "one short paragraph"
        }}

        Scoring rubric:
        - 1.0 = fully correct, covers the important causal/behavioral points
        - 0.75 = mostly correct, minor omissions
        - 0.50 = partially correct, important structure present but key implications missing
        - 0.25 = poor, mostly superficial
        - 0.0 = wrong or empty
        """
    ).strip() + "\n"


def _judge_same_model_prompt(task: dict) -> str:
    return dedent(
        f"""
        You are the judge for a CodeClue drill-down experiment.

        Important constraints:
        - You may be the same underlying model family that produced one or both answers.
        - You must behave like a strict rubric judge, not a collaborator.
        - Do NOT reward stylistic polish.
        - Do NOT infer missing facts charitably.
        - Only score what is explicitly present in the answers.

        Task ID: {task['task_id']}
        Family: {task['family']}
        Operation Family: {task['operation_family']}

        Question:
        {task['question']}

        Ground Truth:
        {task['ground_truth_summary']}

        BEFORE Answer:
        {{PASTE_BEFORE_ANSWER_HERE}}

        AFTER Answer:
        {{PASTE_AFTER_ANSWER_HERE}}

        Return only the JSON object, with no markdown fences and no extra commentary. The output must be suitable for saving verbatim into `answers/judge-result.json`.

        Use this exact JSON shape:
        {{
            "task_id": "{task['task_id']}",
            "judge_mode": "same-model-fallback",
            "before": {{
                "fidelity_score": 0.0,
                "key_points_hit": [],
                "key_points_missed": [],
                "hallucinations": []
            }},
            "after": {{
                "fidelity_score": 0.0,
                "key_points_hit": [],
                "key_points_missed": [],
                "hallucinations": []
            }},
            "delta": 0.0,
            "did_drilldown_help": true,
            "bias_warning": "same model family used for judging; treat as preliminary evidence",
            "summary": "one short paragraph"
        }}

        Scoring rubric:
        - 1.0 = fully correct, covers the important causal/behavioral points
        - 0.75 = mostly correct, minor omissions
        - 0.50 = partially correct, important structure present but key implications missing
        - 0.25 = poor, mostly superficial
        - 0.0 = wrong or empty
        """
    ).strip() + "\n"


def _runbook(task: dict, projection_path: Path) -> str:
    repo_dir = task["repo_dir"]
    return dedent(
        f"""
        # External Drill-Down Runbook

        This packet is prepared for task `{task['task_id']}`.

        ## What you are proving

        Show that an external consumer model gives a better answer after using CodeClue MCP drill-down than it gives from the clue alone.

        ## Files in this packet

        - `task.json`: task metadata
        - `projection-snippet.json`: clue projection used for the experiment
        - `consumer-pre.prompt.md`: paste into the consumer model for the BEFORE pass
        - `consumer-post.prompt.md`: paste into the consumer model for the AFTER pass
        - `judge.prompt.md`: paste into the independent judge after inserting both answers
        - `result-template.json`: fill in the final measured result
        - `server-command.txt`: exact MCP server command

        ## Step 1: Start the MCP server

        Run this in the workspace root:

        ```powershell
        {_server_command(task)}
        ```

        ## Step 2: BEFORE pass

        - Open your external consumer model.
        - Paste `consumer-pre.prompt.md`.
        - Save the full answer into `answers/pre-answer.md`.

        ## Step 3: AFTER pass

        - Connect the same consumer model to the running MCP server.
        - Paste `consumer-post.prompt.md`.
        - Allow it to use MCP tools.
        - Save the full answer into `answers/post-answer.md`.

        ## Step 4: Judge

        - Open a different model family as judge.
        - Open `judge.prompt.md`.
        - Replace the BEFORE and AFTER placeholders with the saved answers.
        - Save the result into `answers/judge-result.json`.

        ## Step 5: Fill the result template

        Copy the judge scores and token totals into `result-template.json`.

        Use these token values from the existing drill-down trial if you reuse the same task flow:

        - clue_tokens: 8958
        - drill_down_tokens: 44102
        - total_tokens: 53060
        - raw_estimate_tokens: 147680
        - etrr: 0.6407

        ## Source of truth

        - Task definition: `{task['task_file']}`
        - Projection: `{projection_path.relative_to(WORKSPACE_ROOT)}`
        - External repo root: `experiments/external-repos/{repo_dir}`
        """
    ).strip() + "\n"


def _copilot_runbook(task: dict, projection_path: Path) -> str:
    repo_dir = task["repo_dir"]
    return dedent(
        f"""
        # Copilot-Only Runbook

        This version assumes the only LLM access you have is through GitHub Copilot in VS Code.

        ## Goal

        Prove one simple thing: the answer gets better after Copilot uses the CodeClue MCP tools.

        ## Best evidence you can get with Copilot

        ### Best case

        If your Copilot model picker exposes different model families, use:

        - Chat A: consumer BEFORE pass
        - Chat B: same consumer family for AFTER pass with MCP enabled
        - Chat C: different model family as judge

        This is acceptable cross-model evidence inside Copilot.

        ### Fallback case

        If Copilot only gives you one model family, use three fresh chats anyway:

        - Chat A: BEFORE pass
        - Chat B: AFTER pass with MCP enabled
        - Chat C: same-model strict judge

        This is still useful, but it is only **pilot evidence**, not independent cross-model validation.

        ## Step 1: Start the MCP server

        In the workspace root, run:

        ```powershell
        {_server_command(task)}
        ```

        ## Step 2: BEFORE pass in Copilot

        - Open a fresh Copilot chat.
        - If you can choose a model, note which one you picked.
        - Paste `consumer-pre.prompt.md`.
        - Save the answer into `answers/pre-answer.md`.

        ## Step 3: AFTER pass in Copilot with MCP

        - Open a second fresh Copilot chat.
        - Use the same consumer model family as Step 2 if possible.
        - Make sure MCP/tool usage is enabled for the chat.
        - Paste `consumer-post.prompt.md`.
        - Let Copilot use the CodeClue MCP tools.
        - Save the answer into `answers/post-answer.md`.

        ## Step 4: Judge in Copilot

        - Open a third fresh Copilot chat.
        - If possible, choose a different model family than the consumer.
        - If a different family is not available, use `judge-same-model.prompt.md` instead of `judge.prompt.md`.
        - Paste the before/after answers into the prompt placeholders.
        - Save the result into `answers/judge-result.json`.

        ## Step 5: Record what happened honestly

        Fill in `result-template.json` and set:

        - `consumer_model_before`
        - `consumer_model_after`
        - `judge_model`
        - `judge_mode`
        - `evidence_tier`

        Use `evidence_tier = "cross-model-copilot"` only if the judge was a different model family.

        Use `evidence_tier = "same-model-copilot-pilot"` if all three chats used the same family.

        ## What to say in the paper

        - If different Copilot model families were used: this is partial external validation.
        - If the same Copilot model family judged the run: this is preliminary pilot evidence only.

        ## Source of truth

        - Task definition: `{task['task_file']}`
        - Projection: `{projection_path.relative_to(WORKSPACE_ROOT)}`
        - External repo root: `experiments/external-repos/{repo_dir}`
        """
    ).strip() + "\n"


def _result_template(task: dict) -> dict:
    return {
        "task_id": task["task_id"],
        "question": task["question"],
        "before_answer_file": "answers/pre-answer.md",
        "after_answer_file": "answers/post-answer.md",
        "judge_result_file": "answers/judge-result.json",
        "consumer_model_before": None,
        "consumer_model_after": None,
        "judge_model": None,
        "judge_mode": None,
        "evidence_tier": None,
        "metrics": {
            "before_fidelity": None,
            "after_fidelity": None,
            "delta": None,
            "clue_tokens": None,
            "drill_down_tokens": None,
            "total_tokens": None,
            "raw_estimate_tokens": None,
            "etrr": None,
            "h5_pass": None,
            "h7_pass": None,
        },
        "notes": "Populate token metrics from the measured drill-down run. Set h5_pass true only if after_fidelity - before_fidelity >= 0.10.",
    }


def build_packet(task_id: str, output_dir: Path) -> None:
    task = _load_task(task_id)
    projection_path, projection = _load_projection(task_id, task["repo_dir"])

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "answers").mkdir(parents=True, exist_ok=True)

    projection_snippet = {
        "confidence": projection.get("confidence", {}),
        "stats": projection.get("stats", {}),
        "projected_nodes": projection.get("projected_nodes", []),
        "projected_edges": projection.get("projected_edges", []),
    }

    (output_dir / "task.json").write_text(json.dumps(task, indent=2), encoding="utf-8")
    (output_dir / "projection-snippet.json").write_text(
        json.dumps(projection_snippet, indent=2),
        encoding="utf-8",
    )
    (output_dir / "consumer-pre.prompt.md").write_text(
        _consumer_pre_prompt(task, projection),
        encoding="utf-8",
    )
    (output_dir / "consumer-post.prompt.md").write_text(
        _consumer_post_prompt(task, projection),
        encoding="utf-8",
    )
    (output_dir / "judge.prompt.md").write_text(
        _judge_prompt(task),
        encoding="utf-8",
    )
    (output_dir / "judge-same-model.prompt.md").write_text(
        _judge_same_model_prompt(task),
        encoding="utf-8",
    )
    (output_dir / "runbook.md").write_text(
        _runbook(task, projection_path),
        encoding="utf-8",
    )
    (output_dir / "copilot-only-runbook.md").write_text(
        _copilot_runbook(task, projection_path),
        encoding="utf-8",
    )
    (output_dir / "server-command.txt").write_text(
        _server_command(task) + "\n",
        encoding="utf-8",
    )
    (output_dir / "result-template.json").write_text(
        json.dumps(_result_template(task), indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare an external drill-down experiment packet")
    parser.add_argument("--task-id", default="flask-tf2-001")
    parser.add_argument(
        "--output-dir",
        default="experiments/reports/external-drilldown/flask-tf2-001",
    )
    args = parser.parse_args()

    output_dir = WORKSPACE_ROOT / args.output_dir
    build_packet(task_id=args.task_id, output_dir=output_dir)
    print(json.dumps({
        "status": "ok",
        "task_id": args.task_id,
        "output_dir": str(output_dir.relative_to(WORKSPACE_ROOT)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())