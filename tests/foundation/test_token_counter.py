"""Tests for token_counter module."""

from __future__ import annotations

from codeclue_research.token_counter import count_tokens, count_tokens_str


class TestTokenCounter:
    def test_simple_string(self) -> None:
        tokens = count_tokens("Hello, world!")
        assert tokens > 0
        assert isinstance(tokens, int)

    def test_dict_input(self) -> None:
        tokens = count_tokens({"key": "value", "nested": {"a": 1}})
        assert tokens > 0

    def test_list_input(self) -> None:
        tokens = count_tokens([1, 2, 3, "hello"])
        assert tokens > 0

    def test_empty_string(self) -> None:
        tokens = count_tokens("")
        assert tokens == 0

    def test_str_function(self) -> None:
        tokens = count_tokens_str("The quick brown fox")
        assert tokens > 0

    def test_larger_content_more_tokens(self) -> None:
        small = count_tokens("hello")
        large = count_tokens("hello " * 100)
        assert large > small

    def test_dict_vs_serialized(self) -> None:
        """Dict token count should match its JSON serialization."""
        d = {"name": "Flask.wsgi_app", "type": "function"}
        import json
        serialized = json.dumps(d, separators=(",", ":"), ensure_ascii=False)
        assert count_tokens(d) == count_tokens_str(serialized)
