"""Analyze ALL 23 projections to determine exactly which fields are useful vs overhead.

This script examines every field across all 7 repos to inform the hybrid design.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.token_counter import count_tokens


def main() -> None:
    runs = ROOT / "experiments" / "runs"
    results = []

    for lane_dir in sorted(runs.glob("v2-lane-a-*")):
        repo = lane_dir.name.replace("v2-lane-a-", "")
        for proj_file in sorted(lane_dir.glob("v2-proj-*.json")):
            with open(proj_file) as f:
                proj = json.load(f)

            nodes = proj.get("projected_nodes", [])
            edges = proj.get("projected_edges", [])
            conf = proj.get("confidence", {})
            pnc = conf.get("per_node_confidence", [])
            pec = conf.get("per_edge_confidence", [])

            # === Content analysis ===
            nodes_with_calls = sum(1 for n in nodes if n.get("semantic_contract", {}).get("calls"))
            nodes_with_called_by = sum(1 for n in nodes if n.get("semantic_contract", {}).get("called_by"))

            # Purpose analysis
            purposes = []
            for n in nodes:
                p = n.get("semantic_contract", {}).get("purpose", "")
                purposes.append(p)
            trivial_purpose = sum(1 for p in purposes if p.startswith("function ") or p.startswith("Module-") or p.startswith("class "))
            non_trivial_purpose = len(purposes) - trivial_purpose

            # Confidence distribution
            confs = [pn.get("confidence", 0) for pn in pnc]
            low_conf = sum(1 for c in confs if c < 0.6)
            mid_conf = sum(1 for c in confs if 0.6 <= c < 0.85)
            high_conf = sum(1 for c in confs if c >= 0.85)

            # Suggested actions
            nodes_with_actions = sum(1 for pn in pnc if pn.get("suggested_actions"))
            total_actions = sum(len(pn.get("suggested_actions", [])) for pn in pnc)

            # Density flags
            density_flagged = sum(1 for pn in pnc if pn.get("density_indicators", {}).get("density_flag"))

            # === Token breakdown ===
            t_total = count_tokens(proj)

            # Category 1: Useful semantic (name, purpose, calls, called_by)
            useful_semantic = []
            for n in nodes:
                sc = n.get("semantic_contract", {})
                useful_semantic.append({
                    "n": sc.get("symbol_name", ""),
                    "p": sc.get("purpose", ""),
                    "c": sc.get("calls", []),
                    "cb": sc.get("called_by", []),
                })
            t_useful_semantic = count_tokens(useful_semantic)

            # Category 2: Identity (node_id, type, file, confidence, lines)
            identity = []
            for n in nodes:
                identity.append({
                    "i": n.get("node_id", ""),
                    "t": n.get("node_type", ""),
                    "f": n.get("source_anchor", {}).get("file_path", ""),
                    "c": n.get("confidence", 0),
                })
            t_identity = count_tokens(identity)

            # Category 3: Edges (type, from, to)
            compact_edges = []
            for e in edges:
                compact_edges.append({
                    "t": e.get("edge_type", ""),
                    "f": e.get("from_node", ""),
                    "o": e.get("to_node", ""),
                })
            t_edges_compact = count_tokens(compact_edges)

            # Category 4: Confidence overall signal
            conf_signal = {
                "overall": conf.get("confidence_overall", 0),
                "hint": conf.get("lookup_decision_hint", ""),
            }
            t_conf_signal = count_tokens(conf_signal)

            # Category 5: Per-node confidence arrays
            t_pnc = count_tokens(pnc) if pnc else 0

            # Category 6: Per-edge confidence arrays
            t_pec = count_tokens(pec) if pec else 0

            # Category 7: Node overhead (hash, bytes, ast, complexity, symbol_type duplication)
            node_overhead = []
            for n in nodes:
                sa = n.get("source_anchor", {})
                sc = n.get("semantic_contract", {})
                node_overhead.append({
                    "h": sa.get("content_hash", ""),
                    "a": sa.get("ast_path", ""),
                    "bs": sa.get("byte_start", 0),
                    "be": sa.get("byte_end", 0),
                    "ci": sc.get("complexity_indicators", {}),
                    "st": sc.get("symbol_type", ""),
                    "lang": sc.get("language", ""),
                    "tier": sc.get("tier", 1),
                })
            t_node_overhead = count_tokens(node_overhead)

            # Category 8: Edge overhead (verbose IDs, evidence)
            edge_overhead = []
            for e in edges:
                edge_overhead.append({
                    "id": e.get("edge_id", ""),
                    "ev": e.get("evidence", {}),
                })
            t_edge_overhead = count_tokens(edge_overhead)

            # Category 9: Projection metadata (policy, reasoning_path, validation, stats)
            meta_fields = {}
            for k in ["policy", "reasoning_path", "validation", "stats", "prompt_profile", "trace_id", "operation_family"]:
                if k in proj:
                    meta_fields[k] = proj[k]
            t_meta = count_tokens(meta_fields)

            # Suggested actions content analysis
            action_tools = defaultdict(int)
            action_rationales = []
            for pn in pnc:
                for a in pn.get("suggested_actions", []):
                    action_tools[a.get("tool", "")] += 1
                    action_rationales.append(a.get("rationale", ""))

            results.append({
                "task": proj_file.stem,
                "repo": repo,
                "n_nodes": len(nodes),
                "n_edges": len(edges),
                "nodes_with_calls": nodes_with_calls,
                "nodes_with_called_by": nodes_with_called_by,
                "non_trivial_purpose": non_trivial_purpose,
                "trivial_purpose": trivial_purpose,
                "low_conf": low_conf,
                "mid_conf": mid_conf,
                "high_conf": high_conf,
                "nodes_with_actions": nodes_with_actions,
                "total_actions": total_actions,
                "density_flagged": density_flagged,
                "t_total": t_total,
                "t_useful_semantic": t_useful_semantic,
                "t_identity": t_identity,
                "t_edges_compact": t_edges_compact,
                "t_conf_signal": t_conf_signal,
                "t_pnc": t_pnc,
                "t_pec": t_pec,
                "t_node_overhead": t_node_overhead,
                "t_edge_overhead": t_edge_overhead,
                "t_meta": t_meta,
                "action_tools": dict(action_tools),
                "unique_rationales": len(set(action_rationales)),
            })

    # === PRINT ANALYSIS ===
    n = len(results)
    print(f"Analyzed {n} projections across {len(set(r['repo'] for r in results))} repos\n")

    # Per-task table
    print(f"{'Task':<35} {'Repo':<8} {'Nodes':>5} {'w/call':>6} {'w/cb':>5} {'LoCnf':>6} {'Actns':>6} {'Total':>7} {'Useful':>7} {'PNC':>7} {'Ovrhd':>7}")
    print("-" * 115)
    for r in results:
        print(f"{r['task']:<35} {r['repo']:<8} {r['n_nodes']:>5} {r['nodes_with_calls']:>6} {r['nodes_with_called_by']:>5} "
              f"{r['low_conf']:>6} {r['total_actions']:>6} {r['t_total']:>7} {r['t_useful_semantic']:>7} {r['t_pnc']:>7} {r['t_node_overhead']:>7}")

    # Aggregates
    print(f"\n{'='*80}")
    print(f"AGGREGATE TOKEN ANALYSIS (mean across {n} projections)")
    print(f"{'='*80}")

    def avg(key):
        return sum(r[key] for r in results) / n

    def pct(key):
        return sum(r[key] for r in results) * 100 / sum(r["t_total"] for r in results)

    categories = [
        ("Useful semantic (name, purpose, calls, called_by)", "t_useful_semantic"),
        ("Identity (node_id, type, file, confidence)", "t_identity"),
        ("Edges compact (type, from, to)", "t_edges_compact"),
        ("Confidence overall signal", "t_conf_signal"),
        ("Per-node confidence arrays", "t_pnc"),
        ("Per-edge confidence arrays", "t_pec"),
        ("Node overhead (hash, bytes, ast, complexity)", "t_node_overhead"),
        ("Edge overhead (verbose IDs, evidence)", "t_edge_overhead"),
        ("Projection metadata (policy, reasoning, validation)", "t_meta"),
    ]

    total_avg = avg("t_total")
    print(f"\n  Total average: {total_avg:.0f} tokens\n")
    print(f"  {'Category':<55} {'Mean':>7} {'%':>6} {'Keep?':>6}")
    print(f"  {'-'*55} {'-'*7} {'-'*6} {'-'*6}")

    keep_tokens = 0
    strip_tokens = 0
    debug_tokens = 0
    for label, key in categories:
        a = avg(key)
        p = pct(key)
        if key in ("t_useful_semantic", "t_identity", "t_edges_compact", "t_conf_signal"):
            keep = "KEEP"
            keep_tokens += a
        elif key in ("t_pnc", "t_node_overhead", "t_edge_overhead"):
            keep = "DEBUG"
            debug_tokens += a
        else:
            keep = "STRIP"
            strip_tokens += a
        print(f"  {label:<55} {a:>7.0f} {p:>5.1f}% {keep:>6}")

    print(f"\n  Summary:")
    print(f"    KEEP for clue:   {keep_tokens:.0f}t ({keep_tokens*100/total_avg:.1f}%)")
    print(f"    DEBUG file:      {debug_tokens:.0f}t ({debug_tokens*100/total_avg:.1f}%)")
    print(f"    STRIP entirely:  {strip_tokens:.0f}t ({strip_tokens*100/total_avg:.1f}%)")

    # Content richness analysis
    print(f"\n{'='*80}")
    print(f"CONTENT RICHNESS ANALYSIS")
    print(f"{'='*80}")
    print(f"  Nodes with calls:      {avg('nodes_with_calls'):.1f}/{avg('n_nodes'):.1f} ({avg('nodes_with_calls')*100/avg('n_nodes'):.0f}%)")
    print(f"  Nodes with called_by:  {avg('nodes_with_called_by'):.1f}/{avg('n_nodes'):.1f} ({avg('nodes_with_called_by')*100/avg('n_nodes'):.0f}%)")
    print(f"  Non-trivial purpose:   {avg('non_trivial_purpose'):.1f}/{avg('n_nodes'):.1f} ({avg('non_trivial_purpose')*100/avg('n_nodes'):.0f}%)")
    print(f"  Trivial purpose:       {avg('trivial_purpose'):.1f}/{avg('n_nodes'):.1f} ({avg('trivial_purpose')*100/avg('n_nodes'):.0f}%)")

    print(f"\n  Confidence distribution:")
    print(f"    Low (<0.6):    {avg('low_conf'):.1f} nodes ({avg('low_conf')*100/max(avg('low_conf')+avg('mid_conf')+avg('high_conf'),1):.0f}%)")
    print(f"    Mid (0.6-0.85):{avg('mid_conf'):.1f} nodes ({avg('mid_conf')*100/max(avg('low_conf')+avg('mid_conf')+avg('high_conf'),1):.0f}%)")
    print(f"    High (>=0.85): {avg('high_conf'):.1f} nodes ({avg('high_conf')*100/max(avg('low_conf')+avg('mid_conf')+avg('high_conf'),1):.0f}%)")

    print(f"\n  Suggested actions:")
    print(f"    Nodes with actions:  {avg('nodes_with_actions'):.1f}")
    print(f"    Total actions:       {avg('total_actions'):.1f}")
    print(f"    Density-flagged:     {avg('density_flagged'):.1f}")

    # Action tool distribution
    all_tools = defaultdict(int)
    all_rationale_set = set()
    for r in results:
        for tool, cnt in r["action_tools"].items():
            all_tools[tool] += cnt

    print(f"\n  Action tool distribution (total across all tasks):")
    for tool, cnt in sorted(all_tools.items(), key=lambda x: -x[1]):
        print(f"    {tool}: {cnt}")

    # Per-repo size comparison
    print(f"\n{'='*80}")
    print(f"PER-REPO TOKEN PROFILE")
    print(f"{'='*80}")
    repo_stats = defaultdict(list)
    for r in results:
        repo_stats[r["repo"]].append(r)
    for repo in sorted(repo_stats.keys()):
        tasks = repo_stats[repo]
        rn = len(tasks)
        avg_total = sum(t["t_total"] for t in tasks) / rn
        avg_useful = sum(t["t_useful_semantic"] for t in tasks) / rn
        avg_pnc = sum(t["t_pnc"] for t in tasks) / rn
        avg_overhead = sum(t["t_node_overhead"] for t in tasks) / rn
        print(f"  {repo:<10}: {rn} tasks, total={avg_total:.0f}t, useful={avg_useful:.0f}t ({avg_useful*100/avg_total:.0f}%), "
              f"pnc={avg_pnc:.0f}t ({avg_pnc*100/avg_total:.0f}%), overhead={avg_overhead:.0f}t ({avg_overhead*100/avg_total:.0f}%)")

    # Save full analysis
    out_path = ROOT / "experiments" / "reports" / "field-level-analysis-all-23.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
