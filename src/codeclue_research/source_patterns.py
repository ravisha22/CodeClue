"""Lightweight static analysis: detect risks, patterns, and signatures from source.

No LLM calls. All detection is regex/heuristic-based on projected source files.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

_EXCEPTION_BROAD = re.compile(
    r"except\s*(?:Exception|BaseException)?\s*(?:as\s+\w+)?\s*:", re.MULTILINE
)
_EXCEPTION_BARE = re.compile(r"except\s*:", re.MULTILINE)
_EXCEPTION_PASS = re.compile(
    r"except[^:]*:\s*\n\s+pass\b", re.MULTILINE
)
_MUTABLE_DEFAULT = re.compile(
    r"def\s+\w+\s*\([^)]*(?:=\s*\[\]|=\s*\{\}|=\s*set\(\))", re.MULTILINE
)
_STATE_MUTATION = re.compile(r"self\.\w+\s*=", re.MULTILINE)
_INIT_DEF = re.compile(r"def\s+__init__\s*\(", re.MULTILINE)
_FINALLY_BLOCK = re.compile(r"\bfinally\s*:", re.MULTILINE)
_RETURN_NONE = re.compile(r"^\s+return\s*$", re.MULTILINE)

# Security patterns
_AUTH_DECORATOR = re.compile(
    r"@(?:login_required|requires_auth|permission_required|"
    r"auth_required|permissions_required|jwt_required|"
    r"authenticated|authorize)",
    re.MULTILINE,
)
_INPUT_VALIDATION = re.compile(
    r"\b(?:sanitize|validate|escape|clean|strip_tags|bleach|"
    r"is_valid|check_input|verify_input)\b",
    re.MULTILINE | re.IGNORECASE,
)
_SQL_INJECTION_RISK = re.compile(
    r"(?:cursor\.execute|\.raw\(|\.extra\()\s*\(?\s*f['\"]|"
    r"(?:cursor\.execute|\.raw\(|\.extra\()\s*\(?\s*['\"].*%s|"
    r"(?:cursor\.execute|\.raw\(|\.extra\()\s*\(?\s*.*\+\s*",
    re.MULTILINE,
)
_PATH_TRAVERSAL_RISK = re.compile(
    r"\bopen\s*\([^)]*(?:request|user|input|param|arg|query)",
    re.MULTILINE | re.IGNORECASE,
)

# Signature extraction
_PYTHON_SIG = re.compile(
    r"^(\s*(?:@\w+(?:\([^)]*\))?\s*\n)*\s*(?:async\s+)?def\s+\w+\s*\([^)]*\)(?:\s*->\s*[^:]+)?)\s*:",
    re.MULTILINE,
)
_TS_SIG = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+\w+\s*(?:<[^>]*>)?\s*\([^)]*\)(?:\s*:\s*[^\{]+)?",
    re.MULTILINE,
)
_GO_SIG = re.compile(
    r"func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\s*\([^)]*\)(?:\s*(?:\([^)]*\)|\w+))?",
    re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Source reading
# ---------------------------------------------------------------------------

_file_cache: dict[str, str | None] = {}


def _read_source(repo_root: str | Path, file_path: str) -> str | None:
    """Read source file, with simple cache per call batch."""
    key = f"{repo_root}:{file_path}"
    if key in _file_cache:
        return _file_cache[key]
    full = Path(repo_root) / file_path
    if not full.is_file():
        _file_cache[key] = None
        return None
    try:
        text = full.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = None
    _file_cache[key] = text
    return text


def _read_lines(repo_root: str | Path, file_path: str, start: int, end: int) -> str:
    """Read specific line range (1-based inclusive)."""
    text = _read_source(repo_root, file_path)
    if text is None:
        return ""
    lines = text.splitlines()
    start_idx = max(0, start - 1)
    end_idx = min(len(lines), end)
    return "\n".join(lines[start_idx:end_idx])


# ---------------------------------------------------------------------------
# Pattern detection
# ---------------------------------------------------------------------------


def _detect_risks(source: str, language: str) -> list[str]:
    """Detect behavioral risk patterns from source snippet."""
    risks: list[str] = []

    if language == "python":
        if _EXCEPTION_PASS.search(source):
            risks.append("exception_swallowed")
        elif _EXCEPTION_BARE.search(source):
            risks.append("bare_except")
        elif _EXCEPTION_BROAD.search(source):
            risks.append("broad_exception_handler")

        if _MUTABLE_DEFAULT.search(source):
            risks.append("mutable_default_arg")

        if _FINALLY_BLOCK.search(source):
            risks.append("runs_in_finally")

        if _RETURN_NONE.search(source):
            risks.append("implicit_none_return")

        # State mutation outside __init__
        if _STATE_MUTATION.search(source) and not _INIT_DEF.search(source):
            risks.append("state_mutation_outside_init")

    # Security risks (language-agnostic patterns)
    if _SQL_INJECTION_RISK.search(source):
        risks.append("sql_injection_risk")
    if _PATH_TRAVERSAL_RISK.search(source):
        risks.append("path_traversal_risk")

    return risks


def _detect_security_markers(source: str) -> list[str]:
    """Detect security-related markers."""
    markers: list[str] = []
    if _AUTH_DECORATOR.search(source):
        markers.append("has_auth_decorator")
    if _INPUT_VALIDATION.search(source):
        markers.append("has_input_validation")
    return markers


def _extract_signature(source: str, language: str) -> str:
    """Extract function/method signature."""
    patterns = {
        "python": _PYTHON_SIG,
        "typescript": _TS_SIG,
        "javascript": _TS_SIG,
        "go": _GO_SIG,
    }
    pattern = patterns.get(language)
    if pattern is None:
        return ""
    match = pattern.search(source)
    if match:
        sig = match.group(0).strip()
        # Normalize multi-line signatures
        sig = re.sub(r"\s*\n\s*", " ", sig)
        # Limit length
        if len(sig) > 200:
            sig = sig[:197] + "..."
        return sig
    return ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def clear_cache() -> None:
    """Clear the source file cache between runs."""
    _file_cache.clear()


def scan_node(
    node_id: str,
    node_type: str,
    file_path: str,
    start_line: int,
    end_line: int,
    language: str,
    repo_root: str | Path,
) -> dict[str, Any]:
    """Scan a single projected node and return detected patterns.

    Returns:
        {
            "risks": [...],
            "security_markers": [...],
            "sig": "...",
            "patterns": [...],          # union of risks + security_markers
        }
    """
    source = _read_lines(repo_root, file_path, start_line, end_line)

    risks = _detect_risks(source, language) if source else []
    security = _detect_security_markers(source) if source else []
    sig = _extract_signature(source, language) if source and node_type != "module" else ""

    return {
        "risks": risks,
        "security_markers": security,
        "sig": sig,
        "patterns": risks + security,
    }


def scan_projected_nodes(
    projected_nodes: list[dict[str, Any]],
    repo_root: str | Path,
) -> dict[str, dict[str, Any]]:
    """Scan all projected nodes and return a mapping of node_id → scan results.

    Each projected_node dict must have:
        - node_id
        - node_type
        - source_anchor.file_path
        - source_anchor (with byte_start/byte_end or we use line heuristic)
        - semantic_contract.language (optional, inferred from file_path)
    """
    clear_cache()
    results: dict[str, dict[str, Any]] = {}

    for node in projected_nodes:
        node_id = node.get("node_id", "")
        node_type = node.get("node_type", "")
        anchor = node.get("source_anchor", {})
        file_path = anchor.get("file_path", "")
        language = node.get("semantic_contract", {}).get("language", "")

        if not language:
            ext = Path(file_path).suffix.lower()
            language = {".py": "python", ".ts": "typescript", ".go": "go", ".js": "javascript"}.get(ext, "")

        # Convert byte offsets to approximate line numbers if we don't have lines
        byte_start = anchor.get("byte_start", 0)
        byte_end = anchor.get("byte_end", 0)

        # Read full file to estimate lines from byte offsets
        full_source = _read_source(repo_root, file_path)
        if full_source:
            start_line = full_source[:byte_start].count("\n") + 1
            end_line = full_source[:byte_end].count("\n") + 1
        else:
            start_line = 1
            end_line = 100

        results[node_id] = scan_node(
            node_id=node_id,
            node_type=node_type,
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            language=language,
            repo_root=repo_root,
        )

    clear_cache()
    return results
