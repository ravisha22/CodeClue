"""Scale test: extract django and measure canonical storage footprint."""
import time
import json
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.io import save_graph

repo_root = Path("experiments/external-repos/django")
out_dir = Path("experiments/runs/scale-django")
out_dir.mkdir(parents=True, exist_ok=True)

# Step 1: Extract
print("Extracting django (Python)...", flush=True)
start = time.time()
graph = extract_graph(repo_root=repo_root, commit_id="HEAD", language="python")
extract_time = time.time() - start
print(f"  Nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}")
print(f"  Time: {extract_time:.1f}s")

# Save graph
graph_path = out_dir / "graph.json"
save_graph(graph_path, graph)
graph_size_mb = graph_path.stat().st_size / (1024 * 1024)
print(f"  Graph size: {graph_size_mb:.1f}MB")

# Step 2: Storage metrics
python_source_bytes = sum(
    path.stat().st_size for path in repo_root.rglob("*.py") if path.is_file()
)
legacy_pretty_bytes = len(
    json.dumps(graph.to_dict(), indent=2, sort_keys=True).encode("utf-8")
)
compact_bytes = graph_path.stat().st_size
storage_ratio = compact_bytes / max(python_source_bytes, 1)
reduction_pct = 1 - (compact_bytes / max(legacy_pretty_bytes, 1))

print(f"  Persisted graph size: {compact_bytes / (1024 * 1024):.1f}MB")
print(f"  Legacy pretty JSON: {legacy_pretty_bytes / (1024 * 1024):.1f}MB")
print(f"  Python source size: {python_source_bytes / (1024 * 1024):.1f}MB")
print(f"  Storage/source ratio: {storage_ratio:.2f}x")
print(f"  Reduction vs legacy serializer: {reduction_pct:.1%}")

# Save summary
summary = {
    "repo": "django/django",
    "nodes": len(graph.nodes),
    "edges": len(graph.edges),
    "extract_time_s": round(extract_time, 1),
    "graph_size_mb": round(compact_bytes / (1024 * 1024), 2),
    "legacy_pretty_graph_mb": round(legacy_pretty_bytes / (1024 * 1024), 2),
    "python_source_mb": round(python_source_bytes / (1024 * 1024), 2),
    "storage_source_ratio": round(storage_ratio, 4),
    "reduction_vs_legacy_pct": round(reduction_pct * 100, 2),
    "under_source_size": compact_bytes <= python_source_bytes,
    "file_budget_pass": graph_size_mb <= 15,
    "measurement_scope": "canonical_storage",
    "measurement_note": (
        "This report measures persisted canonical graph storage only. "
        "Projection-level context efficiency must be evaluated separately."
    ),
}
Path("experiments/reports/scale-django-summary.json").write_text(json.dumps(summary, indent=2))
print(f"\nUnder source size: {'PASS' if compact_bytes <= python_source_bytes else 'FAIL'}")
print(f"File budget (<= 15MB): {'PASS' if graph_size_mb <= 15 else 'FAIL'} ({graph_size_mb:.1f}MB)")
