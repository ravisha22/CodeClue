"""Phase 5: Compile comparative verdict for Plan A vs Plan B.

Loads results from Phases 2-4 and produces stratified comparison tables.

Usage:
    python experiments/runs/compile_ab_verdict.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent


def _safe_div(num: float, den: float) -> float:
    return num / den if den > 0 else 0.0


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    reports_dir = ROOT / "experiments" / "reports"

    # Load all phase results
    compression = _load_json(reports_dir / "compression-ab-results.json")
    clue_only = _load_json(reports_dir / "clue-only-ab-results.json")
    drilldown = _load_json(reports_dir / "drilldown-ab-results.json")

    missing = []
    if not compression:
        missing.append("compression-ab-results.json")
    if not clue_only:
        missing.append("clue-only-ab-results.json")

    if missing:
        print(f"ERROR: Missing phase results: {', '.join(missing)}")
        print("Run the corresponding Phase scripts first.")
        return

    families = ["TF1", "TF2", "TF3", "TF4", "TF5"]
    plans = ["a", "b"]

    # ===== TABLE 1: Head-to-Head Per Family =====
    table1: list[dict[str, Any]] = []
    for fam in families:
        row: dict[str, Any] = {"family": fam}
        for plan in plans:
            # Compression
            comp_tasks = [t for t in compression.get("per_task", []) if t["plan"] == plan and t.get("family") == fam]
            ccrs = [t["ccr"] for t in comp_tasks]
            row[f"{plan}_mean_ccr"] = round(sum(ccrs) / len(ccrs), 4) if ccrs else 0

            # Clue-only DFCR
            co_key = f"{plan}_{fam}"
            co_data = clue_only.get("summary", {}).get(co_key, {})
            row[f"{plan}_dfcr"] = co_data.get("dfcr", 0)
            row[f"{plan}_mean_fidelity"] = co_data.get("mean_fidelity", 0)

        # Winner for this family
        a_dfcr = row.get("a_dfcr", 0)
        b_dfcr = row.get("b_dfcr", 0)
        if a_dfcr > b_dfcr:
            row["winner"] = "A"
        elif b_dfcr > a_dfcr:
            row["winner"] = "B"
        else:
            row["winner"] = "TIE"

        table1.append(row)

    # ===== TABLE 2: Pillar Scorecard =====
    table2: list[dict[str, Any]] = []

    for plan in plans:
        # Pillar 1: Compression
        comp_plan = [t for t in compression.get("per_task", []) if t["plan"] == plan]
        ccrs = [t["ccr"] for t in comp_plan]
        pass_85 = sum(1 for c in ccrs if c >= 0.85)
        pass_rate = _safe_div(pass_85, len(ccrs))

        table2.append({
            "pillar": "1-Compression",
            "plan": plan.upper(),
            "target": "CCR ≥ 0.85 for ≥70% of tasks",
            "value": f"{pass_rate:.1%} ({pass_85}/{len(ccrs)})",
            "pass": pass_rate >= 0.70,
        })

        # Pillar 2: Clue-Only Sufficiency
        co_overall = clue_only.get("summary", {}).get(f"{plan}_overall", {})
        dfcr = co_overall.get("dfcr", 0)
        suff = co_overall.get("sufficient_count", 0)
        total = co_overall.get("task_count", 0)

        # Check per-family (all must be ≥ 0.60)
        per_fam_pass = True
        for fam in families:
            fam_data = clue_only.get("summary", {}).get(f"{plan}_{fam}", {})
            if fam_data and fam_data.get("dfcr", 0) < 0.60:
                per_fam_pass = False

        table2.append({
            "pillar": "2-ClueOnly",
            "plan": plan.upper(),
            "target": "DFCR ≥ 0.60 per family",
            "value": f"Overall={dfcr:.1%} ({suff}/{total}), per-family={'PASS' if per_fam_pass else 'FAIL'}",
            "pass": dfcr >= 0.60 and per_fam_pass,
        })

        # Pillar 3: Drill-Down Dependence
        if drilldown:
            dd_tasks = [t for t in drilldown.get("per_task", []) if t["plan"] == plan]
            drilled = sum(1 for t in dd_tasks if t.get("drilldown_triggered", False))
            ddr = _safe_div(drilled, total)
            table2.append({
                "pillar": "3-DrillDependence",
                "plan": plan.upper(),
                "target": "DDR ≤ 0.40",
                "value": f"DDR={ddr:.1%} ({drilled}/{total})",
                "pass": ddr <= 0.40,
            })

            # Pillar 4: Post-Drill Value
            fu_values = [t["fidelity_uplift"] for t in dd_tasks if t.get("drilldown_triggered")]
            mean_fu = sum(fu_values) / len(fu_values) if fu_values else 0
            table2.append({
                "pillar": "4-PostDrillValue",
                "plan": plan.upper(),
                "target": "FU ≥ 0.10",
                "value": f"Mean FU={mean_fu:+.3f} ({len(fu_values)} tasks)",
                "pass": mean_fu >= 0.10,
            })
        else:
            table2.append({"pillar": "3-DrillDependence", "plan": plan.upper(), "target": "DDR ≤ 0.40", "value": "NOT RUN", "pass": False})
            table2.append({"pillar": "4-PostDrillValue", "plan": plan.upper(), "target": "FU ≥ 0.10", "value": "NOT RUN", "pass": False})

    # ===== VERDICT =====
    verdict: dict[str, Any] = {}
    for plan in plans:
        plan_scores = [s for s in table2 if s["plan"] == plan.upper()]
        all_pass = all(s["pass"] for s in plan_scores)
        pass_count = sum(1 for s in plan_scores if s["pass"])
        verdict[f"plan_{plan}"] = {
            "all_pillars_pass": all_pass,
            "pillars_passed": pass_count,
            "pillars_total": len(plan_scores),
        }

    # Determine winner
    a_pass = verdict["plan_a"]["pillars_passed"]
    b_pass = verdict["plan_b"]["pillars_passed"]
    if a_pass > b_pass:
        overall_winner = "A"
    elif b_pass > a_pass:
        overall_winner = "B"
    else:
        overall_winner = "TIE"

    verdict["overall_winner"] = overall_winner

    output = {
        "table1_per_family": table1,
        "table2_pillar_scorecard": table2,
        "verdict": verdict,
    }

    # Save JSON
    out_json = reports_dir / "ab-verdict.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    # Save markdown
    out_md = reports_dir / "ab-verdict.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Plan A vs Plan B: Comparative Verdict\n\n")

        f.write("## Table 1: Head-to-Head Per Family\n\n")
        f.write("| Family | Plan A DFCR | Plan B DFCR | Plan A CCR | Plan B CCR | Winner |\n")
        f.write("|--------|-------------|-------------|------------|------------|--------|\n")
        for row in table1:
            f.write(f"| {row['family']} | {row.get('a_dfcr', 0):.2f} | {row.get('b_dfcr', 0):.2f} | "
                    f"{row.get('a_mean_ccr', 0):.2f} | {row.get('b_mean_ccr', 0):.2f} | {row.get('winner', '?')} |\n")

        f.write("\n## Table 2: Pillar Scorecard\n\n")
        f.write("| Pillar | Plan | Target | Value | Pass |\n")
        f.write("|--------|------|--------|-------|------|\n")
        for row in table2:
            f.write(f"| {row['pillar']} | {row['plan']} | {row['target']} | {row['value']} | {'✓' if row['pass'] else '✗'} |\n")

        f.write(f"\n## Verdict\n\n")
        f.write(f"**Overall Winner: Plan {overall_winner}**\n\n")
        for plan in plans:
            vp = verdict[f"plan_{plan}"]
            f.write(f"- Plan {plan.upper()}: {vp['pillars_passed']}/{vp['pillars_total']} pillars pass")
            if vp["all_pillars_pass"]:
                f.write(" ✓ ALL PASS")
            f.write("\n")

    print(f"\n=== VERDICT ===")
    print(f"Plan A: {verdict['plan_a']['pillars_passed']}/{verdict['plan_a']['pillars_total']} pillars")
    print(f"Plan B: {verdict['plan_b']['pillars_passed']}/{verdict['plan_b']['pillars_total']} pillars")
    print(f"Winner: Plan {overall_winner}")
    print(f"\nSaved: {out_json}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()
