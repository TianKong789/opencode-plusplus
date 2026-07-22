from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.benchmark_runner import BenchmarkRunner


class BenchmarkRunnerProvider(ABC):
    """Factory for BenchmarkRunner instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> BenchmarkRunner:
        """Create and return a BenchmarkRunner instance."""
