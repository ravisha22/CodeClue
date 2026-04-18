from __future__ import annotations

from pathlib import Path

from codeclue_research.clue_view_mrlf import render_mrlf
from codeclue_research.extractor import extract_graph


def _focus_entries(clue: str) -> dict[str, str]:
    in_focus = False
    current_key: str | None = None
    blocks: dict[str, list[str]] = {}
    for line in clue.splitlines():
        if line == "-- FOCUS":
            in_focus = True
            continue
        if in_focus and line.startswith("-- "):
            break
        if not in_focus:
            continue
        if line and not line.startswith("  "):
            current_key = line.strip()
            blocks[current_key] = [line.rstrip()]
            continue
        if current_key is not None:
            blocks[current_key].append(line.rstrip())
    return {key: "\n".join(value) for key, value in blocks.items()}


def test_mrlf_focus_delta_updates_only_affected_entries(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    (repo / "alpha.py").write_text(
        "def alpha(data):\n"
        "    total = []\n"
        "    for item in data:\n"
        "        total.append(item)\n"
        "    return total\n",
        encoding="utf-8",
    )
    (repo / "beta.py").write_text(
        "def beta(flag):\n"
        "    if not flag:\n"
        "        return 'fallback'\n"
        "    return flag\n",
        encoding="utf-8",
    )
    question = "How do alpha and beta process their inputs?"

    before = render_mrlf(extract_graph(repo, language="python"), question, repo_root=repo)

    (repo / "alpha.py").write_text(
        "def alpha(data):\n"
        "    body = []\n"
        "    for chunk in data:\n"
        "        body.append(chunk)\n"
        "    if not body:\n"
        "        return ['empty']\n"
        "    return body\n",
        encoding="utf-8",
    )

    after = render_mrlf(extract_graph(repo, language="python"), question, repo_root=repo)

    before_focus = _focus_entries(before)
    after_focus = _focus_entries(after)

    changed = {key for key in before_focus if before_focus.get(key) != after_focus.get(key)}
    unchanged = {key for key in before_focus if before_focus.get(key) == after_focus.get(key)}

    assert changed, "Expected at least one FOCUS entry to change after modifying alpha.py"
    assert any("alpha" in key.lower() for key in changed)
    assert any("beta" in key.lower() for key in unchanged), "Unmodified beta entry should remain stable"
