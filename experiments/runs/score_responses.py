"""Score saved LLM responses against clue artifacts.

Reads .response.md files from consumer-prompts/, scores them using
the heuristic judge, and produces the final DFCR per family per plan.

Usage:
    python experiments/runs/score_responses.py

Expects:
    experiments/runs/consumer-prompts/
    ├── manifest.json
    ├── flask-tf1-001_plan-a.response.md   ← you saved these
    ├── flask-tf1-001_plan-a.clue.json     ← auto-generated
    └── ...
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.judge import score_heuristic
from codeclue_research.token_counter import count_tokens


def main() -> None:
    prompts_dir = ROOT / "experiments" / "runs" / "consumer-prompts"
    reports_dir = ROOT / "experiments" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = prompts_dir / "manifest.json"
    if not manifest_path.is_file():
        print("ERROR: No manifest.json found. Run generate_consumer_prompts.py first.")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    results: list[dict[str, Any]] = []
    missing: list[str] = []
    scored: int = 0

    for entry in manifest:
        task_id = entry["task_id"]
        plan = entry["plan"]
        family = entry["family"]
        question = entry["question"]

        response_file = prompts_dir / entry["response_file"]
        clue_file = prompts_dir / entry["clue_file"]

        if not response_file.is_file():
            missing.append(entry["response_file"])
            continue

        if not clue_file.is_file():
            missing.append(entry["clue_file"])
            continue

        # Load response and clue
        answer_text = response_file.read_text(encoding="utf-8")
        with open(clue_file, "r", encoding="utf-8") as f:
            clue = json.load(f)

        # Score using content-quality heuristic
        # Use a reasonable default gold spec (threshold 0.60)
        gold_spec = {
            "thresholds": {"path_fidelity_min": 0.60},
        }
        score = score_heuristic(answer_text, gold_spec, clue)

        results.append({
            "task_id": task_id,
            "family": family,
            "plan": plan,
            "question": question,
            "heuristic_score": score,
            "sufficient": score["sufficient"],
            "path_fidelity": score["path_fidelity"],
            "answer_tokens": count_tokens(answer_text),
            "clue_tokens": entry.get("clue_tokens", 0),
            "response_file": entry["response_file"],
        })
        scored += 1

        status = "✓" if score["sufficient"] else "✗"
        print(f"  {status} {task_id}/plan-{plan}: fidelity={score['path_fidelity']:.3f} "
              f"(sym={score['symbol_recall']:.2f} beh={score['behavior_recall']:.2f} "
              f"risk={score['risk_coverage']:.2f})")

    # Aggregate by family and plan
    families = ["TF1", "TF2", "TF3", "TF4", "TF5"]
    summary: dict[str, Any] = {}

    for plan in ["a", "b"]:
        plan_results = [r for r in results if r["plan"] == plan]
        if not plan_results:
            continue

        for fam in families:
            fam_results = [r for r in plan_results if r["family"] == fam]
            if not fam_results:
                continue
            sufficient = sum(1 for r in fam_results if r["sufficient"])
            key = f"{plan}_{fam}"
            summary[key] = {
                "plan": plan.upper(),
                "family": fam,
                "task_count": len(fam_results),
                "sufficient_count": sufficient,
                "dfcr": round(sufficient / len(fam_results), 4),
                "mean_fidelity": round(
                    sum(r["path_fidelity"] for r in fam_results) / len(fam_results), 4
                ),
            }

        # Overall
        sufficient_all = sum(1 for r in plan_results if r["sufficient"])
        summary[f"{plan}_overall"] = {
            "plan": plan.upper(),
            "family": "ALL",
            "task_count": len(plan_results),
            "sufficient_count": sufficient_all,
            "dfcr": round(sufficient_all / len(plan_results), 4),
            "mean_fidelity": round(
                sum(r["path_fidelity"] for r in plan_results) / len(plan_results), 4
            ),
        }

    output = {
        "per_task": results,
        "summary": summary,
        "scored": scored,
        "missing_responses": missing,
    }

    out_path = reports_dir / "real-consumer-ab-results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n=== REAL CONSUMER SCORING RESULTS ===")
    print(f"Scored: {scored} / {len(manifest)} tasks")
    print(f"Missing responses: {len(missing)}")
    for key, val in sorted(summary.items()):
        print(f"  {key}: DFCR={val['dfcr']:.2f} fidelity={val['mean_fidelity']:.3f} ({val['sufficient_count']}/{val['task_count']})")
    print(f"\nSaved: {out_path}")

    if missing:
        print(f"\nStill need responses for:")
        for m in missing[:10]:
            print(f"  {m}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")


if __name__ == "__main__":
    main()
