from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.interfaces.capability_test import CapabilityTest
from core.models import Capability, CapabilityScore, Model


@runtime_checkable
class CapabilityAssessor(Protocol):
    """Assesses models by running registered capability tests."""

    def register_test(self, test: CapabilityTest) -> None:
        """Register a capability test."""

    def get_test(self, capability: Capability) -> CapabilityTest | None:
        """Get the test registered for a capability."""

    def list_capabilities(self) -> tuple[Capability, ...]:
        """List capabilities with registered tests."""

    def assess(self, model: Model, capability: Capability) -> CapabilityScore | None:
        """Run a capability test against a model."""

    def assess_all(self, model: Model) -> tuple[CapabilityScore, ...]:
        """Run all registered tests against a model."""

    def get_results(self, model_id: str) -> tuple[CapabilityScore, ...]:
        """Get prior assessment results for a model."""

    def clear_results(self, model_id: str | None = None) -> None:
        """Clear results for one model or for all models."""
