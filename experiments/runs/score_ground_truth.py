"""Score LLM responses against ground-truth gold answers.

Compares both Arm A (raw-source) and Arm B (clue-only) responses against
verified gold-truth answers. Produces the definitive fidelity comparison.

Usage:
    python experiments/runs/score_ground_truth.py

Scores:
- Symbol recall: fraction of gold symbols mentioned in response
- Fact recall: fraction of gold facts reflected in response  
- Combined fidelity: weighted average
- Arm A vs Arm B comparison per task and per family
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.token_counter import count_tokens


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _score_against_gold(
    answer_text: str,
    gold: dict[str, Any],
) -> dict[str, Any]:
    """Score a response against gold-truth answer.

    Measures:
    - symbol_recall: fraction of gold symbols mentioned
    - fact_recall: fraction of gold facts reflected (fuzzy keyword match)
    - combined_fidelity: 0.5 * symbol_recall + 0.5 * fact_recall
    """
    normalized = _normalize(answer_text)

    # Symbol recall
    gold_symbols = gold.get("gold_symbols", [])
    symbol_hits = 0
    symbol_details: list[dict] = []
    for sym in gold_symbols:
        # Check various forms: full name, short name, underscored, partial
        variants = [sym.lower()]
        if "." in sym:
            variants.append(sym.rsplit(".", 1)[-1].lower())  # short name
            variants.append(sym.replace(".", "_").lower())    # underscored
        # Also check without leading underscore variations
        for v in list(variants):
            if v.startswith("_"):
                variants.append(v.lstrip("_"))
        found = any(v in normalized for v in variants)
        symbol_details.append({"symbol": sym, "found": found})
        if found:
            symbol_hits += 1

    symbol_recall = symbol_hits / len(gold_symbols) if gold_symbols else 0.0

    # Fact recall (flexible keyword matching)
    gold_facts = gold.get("gold_facts", [])
    fact_hits = 0
    fact_details: list[dict] = []
    for fact in gold_facts:
        # Extract key words (>3 chars) from fact
        fact_words = [w for w in _normalize(fact).split() if len(w) > 3]
        if not fact_words:
            fact_hits += 1
            fact_details.append({"fact": fact, "found": True, "match_ratio": 1.0})
            continue
        # More lenient: check if ANY key concept word appears
        # Also check stemmed/partial matches
        matches = 0
        for w in fact_words:
            if w in normalized:
                matches += 1
            elif len(w) > 5 and w[:5] in normalized:
                matches += 0.7  # partial stem match
            elif any(w in nw or nw in w for nw in normalized.split() if len(nw) > 4):
                matches += 0.5  # substring match
        ratio = matches / len(fact_words)
        found = ratio >= 0.3  # Lowered from 0.4 — facts use different wording
        fact_details.append({"fact": fact, "found": found, "match_ratio": round(ratio, 2)})
        if found:
            fact_hits += 1

    fact_recall = fact_hits / len(gold_facts) if gold_facts else 0.0

    # Combined fidelity
    fidelity = 0.5 * symbol_recall + 0.5 * fact_recall

    return {
        "symbol_recall": round(symbol_recall, 4),
        "fact_recall": round(fact_recall, 4),
        "fidelity": round(fidelity, 4),
        "symbol_hits": symbol_hits,
        "symbol_total": len(gold_symbols),
        "fact_hits": fact_hits,
        "fact_total": len(gold_facts),
        "answer_tokens": count_tokens(answer_text),
        "answer_words": len(answer_text.split()),
        "symbol_details": symbol_details,
        "fact_details": fact_details,
    }


def main() -> None:
    val_dir = ROOT / "experiments" / "runs" / "ground-truth-validation"
    gold_dir = val_dir / "gold"
    arm_a_dir = val_dir / "prompts"
    arm_b_dir = ROOT / "experiments" / "runs" / "consumer-prompts"
    reports_dir = ROOT / "experiments" / "reports"

    manifest_path = val_dir / "manifest.json"
    if not manifest_path.is_file():
        print("ERROR: Run generate_ground_truth_validation.py first")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    results: list[dict[str, Any]] = []
    arm_a_missing: list[str] = []
    arm_b_missing: list[str] = []

    for entry in manifest:
        task_id = entry["task_id"]
        family = entry["family"]

        # Load gold
        gold_path = val_dir / entry["gold_file"]
        with open(gold_path, "r", encoding="utf-8") as f:
            gold = json.load(f)

        # Score Arm A (raw-source response)
        arm_a_resp = arm_a_dir / entry["arm_a_response"]
        arm_a_score = None
        if arm_a_resp.is_file():
            arm_a_text = arm_a_resp.read_text(encoding="utf-8")
            arm_a_score = _score_against_gold(arm_a_text, gold)
            arm_a_score["arm"] = "A"
        else:
            arm_a_missing.append(task_id)

        # Score Arm B (clue response)
        arm_b_resp = arm_b_dir / f"{task_id}_plan-a.response.md"
        arm_b_score = None
        if arm_b_resp.is_file():
            arm_b_text = arm_b_resp.read_text(encoding="utf-8")
            arm_b_score = _score_against_gold(arm_b_text, gold)
            arm_b_score["arm"] = "B"
        else:
            arm_b_missing.append(task_id)

        task_result: dict[str, Any] = {
            "task_id": task_id,
            "family": family,
            "question": entry["question"],
        }

        if arm_a_score:
            task_result["arm_a"] = arm_a_score
        if arm_b_score:
            task_result["arm_b"] = arm_b_score

        # Compute delta if both present
        if arm_a_score and arm_b_score:
            task_result["fidelity_delta"] = round(
                arm_b_score["fidelity"] - arm_a_score["fidelity"], 4
            )
            task_result["symbol_delta"] = round(
                arm_b_score["symbol_recall"] - arm_a_score["symbol_recall"], 4
            )
            task_result["fact_delta"] = round(
                arm_b_score["fact_recall"] - arm_a_score["fact_recall"], 4
            )

        results.append(task_result)

    # Aggregate
    families = ["TF1", "TF2", "TF3", "TF4", "TF5"]
    summary: dict[str, Any] = {}

    for arm_key in ["arm_a", "arm_b"]:
        arm_label = arm_key[-1].upper()
        scored = [r for r in results if arm_key in r]
        if not scored:
            continue

        for fam in families:
            fam_results = [r for r in scored if r["family"] == fam]
            if not fam_results:
                continue
            fidelities = [r[arm_key]["fidelity"] for r in fam_results]
            sym_recalls = [r[arm_key]["symbol_recall"] for r in fam_results]
            fact_recalls = [r[arm_key]["fact_recall"] for r in fam_results]

            summary[f"{arm_label}_{fam}"] = {
                "arm": arm_label,
                "family": fam,
                "n": len(fam_results),
                "mean_fidelity": round(sum(fidelities) / len(fidelities), 4),
                "mean_symbol_recall": round(sum(sym_recalls) / len(sym_recalls), 4),
                "mean_fact_recall": round(sum(fact_recalls) / len(fact_recalls), 4),
            }

        all_fidelities = [r[arm_key]["fidelity"] for r in scored]
        summary[f"{arm_label}_overall"] = {
            "arm": arm_label,
            "family": "ALL",
            "n": len(scored),
            "mean_fidelity": round(sum(all_fidelities) / len(all_fidelities), 4),
        }

    # Delta summary (A vs B)
    both = [r for r in results if "arm_a" in r and "arm_b" in r]
    if both:
        deltas = [r["fidelity_delta"] for r in both]
        summary["delta_overall"] = {
            "n": len(both),
            "mean_fidelity_delta": round(sum(deltas) / len(deltas), 4),
            "b_wins": sum(1 for d in deltas if d > 0),
            "a_wins": sum(1 for d in deltas if d < 0),
            "ties": sum(1 for d in deltas if d == 0),
        }

    output = {
        "per_task": results,
        "summary": summary,
        "arm_a_missing": arm_a_missing,
        "arm_b_missing": arm_b_missing,
    }

    out_path = reports_dir / "ground-truth-validation-results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    # Print results
    print(f"\n{'='*70}")
    print(f"GROUND TRUTH VALIDATION RESULTS")
    print(f"{'='*70}")

    print(f"\n--- Per-Task Scores ---")
    print(f"{'Task':<22} {'Fam':>4} {'Arm A Fid':>10} {'Arm B Fid':>10} {'Delta':>8}")
    print(f"{'-'*22} {'-'*4} {'-'*10} {'-'*10} {'-'*8}")
    for r in results:
        a_fid = f"{r['arm_a']['fidelity']:.3f}" if "arm_a" in r else "---"
        b_fid = f"{r['arm_b']['fidelity']:.3f}" if "arm_b" in r else "---"
        delta = f"{r['fidelity_delta']:+.3f}" if "fidelity_delta" in r else "---"
        print(f"{r['task_id']:<22} {r['family']:>4} {a_fid:>10} {b_fid:>10} {delta:>8}")

    print(f"\n--- Per-Family Summary ---")
    for key in sorted(summary.keys()):
        s = summary[key]
        if "mean_fidelity" in s:
            print(f"  {key}: fidelity={s['mean_fidelity']:.3f} (n={s.get('n', '?')})")

    if "delta_overall" in summary:
        d = summary["delta_overall"]
        print(f"\n--- Arm A vs Arm B ---")
        print(f"  Mean delta (B-A): {d['mean_fidelity_delta']:+.3f}")
        print(f"  B wins: {d['b_wins']}, A wins: {d['a_wins']}, Ties: {d['ties']}")

    print(f"\nArm A (raw) missing: {len(arm_a_missing)} — {arm_a_missing}")
    print(f"Arm B (clue) missing: {len(arm_b_missing)} — {arm_b_missing}")
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
