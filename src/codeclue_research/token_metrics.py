"""Token-level compression metrics for clue view evaluation.

Measures CCR, TRCR, and poisoned-vs-clean compaction ratios.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .token_counter import count_tokens


def _read_source_tokens(repo_root: str | Path, file_paths: list[str]) -> int:
    """Count total tokens across raw source files."""
    total = 0
    for fp in file_paths:
        full = Path(repo_root) / fp
        if full.is_file():
            try:
                text = full.read_text(encoding="utf-8", errors="replace")
                total += count_tokens(text)
            except OSError:
                pass
    return total


def _files_from_clue(clue: dict[str, Any], plan: str) -> list[str]:
    """Extract unique file paths from a clue artifact."""
    files: set[str] = set()
    if plan == "a":
        for entity in clue.get("entities", []):
            f = entity.get("file", "")
            if f:
                files.add(f)
    elif plan == "b":
        for node in clue.get("nodes", []):
            f = node.get("file", "")
            if f:
                files.add(f)
    return sorted(files)


def _files_from_projection(projection: dict[str, Any]) -> list[str]:
    """Extract unique file paths from a projection."""
    files: set[str] = set()
    for node in projection.get("projected_nodes", []):
        anchor = node.get("source_anchor", {})
        fp = anchor.get("file_path", "")
        if fp:
            files.add(fp)
    return sorted(files)


def compute_compression_metrics(
    task_id: str,
    clue_view: dict[str, Any],
    projection_trace: dict[str, Any],
    repo_root: str | Path,
    plan: str = "a",
    drilldown_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute token compression metrics for a single task.

    Args:
        task_id: Task identifier.
        clue_view: Compact clue artifact (Plan A or Plan B).
        projection_trace: Full verbose projection result.
        repo_root: Path to repo root for raw source reading.
        plan: "a" or "b" for file extraction from clue.
        drilldown_context: Optional drill-down output for TRCR calculation.

    Returns:
        Dict with all compression metrics.
    """
    # Token counts
    clue_tokens = count_tokens(clue_view)
    projection_tokens = count_tokens(projection_trace)

    # Raw source: use files referenced in projection (not clue, to be fair)
    source_files = _files_from_projection(projection_trace)
    raw_first_tokens = _read_source_tokens(repo_root, source_files)

    drilldown_tokens = count_tokens(drilldown_context) if drilldown_context else 0

    # Metrics
    ccr = 1.0 - (clue_tokens / raw_first_tokens) if raw_first_tokens > 0 else 0.0
    trcr = (
        1.0 - ((clue_tokens + drilldown_tokens) / raw_first_tokens)
        if raw_first_tokens > 0
        else 0.0
    )
    poisoned_ratio = projection_tokens / clue_tokens if clue_tokens > 0 else 0.0

    return {
        "task_id": task_id,
        "plan": plan,
        "raw_first_tokens": raw_first_tokens,
        "clue_tokens": clue_tokens,
        "projection_tokens": projection_tokens,
        "drilldown_tokens": drilldown_tokens,
        "ccr": round(ccr, 4),
        "trcr": round(trcr, 4),
        "poisoned_vs_clean_ratio": round(poisoned_ratio, 2),
        "source_files": source_files,
        "source_file_count": len(source_files),
    }
