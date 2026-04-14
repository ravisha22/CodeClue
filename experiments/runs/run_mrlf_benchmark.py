"""Generate MRLF clues for all available external repos and report metrics."""

from __future__ import annotations
import json
import time
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store, write_detail_store, _word_count

REPOS = [
    ("flask", "experiments/external-repos/flask"),
    ("fastapi", "experiments/external-repos/fastapi"),
    ("httpx", "experiments/external-repos/httpx"),
    ("gin", "experiments/external-repos/gin"),
    ("nest", "experiments/external-repos/nest"),
    ("typeorm", "experiments/external-repos/typeorm"),
    ("django", "experiments/external-repos/django"),
]

QUESTION = "What is the downstream impact of modifying the configuration loading?"

OUTPUT_DIR = Path("experiments/runs/mrlf-benchmark")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for name, path in REPOS:
        repo_path = Path(path)
        if not repo_path.exists():
            print(f"  {name}: SKIP (not found)")
            continue

        print(f"  {name}: extracting...", end=" ", flush=True)
        t0 = time.time()
        try:
            graph = extract_graph(repo_path)
        except Exception as e:
            print(f"EXTRACT ERROR: {e}")
            continue
        t_extract = time.time() - t0

        n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
        n_sym = len(graph.nodes) - n_mod
        n_edges = len(graph.edges)

        print(f"{n_mod} mod, {n_sym} sym, {n_edges} edges ({t_extract:.1f}s)...", end=" ", flush=True)

        t0 = time.time()
        clue = render_mrlf(graph, QUESTION, repo_root=str(repo_path))
        t_render = time.time() - t0

        words = _word_count(clue)
        tokens_est = int(words * 1.3)

        # Write clue file
        clue_path = OUTPUT_DIR / f"{name}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")

        # Generate and write detail store
        t0 = time.time()
        detail = generate_detail_store(graph, repo_root=str(repo_path))
        t_detail = time.time() - t0
        detail_path = OUTPUT_DIR / f"{name}.codeclue-detail"
        write_detail_store(detail, detail_path)
        detail_size = detail_path.stat().st_size

        record = {
            "repo": name,
            "modules": n_mod,
            "symbols": n_sym,
            "edges": n_edges,
            "clue_words": words,
            "clue_tokens_est": tokens_est,
            "detail_records": len(detail),
            "detail_size_kb": round(detail_size / 1024, 1),
            "extract_time_s": round(t_extract, 2),
            "render_time_s": round(t_render, 2),
            "detail_time_s": round(t_detail, 2),
        }
        results.append(record)
        print(f"{words} words (~{tokens_est} tok), detail={len(detail)} records ({t_render:.2f}s render)")

    # Write summary
    summary_path = OUTPUT_DIR / "mrlf-benchmark-summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSummary written to {summary_path}")

    # Print table
    print(f"\n{'Repo':12s} | {'Mod':>4s} | {'Sym':>5s} | {'Words':>5s} | {'~Tokens':>7s} | {'Detail':>6s} | {'Extract':>7s} | {'Render':>6s}")
    print("-" * 80)
    for r in results:
        print(f"{r['repo']:12s} | {r['modules']:4d} | {r['symbols']:5d} | {r['clue_words']:5d} | {r['clue_tokens_est']:>7d} | {r['detail_records']:6d} | {r['extract_time_s']:6.1f}s | {r['render_time_s']:5.2f}s")


if __name__ == "__main__":
    main()
