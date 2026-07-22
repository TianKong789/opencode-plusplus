"""Routing policies for model selection.

Defines different strategies for selecting the optimal model
based on various optimization criteria.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.ids import ModelId
from core.models import ModelCapabilityProfile


@dataclass(slots=True, frozen=True)
class RoutingContext:
    """Context for routing decisions.

    Attributes:
        profiles: Available model profiles.
        task_description: Description of the task.
        required_capabilities: Capabilities needed for the task.
        max_latency_ms: Maximum acceptable latency.
        max_cost: Maximum acceptable cost per 1K tokens.
    """

    profiles: tuple[ModelCapabilityProfile, ...]
    task_description: str
    required_capabilities: tuple[str, ...] = ()
    max_latency_ms: float = float("inf")
    max_cost: float = float("inf")


class RoutingPolicy(ABC):
    """Base class for routing policies.

    Implementations define different strategies for selecting
    the optimal model from a set of candidates.
    """

    @abstractmethod
    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the best model based on policy criteria.

        Args:
            context: The routing context with candidates and constraints.

        Returns:
            The selected model ID, or None if no model meets criteria.
        """

    @abstractmethod
    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score a model profile for the given context.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            A score where higher is better.
        """

    def _filter_candidates(
        self,
        context: RoutingContext,
    ) -> tuple[ModelCapabilityProfile, ...]:
        """Filter candidates by hard constraints.

        Args:
            context: The routing context.

        Returns:
            Tuple of profiles that meet all constraints.
        """
        return tuple(
            p
            for p in context.profiles
            if p.average_latency_ms <= context.max_latency_ms
            and p.estimated_cost <= context.max_cost
        )


class LatencyPolicy(RoutingPolicy):
    """Selects the model with lowest latency.

    Optimizes for speed over quality or cost. Best for
    real-time applications where response time is critical.
    """

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the fastest model.

        Args:
            context: The routing context.

        Returns:
            The model ID with lowest latency, or None.
        """
        candidates = self._filter_candidates(context)
        if not candidates:
            return None

        best = min(candidates, key=lambda p: p.average_latency_ms)
        return ModelId(best.model_id)

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score based on inverse latency.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            Score where lower latency = higher score.
        """
        if profile.average_latency_ms <= 0:
            return 1.0
        return min(1.0, 1000.0 / profile.average_latency_ms)


class QualityPolicy(RoutingPolicy):
    """Selects the model with highest overall quality score.

    Optimizes for output quality regardless of cost or latency.
    Best for critical tasks where correctness is paramount.
    """

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the highest quality model.

        Args:
            context: The routing context.

        Returns:
            The model ID with highest quality, or None.
        """
        candidates = self._filter_candidates(context)
        if not candidates:
            return None

        best = max(candidates, key=lambda p: p.overall_score)
        return ModelId(best.model_id)

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score based on overall quality.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            Score based on overall_score field.
        """
        return profile.overall_score


class LocalOnlyPolicy(RoutingPolicy):
    """Routes only to local models.

    Filters out cloud-based models for privacy or air-gapped
    environments. Identifies local models by provider or metadata.
    """

    LOCAL_PROVIDERS: frozenset[str] = frozenset({"ollama", "lmstudio", "llama.cpp", "local"})

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select a local model.

        Args:
            context: The routing context.

        Returns:
            A local model ID, or None if no local models available.
        """
        local_profiles = tuple(
            p for p in context.profiles if p.provider.lower() in self.LOCAL_PROVIDERS
        )
        if not local_profiles:
            return None

        best = max(local_profiles, key=lambda p: p.overall_score)
        return ModelId(best.model_id)

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score based on local availability and quality.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            Score where local models get quality score, cloud get 0.
        """
        if profile.provider.lower() not in self.LOCAL_PROVIDERS:
            return 0.0
        return profile.overall_score


class CloudPreferredPolicy(RoutingPolicy):
    """Prefers cloud models but falls back to local.

    Optimizes for quality by preferring cloud providers,
    but can use local models if cloud is unavailable or
    constrained.
    """

    CLOUD_PENALTY: float = 0.1

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select best model, preferring cloud.

        Args:
            context: The routing context.

        Returns:
            The best model ID, preferring cloud providers.
        """
        candidates = self._filter_candidates(context)
        if not candidates:
            return None

        scored = [(p, self.score(p, context)) for p in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)

        return ModelId(scored[0][0].model_id)

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score with cloud preference bonus.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            Score where cloud models get a small bonus.
        """
        base_score = profile.overall_score
        if profile.provider.lower() in LocalOnlyPolicy.LOCAL_PROVIDERS:
            return base_score * (1 - self.CLOUD_PENALTY)
        return base_score


class CostOptimizedPolicy(RoutingPolicy):
    """Selects the most cost-effective model.

    Optimizes for cost while maintaining minimum quality.
    Balances cost savings against output quality.
    """

    MIN_QUALITY: float = 5.0  # Minimum acceptable quality (0.0-10.0 scale)

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the cheapest model meeting quality threshold.

        Args:
            context: The routing context.

        Returns:
            The most cost-effective model ID, or None.
        """
        candidates = self._filter_candidates(context)
        if not candidates:
            return None

        quality_candidates = tuple(
            p for p in candidates if p.overall_score >= self.MIN_QUALITY
        )
        if not quality_candidates:
            return None

        best = min(quality_candidates, key=lambda p: p.estimated_cost)
        return ModelId(best.model_id)

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score based on cost-effectiveness.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            Score based on quality-to-cost ratio.
        """
        if profile.estimated_cost <= 0:
            return profile.overall_score
        return profile.overall_score / (profile.estimated_cost + 0.001)


class BalancedPolicy(RoutingPolicy):
    """Balances quality, cost, and latency.

    Uses weighted scoring to balance multiple objectives.
    Default weights favor quality but consider cost and speed.
    """

    QUALITY_WEIGHT: float = 0.5
    COST_WEIGHT: float = 0.3
    LATENCY_WEIGHT: float = 0.2

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the best balanced model.

        Args:
            context: The routing context.

        Returns:
            The most balanced model ID, or None.
        """
        candidates = self._filter_candidates(context)
        if not candidates:
            return None

        scored = [(p, self.score(p, context)) for p in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)

        return ModelId(scored[0][0].model_id)

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Compute weighted score across all dimensions.

        Args:
            profile: The model profile to score.
            context: The routing context.

        Returns:
            Weighted score combining quality, cost, and latency.
        """
        # Normalize quality to 0-1 (max score is 10.0)
        quality_normalized = profile.overall_score / 10.0
        # Normalize cost: lower is better, max 0.01
        cost_score = max(0.0, 1.0 - (profile.estimated_cost / 0.01))
        # Normalize latency: lower is better, max 1000ms
        latency_score = max(0.0, 1.0 - (profile.average_latency_ms / 1000.0))

        return (
            self.QUALITY_WEIGHT * quality_normalized
            + self.COST_WEIGHT * cost_score
            + self.LATENCY_WEIGHT * latency_score
        )
