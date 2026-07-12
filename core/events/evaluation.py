from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class EvaluationCompleted(BaseEvent):
    """Emitted when the Evaluator finishes assessing an execution."""

    evaluation_id: str = ""
    execution_id: str = ""
    score: float = 0.0
    verdict: str = ""
