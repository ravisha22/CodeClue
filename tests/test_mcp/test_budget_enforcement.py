"""Tests for per-session tool call budget enforcement."""
import pytest
from pathlib import Path

from codeclue_mcp.budget import BudgetTracker
from codeclue_mcp.tools import code_slice
from codeclue_research.io import load_graph


class TestBudgetEnforcement:
    def test_budget_allows_within_limit(self):
        """Calls within budget are allowed."""
        tracker = BudgetTracker(operation_family="OF1", budget=5)
        for i in range(5):
            assert tracker.can_call() is True
            tracker.record_call(tool="code_slice", node_id=f"node_{i}")
        # 5 calls made, at limit
        assert tracker.remaining() == 0

    def test_budget_rejects_over_limit(self):
        """Call after budget is exhausted returns False."""
        tracker = BudgetTracker(operation_family="OF2", budget=3)
        for i in range(3):
            tracker.record_call(tool="code_slice", node_id=f"node_{i}")
        assert tracker.can_call() is False

    def test_default_budgets_per_family(self):
        """Default budgets match PRD: OF1=5, OF2=15, OF3=10, OF4=20, OF5=30."""
        assert BudgetTracker(operation_family="OF1").budget == 5
        assert BudgetTracker(operation_family="OF2").budget == 15
        assert BudgetTracker(operation_family="OF3").budget == 10
        assert BudgetTracker(operation_family="OF4").budget == 20
        assert BudgetTracker(operation_family="OF5").budget == 30

    def test_escalation_on_exhaustion(self):
        """When budget is exhausted, escalation lists unresolved low-confidence nodes."""
        tracker = BudgetTracker(operation_family="OF1", budget=2)
        tracker.record_call(tool="code_slice", node_id="node_a")
        tracker.record_call(tool="code_slice", node_id="node_b")

        # Register remaining low-confidence nodes that weren't addressed
        tracker.register_unresolved(["node_c", "node_d", "node_e"])

        escalation = tracker.get_escalation()
        assert escalation["budget_exhausted"] is True
        assert escalation["operation_family"] == "OF1"
        assert escalation["calls_made"] == 2
        assert escalation["budget"] == 2
        assert set(escalation["unresolved_nodes"]) == {"node_c", "node_d", "node_e"}

    def test_no_escalation_when_within_budget(self):
        """No escalation when budget is not exhausted."""
        tracker = BudgetTracker(operation_family="OF5", budget=30)
        tracker.record_call(tool="code_slice", node_id="node_a")
        escalation = tracker.get_escalation()
        assert escalation["budget_exhausted"] is False

    def test_custom_budget_override(self):
        """Custom budget overrides default."""
        tracker = BudgetTracker(operation_family="OF1", budget=100)
        assert tracker.budget == 100
