"""Routing domain models."""

from __future__ import annotations

from dataclasses import dataclass

from core.models import ModelCapabilityProfile


@dataclass(slots=True, frozen=True)
class RoutingContext:
    """Input candidates and constraints for a routing decision."""

    profiles: tuple[ModelCapabilityProfile, ...]
    task_description: str
    required_capabilities: tuple[str, ...] = ()
    max_latency_ms: float = float("inf")
    max_cost: float = float("inf")


def filter_candidates(
    context: RoutingContext,
) -> tuple[ModelCapabilityProfile, ...]:
    """Return profiles that satisfy hard latency and cost constraints."""
    return tuple(
        profile
        for profile in context.profiles
        if profile.average_latency_ms <= context.max_latency_ms
        and profile.estimated_cost <= context.max_cost
    )
