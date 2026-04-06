"""Tests for behavior_summary module."""

from __future__ import annotations

from codeclue_research.behavior_summary import generate_summary


def _edges(pairs: list[tuple[str, str]]) -> list[dict]:
    return [{"edge_type": "calls", "from_node": f, "to_node": t} for f, t in pairs]


class TestSummaryGeneration:
    def test_entrypoint_summary(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="Flask.wsgi_app",
            role="entrypoint", risks=[], security_markers=[], sig="def wsgi_app(self, environ, start_response)",
            projected_edges=_edges([("n1", "n2"), ("n1", "n3")]),
            node_names={"n2": "full_dispatch_request", "n3": "finalize_request"},
        )
        assert "Entrypoint" in summary
        assert "full_dispatch_request" in summary or "finalize_request" in summary

    def test_dispatcher_summary(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="dispatch",
            role="dispatcher", risks=[], security_markers=[], sig="def dispatch(self)",
            projected_edges=_edges([("n1", "n2"), ("n1", "n3"), ("n1", "n4")]),
            node_names={"n2": "handler_a", "n3": "handler_b", "n4": "handler_c"},
        )
        assert "Dispatcher" in summary

    def test_error_handler_summary(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="handle_exception",
            role="error_handler", risks=["broad_exception_handler"], security_markers=[],
            sig="def handle_exception(self, e)",
            projected_edges=_edges([("n1", "n2")]),
            node_names={"n2": "make_response"},
        )
        assert "Error handler" in summary
        assert "broad exception" in summary.lower()

    def test_handler_summary(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="process_request",
            role="handler", risks=[], security_markers=[], sig="def process_request(self)",
            projected_edges=_edges([("n2", "n1")]),
            node_names={"n2": "dispatcher"},
        )
        assert "handler" in summary.lower()

    def test_module_summary(self) -> None:
        edges = [{"edge_type": "contains", "from_node": "m1", "to_node": "n1"},
                 {"edge_type": "contains", "from_node": "m1", "to_node": "n2"}]
        summary = generate_summary(
            node_id="m1", node_type="module", symbol_name="app.py",
            role="module_root", risks=[], security_markers=[], sig="",
            projected_edges=edges, node_names={},
        )
        assert "Module" in summary
        assert "2" in summary

    def test_summary_not_empty(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="unknown",
            role="utility", risks=[], security_markers=[], sig="",
            projected_edges=[], node_names={},
        )
        assert len(summary) > 0

    def test_summary_under_word_limit(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="big_func",
            role="dispatcher", risks=["broad_exception_handler", "mutable_default_arg"],
            security_markers=["has_auth_decorator"],
            sig="def big_func(self, a, b, c, d, e, f)",
            projected_edges=_edges([("n1", f"t{i}") for i in range(10)]),
            node_names={f"t{i}": f"target_{i}" for i in range(10)},
        )
        assert len(summary.split()) <= 45

    def test_async_prefix(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="fetch",
            role="entrypoint", risks=[], security_markers=[],
            sig="async def fetch(self, url)",
            projected_edges=_edges([("n1", "n2")]),
            node_names={"n2": "parser"},
        )
        assert "Async" in summary

    def test_auth_prefix(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="admin_view",
            role="handler", risks=[], security_markers=["has_auth_decorator"],
            sig="def admin_view(self)",
            projected_edges=_edges([("n2", "n1")]),
            node_names={"n2": "router"},
        )
        assert "Auth-protected" in summary

    def test_risk_clause_appended(self) -> None:
        summary = generate_summary(
            node_id="n1", node_type="function", symbol_name="process",
            role="middleware", risks=["runs_in_finally"], security_markers=[],
            sig="def process(self)",
            projected_edges=_edges([("n0", "n1"), ("n1", "n2")]),
            node_names={"n0": "caller", "n2": "callee"},
        )
        assert "finally" in summary.lower()
