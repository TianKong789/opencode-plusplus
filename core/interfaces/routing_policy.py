"""Contracts for selecting models from capability profiles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.ids import ModelId
from core.models import ModelCapabilityProfile


@dataclass(slots=True, frozen=True)
class RoutingContext:
    """Input candidates and constraints for a routing decision."""

    profiles: tuple[ModelCapabilityProfile, ...]
    task_description: str
    required_capabilities: tuple[str, ...] = ()
    max_latency_ms: float = float("inf")
    max_cost: float = float("inf")


class RoutingPolicy(ABC):
    """Selects and scores models for a routing context."""

    @abstractmethod
    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the best eligible model, if any."""

    @abstractmethod
    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score a model profile for a routing context."""

    def _filter_candidates(
        self,
        context: RoutingContext,
    ) -> tuple[ModelCapabilityProfile, ...]:
        """Return profiles that satisfy hard latency and cost constraints."""
        return tuple(
            profile
            for profile in context.profiles
            if profile.average_latency_ms <= context.max_latency_ms
            and profile.estimated_cost <= context.max_cost
        )
