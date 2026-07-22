"""Port for tests that assess a model capability."""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.models import Capability, CapabilityScore, Model


class CapabilityTest(ABC):
    """Defines a test that evaluates one model capability."""

    @abstractmethod
    def capability(self) -> Capability:
        """Return the capability this test evaluates."""

    @abstractmethod
    def run(self, model: Model) -> CapabilityScore:
        """Execute the test against a model."""

    @abstractmethod
    def load_tasks(self) -> tuple[dict[str, object], ...]:
        """Load test tasks for this capability."""
