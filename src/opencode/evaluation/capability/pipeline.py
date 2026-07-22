from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from core.ids import ModelId
from core.models import Capability, CapabilityScore, ModelCapabilityProfile
from src.opencode.evaluation.capability.assessor import CapabilityAssessor
from src.opencode.evaluation.capability.profiler import Profiler
from src.opencode.evaluation.capability.registry import ModelRegistry
from src.opencode.evaluation.capability.test_runner import (
    TaskDefinition,
    TestRunner,
    TestSuiteResult,
)

LoadedSuites = tuple[tuple[Capability, tuple[TaskDefinition, ...]], ...]
ExecutionResults = tuple[tuple[Capability, TestSuiteResult], ...]


@dataclass
class AssessmentPipeline:
    registry: ModelRegistry = field(default_factory=ModelRegistry)
    assessor: CapabilityAssessor = field(default_factory=CapabilityAssessor)
    profiler: Profiler = field(default_factory=Profiler)
    test_runner: TestRunner = field(default_factory=TestRunner)
    benchmark_dir: Path = field(default_factory=lambda: Path("benchmarks/capabilities"))
    quality_threshold: float = 0.7

    def register_model(
        self,
        model_id: str,
        name: str,
        provider: str,
        capabilities: tuple[str, ...] = (),
    ) -> None:
        self.registry.register(ModelId(model_id), name, provider, capabilities)

    def assess_model(
        self,
        model_id: str,
        executor: Callable[[str, str], str],
        capabilities: tuple[Capability, ...] = (),
    ) -> ModelCapabilityProfile:
        selected_capabilities = capabilities or tuple(Capability)
        loaded_suites = self.load(selected_capabilities)
        execution_results = self.execute(model_id, loaded_suites, executor)
        capability_scores = self.score(model_id, execution_results)
        qualified_scores = self.filter(capability_scores)
        return self.rank(model_id, qualified_scores)

    def load(self, capabilities: tuple[Capability, ...]) -> LoadedSuites:
        return tuple(
            (capability, self.test_runner.load_tasks(capability.value))
            for capability in capabilities
        )

    def execute(
        self,
        model_id: str,
        loaded_suites: LoadedSuites,
        executor: Callable[[str, str], str],
    ) -> ExecutionResults:
        return tuple(
            (
                capability,
                self.test_runner.run_suite(
                    capability.value,
                    lambda task_input: executor(model_id, task_input),
                    tasks,
                ),
            )
            for capability, tasks in loaded_suites
        )

    def score(
        self, model_id: str, execution_results: ExecutionResults
    ) -> tuple[CapabilityScore, ...]:
        scoring_profiler = Profiler()
        scores: list[CapabilityScore] = []
        for capability, result in execution_results:
            normalized_score = result.average_score * 10.0
            scoring_profiler.record_result(model_id, capability, normalized_score)
            scores.append(CapabilityScore(capability=capability, score=normalized_score))
        return tuple(scores)

    def filter(
        self, scores: tuple[CapabilityScore, ...]
    ) -> tuple[CapabilityScore, ...]:
        return tuple(
            score
            for score in scores
            if score.score / 10.0 >= self.quality_threshold
        )

    def rank(
        self, model_id: str, scores: tuple[CapabilityScore, ...]
    ) -> ModelCapabilityProfile:
        model_info = self.registry.get(ModelId(model_id))
        if model_info is None:
            raise ValueError(f"Model {model_id} not registered")

        for score in sorted(scores, key=lambda value: value.score, reverse=True):
            self.profiler.record_result(
                model_id,
                score.capability,
                score.score,
                score.confidence,
                score.evidence,
            )
        return self.profiler.build_profile(
            model_id=model_id,
            provider=model_info["provider"] or "",
            model_name=model_info["name"] or "",
            version="1.0",
            context_window=128000,
            max_output_tokens=8192,
        )

    def get_model_profile(self, model_id: str) -> ModelCapabilityProfile | None:
        if not self.profiler.get_all_scores(model_id):
            return None
        model_info = self.registry.get(ModelId(model_id))
        return self.profiler.build_profile(
            model_id=model_id,
            provider=(model_info["provider"] if model_info else "unknown"),
            model_name=(model_info["name"] if model_info else model_id),
            version="1.0",
            context_window=128000,
            max_output_tokens=8192,
        )

    def list_assessed_models(self) -> tuple[str, ...]:
        return tuple(str(model_id) for model_id in self.registry.list_models())
