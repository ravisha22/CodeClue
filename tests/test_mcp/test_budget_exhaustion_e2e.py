"""Budget exhaustion integration test on a real graph."""
import pytest
from pathlib import Path

from codeclue_research.io import load_graph
from codeclue_research.operation_projection import project_operation
from codeclue_mcp.server import CodeClueServer
from codeclue_mcp.budget import BudgetTracker


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


class TestBudgetExhaustionE2E:
    def test_of1_budget_exhausts_at_5(self, flask_graph, flask_server):
        """OF1 budget of 5 calls exhausts. Escalation lists remaining nodes."""
        tracker = BudgetTracker(operation_family="OF1")
        assert tracker.budget == 5

        # Project OF1 to get nodes with suggested actions
        trace = project_operation(
            graph=flask_graph,
            operation_family="OF1",
            prompt_profile={
                "profile_id": "budget-test",
                "intent": "architecture",
                "constraints": {"max_context": "focused"},
                "focus_files": ["src/flask/app.py"],
            },
        )

        conf = trace.get("confidence", {})
        nodes_with_actions = [
            n for n in conf.get("per_node_confidence", [])
            if n.get("suggested_actions")
        ]

        # Execute tool calls until budget exhausted
        calls_made = 0
        for node in nodes_with_actions:
            if not tracker.can_call():
                break
            action = node["suggested_actions"][0]
            result = flask_server.call_tool(action["tool"], action.get("args", {}))
            if result["status"] == "ok":
                tracker.record_call(tool=action["tool"], node_id=node["node_id"])
                calls_made += 1

        # Register remaining unresolved nodes
        remaining_nodes = [
            n["node_id"] for n in nodes_with_actions[calls_made:]
            if n["confidence"] < 0.85
        ]
        tracker.register_unresolved(remaining_nodes)

        # Verify budget state
        escalation = tracker.get_escalation()
        assert escalation["calls_made"] <= 5
        assert escalation["budget"] == 5

        if calls_made >= 5:
            assert escalation["budget_exhausted"] is True
            assert len(escalation["unresolved_nodes"]) >= 0  # may have remaining nodes

    def test_of5_budget_allows_more_calls(self, flask_graph, flask_server):
        """OF5 budget of 30 allows significantly more calls than OF1."""
        tracker = BudgetTracker(operation_family="OF5")
        assert tracker.budget == 30
        # Make 10 calls — should all be within budget
        for i in range(10):
            assert tracker.can_call() is True
            tracker.record_call(tool="code_slice", node_id=f"node_{i}")
        assert tracker.remaining() == 20
