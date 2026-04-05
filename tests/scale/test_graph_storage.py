import json

from codeclue_research.io import load_graph, save_graph
from codeclue_research.models import CanonicalClueGraph, Edge, Node, SourceAnchor


def _sample_graph() -> CanonicalClueGraph:
    module = Node(
        node_id="module:app.py",
        node_type="module",
        source_anchor=SourceAnchor(
            file_path="app.py",
            byte_start=0,
            byte_end=120,
            ast_path="Module",
            content_hash="module-hash",
        ),
        semantic_contract={
            "purpose": "Module-level semantic container",
            "language": "python",
            "symbol_name": "app.py",
            "symbol_type": "module",
            "tier": 1,
            "calls": [],
            "called_by": [],
            "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0,
            },
        },
        confidence=1.0,
    )
    function = Node(
        node_id="function:app.py:handler",
        node_type="function",
        source_anchor=SourceAnchor(
            file_path="app.py",
            byte_start=20,
            byte_end=80,
            ast_path="Module/FunctionDef[handler]",
            content_hash="function-hash",
        ),
        semantic_contract={
            "purpose": "function handler",
            "language": "python",
            "symbol_name": "handler",
            "symbol_type": "function",
            "tier": 1,
            "calls": [{"target": "function:app.py:dep", "is_external": False}],
            "called_by": [],
            "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0,
            },
        },
        confidence=0.9,
    )
    dependency = Node(
        node_id="function:app.py:dep",
        node_type="function",
        source_anchor=SourceAnchor(
            file_path="app.py",
            byte_start=81,
            byte_end=110,
            ast_path="Module/FunctionDef[dep]",
            content_hash="dep-hash",
        ),
        semantic_contract={
            "purpose": "function dep",
            "language": "python",
            "symbol_name": "dep",
            "symbol_type": "function",
            "tier": 1,
            "calls": [],
            "called_by": [{"source": "function:app.py:handler"}],
            "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0,
            },
        },
        confidence=0.88,
    )

    return CanonicalClueGraph(
        metadata={"schema_version": "1.0.0"},
        repository={"name": "sample"},
        nodes=[module, function, dependency],
        edges=[
            Edge(
                edge_id="contains:module:app.py:function:app.py:handler",
                edge_type="contains",
                from_node="module:app.py",
                to_node="function:app.py:handler",
                evidence={"rel": "ast_containment"},
            ),
            Edge(
                edge_id="calls:function:app.py:handler:function:app.py:dep:12",
                edge_type="calls",
                from_node="function:app.py:handler",
                to_node="function:app.py:dep",
                evidence={"rel": "ast_call", "line": 12},
            ),
        ],
        operations={"OF1": {}},
        invariants={
            "connectivity_invariant": True,
            "anchor_invariant": True,
            "no_gap_invariant": True,
            "round_trip_invariant": True,
        },
    )


def test_save_graph_uses_compact_storage(tmp_path):
    graph = _sample_graph()
    out = tmp_path / "graph.json"

    save_graph(out, graph)

    raw_bytes = out.read_bytes()
    payload = json.loads(raw_bytes.decode("utf-8"))
    verbose_bytes = json.dumps(graph.to_dict(), indent=2, sort_keys=True).encode("utf-8")

    assert payload["metadata"]["storage_format"] == "compact-v1"
    assert "path_table" in payload
    assert all("i" not in edge for edge in payload["edges"])
    assert all("calls" not in node.get("sc", {}) for node in payload["nodes"])
    assert all("called_by" not in node.get("sc", {}) for node in payload["nodes"])
    assert all(len(node["a"]["h"]) <= 16 for node in payload["nodes"])
    assert len(raw_bytes) < len(verbose_bytes)


def test_load_graph_restores_derived_contract_fields(tmp_path):
    graph = _sample_graph()
    out = tmp_path / "graph.json"

    save_graph(out, graph)
    loaded = load_graph(out)

    handler = next(node for node in loaded.nodes if node.node_id == "function:app.py:handler")
    dependency = next(node for node in loaded.nodes if node.node_id == "function:app.py:dep")

    assert handler.semantic_contract["purpose"] == "function handler"
    assert handler.semantic_contract["language"] == "python"
    assert handler.semantic_contract["symbol_type"] == "function"
    assert handler.semantic_contract["tier"] == 1
    assert handler.semantic_contract["complexity_indicators"]["decorator_depth"] == 0
    assert handler.semantic_contract["calls"] == [
        {"target": "function:app.py:dep", "is_external": False}
    ]
    assert dependency.semantic_contract["called_by"] == [
        {"source": "function:app.py:handler"}
    ]
    assert {edge.edge_id for edge in loaded.edges} == {
        "contains:module:app.py:function:app.py:handler",
        "calls:function:app.py:handler:function:app.py:dep:12",
    }