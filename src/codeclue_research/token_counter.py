"""Token counting utility using tiktoken cl100k_base.

Provides consistent token measurement for compression metrics.
"""

from __future__ import annotations

import json
from typing import Any

import tiktoken


_ENCODING_NAME = "cl100k_base"
_encoder: tiktoken.Encoding | None = None


def _get_encoder() -> tiktoken.Encoding:
    global _encoder
    if _encoder is None:
        _encoder = tiktoken.get_encoding(_ENCODING_NAME)
    return _encoder


def count_tokens(content: str | dict[str, Any] | list[Any]) -> int:
    """Count tokens using cl100k_base encoding.

    Args:
        content: A string, dict, or list. Dicts/lists are serialized to JSON first.

    Returns:
        Token count (int).
    """
    if isinstance(content, (dict, list)):
        text = json.dumps(content, separators=(",", ":"), ensure_ascii=False)
    else:
        text = str(content)
    return len(_get_encoder().encode(text))


def count_tokens_str(text: str) -> int:
    """Count tokens for a plain string."""
    return len(_get_encoder().encode(text))
