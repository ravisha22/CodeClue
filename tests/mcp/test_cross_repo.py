"""Cross-epic validation: MCP tools work on all 7 repos, all graph sizes, all languages."""
import pytest
from pathlib import Path

from codeclue_research.io import load_graph
from codeclue_mcp.server import CodeClueServer


_REPOS = [
    ("flask", "experiments/runs/v2-lane-a-flask/graph.json", "experiments/external-repos/flask", "python"),
    ("fastapi", "experiments/runs/v2-lane-a-fastapi/graph.json", "experiments/external-repos/fastapi", "python"),
    ("nest", "experiments/runs/v2-lane-a-nest/graph.json", "experiments/external-repos/nest", "typescript"),
    ("httpx", "experiments/runs/v2-lane-a-httpx/graph.json", "experiments/external-repos/httpx", "python"),
    ("express", "experiments/runs/v2-lane-a-express/graph.json", "experiments/external-repos/express", "typescript"),
    ("typeorm", "experiments/runs/v2-lane-a-typeorm/graph.json", "experiments/external-repos/typeorm", "typescript"),
    ("gin", "experiments/runs/v2-lane-a-gin/graph.json", "experiments/external-repos/gin", "go"),
]


@pytest.fixture(params=[r[0] for r in _REPOS], ids=[r[0] for r in _REPOS])
def repo_server(request):
    """Parameterized fixture: one server per repo."""
    name = request.param
    entry = next(r for r in _REPOS if r[0] == name)
    graph_path = Path(entry[1])
    repo_path = Path(entry[2])
    if not graph_path.exists():
        pytest.skip(f"Graph not available for {name}")
    if not repo_path.exists():
        pytest.skip(f"Repo not cloned for {name}")
    graph = load_graph(graph_path)
    server = CodeClueServer(graph=graph, repo_root=str(repo_path))
    return name, graph, server


class TestCrossRepoValidation:
    def test_server_creates_for_all_repos(self, repo_server):
        name, graph, server = repo_server
        assert server is not None
        assert len(graph.nodes) > 0

    def test_list_tools_works(self, repo_server):
        name, graph, server = repo_server
        tools = server.list_tools()
        assert len(tools) == 5

    def test_code_slice_works(self, repo_server):
        name, graph, server = repo_server
        # Find a module with non-empty source
        modules = [n for n in graph.nodes if n.node_type == "module"]
        target_module = None
        for m in modules:
            fp = Path(repo_server[2]._repo_root) / m.source_anchor.file_path
            if fp.exists() and fp.stat().st_size > 0:
                target_module = m
                break
        if target_module is None:
            pytest.skip(f"No non-empty module in {name}")
        result = server.call_tool("code_slice", {
            "file_path": target_module.source_anchor.file_path,
            "start_line": 1,
            "end_line": 5,
        })
        assert result["status"] == "ok"
        assert len(result["lines"]) > 0

    def test_resolve_dependency_works(self, repo_server):
        name, graph, server = repo_server
        first_func = [n for n in graph.nodes if n.node_type in ("function", "class", "struct")]
        if not first_func:
            pytest.skip(f"No function nodes in {name}")
        result = server.call_tool("resolve_dependency", {
            "node_id": first_func[0].node_id,
            "depth": 1,
        })
        assert result["status"] == "ok"

    def test_check_freshness_works(self, repo_server):
        name, graph, server = repo_server
        module = [n for n in graph.nodes if n.node_type == "module"][0]
        result = server.call_tool("check_freshness", {"module_id": module.node_id})
        assert result["status"] == "ok"
        assert "stale" in result

    def test_expand_projection_works(self, repo_server):
        name, graph, server = repo_server
        node = graph.nodes[0]
        result = server.call_tool("expand_projection", {
            "node_id": node.node_id,
            "additional_hops": 1,
        })
        assert result["status"] == "ok"

    def test_fetch_contract_works(self, repo_server):
        name, graph, server = repo_server
        node = graph.nodes[0]
        result = server.call_tool("fetch_contract", {"node_id": node.node_id})
        assert result["status"] == "ok"
        assert "semantic_contract" in result
