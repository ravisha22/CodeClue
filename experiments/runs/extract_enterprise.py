"""Extract graphs for enterprise repos and report sizes."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
from codeclue_research.extractor import extract_graph

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

REPOS = [
    ("saleor", "python"),
    ("netbox", "python"),
    ("maybe", "typescript"),
    ("calcom", "typescript"),
    ("mattermost", "go"),
    ("consul", "go"),
    ("grafana", "go"),
    ("supabase", "typescript"),
]

for repo_name, lang in REPOS:
    repo_path = REPO_ROOT / "experiments" / "external-repos" / repo_name
    print(f"\n=== {repo_name} ({lang}) ===")
    try:
        start = time.time()
        graph = extract_graph(repo_path, language=lang)
        elapsed = time.time() - start
        print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges ({elapsed:.1f}s)")
    except Exception as e:
        print(f"  ERROR: {e}")
