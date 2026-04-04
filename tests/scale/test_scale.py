"""RED tests for Epic 3: Scale Testing on 500K+ token repos.
All tests should FAIL until large repos are cloned and scale infrastructure is built."""
import pytest
import time
from pathlib import Path

from codeclue_research.extractor import extract_graph
from codeclue_research.operation_projection import project_operation
from codeclue_research.io import load_graph, save_graph


# Large repo candidates — must be cloned to experiments/external-repos/
_LARGE_REPOS = [
    ("django", "experiments/external-repos/django", "python"),
]


@pytest.fixture(params=[r[0] for r in _LARGE_REPOS], ids=[r[0] for r in _LARGE_REPOS])
def large_repo(request):
    name = request.param
    entry = next(r for r in _LARGE_REPOS if r[0] == name)
    repo_path = Path(entry[1])
    if not repo_path.exists():
        pytest.skip(f"Large repo {name} not cloned")
    return name, repo_path, entry[2]


class TestLargeRepoExtraction:
    def test_extract_completes_within_30_min(self, large_repo, tmp_path):
        """Extraction completes on a 500K+ token repo within 30 minutes."""
        name, repo_path, lang = large_repo
        out = tmp_path / "graph.json"
        start = time.time()
        graph = extract_graph(repo_root=repo_path, commit_id="HEAD", language=lang)
        save_graph(out, graph)
        elapsed = time.time() - start
        assert elapsed < 1800, f"Extraction took {elapsed:.0f}s (>30min)"
        assert out.exists()
        assert len(graph.nodes) > 1000, f"Only {len(graph.nodes)} nodes — expected >1000 for large repo"

    def test_no_oom(self, large_repo, tmp_path):
        """Extraction does not OOM (implicit — if it completes, no OOM)."""
        name, repo_path, lang = large_repo
        graph = extract_graph(repo_root=repo_path, commit_id="HEAD", language=lang)
        assert len(graph.nodes) > 0


class TestLargeRepoProjection:
    def test_of1_through_of5_complete(self, large_repo, tmp_path):
        """OF1-OF5 projections complete within 5 minutes each on large repo."""
        name, repo_path, lang = large_repo
        graph = extract_graph(repo_root=repo_path, commit_id="HEAD", language=lang)

        for of in ["OF1", "OF2", "OF3", "OF4", "OF5"]:
            start = time.time()
            trace = project_operation(graph=graph, operation_family=of)
            elapsed = time.time() - start
            assert elapsed < 300, f"{of} took {elapsed:.0f}s (>5min)"
            assert "confidence" in trace
            assert trace["stats"]["projected_node_count"] > 0


class TestFileSizeBudget:
    def test_total_codeclue_under_15mb(self, large_repo, tmp_path):
        """Total .codeclue/ directory <= 15MB per PRD Section 6.1."""
        name, repo_path, lang = large_repo
        graph = extract_graph(repo_root=repo_path, commit_id="HEAD", language=lang)
        graph_file = tmp_path / "graph.json"
        save_graph(graph_file, graph)
        size_mb = graph_file.stat().st_size / (1024 * 1024)
        assert size_mb <= 15, f"Graph file is {size_mb:.1f}MB (>15MB)"


class TestTRRAtScale:
    def test_trr_above_80_percent(self, large_repo, tmp_path):
        """TRR >= 80% on 500K+ token repo."""
        name, repo_path, lang = large_repo
        graph = extract_graph(repo_root=repo_path, commit_id="HEAD", language=lang)

        # Estimate raw token count (rough: 4 chars per token)
        total_source_bytes = 0
        for node in graph.nodes:
            total_source_bytes += node.source_anchor.byte_end - node.source_anchor.byte_start
        raw_tokens_est = total_source_bytes / 4

        # Clue tokens = graph JSON size / 4
        graph_file = tmp_path / "graph.json"
        save_graph(graph_file, graph)
        clue_tokens_est = graph_file.stat().st_size / 4

        trr = 1 - (clue_tokens_est / max(raw_tokens_est, 1))
        assert trr >= 0.80, f"TRR {trr:.3f} below 0.80 at scale"
