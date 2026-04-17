"""Tests for invocation trace logging — every tool call produces a trace entry."""
import json
import pytest
import tempfile
from pathlib import Path

from codeclue_mcp.tracer import InvocationTracer
from codeclue_mcp.tools import code_slice
from codeclue_research.io import load_graph


@pytest.fixture
def flask_repo():
    p = Path("experiments/external-repos/flask")
    if not p.exists():
        pytest.skip("Flask repo not cloned")
    return p


@pytest.fixture
def trace_dir(tmp_path):
    return tmp_path / "traces"


class TestInvocationTrace:
    def test_trace_file_created(self, trace_dir):
        """InvocationTracer creates a trace file on first log."""
        tracer = InvocationTracer(trace_dir=trace_dir)
        tracer.log(tool="code_slice", args={"file": "a.py"}, output_hash="abc123",
                   source_anchor="a.py:1-10", confidence_trigger=0.62, session_id="test-1")
        trace_files = list(trace_dir.glob("*.jsonl"))
        assert len(trace_files) == 1

    def test_trace_entry_has_required_fields(self, trace_dir):
        """Each trace entry contains all required fields per PRD."""
        tracer = InvocationTracer(trace_dir=trace_dir)
        tracer.log(tool="resolve_dependency", args={"node_id": "x", "depth": 2},
                   output_hash="def456", source_anchor="b.py:module",
                   confidence_trigger=0.45, session_id="test-2")

        trace_file = list(trace_dir.glob("*.jsonl"))[0]
        entry = json.loads(trace_file.read_text().strip().split("\n")[-1])

        assert "timestamp" in entry
        assert entry["tool"] == "resolve_dependency"
        assert entry["args"] == {"node_id": "x", "depth": 2}
        assert entry["output_hash"] == "def456"
        assert entry["source_anchor"] == "b.py:module"
        assert entry["confidence_trigger"] == 0.45
        assert entry["session_id"] == "test-2"

    def test_trace_entry_includes_confidence_when_provided(self, trace_dir):
        tracer = InvocationTracer(trace_dir=trace_dir)
        tracer.log(
            tool="fetch_contract",
            args={"node_id": "x"},
            output_hash="hash123",
            source_anchor="x",
            confidence_trigger=0.8,
            session_id="test-3",
            confidence=0.72,
            warning="confidence 0.72 below session threshold 0.80",
        )
        trace_file = list(trace_dir.glob("*.jsonl"))[0]
        entry = json.loads(trace_file.read_text().strip().split("\n")[-1])
        assert entry["confidence"] == 0.72
        assert "warning" in entry

    def test_multiple_entries_appended(self, trace_dir):
        """Multiple log calls append to the same file."""
        tracer = InvocationTracer(trace_dir=trace_dir)
        tracer.log(tool="a", args={}, output_hash="1", source_anchor="", confidence_trigger=0.5, session_id="s")
        tracer.log(tool="b", args={}, output_hash="2", source_anchor="", confidence_trigger=0.3, session_id="s")
        tracer.log(tool="c", args={}, output_hash="3", source_anchor="", confidence_trigger=0.1, session_id="s")

        trace_file = list(trace_dir.glob("*.jsonl"))[0]
        lines = [l for l in trace_file.read_text().strip().split("\n") if l]
        assert len(lines) == 3

    def test_trace_is_valid_jsonl(self, trace_dir):
        """Every line in trace file is valid JSON."""
        tracer = InvocationTracer(trace_dir=trace_dir)
        for i in range(5):
            tracer.log(tool=f"tool_{i}", args={"i": i}, output_hash=f"h{i}",
                       source_anchor="", confidence_trigger=0.5, session_id="s")

        trace_file = list(trace_dir.glob("*.jsonl"))[0]
        for line in trace_file.read_text().strip().split("\n"):
            if line:
                json.loads(line)  # Should not raise
