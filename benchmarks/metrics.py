from __future__ import annotations

from dataclasses import dataclass, field

from core.models.evaluation import Evaluation


@dataclass(slots=True)
class MetricsTracker:
    """Tracks performance metrics over time.

    Stores evaluation results and computes aggregate statistics.
    """

    _history: list[Evaluation] = field(default_factory=list, init=False, repr=False)

    def record(self, evaluation: Evaluation) -> None:
        """Record an evaluation result.

        Args:
            evaluation: The evaluation to record.
        """
        self._history.append(evaluation)

    def average_score(self) -> float:
        """Compute the average score across all recorded evaluations.

        Returns:
            The mean score, or 0.0 if no evaluations exist.
        """
        if not self._history:
            return 0.0
        return sum(e.score for e in self._history) / len(self._history)

    def pass_rate(self) -> float:
        """Compute the pass rate across all recorded evaluations.

        Returns:
            The fraction of passing evaluations, or 0.0 if none exist.
        """
        if not self._history:
            return 0.0
        passing = sum(1 for e in self._history if e.is_passing())
        return passing / len(self._history)

    def count(self) -> int:
        """Return the number of recorded evaluations.

        Returns:
            The evaluation count.
        """
        return len(self._history)
