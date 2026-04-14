"""Evaluation monitor for CodeClue MRLF generalization.

Prevents overfitting by enforcing dev/validation/blind splits,
computing per-knowledge-type accuracy, and detecting dev-val gaps.

Usage:
    python -m experiments.runs.eval_monitor baseline
    python -m experiments.runs.eval_monitor check
    python -m experiments.runs.eval_monitor report --split validation
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EVAL_CONFIG = REPO_ROOT / "experiments" / "eval-config.json"
GOLD_TASKS = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "blind-gold-tasks.json"
RESULTS_FILE = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "blind-eval-results.jsonl"
BASELINE_FILE = REPO_ROOT / "experiments" / "runs" / "eval-baseline.json"


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
@dataclass
class EvalResult:
    """Result for a single knowledge type on a single split."""
    knowledge_type: str
    split: str
    covered: int
    total: int

    @property
    def accuracy(self) -> float:
        return self.covered / self.total if self.total > 0 else 0.0

    @property
    def wilson_ci(self) -> tuple[float, float]:
        """Wilson score 95% confidence interval."""
        n = self.total
        if n == 0:
            return (0.0, 1.0)
        z = 1.96  # 95% CI
        p_hat = self.covered / n
        denom = 1 + z**2 / n
        center = (p_hat + z**2 / (2 * n)) / denom
        spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n) / denom
        return (max(0.0, center - spread), min(1.0, center + spread))


def format_result(r: EvalResult) -> str:
    """Format an EvalResult as a human-readable string."""
    ci = r.wilson_ci
    return (
        f"  {r.knowledge_type:15s} {r.covered:3d}/{r.total:<3d} = {r.accuracy:.1%}  "
        f"95% CI [{ci[0]:.1%}, {ci[1]:.1%}]"
    )


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------
def load_config() -> dict[str, Any]:
    """Load evaluation configuration."""
    with open(EVAL_CONFIG) as f:
        return json.load(f)


def get_split_for_repo(repo_name: str, config: dict) -> str | None:
    """Determine which split a repo belongs to."""
    for split_name, split_info in config["splits"].items():
        if repo_name in split_info["repos"]:
            return split_name
    return None


# ---------------------------------------------------------------------------
# Gold task knowledge type tagging
# ---------------------------------------------------------------------------
# Tags for existing gold facts. Each fact is tagged with its knowledge type.
# These are hand-assigned based on what information is required to answer.
GOLD_FACT_KNOWLEDGE_TYPES: dict[str, list[str]] = {
    # aiohttp-1: all mechanistic (require method body logic)
    "blind-aiohttp-1": ["mechanistic", "mechanistic", "mechanistic", "mechanistic"],
    # aiohttp-2: all mechanistic (require wiring/cleanup/unwind logic)
    "blind-aiohttp-2": ["mechanistic", "mechanistic", "mechanistic", "mechanistic"],
    # fiber-1: all mechanistic (require dispatch/routing internals)
    "blind-fiber-1": ["mechanistic", "mechanistic", "mechanistic", "mechanistic"],
    # fiber-2: all mechanistic (require panic/error handling flow)
    "blind-fiber-2": ["mechanistic", "mechanistic", "mechanistic", "mechanistic"],
    # click-1: all mechanistic (require decorator/dispatch chain)
    "blind-click-1": ["mechanistic", "mechanistic", "mechanistic", "mechanistic"],
    # click-2: all mechanistic (require precedence/conversion logic)
    "blind-click-2": ["mechanistic", "mechanistic", "mechanistic", "mechanistic"],
}


# ---------------------------------------------------------------------------
# Result loading and scoring
# ---------------------------------------------------------------------------
def load_results(results_path: Path | None = None) -> list[dict]:
    """Load evaluation results from JSONL file."""
    path = results_path or RESULTS_FILE
    if not path.exists():
        return []
    results = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def score_by_split_and_type(
    results: list[dict],
    config: dict,
) -> dict[str, dict[str, EvalResult]]:
    """Score results grouped by split and knowledge type.

    Returns: {split: {knowledge_type: EvalResult}}
    """
    # Initialize counters
    scores: dict[str, dict[str, dict[str, int]]] = {}

    for result in results:
        task_id = result["task_id"]
        # Extract repo name from task_id (e.g., "blind-aiohttp-1" -> "aiohttp")
        parts = task_id.split("-")
        if len(parts) >= 3:
            repo = parts[1]
        else:
            continue

        split = get_split_for_repo(repo, config)
        if split is None:
            continue

        # Get knowledge types for this task's facts
        kt_list = GOLD_FACT_KNOWLEDGE_TYPES.get(task_id, [])
        if not kt_list:
            continue

        if split not in scores:
            scores[split] = {}

        for i, score_entry in enumerate(result.get("scores", [])):
            if i >= len(kt_list):
                break
            kt = kt_list[i]
            if kt not in scores[split]:
                scores[split][kt] = {"covered": 0, "total": 0}
            scores[split][kt]["total"] += 1
            if score_entry.get("verdict") == "COVERED":
                scores[split][kt]["covered"] += 1

    # Convert to EvalResult objects
    output: dict[str, dict[str, EvalResult]] = {}
    for split_name, kt_data in scores.items():
        output[split_name] = {}
        for kt, counts in kt_data.items():
            output[split_name][kt] = EvalResult(
                knowledge_type=kt,
                split=split_name,
                covered=counts["covered"],
                total=counts["total"],
            )
    return output


# ---------------------------------------------------------------------------
# Overfitting detection
# ---------------------------------------------------------------------------
def check_overfitting(
    dev_results: dict[str, EvalResult],
    val_results: dict[str, EvalResult],
    max_gap_pp: float = 10.0,
) -> list[str]:
    """Check if dev accuracy exceeds validation accuracy by too much.

    Returns list of warnings (empty = no overfitting detected).
    """
    warnings = []
    all_types = set(dev_results.keys()) | set(val_results.keys())

    for kt in sorted(all_types):
        dev_acc = dev_results.get(kt, EvalResult(kt, "dev", 0, 0)).accuracy
        val_acc = val_results.get(kt, EvalResult(kt, "validation", 0, 0)).accuracy
        gap = (dev_acc - val_acc) * 100  # percentage points

        if gap > max_gap_pp:
            warnings.append(
                f"OVERFITTING on {kt}: dev={dev_acc:.1%} val={val_acc:.1%} "
                f"gap={gap:.1f}pp > {max_gap_pp}pp threshold"
            )

    return warnings


# ---------------------------------------------------------------------------
# Baseline capture
# ---------------------------------------------------------------------------
def capture_baseline(results: list[dict], config: dict) -> dict:
    """Capture current metrics as baseline for comparison."""
    scored = score_by_split_and_type(results, config)

    baseline = {
        "timestamp": "2026-04-14",
        "commit": "pre-generalization",
        "description": "Baseline before generalization plan implementation",
        "splits": {},
    }

    for split_name, kt_results in scored.items():
        baseline["splits"][split_name] = {}
        for kt, result in kt_results.items():
            ci = result.wilson_ci
            baseline["splits"][split_name][kt] = {
                "covered": result.covered,
                "total": result.total,
                "accuracy": round(result.accuracy, 4),
                "ci_lower": round(ci[0], 4),
                "ci_upper": round(ci[1], 4),
            }

    return baseline


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def print_report(results: list[dict], config: dict, split_filter: str | None = None):
    """Print formatted evaluation report."""
    scored = score_by_split_and_type(results, config)

    print("=" * 65)
    print("CodeClue MRLF Evaluation Report")
    print("=" * 65)

    for split_name in ["dev", "validation", "blind"]:
        if split_filter and split_name != split_filter:
            continue
        if split_name not in scored:
            print(f"\n--- {split_name.upper()} --- (no results)")
            continue

        print(f"\n--- {split_name.upper()} ---")
        kt_results = scored[split_name]
        total_covered = sum(r.covered for r in kt_results.values())
        total_facts = sum(r.total for r in kt_results.values())

        for kt in ["structural", "relational", "declarative", "mechanistic", "invariant"]:
            if kt in kt_results:
                print(format_result(kt_results[kt]))

        if total_facts > 0:
            overall = EvalResult("OVERALL", split_name, total_covered, total_facts)
            print(f"  {'─' * 50}")
            print(format_result(overall))

    # Overfitting check
    dev_results = scored.get("dev", {})
    val_results = scored.get("validation", {})
    if dev_results and val_results:
        max_gap = config.get("overfitting_detection", {}).get("max_dev_val_gap_pp", 10)
        warnings = check_overfitting(dev_results, val_results, max_gap)
        if warnings:
            print(f"\n⚠️  OVERFITTING DETECTED:")
            for w in warnings:
                print(f"  {w}")
        else:
            print(f"\n✅ No overfitting detected (dev-val gap < {max_gap}pp)")

    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python eval_monitor.py <baseline|check|report> [--split dev|validation|blind]")
        sys.exit(1)

    command = sys.argv[1]
    config = load_config()
    results = load_results()

    if command == "baseline":
        baseline = capture_baseline(results, config)
        with open(BASELINE_FILE, "w") as f:
            json.dump(baseline, f, indent=2)
        print(f"Baseline saved to {BASELINE_FILE}")
        print_report(results, config)

    elif command == "check":
        print_report(results, config)

    elif command == "report":
        split_filter = None
        if "--split" in sys.argv:
            idx = sys.argv.index("--split")
            if idx + 1 < len(sys.argv):
                split_filter = sys.argv[idx + 1]
        print_report(results, config, split_filter)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
