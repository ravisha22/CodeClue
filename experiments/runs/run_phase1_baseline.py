"""Phase 1: Baseline CCR Measurement.

For each repo:
  1. Count raw source tokens (all source files, excluding tests/docs/generated)
  2. Count MRLF clue tokens (from generated .codeclue files)
  3. Compute CCR = 1 - (clue_tokens / raw_tokens)
  4. Include Django scale test

Uses tiktoken (cl100k_base) for tokenization — same as GPT-4/Claude.
"""

from __future__ import annotations

import json
import time
import traceback
from pathlib import Path

import tiktoken

from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf, generate_detail_store, write_detail_store, _word_count

# Tokenizer
ENC = tiktoken.get_encoding("cl100k_base")

# Directories to exclude from raw token count
EXCLUDE_DIRS = {
    "__pycache__", ".git", ".github", ".tox", ".mypy_cache", ".pytest_cache",
    "node_modules", ".venv", "venv", ".eggs", "dist", "build", "vendor",
    ".generated", "__generated__",
}

# File patterns to exclude
EXCLUDE_PATTERNS = {"_test.go", "_test.py"}  # Go/Python test conventions

REPOS = [
    ("flask", "experiments/external-repos/flask", [".py"]),
    ("httpx", "experiments/external-repos/httpx", [".py"]),
    ("gin", "experiments/external-repos/gin", [".go"]),
    ("fastapi", "experiments/external-repos/fastapi", [".py"]),
    ("django", "experiments/external-repos/django", [".py"]),
]

QUESTION = "What is the downstream impact of modifying the configuration loading?"
OUTPUT_DIR = Path("experiments/runs/mrlf-benchmark")


def _should_exclude_path(path: Path) -> bool:
    """Check if a path should be excluded from raw token counting."""
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    name = path.name.lower()
    # Exclude test files
    if name.startswith("test_") or name.endswith("_test.py") or name.endswith("_test.go"):
        return True
    if "/tests/" in str(path).replace("\\", "/") or "\\tests\\" in str(path):
        return True
    # Exclude docs
    if "/docs/" in str(path).replace("\\", "/") or "\\docs\\" in str(path):
        return True
    return False


def count_raw_tokens(repo_path: Path, extensions: list[str]) -> tuple[int, int]:
    """Count total tokens in all source files (excluding tests/docs/generated).
    
    Returns (token_count, file_count).
    """
    total_tokens = 0
    file_count = 0
    for ext in extensions:
        for f in repo_path.rglob(f"*{ext}"):
            if _should_exclude_path(f.relative_to(repo_path)):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
                tokens = len(ENC.encode(text))
                total_tokens += tokens
                file_count += 1
            except OSError:
                continue
    return total_tokens, file_count


