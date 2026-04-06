"""Action-task benchmark: tests whether the clue helps an LLM perform
developer tasks correctly (refactor, trace, impact analysis, etc.)

Metrics:
- Localization accuracy: did the LLM identify the right files/symbols?
- Impact completeness: did it find all affected symbols?
- Drill-down efficiency: did it request the right source?
- Token efficiency: how much context was needed vs raw-source-first?

Produces parallel prompt sets:
- Arm A: raw source → perform task
- Arm B: clue file → perform task (with optional drill-down)

Usage:
    python experiments/runs/run_action_benchmark.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.io import load_graph
from codeclue_research.clue_view_plan_a import render_clue_plan_a
from codeclue_research.token_counter import count_tokens


# Action tasks — real developer tasks, not comprehension questions
ACTION_TASKS = [
    # TF1-like: Architecture navigation (refactoring target identification)
    {
        "task_id": "action-flask-refactor-001",
        "family": "TF1-Action",
        "repo": "flask",
        "lane_dir": "v2-lane-a-flask",
        "proj_file": "v2-proj-flask-tf1-001.json",
        "task": "Refactor Flask's request handling to support async middleware. List every file and function that must be modified.",
        "gold_files": ["src/flask/app.py", "src/flask/ctx.py"],
        "gold_symbols": ["wsgi_app", "full_dispatch_request", "finalize_request", "preprocess_request",
                         "process_response", "__call__", "request_context"],
        "gold_type": "localization",
    },
    {
        "task_id": "action-express-navigate-001",
        "family": "TF1-Action",
        "repo": "express",
        "lane_dir": "v2-lane-a-express",
        "proj_file": "v2-proj-express-tf1-001.json",
        "task": "A developer new to Express needs to understand the middleware pipeline to add rate limiting. Identify the entry point, middleware registration, and execution flow.",
        "gold_files": ["lib/application.js"],
        "gold_symbols": ["app.handle", "router.handle", "app.use", "router.use"],
        "gold_type": "localization",
    },
    # TF2-like: Impact analysis (change impact identification)
    {
        "task_id": "action-flask-impact-001",
        "family": "TF2-Action",
        "repo": "flask",
        "lane_dir": "v2-lane-a-flask",
        "proj_file": "v2-proj-flask-tf2-001.json",
        "task": "We're modifying Flask.wsgi_app to add request logging. List ALL functions that could be affected by this change and explain the propagation path.",
        "gold_files": ["src/flask/app.py"],
        "gold_symbols": ["wsgi_app", "full_dispatch_request", "dispatch_request", "finalize_request",
                         "handle_exception", "handle_user_exception", "request_context",
                         "preprocess_request", "process_response"],
        "gold_type": "impact",
    },
    {
        "task_id": "action-httpx-impact-001",
        "family": "TF2-Action",
        "repo": "httpx",
        "lane_dir": "v2-lane-a-httpx",
        "proj_file": "v2-proj-httpx-tf2-001.json",
        "task": "We need to add HTTP/3 support to httpx. Identify every component in the transport layer that would need modification.",
        "gold_files": ["httpx/_transports/default.py", "httpx/_client.py"],
        "gold_symbols": ["handle_request", "_transport_for_url", "_send_single_request", "Client"],
        "gold_type": "impact",
    },
    # TF3-like: Edit localization (where exactly to make a change)
    {
        "task_id": "action-flask-edit-001",
        "family": "TF3-Action",
        "repo": "flask",
        "lane_dir": "v2-lane-a-flask",
        "proj_file": "v2-proj-flask-tf3-001.json",
        "task": "Add a new 'after_dispatch' hook that runs after the view function returns but before after_request hooks. Specify the exact file and insertion point.",
        "gold_files": ["src/flask/app.py", "src/flask/sansio/scaffold.py"],
        "gold_symbols": ["full_dispatch_request", "finalize_request", "dispatch_request",
                         "after_request", "before_request"],
        "gold_type": "localization",
    },
    {
        "task_id": "action-fastapi-edit-001",
        "family": "TF3-Action",
        "repo": "fastapi",
        "lane_dir": "v2-lane-a-fastapi",
        "proj_file": "v2-proj-fastapi-tf3-001.json",
        "task": "Add request body size limiting middleware to FastAPI. Which files define middleware registration and where should the new middleware be inserted?",
        "gold_files": ["fastapi/applications.py"],
        "gold_symbols": ["add_middleware", "build_middleware_stack"],
        "gold_type": "localization",
    },
    # TF4-like: Crash/bug tracing
    {
        "task_id": "action-flask-trace-001",
        "family": "TF4-Action",
        "repo": "flask",
        "lane_dir": "v2-lane-a-flask",
        "proj_file": "v2-proj-flask-tf4-001.json",
        "task": "A user reports that their after_request handler silently fails when an exception occurs during dispatch. Trace the execution path to identify where the exception is caught and why the handler might not execute.",
        "gold_files": ["src/flask/app.py"],
        "gold_symbols": ["full_dispatch_request", "finalize_request", "handle_user_exception",
                         "handle_exception", "after_request"],
        "gold_type": "trace",
    },
    {
        "task_id": "action-nest-trace-001",
        "family": "TF4-Action",
        "repo": "nest",
        "lane_dir": "v2-lane-a-nest",
        "proj_file": "v2-proj-nest-tf4-001.json",
        "task": "A NestJS middleware is not executing for certain routes. Trace the middleware resolution and binding flow to identify why route-specific middleware might be skipped.",
        "gold_files": ["packages/core/middleware/resolver.ts", "packages/core/middleware/builder.ts"],
        "gold_symbols": ["resolveInstances", "apply", "forRoutes", "exclude"],
        "gold_type": "trace",
    },
    # TF5-like: Security audit
    {
        "task_id": "action-flask-security-001",
        "family": "TF5-Action",
        "repo": "flask",
        "lane_dir": "v2-lane-a-flask",
        "proj_file": "v2-proj-flask-tf5-001.json",
        "task": "Audit Flask's session handling for security vulnerabilities. List every file involved in session creation, signing, and cookie setting.",
        "gold_files": ["src/flask/sessions.py"],
        "gold_symbols": ["SecureCookieSessionInterface", "save_session", "open_session",
                         "get_signing_serializer", "should_set_cookie"],
        "gold_type": "localization",
    },
    {
        "task_id": "action-gin-security-001",
        "family": "TF5-Action",
        "repo": "gin",
        "lane_dir": "v2-lane-a-gin",
        "proj_file": "v2-proj-gin-tf5-001.json",
        "task": "Audit Gin's middleware chain for security risks. Identify where auth middleware runs relative to route handlers and whether middleware can be bypassed.",
        "gold_files": ["gin.go", "context.go", "auth.go"],
        "gold_symbols": ["ServeHTTP", "handleHTTPRequest", "Next", "Abort", "BasicAuth"],
        "gold_type": "localization",
    },
]


def _score_action_task(
    answer_text: str,
    gold: dict[str, Any],
) -> dict[str, Any]:
    """Score an action task response.

    Measures:
    - file_recall: fraction of gold files mentioned
    - symbol_recall: fraction of gold symbols mentioned
    - localization_accuracy: combined file + symbol recall
    """
    normalized = answer_text.lower()

    # File recall
    gold_files = gold.get("gold_files", [])
    file_hits = 0
    for gf in gold_files:
        # Check various forms: full path, basename, partial
        basename = Path(gf).name.lower()
        parts = gf.lower().replace("/", " ").replace("\\", " ").split()
        if gf.lower() in normalized or basename in normalized:
            file_hits += 1
        elif any(p in normalized for p in parts if len(p) > 3):
            file_hits += 0.5  # partial match
    file_recall = file_hits / len(gold_files) if gold_files else 0.0

    # Symbol recall
    gold_symbols = gold.get("gold_symbols", [])
    symbol_hits = 0
    for sym in gold_symbols:
        variants = [sym.lower()]
        if "." in sym:
            variants.append(sym.rsplit(".", 1)[-1].lower())
        variants.append(sym.lower().replace("_", ""))
        if any(v in normalized for v in variants):
            symbol_hits += 1
    symbol_recall = symbol_hits / len(gold_symbols) if gold_symbols else 0.0

    # Combined
    localization_accuracy = 0.4 * file_recall + 0.6 * symbol_recall

    return {
        "file_recall": round(file_recall, 4),
        "symbol_recall": round(symbol_recall, 4),
        "localization_accuracy": round(localization_accuracy, 4),
        "file_hits": file_hits,
        "file_total": len(gold_files),
        "symbol_hits": symbol_hits,
        "symbol_total": len(gold_symbols),
        "sufficient": localization_accuracy >= 0.60,
    }


def _build_arm_a_prompt(task: dict, repo_root: Path) -> str:
    """Build raw-source prompt for an action task."""
    source_files = task["gold_files"]
    parts = [
        "You are a senior software engineer performing a development task.",
        "You have access to the source code below. Perform the requested task.",
        "",
        f"## Task",
        f"{task['task']}",
        "",
        "## Source Code",
    ]
    for sf in source_files:
        full = repo_root / sf
        if full.is_file():
            src = full.read_text(encoding="utf-8", errors="replace")
            lines = src.splitlines()
            if len(lines) > 500:
                src = "\n".join(lines[:500]) + f"\n\n... [{len(lines)-500} more lines]"
            parts.append(f"\n### {sf}\n```\n{src}\n```")
    parts.extend(["", "## Required Output",
                   "- List every file that must be modified",
                   "- List every function/class that is involved",
                   "- Explain the execution/impact path",
                   "- Identify what source you would need to read for implementation"])
    return "\n".join(parts)


def _build_arm_b_prompt(task: dict, clue: dict) -> str:
    """Build clue-based prompt for an action task."""
    parts = [
        "You are a senior software engineer performing a development task.",
        "You have access to a CodeClue artifact — a compact comprehension file",
        "that describes the relevant code subsystem. Use it to plan your approach.",
        "",
        f"## Task",
        f"{task['task']}",
        "",
        "## CodeClue Artifact",
        "```json",
        json.dumps(clue, indent=2, ensure_ascii=False),
        "```",
        "",
        "## Required Output",
        "- List every file that must be modified",
        "- List every function/class that is involved (cite entity IDs)",
        "- Explain the execution/impact path based on the clue",
        "- Identify what additional source you would need via drill-down",
    ]
    return "\n".join(parts)


def main() -> None:
    runs_dir = ROOT / "experiments" / "runs"
    out_dir = ROOT / "experiments" / "runs" / "action-benchmark"
    reports_dir = ROOT / "experiments" / "reports"
    external_repos = ROOT / "experiments" / "external-repos"

    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    repo_dirs = {
        "flask": external_repos / "flask",
        "fastapi": external_repos / "fastapi",
        "nest": external_repos / "nest",
        "httpx": external_repos / "httpx",
        "express": external_repos / "express",
        "typeorm": external_repos / "typeorm",
        "gin": external_repos / "gin",
    }

    manifest: list[dict] = []
    clue_scores: list[dict] = []  # score clue content directly against gold

    for task in ACTION_TASKS:
        task_id = task["task_id"]
        family = task["family"]
        repo = task["repo"]
        repo_root = repo_dirs.get(repo, ROOT)

        proj_path = runs_dir / task["lane_dir"] / task["proj_file"]
        graph_path = runs_dir / task["lane_dir"] / "graph.json"

        if not proj_path.is_file() or not graph_path.is_file():
            print(f"  SKIP {task_id}: missing projection/graph")
            continue

        with open(proj_path) as f:
            projection = json.load(f)
        graph = load_graph(graph_path)

        # Render Plan A clue
        clue = render_clue_plan_a(projection, graph, task["task"], str(repo_root))

        # Score clue content directly against gold (automated — no LLM needed)
        clue_text = json.dumps(clue, ensure_ascii=False)
        clue_score = _score_action_task(clue_text, task)
        clue_score["task_id"] = task_id
        clue_score["family"] = family
        clue_score["clue_tokens"] = count_tokens(clue)
        clue_scores.append(clue_score)

        # Generate Arm A prompt (raw source)
        arm_a = _build_arm_a_prompt(task, repo_root)
        arm_a_fname = f"{task_id}_arm-a.prompt.md"
        (out_dir / arm_a_fname).write_text(arm_a, encoding="utf-8")

        # Generate Arm B prompt (clue)
        arm_b = _build_arm_b_prompt(task, clue)
        arm_b_fname = f"{task_id}_arm-b.prompt.md"
        (out_dir / arm_b_fname).write_text(arm_b, encoding="utf-8")

        # Save clue for scoring
        clue_fname = f"{task_id}_arm-b.clue.json"
        (out_dir / clue_fname).write_text(json.dumps(clue, indent=2), encoding="utf-8")

        manifest.append({
            "task_id": task_id,
            "family": family,
            "task": task["task"],
            "gold_type": task["gold_type"],
            "arm_a_prompt": arm_a_fname,
            "arm_a_response": arm_a_fname.replace(".prompt.md", ".response.md"),
            "arm_b_prompt": arm_b_fname,
            "arm_b_response": arm_b_fname.replace(".prompt.md", ".response.md"),
            "clue_file": clue_fname,
            "arm_a_tokens": count_tokens(arm_a),
            "arm_b_tokens": count_tokens(arm_b),
            "clue_tokens": count_tokens(clue),
            "gold_files": task["gold_files"],
            "gold_symbols": task["gold_symbols"],
        })

        print(f"  {task_id}: clue_loc={clue_score['localization_accuracy']:.3f} "
              f"(files={clue_score['file_recall']:.2f} sym={clue_score['symbol_recall']:.2f}) "
              f"tokens: arm_a={count_tokens(arm_a)} arm_b={count_tokens(arm_b)}")

    # Save manifest
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Aggregate clue-content scores (automated, no LLM needed)
    families = sorted(set(s["family"] for s in clue_scores))
    print(f"\n{'='*70}")
    print(f"AUTOMATED CLUE-CONTENT SCORING (clue artifact vs gold localization)")
    print(f"{'='*70}")
    print(f"\n{'Task':<35} {'Fam':<12} {'FilRec':>7} {'SymRec':>7} {'LocAcc':>7} {'Suff':>5}")
    print(f"{'-'*35} {'-'*12} {'-'*7} {'-'*7} {'-'*7} {'-'*5}")

    for s in clue_scores:
        suff = "YES" if s["sufficient"] else "no"
        print(f"{s['task_id']:<35} {s['family']:<12} {s['file_recall']:>7.3f} {s['symbol_recall']:>7.3f} {s['localization_accuracy']:>7.3f} {suff:>5}")

    # Per-family summary
    print(f"\nPer-Family:")
    for fam in families:
        fam_scores = [s for s in clue_scores if s["family"] == fam]
        mean_loc = sum(s["localization_accuracy"] for s in fam_scores) / len(fam_scores)
        mean_file = sum(s["file_recall"] for s in fam_scores) / len(fam_scores)
        mean_sym = sum(s["symbol_recall"] for s in fam_scores) / len(fam_scores)
        suff_count = sum(1 for s in fam_scores if s["sufficient"])
        print(f"  {fam}: loc={mean_loc:.3f} file={mean_file:.3f} sym={mean_sym:.3f} suff={suff_count}/{len(fam_scores)}")

    # Overall
    overall_loc = sum(s["localization_accuracy"] for s in clue_scores) / len(clue_scores)
    overall_suff = sum(1 for s in clue_scores if s["sufficient"])
    print(f"\n  OVERALL: loc={overall_loc:.3f}, sufficient={overall_suff}/{len(clue_scores)} ({overall_suff*100/len(clue_scores):.0f}%)")

    # Token comparison
    if manifest:
        mean_a = sum(m["arm_a_tokens"] for m in manifest) / len(manifest)
        mean_b = sum(m["arm_b_tokens"] for m in manifest) / len(manifest)
        mean_clue = sum(m["clue_tokens"] for m in manifest) / len(manifest)
        print(f"\n  Token comparison: Arm A (raw)={mean_a:.0f}t, Arm B (clue)={mean_b:.0f}t, ratio={mean_b/mean_a:.2f}")

    # Save results
    results_path = reports_dir / "action-benchmark-results.json"
    with open(results_path, "w") as f:
        json.dump({
            "clue_content_scores": clue_scores,
            "manifest": manifest,
            "overall_localization": overall_loc,
            "overall_sufficient": overall_suff,
            "total_tasks": len(clue_scores),
        }, f, indent=2)

    print(f"\nSaved: {results_path}")
    print(f"Prompts: {out_dir}")
    print(f"\nTo get LLM scores: paste .prompt.md files into LLM, save as .response.md")
    print(f"Then run: python experiments/runs/score_action_responses.py")


if __name__ == "__main__":
    main()
