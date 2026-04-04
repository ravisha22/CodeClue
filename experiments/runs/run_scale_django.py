"""Scale test: extract django, measure time, file size, TRR."""
import time
import json
from pathlib import Path
from codeclue_research.extractor import extract_graph
from codeclue_research.io import save_graph
from codeclue_research.operation_projection import project_operation

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

# Step 2: Token estimate
total_source_bytes = sum(
    n.source_anchor.byte_end - n.source_anchor.byte_start
    for n in graph.nodes
)
raw_tokens_est = total_source_bytes / 4
clue_tokens_est = graph_path.stat().st_size / 4
trr = 1 - (clue_tokens_est / max(raw_tokens_est, 1))
print(f"  Raw tokens (est): {raw_tokens_est:.0f}")
print(f"  Clue tokens (est): {clue_tokens_est:.0f}")
print(f"  TRR: {trr:.4f}")

# Step 3: Project OF1-OF5
for of in ["OF1", "OF2", "OF3", "OF4", "OF5"]:
    start = time.time()
    trace = project_operation(graph=graph, operation_family=of)
    proj_time = time.time() - start
    conf = trace.get("confidence", {})
    print(f"  {of}: nodes={trace['stats']['projected_node_count']}, "
          f"conf={conf.get('confidence_overall', -1):.3f}, "
          f"time={proj_time:.1f}s")

# Save summary
summary = {
    "repo": "django/django",
    "nodes": len(graph.nodes),
    "edges": len(graph.edges),
    "extract_time_s": round(extract_time, 1),
    "graph_size_mb": round(graph_size_mb, 2),
    "raw_tokens_est": int(raw_tokens_est),
    "clue_tokens_est": int(clue_tokens_est),
    "trr": round(trr, 4),
    "h1_pass": trr >= 0.80,
    "file_budget_pass": graph_size_mb <= 15,
}
Path("experiments/reports/scale-django-summary.json").write_text(json.dumps(summary, indent=2))
print(f"\nH1 (TRR >= 80%): {'PASS' if trr >= 0.80 else 'FAIL'} ({trr:.1%})")
print(f"File budget (<= 15MB): {'PASS' if graph_size_mb <= 15 else 'FAIL'} ({graph_size_mb:.1f}MB)")
