from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.evaluation import Evaluation
from core.models.execution import Execution


@runtime_checkable
class Evaluator(Protocol):
    """Assesses execution results against defined criteria."""

    def evaluate(self, execution: Execution) -> Evaluation:
        """Evaluate a completed execution.

        Args:
            execution: The execution to evaluate. Must be in a terminal state.

        Returns:
            An evaluation with score and verdict.
        """

    def get_evaluation(self, evaluation_id: str) -> Evaluation | None:
        """Retrieve an evaluation by its identifier.

        Args:
            evaluation_id: The unique identifier of the evaluation.

        Returns:
            The evaluation if found, None otherwise.
        """
