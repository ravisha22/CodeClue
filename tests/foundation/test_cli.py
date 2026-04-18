from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

from codeclue_research.cli import main
from codeclue_research.deep_context import default_context_output_path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def test_extract_deep_writes_deterministic_context(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    _write(repo_root / "app.py", "def main() -> int:\n    return 1\n")
    _write(
        repo_root / "README.md",
        """
        # Sample Platform

        ## Architecture
        API service with Django models and routed endpoints.
        """,
    )
    _write(
        repo_root / "settings.py",
        """
        INSTALLED_APPS = ["store"]
        MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]
        """,
    )
    _write(
        repo_root / "store" / "models.py",
        """
        from django.db import models

        class Author(models.Model):
            pass

        class Book(models.Model):
            author = models.ForeignKey(Author, on_delete=models.CASCADE)
        """,
    )
    _write(
        repo_root / "store" / "urls.py",
        """
        from django.urls import path

        def book_list():
            return []

        urlpatterns = [
            path("books/", book_list),
        ]
        """,
    )
    _write(
        repo_root / "pyproject.toml",
        """
        [project]
        dependencies = ["django", "celery"]
        """,
    )

    output_path = tmp_path / "artifacts" / "graph.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "codeclue",
            "extract",
            "--repo-root",
            str(repo_root),
            "--output",
            str(output_path),
            "--language",
            "python",
            "--deep",
        ],
    )

    assert main() == 0
    context_path = default_context_output_path(output_path)
    payload = json.loads(context_path.read_text(encoding="utf-8"))
    files = {item["path"]: item for item in payload["files"]}

    assert output_path.exists()
    assert context_path.exists()
    assert "README.md" in files
    assert "settings.py" in files
    assert files["settings.py"]["summary"]["settings_refs"]["INSTALLED_APPS"] == ["store"]
    assert files["store/models.py"]["summary"]["classes"] == ["Author", "Book"]
    assert "Book.author->Author (ForeignKey)" in files["store/models.py"]["summary"]["relations"]
    assert any("books/" in route and "book_list" in route for route in files["store/urls.py"]["summary"]["routes"])
