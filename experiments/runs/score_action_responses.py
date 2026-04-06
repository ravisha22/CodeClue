"""Score action-benchmark LLM responses against gold localization data.

Reads .response.md files for both Arm A (raw) and Arm B (clue),
scores against gold files/symbols, produces Arm A vs B comparison.

Usage:
    python experiments/runs/score_action_responses.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.token_counter import count_tokens


def _score(answer_text: str, gold_files: list[str], gold_symbols: list[str]) -> dict[str, Any]:
    normalized = answer_text.lower()

    file_hits = 0
    for gf in gold_files:
        basename = Path(gf).name.lower()
        if gf.lower() in normalized or basename in normalized:
            file_hits += 1
        elif any(p in normalized for p in gf.lower().replace("/", " ").split() if len(p) > 3):
            file_hits += 0.5
    file_recall = file_hits / len(gold_files) if gold_files else 0.0

    symbol_hits = 0
    for sym in gold_symbols:
        variants = [sym.lower()]
        if "." in sym:
            variants.append(sym.rsplit(".", 1)[-1].lower())
        if any(v in normalized for v in variants):
            symbol_hits += 1
    symbol_recall = symbol_hits / len(gold_symbols) if gold_symbols else 0.0

    loc_acc = 0.4 * file_recall + 0.6 * symbol_recall

    return {
        "file_recall": round(file_recall, 4),
        "symbol_recall": round(symbol_recall, 4),
        "localization_accuracy": round(loc_acc, 4),
        "sufficient": loc_acc >= 0.60,
    }


def main() -> None:
    bench_dir = ROOT / "experiments" / "runs" / "action-benchmark"
    reports_dir = ROOT / "experiments" / "reports"

    manifest_path = bench_dir / "manifest.json"
    if not manifest_path.is_file():
        print("ERROR: Run run_action_benchmark.py first")
        return

    with open(manifest_path) as f:
        manifest = json.load(f)

    results = []
    for entry in manifest:
        task_id = entry["task_id"]
        gold_files = entry["gold_files"]
        gold_symbols = entry["gold_symbols"]

        arm_a_path = bench_dir / entry["arm_a_response"]
        arm_b_path = bench_dir / entry["arm_b_response"]

        arm_a_score = None
        if arm_a_path.is_file():
            arm_a_score = _score(arm_a_path.read_text(encoding="utf-8"), gold_files, gold_symbols)
            arm_a_score["arm"] = "A"
            arm_a_score["tokens"] = entry["arm_a_tokens"]

        arm_b_score = None
        if arm_b_path.is_file():
            arm_b_score = _score(arm_b_path.read_text(encoding="utf-8"), gold_files, gold_symbols)
            arm_b_score["arm"] = "B"
            arm_b_score["tokens"] = entry["arm_b_tokens"]

        row = {"task_id": task_id, "family": entry["family"]}
        if arm_a_score:
            row["arm_a"] = arm_a_score
        if arm_b_score:
            row["arm_b"] = arm_b_score
        if arm_a_score and arm_b_score:
            row["delta"] = round(arm_b_score["localization_accuracy"] - arm_a_score["localization_accuracy"], 4)
            row["token_ratio"] = round(arm_b_score["tokens"] / arm_a_score["tokens"], 3) if arm_a_score["tokens"] else 0

        results.append(row)

    # Print
    print(f"\n{'Task':<35} {'ArmA Loc':>8} {'ArmB Loc':>8} {'Delta':>7} {'TokRatio':>9}")
    print("-" * 72)
    for r in results:
        a = f"{r['arm_a']['localization_accuracy']:.3f}" if "arm_a" in r else "---"
        b = f"{r['arm_b']['localization_accuracy']:.3f}" if "arm_b" in r else "---"
        d = f"{r['delta']:+.3f}" if "delta" in r else "---"
        tr = f"{r['token_ratio']:.3f}" if "token_ratio" in r else "---"
        print(f"{r['task_id']:<35} {a:>8} {b:>8} {d:>7} {tr:>9}")

    out_path = reports_dir / "action-benchmark-scored.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
