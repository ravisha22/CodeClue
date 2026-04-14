"""Session state model for the workspace-aware CodeClue MCP server."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codeclue_research.models import CanonicalClueGraph


@dataclass
class RepoInfo:
    """Describes a discovered repository in the workspace."""

    repo_name: str
    repo_path: str
    language_hint: str
    has_existing_clue: bool = False


@dataclass
class SessionState:
    """In-memory session state for the workspace-aware MCP server.

    Not persisted across restarts — graph files on disk are the durable state.
    """

    workspace_root: str | None = None
    discovered_repos: list[RepoInfo] = field(default_factory=list)
    active_repo: str | None = None
    active_clue_path: str | None = None
    active_graph: CanonicalClueGraph | None = None
    active_projection_path: str | None = None

    @property
    def has_graph(self) -> bool:
        return self.active_graph is not None
