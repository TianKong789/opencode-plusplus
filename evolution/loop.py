from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class EvolutionLoop:
    """Coordinates the recursive improvement cycle.

    Drives the Reflection → Experience → Skill → Benchmark loop
    and tracks improvement over iterations.
    """

    max_iterations: int = 10
    current_iteration: int = 0

    def should_continue(self) -> bool:
        """Check whether another evolution iteration should run.

        Returns:
            True if under the iteration limit.
        """
        return self.current_iteration < self.max_iterations

    def record_iteration(self) -> EvolutionLoop:
        """Increment the iteration counter.

        Returns:
            A new EvolutionLoop with the incremented counter.
        """
        return EvolutionLoop(
            max_iterations=self.max_iterations,
            current_iteration=self.current_iteration + 1,
        )
