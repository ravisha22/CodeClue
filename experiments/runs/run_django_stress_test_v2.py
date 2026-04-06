"""Django stress test v2: optimized for 45K-node scale.

Skips full confidence computation (the O(N*E) bottleneck).
Uses lightweight projection + direct clue rendering.

Usage:
    python experiments/runs/run_django_stress_test_v2.py
"""

from __future__ import annotations

import json
import sys
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.io import load_graph
from codeclue_research.models import CanonicalClueGraph
from codeclue_research.clue_view_plan_a import render_clue_plan_a, validate_clue_purity
from codeclue_research.token_metrics import compute_compression_metrics
from codeclue_research.token_counter import count_tokens


DJANGO_TASKS = [
    {
        "task_id": "django-tf1-001",
        "family": "TF1",
        "operation_family": "OF1",
        "question": "What is the high-level architecture of Django's HTTP request handling pipeline from WSGI entry to response?",
        "focus_files": ["django/core/handlers/wsgi.py", "django/core/handlers/base.py"],
        "focus_symbols": ["WSGIHandler", "BaseHandler", "get_response"],
        "focus_keywords": ["request", "response", "middleware", "handler", "wsgi"],
        "max_depth": 2,
    },
    {
        "task_id": "django-tf2-001",
        "family": "TF2",
        "operation_family": "OF2",
        "question": "What is the downstream impact of modifying Django's BaseHandler.get_response method?",
        "focus_files": ["django/core/handlers/base.py"],
        "focus_symbols": ["BaseHandler.get_response", "BaseHandler._get_response"],
        "focus_keywords": ["get_response", "middleware", "resolve"],
        "max_depth": 3,
    },
    {
        "task_id": "django-tf3-001",
        "family": "TF3",
        "operation_family": "OF3",
        "question": "Where in Django's codebase should an edit be made to add a new middleware hook that runs after URL resolution but before view dispatch?",
        "focus_files": ["django/core/handlers/base.py"],
        "focus_symbols": ["BaseHandler", "get_response"],
        "focus_keywords": ["middleware", "resolve", "dispatch"],
        "max_depth": 2,
    },
    {
        "task_id": "django-tf4-001",
        "family": "TF4",
        "operation_family": "OF4",
        "question": "What behavioral gotchas exist in Django's middleware exception handling during request processing?",
        "focus_files": ["django/core/handlers/base.py", "django/core/handlers/exception.py"],
        "focus_symbols": ["convert_exception_to_response", "get_response"],
        "focus_keywords": ["exception", "middleware", "error", "handler"],
        "max_depth": 3,
    },
    {
        "task_id": "django-tf5-001",
        "family": "TF5",
        "operation_family": "OF5",
        "question": "What security concerns exist in Django's CSRF middleware implementation?",
        "focus_files": ["django/middleware/csrf.py"],
        "focus_symbols": ["CsrfViewMiddleware", "process_view"],
        "focus_keywords": ["csrf", "token", "secret", "cookie", "validate"],
        "max_depth": 2,
    },
]


def _fast_project(
    graph: CanonicalClueGraph,
    focus_files: list[str],
    focus_symbols: list[str],
    focus_keywords: list[str],
    max_depth: int,
    node_budget: int = 160,
    operation_family: str = "OF2",
) -> dict[str, Any]:
    """Fast lightweight projection that avoids O(N*E) confidence computation.

    Pre-computes adjacency once, seeds from focus params, BFS to max_depth.
    """
    t0 = time.time()

    # Pre-compute adjacency (O(E))
    adjacency: dict[str, set[str]] = defaultdict(set)
    reverse_adj: dict[str, set[str]] = defaultdict(set)
    for edge in graph.edges:
        adjacency[edge.from_node].add(edge.to_node)
        reverse_adj[edge.to_node].add(edge.from_node)

    adj_time = time.time() - t0
    print(f"    Adjacency built in {adj_time:.1f}s")

    # Seed nodes (O(N) single pass)
    node_map = {n.node_id: n for n in graph.nodes}
    focus_files_set = set(focus_files)
    focus_symbols_lower = {s.lower() for s in focus_symbols}
    focus_keywords_lower = [k.lower() for k in focus_keywords]

    seeds: set[str] = set()
    for node in graph.nodes:
        # File match
        if node.source_anchor.file_path in focus_files_set:
            seeds.add(node.node_id)
            continue
        # Symbol match
        sym = node.semantic_contract.get("symbol_name", "").lower()
        if sym in focus_symbols_lower:
            seeds.add(node.node_id)
            continue
        # Keyword match (only if in focus files or nearby)
        if focus_keywords_lower and node.source_anchor.file_path in focus_files_set:
            text = f"{node.node_id} {sym}".lower()
            if any(kw in text for kw in focus_keywords_lower):
                seeds.add(node.node_id)

    seed_time = time.time() - t0 - adj_time
    print(f"    Seeds: {len(seeds)} in {seed_time:.1f}s")

    # BFS from seeds (O(budget))
    visited: set[str] = set()
    queue: deque[tuple[str, int]] = deque()
    for s in seeds:
        queue.append((s, 0))

    while queue and len(visited) < node_budget:
        nid, depth = queue.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        if depth < max_depth:
            for neighbor in adjacency.get(nid, set()):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
            for neighbor in reverse_adj.get(nid, set()):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

    bfs_time = time.time() - t0 - adj_time - seed_time
    print(f"    BFS: {len(visited)} nodes in {bfs_time:.1f}s")

    # Build projected nodes/edges
    projected_nodes = []
    for nid in visited:
        node = node_map.get(nid)
        if node:
            projected_nodes.append(node.to_dict())

    projected_edges = []
    edge_set: set[str] = set()
    for edge in graph.edges:
        if edge.from_node in visited and edge.to_node in visited:
            if edge.edge_id not in edge_set:
                projected_edges.append(edge.to_dict())
                edge_set.add(edge.edge_id)

    edge_time = time.time() - t0 - adj_time - seed_time - bfs_time
    print(f"    Edges: {len(projected_edges)} in {edge_time:.1f}s")

    # Lightweight confidence (no fan-out z-scores)
    confidence = {
        "confidence_overall": 0.65,
        "lookup_decision_hint": "targeted_lookup",
        "per_node_confidence": [],
        "per_edge_confidence": [],
    }

    total_time = time.time() - t0
    print(f"    Total projection: {total_time:.1f}s")

    return {
        "trace_id": f"trace-django-fast-{operation_family}",
        "operation_family": operation_family,
        "prompt_profile": {},
        "projected_nodes": projected_nodes,
        "projected_edges": projected_edges,
        "confidence": confidence,
        "reasoning_path": [],
        "validation": {},
        "stats": {
            "seed_count": len(seeds),
            "projected_node_count": len(projected_nodes),
            "projected_edge_count": len(projected_edges),
            "graph_node_count": len(graph.nodes),
        },
    }


