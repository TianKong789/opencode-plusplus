"""Contracts for selecting models from capability profiles."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.ids import ModelId
from core.models import ModelCapabilityProfile
from core.models.routing import RoutingContext


@runtime_checkable
class RoutingPolicy(Protocol):
    """Selects and scores models for a routing context."""

    def select(self, context: RoutingContext) -> ModelId | None:
        """Select the best eligible model, if any."""

    def score(self, profile: ModelCapabilityProfile, context: RoutingContext) -> float:
        """Score a model profile for a routing context."""
