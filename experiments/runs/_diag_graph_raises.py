"""Diagnostic: Check full extraction + graph for NullSession raises."""
import json
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf

repo_path = Path("experiments/external-repos/flask")
graph = extract_graph(repo_path)

# Find NullSession node and print its semantic_contract
for node in graph.nodes:
    sc = node.semantic_contract or {}
    sym_name = sc.get("symbol_name", "")
    if "NullSession" in sym_name or "SecureCookieSessionInterface" in sym_name:
        print(f"NODE: {node.node_id}")
        print(f"  name: {sym_name}")
        print(f"  type: {node.node_type}")
        print(f"  raises: {sc.get('raises', 'NOT SET')}")
        print(f"  calls: {sc.get('calls', [])}")
        print()

# Also check _fail method
for node in graph.nodes:
    sc = node.semantic_contract or {}
    sym_name = sc.get("symbol_name", "")
    if "_fail" in sym_name and "session" in str(node.source_anchor.file_path).lower():
        print(f"NODE: {node.node_id}")
        print(f"  name: {sym_name}")
        print(f"  type: {node.node_type}")
        print(f"  raises: {sc.get('raises', 'NOT SET')}")
        print()

# Now render with the session security question and check output
clue = render_mrlf(graph, "What security measures protect Flask session data, and what are the attack vectors?", repo_root=str(repo_path))

# Extract NullSession entry from FOCUS
in_focus = False
lines = clue.split("\n")
for i, line in enumerate(lines):
    if "-- FOCUS" in line:
        in_focus = True
    if "-- GAPS" in line:
        in_focus = False
    if in_focus and "NullSession" in line:
        # Print surrounding context
        for j in range(i, min(i + 10, len(lines))):
            if lines[j].strip() == "" and j > i + 1:
                break
            print(lines[j])
        print()
    if in_focus and "SecureCookieSessionInterface" in line:
        print("=== SecureCookieSessionInterface FOCUS entry ===")
        for j in range(i, min(i + 20, len(lines))):
            print(lines[j])
            if lines[j].strip() == "" and j > i + 1:
                break
        print()

# Also check: which calls does SecureCookieSessionInterface show?
print("=== Calls truncation check ===")
for node in graph.nodes:
    sc = node.semantic_contract or {}
    if sc.get("symbol_name") == "SecureCookieSessionInterface":
        calls = sc.get("calls", [])
        print(f"Total calls in graph: {len(calls)}")
        for c in calls:
            target = c.get("target", c) if isinstance(c, dict) else c
            print(f"  {target}")
