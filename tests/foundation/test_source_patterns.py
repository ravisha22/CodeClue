"""Tests for source_patterns module."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from codeclue_research.source_patterns import (
    clear_cache,
    scan_node,
    scan_projected_nodes,
)


def _write_file(tmpdir: Path, relpath: str, content: str) -> None:
    full = tmpdir / relpath
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")


class TestRiskDetection:
    def test_exception_swallowed(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def foo():\n    try:\n        pass\n    except:\n        pass\n")
        result = scan_node("n1", "function", "mod.py", 1, 5, "python", tmp_path)
        assert "exception_swallowed" in result["risks"]

    def test_bare_except(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def foo():\n    try:\n        pass\n    except:\n        log()\n")
        result = scan_node("n1", "function", "mod.py", 1, 5, "python", tmp_path)
        assert "bare_except" in result["risks"]

    def test_broad_exception(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def foo():\n    try:\n        pass\n    except Exception as e:\n        log(e)\n")
        result = scan_node("n1", "function", "mod.py", 1, 5, "python", tmp_path)
        assert "broad_exception_handler" in result["risks"]

    def test_mutable_default(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def foo(items=[]):\n    return items\n")
        result = scan_node("n1", "function", "mod.py", 1, 2, "python", tmp_path)
        assert "mutable_default_arg" in result["risks"]

    def test_finally_block(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def foo():\n    try:\n        pass\n    finally:\n        cleanup()\n")
        result = scan_node("n1", "function", "mod.py", 1, 5, "python", tmp_path)
        assert "runs_in_finally" in result["risks"]

    def test_no_risks_clean_code(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def add(a: int, b: int) -> int:\n    return a + b\n")
        result = scan_node("n1", "function", "mod.py", 1, 2, "python", tmp_path)
        assert result["risks"] == []

    def test_implicit_none_return(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def foo():\n    if True:\n        return\n    pass\n")
        result = scan_node("n1", "function", "mod.py", 1, 4, "python", tmp_path)
        assert "implicit_none_return" in result["risks"]


class TestSecurityMarkers:
    def test_auth_decorator(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "@login_required\ndef view():\n    pass\n")
        result = scan_node("n1", "function", "mod.py", 1, 3, "python", tmp_path)
        assert "has_auth_decorator" in result["security_markers"]

    def test_input_validation(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def process():\n    sanitize(data)\n    validate(input)\n")
        result = scan_node("n1", "function", "mod.py", 1, 3, "python", tmp_path)
        assert "has_input_validation" in result["security_markers"]

    def test_no_security_markers(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def add(a, b):\n    return a + b\n")
        result = scan_node("n1", "function", "mod.py", 1, 2, "python", tmp_path)
        assert result["security_markers"] == []


class TestSignatureExtraction:
    def test_python_sig(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "def greet(name: str) -> str:\n    return f'hello {name}'\n")
        result = scan_node("n1", "function", "mod.py", 1, 2, "python", tmp_path)
        assert "def greet(name: str) -> str" in result["sig"]

    def test_module_no_sig(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "import os\nX = 1\n")
        result = scan_node("n1", "module", "mod.py", 1, 2, "python", tmp_path)
        assert result["sig"] == ""


class TestBatchScan:
    def test_scan_projected_nodes(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "app.py", "def handler():\n    try:\n        pass\n    except:\n        pass\n")
        nodes = [
            {
                "node_id": "symbol:app.py:handler:1",
                "node_type": "function",
                "source_anchor": {"file_path": "app.py", "byte_start": 0, "byte_end": 60},
                "semantic_contract": {"language": "python"},
            }
        ]
        results = scan_projected_nodes(nodes, tmp_path)
        assert "symbol:app.py:handler:1" in results
        assert "exception_swallowed" in results["symbol:app.py:handler:1"]["risks"]

    def test_missing_file_no_crash(self, tmp_path: Path) -> None:
        nodes = [
            {
                "node_id": "symbol:missing.py:foo:1",
                "node_type": "function",
                "source_anchor": {"file_path": "missing.py", "byte_start": 0, "byte_end": 100},
                "semantic_contract": {"language": "python"},
            }
        ]
        results = scan_projected_nodes(nodes, tmp_path)
        assert results["symbol:missing.py:foo:1"]["risks"] == []


class TestPatternsCombined:
    def test_patterns_is_union(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "mod.py", "@login_required\ndef foo():\n    try:\n        pass\n    except:\n        pass\n")
        result = scan_node("n1", "function", "mod.py", 1, 6, "python", tmp_path)
        assert "exception_swallowed" in result["patterns"]
        assert "has_auth_decorator" in result["patterns"]
