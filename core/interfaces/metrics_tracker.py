from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.evaluation import Evaluation


class MetricsTrackerPort(ABC):
    """Records evaluations and exposes aggregate scores."""

    @abstractmethod
    def record(self, evaluation: Evaluation) -> MetricsTrackerPort:
        """Return a tracker that includes an evaluation.

        Args:
            evaluation: The evaluation to record.

        Returns:
            A tracker containing the supplied evaluation.
        """

    @abstractmethod
    def average_score(self) -> float:
        """Return the average score across recorded evaluations."""
