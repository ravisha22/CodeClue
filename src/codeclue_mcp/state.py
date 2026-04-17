"""Session state model for the workspace-aware CodeClue MCP server."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from codeclue_research.models import CanonicalClueGraph


@dataclass
class RepoInfo:
    """Describes a discovered repository in the workspace."""

    repo_name: str
    repo_path: str
    language_hint: str
    has_existing_clue: bool = False
    clue_dir: str | None = None
    clue_path: str | None = None
    detail_path: str | None = None


@dataclass
class SessionState:
    """In-memory session state for the workspace-aware MCP server."""

    workspace_root: str | None = None
    discovered_repos: list[RepoInfo] = field(default_factory=list)
    active_repo: str | None = None
    active_clue_dir: str | None = None
    active_clue_path: str | None = None
    active_detail_path: str | None = None
    active_clue_text: str | None = None
    active_detail_records: list[dict[str, Any]] = field(default_factory=list)
    active_graph_path: str | None = None
    active_graph: CanonicalClueGraph | None = None
    active_projection_path: str | None = None
    confidence_threshold: float = 0.0

    @property
    def has_graph(self) -> bool:
        return self.active_graph is not None

    @property
    def has_clue(self) -> bool:
        return bool(self.active_clue_path and self.active_clue_text is not None)