def main() -> None:
    graph_path = ROOT / "experiments" / "runs" / "scale-django" / "graph.json"
    repo_root = ROOT / "experiments" / "external-repos" / "django"
    out_dir = ROOT / "experiments" / "runs" / "django-stress-test"
    prompts_dir = out_dir / "consumer-prompts"
    reports_dir = ROOT / "experiments" / "reports"

    out_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading Django graph...")
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

        print(f"\n{'='*60}")
        print(f"Task: {task_id} ({family}/{of})")

        # Fast projection
        projection = _fast_project(
            graph,
            focus_files=task["focus_files"],
            focus_symbols=task["focus_symbols"],
            focus_keywords=task["focus_keywords"],
            max_depth=task["max_depth"],
            operation_family=of,
        )
        proj_nodes = len(projection["projected_nodes"])
        proj_edges = len(projection["projected_edges"])

        # Save projection
        proj_path = out_dir / f"proj-{task_id}.json"
        with open(proj_path, "w", encoding="utf-8") as f:
            json.dump(projection, f, indent=2)

        # Render Plan A clue
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

        # Purity
        passed, violations = validate_clue_purity(clue)

        # Compression
        metrics = compute_compression_metrics(
            task_id=task_id, clue_view=clue, projection_trace=projection,
            repo_root=str(repo_root), plan="a",
        )

        print(f"  Tokens: clue={metrics['clue_tokens']}, raw={metrics['raw_first_tokens']}, proj={metrics['projection_tokens']}")
        print(f"  CCR: {metrics['ccr']:.4f} ({'PASS' if metrics['ccr'] >= 0.85 else 'FAIL'})")
        print(f"  Purity: {'PASS' if passed else 'FAIL'}")

        # Consumer prompt
        template = (ROOT / "scaffold" / "prompts" / "arm-plan-a.md").read_text(encoding="utf-8")
        prompt = template.replace("{{QUESTION}}", question)
        prompt = prompt.replace("{{CLUE_JSON}}", json.dumps(clue, indent=2, ensure_ascii=False))

        prompt_fname = f"{task_id}_plan-a.prompt.md"
        (prompts_dir / prompt_fname).write_text(prompt, encoding="utf-8")
        clue_fname = f"{task_id}_plan-a.clue.json"
        (prompts_dir / clue_fname).write_text(
            json.dumps(clue, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        prompt_manifest.append({
            "task_id": task_id, "family": family, "plan": "a",
            "prompt_file": prompt_fname,
            "response_file": prompt_fname.replace(".prompt.md", ".response.md"),
            "clue_file": clue_fname,
            "question": question,
            "prompt_tokens": count_tokens(prompt),
            "clue_tokens": metrics["clue_tokens"],
        })

        results.append({
            "task_id": task_id, "family": family, "operation_family": of,
            "proj_nodes": proj_nodes, "proj_edges": proj_edges,
            "entity_count": entity_count,
            "purity_pass": passed,
            "clue_tokens": metrics["clue_tokens"],
            "raw_tokens": metrics["raw_first_tokens"],
            "proj_tokens": metrics["projection_tokens"],
            "ccr": metrics["ccr"],
            "ccr_pass": metrics["ccr"] >= 0.85,
        })

    # Save
    results_path = reports_dir / "django-stress-test-results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    manifest_path = prompts_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(prompt_manifest, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print(f"DJANGO STRESS TEST RESULTS (45K nodes)")
    print(f"{'='*60}")
    successful = [r for r in results if "error" not in r]
    if successful:
        for r in successful:
            print(f"  {r['task_id']}: CCR={r['ccr']:.4f} clue={r['clue_tokens']}t "
                  f"raw={r['raw_tokens']}t entities={r['entity_count']} "
                  f"purity={'OK' if r['purity_pass'] else 'FAIL'}")
        mean_ccr = sum(r["ccr"] for r in successful) / len(successful)
        pass_85 = sum(1 for r in successful if r["ccr_pass"])
        print(f"\n  Mean CCR: {mean_ccr:.4f}")
        print(f"  Pass ≥0.85: {pass_85}/{len(successful)}")
        print(f"  All purity: {sum(1 for r in successful if r['purity_pass'])}/{len(successful)}")

    print(f"\n  Prompts: {prompts_dir}")
    print(f"  Results: {results_path}")


if __name__ == "__main__":
    main()
