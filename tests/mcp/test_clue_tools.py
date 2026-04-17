from __future__ import annotations

from pathlib import Path

import pytest

from codeclue_mcp.server import CodeClueServer
from codeclue_research.extractor import extract_graph


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    (tmp_path / "app.py").write_text(
        "def choose(value):\n"
        "    if value is None:\n"
        "        return 'default'\n"
        "    return value\n",
        encoding="utf-8",
    )
    return tmp_path


def test_get_clue_and_drill_targets_round_trip(tiny_repo: Path):
    graph = extract_graph(tiny_repo, language="python")
    server = CodeClueServer(graph=graph, repo_root=str(tiny_repo), confidence_threshold=0.95)

    clue_result = server.call_tool("get_clue", {"question": "How does choose work?"})
    assert clue_result["status"] == "ok"
    assert "-- GAPS" in clue_result["clue"]

    server.state.active_clue_text = clue_result["clue"]
    drill_result = server.call_tool("get_drill_targets", {})
    assert drill_result["status"] == "ok"
    assert "targets" in drill_result