def count_clue_tokens(clue_text: str) -> int:
    """Count actual tokens in a clue string using tiktoken."""
    return len(ENC.encode(clue_text))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    print("Phase 1: Baseline CCR Measurement")
    print("=" * 80)

    for name, path, exts in REPOS:
        repo_path = Path(path)
        if not repo_path.exists():
            print(f"  {name}: SKIP (not found)")
            continue

        print(f"\n  {name}:")

        # Step 1: Raw source tokens
        print(f"    Counting raw source tokens...", end=" ", flush=True)
        t0 = time.time()
        raw_tokens, raw_files = count_raw_tokens(repo_path, exts)
        t_raw = time.time() - t0
        print(f"{raw_tokens:,} tokens across {raw_files} files ({t_raw:.1f}s)")

        # Step 2: Extract graph + render MRLF
        print(f"    Extracting graph...", end=" ", flush=True)
        t0 = time.time()
        try:
            graph = extract_graph(repo_path)
        except Exception as e:
            print(f"EXTRACT ERROR: {e}")
            traceback.print_exc()
            continue
        t_extract = time.time() - t0
        n_mod = sum(1 for n in graph.nodes if n.node_type == "module")
        n_sym = len(graph.nodes) - n_mod
        n_edges = len(graph.edges)
        print(f"{n_mod} mod, {n_sym} sym, {n_edges} edges ({t_extract:.1f}s)")

        print(f"    Rendering MRLF clue...", end=" ", flush=True)
        t0 = time.time()
        clue = render_mrlf(graph, QUESTION, repo_root=str(repo_path))
        t_render = time.time() - t0

        # Step 3: Clue tokens (actual tiktoken, not estimate)
        clue_tokens = count_clue_tokens(clue)
        clue_words = _word_count(clue)
        actual_ratio = clue_tokens / clue_words if clue_words > 0 else 0
        print(f"{clue_words} words, {clue_tokens} tokens (ratio={actual_ratio:.2f}) ({t_render:.1f}s)")

        # Save clue
        clue_path = OUTPUT_DIR / f"{name}.codeclue"
        clue_path.write_text(clue, encoding="utf-8")

        # Generate detail store
        print(f"    Generating detail store...", end=" ", flush=True)
        t0 = time.time()
        detail = generate_detail_store(graph, repo_root=str(repo_path))
        t_detail = time.time() - t0
        detail_path = OUTPUT_DIR / f"{name}.codeclue-detail"
        write_detail_store(detail, detail_path)
        detail_size_kb = detail_path.stat().st_size / 1024
        print(f"{len(detail)} records, {detail_size_kb:.1f} KB ({t_detail:.1f}s)")

        # Step 4: CCR
        ccr = 1 - (clue_tokens / raw_tokens) if raw_tokens > 0 else 0
        ccr_pass = ccr >= 0.85

        print(f"    CCR = {ccr:.4f} ({ccr*100:.1f}%) {'PASS' if ccr_pass else 'FAIL'}")
        print(f"    Budget: {clue_tokens}/4150 tokens ({clue_tokens/4150*100:.0f}%)")

        record = {
            "repo": name,
            "modules": n_mod,
            "symbols": n_sym,
            "edges": n_edges,
            "raw_files": raw_files,
            "raw_tokens": raw_tokens,
            "clue_words": clue_words,
            "clue_tokens": clue_tokens,
            "word_token_ratio": round(actual_ratio, 3),
            "ccr": round(ccr, 4),
            "ccr_pass": ccr_pass,
            "budget_pct": round(clue_tokens / 4150 * 100, 1),
            "detail_records": len(detail),
            "detail_size_kb": round(detail_size_kb, 1),
            "extract_time_s": round(t_extract, 2),
            "render_time_s": round(t_render, 2),
        }
        results.append(record)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n{'Repo':12s} | {'Raw Tok':>8s} | {'Clue Tok':>8s} | {'CCR':>6s} | {'Pass':>4s} | {'Budget%':>7s}")
    print("-" * 60)
    for r in results:
        print(f"{r['repo']:12s} | {r['raw_tokens']:>8,} | {r['clue_tokens']:>8,} | {r['ccr']:.4f} | {'YES' if r['ccr_pass'] else 'NO':>4s} | {r['budget_pct']:>6.1f}%")

    passing = sum(1 for r in results if r["ccr_pass"])
    total = len(results)
    gate_pass = passing >= 3  # Gate: ≥3 of repos pass
    print(f"\nGate: CCR ≥ 0.85 for ≥ 3 repos: {passing}/{total} pass → {'GATE PASS' if gate_pass else 'GATE FAIL'}")

    # Word-to-token ratio validation
    ratios = [r["word_token_ratio"] for r in results if r["word_token_ratio"] > 0]
    if ratios:
        mean_ratio = sum(ratios) / len(ratios)
        print(f"Mean word-to-token ratio: {mean_ratio:.3f} (design assumed 1.3)")

    # Save results
    summary_path = OUTPUT_DIR / "phase1-ccr-results.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {summary_path}")


if __name__ == "__main__":
    main()
