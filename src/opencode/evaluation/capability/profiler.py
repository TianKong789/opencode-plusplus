"""Capability profiler.

Builds ModelCapabilityProfile instances by running test suites
and aggregating scores across capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.models import CapabilityScore, ModelCapabilityProfile


@dataclass
class Profiler:
    """Builds capability profiles from test results.

    Aggregates scores from multiple capability assessments into
    a single ModelCapabilityProfile.
    """

    _test_results: dict[str, dict[Capability, tuple[float, float, tuple[str, ...]]]] = (
        field(default_factory=dict)
    )

    def record_result(
        self,
        model_id: str,
        capability: Capability,
        score: float,
        confidence: float = 1.0,
        evidence: tuple[str, ...] = (),
    ) -> None:
        """Record a test result for a model and capability.

        Args:
            model_id: The model identifier.
            capability: The capability that was tested.
            score: The score (0.0 to 10.0).
            confidence: Confidence in the score (0.0 to 1.0).
            evidence: Supporting evidence for the score.
        """
        if not 0.0 <= score <= 10.0:
            raise ValueError(f"score must be 0.0-10.0, got {score}")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {confidence}")

        if model_id not in self._test_results:
            self._test_results[model_id] = {}
        self._test_results[model_id][capability] = (score, confidence, evidence)

    def get_score(self, model_id: str, capability: Capability) -> float | None:
        """Get the score for a specific model and capability.

        Args:
            model_id: The model identifier.
            capability: The capability to check.

        Returns:
            The score if available, None otherwise.
        """
        result = self._test_results.get(model_id, {}).get(capability)
        return result[0] if result else None

    def get_all_scores(self, model_id: str) -> dict[Capability, float]:
        """Get all capability scores for a model.

        Args:
            model_id: The model identifier.

        Returns:
            A dictionary of capability scores.
        """
        results = self._test_results.get(model_id, {})
        return {cap: data[0] for cap, data in results.items()}

    def build_profile(
        self,
        model_id: str,
        provider: str,
        model_name: str,
        version: str,
        context_window: int,
        max_output_tokens: int,
        **kwargs: object,
    ) -> ModelCapabilityProfile:
        """Build a ModelCapabilityProfile from recorded test results.

        Args:
            model_id: The model identifier.
            provider: The provider name.
            model_name: Human-readable model name.
            version: Model version.
            context_window: Context window size.
            max_output_tokens: Max output tokens.
            **kwargs: Additional fields for the profile.

        Returns:
            A populated ModelCapabilityProfile.
        """
        scores = self._test_results.get(model_id, {})

        # Build CapabilityScore objects
        capability_scores = []
        for cap, (score, confidence, evidence) in scores.items():
            capability_scores.append(
                CapabilityScore(
                    capability=cap,
                    score=score,
                    confidence=confidence,
                    evidence=evidence,
                )
            )

        # Calculate overall score as average of all capability scores
        if capability_scores:
            overall_score = sum(cs.score for cs in capability_scores) / len(
                capability_scores
            )
        else:
            overall_score = 0.0

        # Extract known fields from kwargs
        known_fields = {
            "supports_tools",
            "supports_function_calling",
            "supports_images",
            "supports_reasoning",
            "supported_languages",
            "supported_domains",
            "average_latency_ms",
            "tokens_per_second",
            "estimated_cost",
            "reliability",
            "metadata",
        }
        profile_kwargs = {k: v for k, v in kwargs.items() if k in known_fields}

        return ModelCapabilityProfile(
            model_id=model_id,
            provider=provider,
            model_name=model_name,
            version=version,
            context_window=context_window,
            max_output_tokens=max_output_tokens,
            capability_scores=tuple(capability_scores),
            overall_score=overall_score,
            **profile_kwargs,
        )
