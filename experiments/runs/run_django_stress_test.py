"""Django stress test: define tasks, run projections, render Plan A clues,
measure compression, generate consumer prompts.

Tests the full pipeline at 45K-node scale across all 5 task families.

Usage:
    python experiments/runs/run_django_stress_test.py
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
from codeclue_research.operation_projection import project_operation
from codeclue_research.clue_view_plan_a import render_clue_plan_a, validate_clue_purity
from codeclue_research.token_metrics import compute_compression_metrics
from codeclue_research.token_counter import count_tokens


# Django task definitions: 5 tasks, one per family
DJANGO_TASKS = [
    {
        "task_id": "django-tf1-001",
        "family": "TF1",
        "operation_family": "OF1",
        "question": "What is the high-level architecture of Django's HTTP request handling pipeline from WSGI entry to response?",
        "prompt_profile": {
            "profile_id": "django-arch-v1",
            "intent": "architecture-comprehension",
            "constraints": {"max_context": "broad"},
            "focus_files": ["django/core/handlers/wsgi.py", "django/core/handlers/base.py"],
            "focus_symbols": ["WSGIHandler", "BaseHandler", "get_response"],
            "focus_keywords": ["request", "response", "middleware", "handler", "wsgi"],
            "strict_mode": True,
        },
    },
    {
        "task_id": "django-tf2-001",
        "family": "TF2",
        "operation_family": "OF2",
        "question": "What is the downstream impact of modifying Django's BaseHandler.get_response method?",
        "prompt_profile": {
            "profile_id": "django-impact-v1",
            "intent": "impact-analysis",
            "constraints": {"max_context": "balanced"},
            "focus_files": ["django/core/handlers/base.py"],
            "focus_symbols": ["BaseHandler.get_response", "BaseHandler._get_response"],
            "focus_keywords": ["get_response", "middleware", "resolve", "dispatch"],
            "strict_mode": True,
        },
    },
    {
        "task_id": "django-tf3-001",
        "family": "TF3",
        "operation_family": "OF3",
        "question": "Where in Django's codebase should an edit be made to add a new middleware hook that runs after URL resolution but before view dispatch?",
        "prompt_profile": {
            "profile_id": "django-edit-v1",
            "intent": "edit-localization",
            "constraints": {"max_context": "focused"},
            "focus_files": ["django/core/handlers/base.py", "django/middleware/__init__.py"],
            "focus_symbols": ["BaseHandler", "get_response", "resolve"],
            "focus_keywords": ["middleware", "resolve", "dispatch", "view", "hook"],
            "strict_mode": True,
        },
    },
    {
        "task_id": "django-tf4-001",
        "family": "TF4",
        "operation_family": "OF4",
        "question": "What behavioral gotchas exist in Django's middleware exception handling during request processing?",
        "prompt_profile": {
            "profile_id": "django-behavior-v1",
            "intent": "behavior-debugging",
            "constraints": {"max_context": "balanced"},
            "focus_files": ["django/core/handlers/base.py", "django/core/handlers/exception.py"],
            "focus_symbols": ["BaseHandler", "convert_exception_to_response", "get_response"],
            "focus_keywords": ["exception", "middleware", "error", "handler", "response", "convert"],
            "strict_mode": True,
        },
    },
    {
        "task_id": "django-tf5-001",
        "family": "TF5",
        "operation_family": "OF5",
        "question": "What security concerns exist in Django's CSRF middleware implementation?",
        "prompt_profile": {
            "profile_id": "django-security-v1",
            "intent": "security-compliance",
            "constraints": {"max_context": "focused"},
            "focus_files": ["django/middleware/csrf.py"],
            "focus_symbols": ["CsrfViewMiddleware", "process_view", "_check_token"],
            "focus_keywords": ["csrf", "token", "secret", "cookie", "validate", "origin", "referer"],
            "strict_mode": True,
        },
    },
]


def main() -> None:
    graph_path = ROOT / "experiments" / "runs" / "scale-django" / "graph.json"
    repo_root = ROOT / "experiments" / "external-repos" / "django"
    out_dir = ROOT / "experiments" / "runs" / "django-stress-test"
    prompts_dir = out_dir / "consumer-prompts"
    reports_dir = ROOT / "experiments" / "reports"

    out_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading Django graph from {graph_path}...")
    t0 = time.time()
    graph = load_graph(graph_path)
    print(f"  Loaded: {len(graph.nodes)} nodes, {len(graph.edges)} edges in {time.time()-t0:.1f}s")

    results: list[dict[str, Any]] = []
    prompt_manifest: list[dict] = []

    for task in DJANGO_TASKS:
        task_id = task["task_id"]
        family = task["family"]
        of = task["operation_family"]
        question = task["question"]
        profile = task["prompt_profile"]

        print(f"\n{'='*60}")
        print(f"Task: {task_id} ({family}/{of})")
        print(f"Q: {question}")

        # Step 1: Run projection
        print(f"  Running projection ({of})...")
        t0 = time.time()
        try:
            projection = project_operation(graph, of, profile)
        except Exception as e:
            print(f"  ERROR in projection: {e}")
            results.append({
                "task_id": task_id, "family": family, "error": str(e),
            })
            continue
        proj_time = time.time() - t0
        proj_nodes = len(projection.get("projected_nodes", []))
        proj_edges = len(projection.get("projected_edges", []))
        print(f"  Projection: {proj_nodes} nodes, {proj_edges} edges in {proj_time:.1f}s")

        # Save projection
        proj_path = out_dir / f"proj-{task_id}.json"
        with open(proj_path, "w", encoding="utf-8") as f:
            json.dump(projection, f, indent=2)

        # Step 2: Render Plan A clue
        print(f"  Rendering Plan A clue...")
        t0 = time.time()
        clue = render_clue_plan_a(projection, graph, question, str(repo_root))
        clue_time = time.time() - t0
        entity_count = len(clue.get("entities", []))
        print(f"  Clue: {entity_count} entities in {clue_time:.1f}s")

        # Save clue
        clue_path = out_dir / f"clue-{task_id}.json"
        with open(clue_path, "w", encoding="utf-8") as f:
            json.dump(clue, f, indent=2)

        # Step 3: Purity check
        passed, violations = validate_clue_purity(clue)
        print(f"  Purity: {'PASS' if passed else 'FAIL'} ({len(violations)} violations)")

        # Step 4: Compression metrics
        metrics = compute_compression_metrics(
            task_id=task_id,
            clue_view=clue,
            projection_trace=projection,
            repo_root=str(repo_root),
            plan="a",
        )
        ccr = metrics["ccr"]
        clue_tokens = metrics["clue_tokens"]
        raw_tokens = metrics["raw_first_tokens"]
        proj_tokens = metrics["projection_tokens"]
        print(f"  Tokens: clue={clue_tokens}, raw={raw_tokens}, proj={proj_tokens}")
        print(f"  CCR: {ccr:.4f} ({'PASS' if ccr >= 0.85 else 'FAIL'})")
        print(f"  Compaction: projection is {proj_tokens/clue_tokens:.1f}x larger than clue")

        # Step 5: Generate consumer prompt
        template_path = ROOT / "scaffold" / "prompts" / "arm-plan-a.md"
        template = template_path.read_text(encoding="utf-8")
        prompt = template.replace("{{QUESTION}}", question)
        prompt = prompt.replace("{{CLUE_JSON}}", json.dumps(clue, indent=2, ensure_ascii=False))

        prompt_fname = f"{task_id}_plan-a.prompt.md"
        (prompts_dir / prompt_fname).write_text(prompt, encoding="utf-8")

        # Save clue for scorer
        clue_fname = f"{task_id}_plan-a.clue.json"
        (prompts_dir / clue_fname).write_text(
            json.dumps(clue, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        prompt_manifest.append({
            "task_id": task_id,
            "family": family,
            "plan": "a",
            "prompt_file": prompt_fname,
            "response_file": prompt_fname.replace(".prompt.md", ".response.md"),
            "clue_file": clue_fname,
            "question": question,
            "prompt_tokens": count_tokens(prompt),
            "clue_tokens": clue_tokens,
        })

        results.append({
            "task_id": task_id,
            "family": family,
            "operation_family": of,
            "proj_nodes": proj_nodes,
            "proj_edges": proj_edges,
            "proj_time_s": round(proj_time, 2),
            "entity_count": entity_count,
            "clue_time_s": round(clue_time, 2),
            "purity_pass": passed,
            "purity_violations": len(violations),
            "clue_tokens": clue_tokens,
            "raw_tokens": raw_tokens,
            "proj_tokens": proj_tokens,
            "ccr": ccr,
            "ccr_pass": ccr >= 0.85,
            "compaction_ratio": round(proj_tokens / clue_tokens, 1) if clue_tokens > 0 else 0,
        })

    # Save results
    results_path = reports_dir / "django-stress-test-results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Save manifest
    manifest_path = prompts_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(prompt_manifest, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print(f"DJANGO STRESS TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    print(f"Tasks: {len(results)}")

    successful = [r for r in results if "error" not in r]
    if successful:
        mean_ccr = sum(r["ccr"] for r in successful) / len(successful)
        pass_85 = sum(1 for r in successful if r["ccr_pass"])
        mean_clue = sum(r["clue_tokens"] for r in successful) / len(successful)
        mean_raw = sum(r["raw_tokens"] for r in successful) / len(successful)

        print(f"\nCompression:")
        for r in successful:
            print(f"  {r['task_id']}: CCR={r['ccr']:.4f} clue={r['clue_tokens']}t raw={r['raw_tokens']}t "
                  f"proj={r['proj_tokens']}t ({r['compaction_ratio']}x compaction)")
        print(f"\n  Mean CCR: {mean_ccr:.4f}")
        print(f"  Pass ≥0.85: {pass_85}/{len(successful)}")
        print(f"  Mean clue: {mean_clue:.0f} tokens")
        print(f"  Mean raw: {mean_raw:.0f} tokens")
        print(f"  Purity: {sum(1 for r in successful if r['purity_pass'])}/{len(successful)} pass")

    errors = [r for r in results if "error" in r]
    if errors:
        print(f"\nErrors: {len(errors)}")
        for r in errors:
            print(f"  {r['task_id']}: {r['error']}")

    print(f"\nPrompts saved to: {prompts_dir}")
    print(f"Results saved to: {results_path}")
    print(f"\nNext: paste each .prompt.md into GPT/Gemini/Claude,")
    print(f"save response as .response.md, then run score_responses.py")


if __name__ == "__main__":
    main()
