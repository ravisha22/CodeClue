"""RED tests for Epic 2: Delta Drift Testing.
Tests H3 (delta non-inferiority, DNG <= 0.05) and H4 (50-commit drift resilience).
All tests should FAIL until drift.py is implemented."""
import pytest
from pathlib import Path

from codeclue_research.drift import (
    apply_single_delta,
    run_drift_protocol,
    detect_reset_trigger,
)
from codeclue_research.io import load_graph


@pytest.fixture
def flask_repo():
    p = Path("experiments/external-repos/flask")
    if not p.exists():
        pytest.skip("Flask repo not cloned")
    return p


@pytest.fixture
def flask_graph():
    p = Path("experiments/runs/v2-lane-a-flask/graph.json")
    if not p.exists():
        pytest.skip("Flask v2 graph not available")
    return load_graph(p)


class TestSingleDelta:
    def test_returns_updated_graph(self, flask_graph, flask_repo):
        """apply_single_delta returns a new graph and a fidelity delta report."""
        result = apply_single_delta(
            graph=flask_graph,
            repo_root=flask_repo,
            from_commit="HEAD~1",
            to_commit="HEAD",
        )
        assert "updated_graph" in result
        assert "fidelity_delta" in result
        assert "dng" in result

    def test_dng_within_threshold(self, flask_graph, flask_repo):
        """DNG (delta non-inferiority gap) is <= 0.05 for a single commit."""
        result = apply_single_delta(
            graph=flask_graph,
            repo_root=flask_repo,
            from_commit="HEAD~1",
            to_commit="HEAD",
        )
        assert result["dng"] <= 0.05, f"DNG {result['dng']} exceeds 0.05 threshold"

    def test_confidence_recomputed_locally(self, flask_graph, flask_repo):
        """Delta update recomputes confidence for changed + 1-hop nodes only."""
        result = apply_single_delta(
            graph=flask_graph,
            repo_root=flask_repo,
            from_commit="HEAD~1",
            to_commit="HEAD",
        )
        assert "recomputed_nodes" in result
        assert len(result["recomputed_nodes"]) > 0
        # Unchanged nodes should NOT be in recomputed list
        total_nodes = len(flask_graph.nodes)
        assert len(result["recomputed_nodes"]) < total_nodes


class TestSequentialDrift:
    def test_10_step_drift(self, flask_graph, flask_repo):
        """Apply 10 sequential deltas, fidelity floor maintained."""
        result = run_drift_protocol(
            repo_root=flask_repo,
            n_commits=10,
            operation_family="OF2",
        )
        assert result["steps_completed"] == 10
        for step in result["steps"]:
            assert step["fidelity"] >= 0.80, f"Step {step['index']}: FS {step['fidelity']} below 0.80"

    def test_drift_slope(self, flask_graph, flask_repo):
        """Drift slope >= -0.002 per update."""
        result = run_drift_protocol(
            repo_root=flask_repo,
            n_commits=10,
            operation_family="OF2",
        )
        assert result["slope"] >= -0.002, f"Slope {result['slope']} below -0.002"


class TestResetTrigger:
    def test_triggers_on_floor_breach(self):
        """Reset triggers when FS drops below floor."""
        history = [
            {"fidelity": 0.90},
            {"fidelity": 0.87},
            {"fidelity": 0.82},
            {"fidelity": 0.78},  # Below 0.80 floor
        ]
        assert detect_reset_trigger(history, floor=0.80) is True

    def test_no_trigger_above_floor(self):
        """No reset when all FS above floor and slope is gentle."""
        history = [
            {"fidelity": 0.92},
            {"fidelity": 0.92},
            {"fidelity": 0.92},
            {"fidelity": 0.915},
        ]
        assert detect_reset_trigger(history, floor=0.80) is False

    def test_triggers_on_steep_slope(self):
        """Reset triggers when slope exceeds guard band."""
        history = [
            {"fidelity": 0.90},
            {"fidelity": 0.88},
            {"fidelity": 0.84},
            {"fidelity": 0.81},
        ]
        # Slope is about -0.003 per step, exceeds -0.002 guard
        assert detect_reset_trigger(history, floor=0.80, slope_guard=-0.002) is True


class TestFullDriftProtocol:
    @pytest.mark.slow
    def test_50_commit_drift_flask(self, flask_repo):
        """Full 50-commit H4 protocol on Flask."""
        result = run_drift_protocol(
            repo_root=flask_repo,
            n_commits=50,
            operation_family="OF2",
        )
        assert result["steps_completed"] == 50
        assert result["floor_maintained"] is True, "H4 FAIL: fidelity dropped below floor"
        assert result["slope"] >= -0.002, f"H4 FAIL: slope {result['slope']}"
