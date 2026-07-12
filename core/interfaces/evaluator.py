from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.evaluation import Evaluation
from core.models.execution import Execution


class Evaluator(ABC):
    """Assesses execution results against defined criteria."""

    @abstractmethod
    def evaluate(self, execution: Execution) -> Evaluation:
        """Evaluate a completed execution.

        Args:
            execution: The execution to evaluate. Must be in a terminal state.

        Returns:
            An evaluation with score and verdict.
        """

    @abstractmethod
    def get_evaluation(self, evaluation_id: str) -> Evaluation | None:
        """Retrieve an evaluation by its identifier.

        Args:
            evaluation_id: The unique identifier of the evaluation.

        Returns:
            The evaluation if found, None otherwise.
        """
