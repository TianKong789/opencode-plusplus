"""Shared domain models for model capability profiling."""

from __future__ import annotations

from dataclasses import dataclass

from core.models.capability import Capability


@dataclass(slots=True, frozen=True)
class Model:
    """Minimal model representation for capability assessment."""

    model_id: str
    provider: str
    api_endpoint: str = ""


@dataclass(slots=True, frozen=True)
class CapabilityScore:
    """A scored capability with evidence."""

    capability: Capability
    score: float
    confidence: float = 1.0
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 10.0:
            raise ValueError(f"score must be 0.0-10.0, got {self.score}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {self.confidence}")


@dataclass(slots=True, frozen=True)
class ModelCapabilityProfile:
    """Immutable profile of a model's capabilities and performance."""

    model_id: str
    provider: str
    model_name: str
    version: str
    context_window: int
    max_output_tokens: int
    supports_tools: bool = False
    supports_function_calling: bool = False
    supports_images: bool = False
    supports_reasoning: bool = False
    supported_languages: tuple[str, ...] = ()
    supported_domains: tuple[str, ...] = ()
    average_latency_ms: float = 0.0
    tokens_per_second: float = 0.0
    estimated_cost: float = 0.0
    reliability: float = 0.0
    capability_scores: tuple[CapabilityScore, ...] = ()
    overall_score: float = 0.0
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.model_id:
            raise ValueError("model_id must not be empty")
        if not self.provider:
            raise ValueError("provider must not be empty")
        if not self.model_name:
            raise ValueError("model_name must not be empty")
        if not self.version:
            raise ValueError("version must not be empty")
        if self.context_window <= 0:
            raise ValueError("context_window must be positive")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        if self.average_latency_ms < 0:
            raise ValueError("average_latency_ms must not be negative")
        if self.tokens_per_second < 0:
            raise ValueError("tokens_per_second must not be negative")
        if self.estimated_cost < 0:
            raise ValueError("estimated_cost must not be negative")
        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError(f"reliability must be 0.0-1.0, got {self.reliability}")
        if not 0.0 <= self.overall_score <= 10.0:
            raise ValueError(f"overall_score must be 0.0-10.0, got {self.overall_score}")

        seen: set[Capability] = set()
        for capability_score in self.capability_scores:
            if capability_score.capability in seen:
                raise ValueError(f"Duplicate capability: {capability_score.capability}")
            seen.add(capability_score.capability)

    def get_capability_score(self, capability: Capability) -> CapabilityScore | None:
        """Get the score for a specific capability."""
        for capability_score in self.capability_scores:
            if capability_score.capability == capability:
                return capability_score
        return None

    def has_capability(self, capability: Capability) -> bool:
        """Check whether the model has a positive score for a capability."""
        capability_score = self.get_capability_score(capability)
        return capability_score is not None and capability_score.score > 0.0

    def capability_score(self, capability: Capability) -> float:
        """Get the score for a capability, defaulting to zero."""
        capability_score = self.get_capability_score(capability)
        return capability_score.score if capability_score is not None else 0.0

    def top_capabilities(self, n: int = 5) -> tuple[CapabilityScore, ...]:
        """Get the top N capabilities by score."""
        sorted_scores = sorted(
            self.capability_scores,
            key=lambda capability_score: capability_score.score,
            reverse=True,
        )
        return tuple(sorted_scores[:n])

    def get_metadata(self, key: str, default: str = "") -> str:
        """Retrieve a metadata value by key."""
        for metadata_key, value in self.metadata:
            if metadata_key == key:
                return value
        return default

    def supports_language(self, language: str) -> bool:
        """Check if the model supports a programming language."""
        return language.lower() in self.supported_languages
