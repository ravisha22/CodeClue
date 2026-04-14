"""Diagnostic: Dump the regenerated flask-tf5 clue to see full content."""
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf

repo_path = Path("experiments/external-repos/flask")
graph = extract_graph(repo_path)
clue = render_mrlf(graph, "What security measures protect Flask session data, and what are the attack vectors?", repo_root=str(repo_path))

# Write it out
out = Path("experiments/runs/_diag_flask_tf5_regen.codeclue")
out.write_text(clue, encoding="utf-8")
print(f"Written to {out} ({len(clue)} chars)")

# Find all session-related content in FOCUS
in_focus = False
for line in clue.split("\n"):
    if "-- FOCUS" in line:
        in_focus = True
    if "-- GAPS" in line:
        in_focus = False
    if in_focus and ("Session" in line or "session" in line or "Cookie" in line or "cookie" in line or "raises:" in line):
        print(line)
