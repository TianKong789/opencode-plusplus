"""Port for tests that assess a model capability."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models import Capability, CapabilityScore, Model


@runtime_checkable
class CapabilityTest(Protocol):
    """Defines a test that evaluates one model capability."""

    def capability(self) -> Capability:
        """Return the capability this test evaluates."""

    def run(self, model: Model) -> CapabilityScore:
        """Execute the test against a model."""

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        """Load test tasks for this capability."""
