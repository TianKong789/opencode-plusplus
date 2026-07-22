"""Assessment Pipeline.

Orchestrates the full capability assessment flow:

    Model → Capability Assessor → Capability Test Suites → Scoring → Capability Profile → Registry

This module provides the main entry point for assessing models
and building capability profiles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from core.ids import ModelId

from src.opencode.evaluation.capability.assessor import CapabilityAssessor
from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.models import ModelCapabilityProfile
from src.opencode.evaluation.capability.profiler import Profiler
from src.opencode.evaluation.capability.registry import ModelRegistry
from src.opencode.evaluation.capability.test_runner import TestRunner


@dataclass
class AssessmentPipeline:
    """End-to-end capability assessment pipeline.

    Orchestrates:
    1. Model registration
    2. Test suite execution
    3. Score aggregation
    4. Profile generation
    5. Registry update

    Note: Routing is a separate concern — compose ModelRouter externally.

    Attributes:
        registry: Model metadata registry.
        assessor: Capability assessment engine.
        profiler: Profile builder.
        test_runner: Test suite executor.
        benchmark_dir: Path to benchmark suites.
    """

    registry: ModelRegistry = field(default_factory=ModelRegistry)
    assessor: CapabilityAssessor = field(default_factory=CapabilityAssessor)
    profiler: Profiler = field(default_factory=Profiler)
    test_runner: TestRunner = field(default_factory=TestRunner)
    benchmark_dir: Path = field(default_factory=lambda: Path("benchmarks/capabilities"))

    def register_model(
        self,
        model_id: str,
        name: str,
        provider: str,
        capabilities: tuple[str, ...] = (),
    ) -> None:
        """Register a model for assessment.

        Args:
            model_id: Unique identifier for the model.
            name: Human-readable model name.
            provider: The provider or vendor.
            capabilities: Initial capability tags.
        """
        self.registry.register(
            model_id=ModelId(model_id),
            name=name,
            provider=provider,
            capabilities=capabilities,
        )

    def assess_model(
        self,
        model_id: str,
        executor: callable,
        capabilities: tuple[Capability, ...] = (),
    ) -> ModelCapabilityProfile:
        """Run full assessment pipeline for a model.

        Args:
            model_id: The model to assess.
            executor: A callable that takes (model_id, task_input) and returns output.
            capabilities: Capabilities to assess (default: all).

        Returns:
            A populated ModelCapabilityProfile.
        """
        if not capabilities:
            capabilities = tuple(Capability)

        for capability in capabilities:
            self._assess_capability(model_id, capability, executor)

        model_info = self.registry.get(ModelId(model_id))
        if model_info is None:
            raise ValueError(f"Model {model_id} not registered")

        profile = self.profiler.build_profile(
            model_id=model_id,
            provider=str(model_info.get("provider", "")),
            model_name=str(model_info.get("name", "")),
            version="1.0",
            context_window=128000,
            max_output_tokens=8192,
        )

        return profile

    def _assess_capability(
        self,
        model_id: str,
        capability: Capability,
        executor: callable,
    ) -> None:
        """Assess a single capability for a model.

        Args:
            model_id: The model to assess.
            capability: The capability to assess.
            executor: A callable that takes (model_id, task_input) and returns output.
        """
        def task_executor(task_input: str) -> str:
            return executor(model_id, task_input)

        result = self.test_runner.run_suite(
            capability=capability.value,
            executor=task_executor,
        )

        self.profiler.record_result(
            model_id=model_id,
            capability=capability,
            score=result.average_score,
        )

    def get_model_profile(self, model_id: str) -> ModelCapabilityProfile | None:
        """Get the capability profile for a model.

        Delegates to the profiler to build a profile from recorded results.
        Returns None if the model has no recorded assessment data.

        Args:
            model_id: The model identifier.

        Returns:
            The profile if available, None otherwise.
        """
        all_scores = self.profiler.get_all_scores(model_id)
        if not all_scores:
            return None

        model_info = self.registry.get(ModelId(model_id))
        provider = str(model_info.get("provider", "")) if model_info else "unknown"
        model_name = str(model_info.get("name", model_id)) if model_info else model_id

        return self.profiler.build_profile(
            model_id=model_id,
            provider=provider,
            model_name=model_name,
            version="1.0",
            context_window=128000,
            max_output_tokens=8192,
        )

    def list_assessed_models(self) -> tuple[str, ...]:
        """List all models that have been assessed.

        Returns:
            A tuple of assessed model IDs.
        """
        return tuple(
            str(model_id) for model_id in self.registry.list_models()
        )
