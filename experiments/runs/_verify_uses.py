"""Verify: does get_signing_serializer get uses: URLSafeTimedSerializer?"""
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.clue_view_mrlf import render_mrlf

repo_path = Path("experiments/external-repos/flask")
graph = extract_graph(repo_path)

# Check nodes with uses data
print("=== Symbols with uses: data ===")
count = 0
for node in graph.nodes:
    sc = node.semantic_contract or {}
    uses = sc.get("uses", [])
    if uses:
        count += 1
        sym = sc.get("symbol_name", "")
        print(f"  {sym}: uses={uses}")
        if count >= 20:
            print("  ... (capped at 20)")
            break

print(f"\nTotal symbols with uses: {count}")

# Generate clue and check for uses: lines
clue = render_mrlf(graph, "What security measures protect Flask session data?", repo_root=str(repo_path))
print("\n=== uses: lines in generated clue ===")
for line in clue.split("\n"):
    if "uses:" in line:
        print(f"  {line.strip()}")
