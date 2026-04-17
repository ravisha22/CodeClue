"""Per-session tool call budget tracker."""
from __future__ import annotations

from typing import Any


_DEFAULT_BUDGETS: dict[str, int] = {
    "OF1": 5,
    "OF2": 15,
    "OF3": 10,
    "OF4": 20,
    "OF5": 30,
}

DEFAULT_CONFIDENCE_THRESHOLD = 0.8


class BudgetTracker:
    def __init__(self, operation_family: str, budget: int | None = None) -> None:
        self.operation_family = operation_family
        self.budget = budget if budget is not None else _DEFAULT_BUDGETS.get(operation_family, 15)
        self._calls: list[dict[str, Any]] = []
        self._unresolved: list[str] = []

    def can_call(self) -> bool:
        return len(self._calls) < self.budget

    def remaining(self) -> int:
        return max(0, self.budget - len(self._calls))

    def record_call(self, tool: str, node_id: str, confidence: float | None = None) -> None:
        entry: dict[str, Any] = {"tool": tool, "node_id": node_id}
        if confidence is not None:
            entry["confidence"] = float(confidence)
        self._calls.append(entry)

    def register_unresolved(self, node_ids: list[str]) -> None:
        self._unresolved = list(node_ids)

    def get_escalation(self) -> dict[str, Any]:
        exhausted = len(self._calls) >= self.budget
        return {
            "budget_exhausted": exhausted,
            "operation_family": self.operation_family,
            "calls_made": len(self._calls),
            "budget": self.budget,
            "remaining": self.remaining(),
            "calls": list(self._calls),
            "unresolved_nodes": self._unresolved if exhausted else [],
        }
