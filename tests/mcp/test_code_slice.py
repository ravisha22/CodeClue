"""Tests for code_slice tool — fetches raw source lines from a file."""
import json
import pytest
from pathlib import Path

# The tool module will be at src/codeclue_mcp/tools.py
# Import will fail in RED phase — that's expected.
from codeclue_mcp.tools import code_slice


@pytest.fixture
def flask_repo():
    """Path to the flask repo used as fixture."""
    p = Path("experiments/external-repos/flask")
    if not p.exists():
        pytest.skip("Flask repo not cloned")
    return p


class TestCodeSlice:
    def test_returns_correct_lines(self, flask_repo):
        """code_slice returns the exact source lines requested."""
        result = code_slice(
            repo_root=str(flask_repo),
            file_path="src/flask/app.py",
            start_line=1,
            end_line=10,
        )
        assert result["status"] == "ok"
        assert len(result["lines"]) == 10
        assert result["lines"][0]["line_number"] == 1
        assert "flask" in result["lines"][0]["content"].lower() or "import" in result["lines"][0]["content"].lower()

    def test_returns_line_numbers(self, flask_repo):
        """Each returned line includes its 1-based line number."""
        result = code_slice(
            repo_root=str(flask_repo),
            file_path="src/flask/app.py",
            start_line=5,
            end_line=8,
        )
        assert result["lines"][0]["line_number"] == 5
        assert result["lines"][-1]["line_number"] == 8

    def test_matches_raw_file_read(self, flask_repo):
        """Output matches reading the file directly."""
        target = flask_repo / "src" / "flask" / "app.py"
        raw_lines = target.read_text(encoding="utf-8").splitlines()

        result = code_slice(
            repo_root=str(flask_repo),
            file_path="src/flask/app.py",
            start_line=1,
            end_line=5,
        )
        for entry in result["lines"]:
            ln = entry["line_number"]
            assert entry["content"] == raw_lines[ln - 1]

    def test_different_files(self, flask_repo):
        """Works on multiple different files."""
        for fpath in ["src/flask/ctx.py", "src/flask/sessions.py", "src/flask/config.py"]:
            result = code_slice(
                repo_root=str(flask_repo),
                file_path=fpath,
                start_line=1,
                end_line=3,
            )
            assert result["status"] == "ok"
            assert len(result["lines"]) == 3

    def test_invalid_file_returns_error(self, flask_repo):
        """Requesting a nonexistent file returns an error status."""
        result = code_slice(
            repo_root=str(flask_repo),
            file_path="nonexistent/file.py",
            start_line=1,
            end_line=5,
        )
        assert result["status"] == "error"

    def test_out_of_range_clamps(self, flask_repo):
        """Requesting beyond file end returns available lines without error."""
        result = code_slice(
            repo_root=str(flask_repo),
            file_path="src/flask/__init__.py",
            start_line=1,
            end_line=99999,
        )
        assert result["status"] == "ok"
        assert len(result["lines"]) > 0
        assert len(result["lines"]) < 99999

    def test_path_traversal_blocked(self, flask_repo):
        """Path traversal attempts are rejected."""
        result = code_slice(
            repo_root=str(flask_repo),
            file_path="../../etc/passwd",
            start_line=1,
            end_line=5,
        )
        assert result["status"] == "error"

    def test_symbol_lookup_uses_detail_store(self, tmp_path):
        source = tmp_path / "example.py"
        source.write_text("def target():\n    return 42\n", encoding="utf-8")
        result = code_slice(
            repo_root=str(tmp_path),
            symbol_name="target",
            graph=None,
            detail_records=[
                {
                    "symbol": "target",
                    "file": "example.py",
                    "lines": [1, 2],
                    "source": "def target():\n    return 42",
                }
            ],
        )
        assert result["status"] == "ok"
        assert result["symbol_name"] == "target"
        assert result["confidence"] == 1.0
        assert result["lines"][0]["content"].startswith("def target")
