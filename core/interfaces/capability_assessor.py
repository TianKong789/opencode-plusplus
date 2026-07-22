from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.capability_test import CapabilityTest
from core.models import Capability, CapabilityScore, Model


class CapabilityAssessor(ABC):
    """Assesses models by running registered capability tests."""

    @abstractmethod
    def register_test(self, test: CapabilityTest) -> None:
        """Register a capability test."""

    @abstractmethod
    def get_test(self, capability: Capability) -> CapabilityTest | None:
        """Get the test registered for a capability."""

    @abstractmethod
    def list_capabilities(self) -> tuple[Capability, ...]:
        """List capabilities with registered tests."""

    @abstractmethod
    def assess(self, model: Model, capability: Capability) -> CapabilityScore | None:
        """Run a capability test against a model."""

    @abstractmethod
    def assess_all(self, model: Model) -> tuple[CapabilityScore, ...]:
        """Run all registered tests against a model."""

    @abstractmethod
    def get_results(self, model_id: str) -> tuple[CapabilityScore, ...]:
        """Get prior assessment results for a model."""

    @abstractmethod
    def clear_results(self, model_id: str | None = None) -> None:
        """Clear results for one model or for all models."""
