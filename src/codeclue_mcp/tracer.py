"""Invocation trace middleware — logs every tool call to JSONL."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class InvocationTracer:
    def __init__(self, trace_dir: Path | str) -> None:
        self._trace_dir = Path(trace_dir)
        self._trace_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        self._trace_file = self._trace_dir / f"trace-{ts}.jsonl"

    def log(
        self,
        tool: str,
        args: dict[str, Any],
        output_hash: str,
        source_anchor: str,
        confidence_trigger: float,
        session_id: str,
        confidence: float | None = None,
        warning: str | None = None,
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": tool,
            "args": args,
            "output_hash": output_hash,
            "source_anchor": source_anchor,
            "confidence_trigger": confidence_trigger,
            "session_id": session_id,
        }
        if confidence is not None:
            entry["confidence"] = confidence
        if warning:
            entry["warning"] = warning
        with self._trace_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")

    @property
    def trace_path(self) -> Path:
        return self._trace_file


def hash_output(data: Any) -> str:
    """Compute a content hash for a tool output."""
    blob = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
