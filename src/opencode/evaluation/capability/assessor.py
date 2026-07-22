"""Capability assessor implementation.

Discovers and runs CapabilityTest instances to evaluate model capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.capability_test import (
    CapabilityTest,
    Model,
    get_all_tests,
)
from src.opencode.evaluation.capability.models import CapabilityScore


@dataclass
class CapabilityAssessor:
    """Assesses model capabilities by running registered tests.

    Discovers CapabilityTest implementations and executes them
    against models to produce CapabilityScore results.
    """

    _tests: dict[Capability, CapabilityTest] = field(default_factory=dict)
    _results: dict[str, list[CapabilityScore]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self._tests:
            for test in get_all_tests():
                self._tests[test.capability()] = test

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
