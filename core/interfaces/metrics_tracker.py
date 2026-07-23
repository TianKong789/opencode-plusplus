from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.evaluation import Evaluation


@runtime_checkable
class MetricsTrackerPort(Protocol):
    """Records evaluations and exposes aggregate scores."""

    def record(self, evaluation: Evaluation) -> MetricsTrackerPort:
        """Return a tracker that includes an evaluation.

        Args:
            evaluation: The evaluation to record.

        Returns:
            A tracker containing the supplied evaluation.
        """

    def average_score(self) -> float:
        """Return the average score across recorded evaluations."""
