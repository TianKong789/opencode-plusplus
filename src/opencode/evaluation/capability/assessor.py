"""Capability assessor implementation.

Assesses model capabilities using registered tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.interfaces import CapabilityAssessor as CapabilityAssessorPort
from core.interfaces import CapabilityTest
from core.models import Capability, CapabilityScore, Model


@dataclass
class CapabilityAssessor(CapabilityAssessorPort):
    """Assesses model capabilities by running registered tests.

    Tests are injected via constructor or registered after init.
    No auto-discovery — fully explicit for architectural purity.
    """

    _tests: dict[Capability, CapabilityTest] = field(default_factory=dict)
    _results: dict[str, list[CapabilityScore]] = field(default_factory=dict)

    def register_test(self, test: CapabilityTest) -> None:
        """Register a capability test.

        Args:
            test: The test implementation to register.
        """
        self._tests[test.capability()] = test

    def get_test(self, capability: Capability) -> CapabilityTest | None:
        """Get the test for a specific capability.

        Args:
            capability: The capability to find.

        Returns:
            The registered test, or None.
        """
        return self._tests.get(capability)

    def list_capabilities(self) -> tuple[Capability, ...]:
        """List all registered capability tests.

        Returns:
            Tuple of capabilities with registered tests.
        """
        return tuple(self._tests.keys())

    def assess(self, model: Model, capability: Capability) -> CapabilityScore | None:
        """Run a specific capability test against a model.

        Args:
            model: The model to assess.
            capability: The capability to test.

        Returns:
            The CapabilityScore if test exists, None otherwise.
        """
        test = self._tests.get(capability)
        if test is None:
            return None

        score = test.run(model)

        if model.model_id not in self._results:
            self._results[model.model_id] = []
        self._results[model.model_id].append(score)

        return score

    def assess_all(self, model: Model) -> tuple[CapabilityScore, ...]:
        """Run all registered tests against a model.

        Args:
            model: The model to assess.

        Returns:
            Tuple of CapabilityScore for all registered capabilities.
        """
        scores = []
        for capability, test in self._tests.items():
            score = test.run(model)
            scores.append(score)

            if model.model_id not in self._results:
                self._results[model.model_id] = []
            self._results[model.model_id].append(score)

        return tuple(scores)

    def get_results(self, model_id: str) -> tuple[CapabilityScore, ...]:
        """Get all assessment results for a model.

        Args:
            model_id: The model identifier.

        Returns:
            Tuple of CapabilityScore from previous assessments.
        """
        return tuple(self._results.get(model_id, []))

    def clear_results(self, model_id: str | None = None) -> None:
        """Clear assessment results.

        Args:
            model_id: If provided, clear results for this model only.
                      If None, clear all results.
        """
        if model_id is None:
            self._results.clear()
        elif model_id in self._results:
            del self._results[model_id]
