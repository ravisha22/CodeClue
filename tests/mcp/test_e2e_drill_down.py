"""End-to-end integration test: projection → low confidence → drill-down → trace."""
import json
import pytest
from pathlib import Path

from codeclue_research.io import load_graph
from codeclue_research.operation_projection import project_operation
from codeclue_mcp.server import CodeClueServer
from codeclue_mcp.tracer import InvocationTracer, hash_output


@pytest.fixture
def flask_graph():
    p = Path("experiments/runs/v2-lane-a-flask/graph.json")
    if not p.exists():
        pytest.skip("Flask v2 graph not available")
    return load_graph(p)


@pytest.fixture
def flask_server(flask_graph):
    return CodeClueServer(
        graph=flask_graph,
        repo_root="experiments/external-repos/flask",
    )


class TestE2EDrillDown:
    def test_full_drill_down_flow(self, flask_graph, flask_server, tmp_path):
        """Full flow: project → find low-confidence node → call code_slice → verify trace."""
        # Step 1: Project OF2 (impact analysis) — expected to have low-confidence nodes
        trace = project_operation(
            graph=flask_graph,
            operation_family="OF2",
            prompt_profile={
                "profile_id": "test-e2e",
                "intent": "impact-analysis",
                "constraints": {"max_context": "focused"},
                "focus_files": ["src/flask/ctx.py"],
                "focus_symbols": ["push"],
            },
        )

        # Step 2: Find a node with suggested actions
        confidence_block = trace.get("confidence", {})
        nodes_with_actions = [
            n for n in confidence_block.get("per_node_confidence", [])
            if n.get("suggested_actions")
        ]

        # Step 3: Execute a suggested action
        tracer = InvocationTracer(trace_dir=tmp_path / "traces")

        if nodes_with_actions:
            node = nodes_with_actions[0]
            action = node["suggested_actions"][0]
            tool_name = action["tool"]

            if tool_name == "code_slice":
                result = flask_server.call_tool("code_slice", action["args"])
            elif tool_name == "resolve_dependency":
                result = flask_server.call_tool("resolve_dependency", action["args"])
            elif tool_name == "fetch_contract":
                result = flask_server.call_tool("fetch_contract", action["args"])
            else:
                result = flask_server.call_tool(tool_name, action.get("args", {}))

            assert result["status"] == "ok"

            # Step 4: Log the trace
            tracer.log(
                tool=tool_name,
                args=action["args"],
                output_hash=hash_output(result),
                source_anchor=node["node_id"],
                confidence_trigger=node["confidence"],
                session_id="e2e-test",
            )

            # Step 5: Verify trace was logged
            trace_files = list((tmp_path / "traces").glob("*.jsonl"))
            assert len(trace_files) == 1
            entry = json.loads(trace_files[0].read_text().strip().split("\n")[-1])
            assert entry["tool"] == tool_name
            assert entry["session_id"] == "e2e-test"
        else:
            # Even if no actions, the projection itself should have confidence
            assert "confidence_overall" in confidence_block

    def test_server_handles_all_tool_types(self, flask_graph, flask_server):
        """Server correctly dispatches all 5 tool types."""
        module_id = [n.node_id for n in flask_graph.nodes if n.node_type == "module"][0]
        func_id = [n.node_id for n in flask_graph.nodes if n.node_type == "function"][0]

        # code_slice
        r1 = flask_server.call_tool("code_slice", {
            "file_path": flask_graph.nodes[0].source_anchor.file_path,
            "start_line": 1, "end_line": 5,
        })
        assert r1["status"] == "ok"

        # resolve_dependency
        r2 = flask_server.call_tool("resolve_dependency", {"node_id": func_id, "depth": 1})
        assert r2["status"] == "ok"

        # check_freshness
        r3 = flask_server.call_tool("check_freshness", {"module_id": module_id})
        assert r3["status"] == "ok"

        # expand_projection
        r4 = flask_server.call_tool("expand_projection", {"node_id": func_id, "additional_hops": 1})
        assert r4["status"] == "ok"

        # fetch_contract
        r5 = flask_server.call_tool("fetch_contract", {"node_id": func_id})
        assert r5["status"] == "ok"

    def test_unknown_tool_returns_error(self, flask_server):
        """Calling a nonexistent tool returns error."""
        result = flask_server.call_tool("nonexistent_tool", {})
        assert result["status"] == "error"
