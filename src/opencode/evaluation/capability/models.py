"""Domain models for model capability profiling.

Defines the data structures used to describe and compare LLM capabilities
across different dimensions (performance, cost, task suitability).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.opencode.evaluation.capability.capabilities import Capability


@dataclass(frozen=True)
class Model:
    """Minimal model representation for capability assessment.

    Attributes:
        model_id: Unique model identifier.
        provider: The model provider.
        api_endpoint: Optional API endpoint for inference.
    """

    model_id: str
    provider: str
    api_endpoint: str = ""


@dataclass(slots=True, frozen=True)
class CapabilityScore:
    """A scored capability with evidence.

    Attributes:
        capability: The capability being scored.
        score: Score from 0.0 (no capability) to 10.0 (expert).
        confidence: Confidence in the score (0.0 to 1.0).
        evidence: Supporting evidence for the score.
    """

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
    """Immutable profile capturing a model's capabilities and performance characteristics.

    Used by CapabilityAssessor and ModelRouter to select the optimal model
    for a given task based on capability scores and operational metrics.

    All numeric fields are validated at construction time. Capability scores
    use the CapabilityScore collection for extensibility.

    Attributes:
        model_id: Unique identifier for the model (e.g. "claude-sonnet-4-20250514").
        provider: The provider or vendor (e.g. "anthropic", "openai").
        model_name: Human-readable model name.
        version: Model version string (e.g. "2024-02-15").
        context_window: Maximum context window size in tokens.
        max_output_tokens: Maximum output tokens per request.
        supports_tools: Whether the model supports tool use.
        supports_function_calling: Whether the model supports function calling.
        supports_images: Whether the model supports image inputs.
        supports_reasoning: Whether the model supports chain-of-thought reasoning.
        supported_languages: Programming languages the model handles well.
        supported_domains: Problem domains the model excels at.
        average_latency_ms: Average response latency in milliseconds.
        tokens_per_second: Average token generation speed.
        estimated_cost: Estimated cost per 1K input tokens (USD).
        reliability: Reliability score (0.0 to 1.0).
        capability_scores: Collection of scored capabilities.
        overall_score: Weighted aggregate capability score (0.0 to 10.0).
        metadata: Arbitrary key-value metadata for extensibility.
    """

    model_id: str
    """Unique identifier for the model."""

    provider: str
    """The provider or vendor."""

    model_name: str
    """Human-readable model name."""

    version: str
    """Model version string."""

    context_window: int
    """Maximum context window size in tokens."""

    max_output_tokens: int
    """Maximum output tokens per request."""

    supports_tools: bool = False
    """Whether the model supports tool use."""

    supports_function_calling: bool = False
    """Whether the model supports function calling."""

    supports_images: bool = False
    """Whether the model supports image inputs."""

    supports_reasoning: bool = False
    """Whether the model supports chain-of-thought reasoning."""

    supported_languages: tuple[str, ...] = ()
    """Programming languages the model handles well."""

    supported_domains: tuple[str, ...] = ()
    """Problem domains the model excels at."""

    average_latency_ms: float = 0.0
    """Average response latency in milliseconds."""

    tokens_per_second: float = 0.0
    """Average token generation speed."""

    estimated_cost: float = 0.0
    """Estimated cost per 1K input tokens (USD)."""

    reliability: float = 0.0
    """Reliability score (0.0 to 1.0)."""

    # ── capability scores (extensible collection) ─────────────────────

    capability_scores: tuple[CapabilityScore, ...] = ()
    """Collection of scored capabilities."""

    overall_score: float = 0.0
    """Weighted aggregate capability score (0.0 to 10.0)."""

    metadata: tuple[tuple[str, str], ...] = ()
    """Arbitrary key-value metadata for extensibility."""

    def __post_init__(self) -> None:
        """Validate all field values."""
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

        # Validate no duplicate capabilities
        seen = set()
        for cs in self.capability_scores:
            if cs.capability in seen:
                raise ValueError(f"Duplicate capability: {cs.capability}")
            seen.add(cs.capability)

    # ── query helpers ───────────────────────────────────────────────

    def get_capability_score(self, capability: Capability) -> CapabilityScore | None:
        """Get the score for a specific capability.

        Args:
            capability: The capability to look up.

        Returns:
            The CapabilityScore if present, None otherwise.
        """
        for cs in self.capability_scores:
            if cs.capability == capability:
                return cs
        return None

    def has_capability(self, capability: Capability) -> bool:
        """Check if the model has a specific capability.

        Args:
            capability: The capability to check.

        Returns:
            True if the model has this capability with score > 0.
        """
        cs = self.get_capability_score(capability)
        return cs is not None and cs.score > 0.0

    def capability_score(self, capability: Capability) -> float:
        """Get the score for a capability, defaulting to 0.0.

        Args:
            capability: The capability to look up.

        Returns:
            The score, or 0.0 if not present.
        """
        cs = self.get_capability_score(capability)
        return cs.score if cs is not None else 0.0

    def top_capabilities(self, n: int = 5) -> tuple[CapabilityScore, ...]:
        """Get the top N capabilities by score.

        Args:
            n: Number of top capabilities to return.

        Returns:
            Tuple of CapabilityScore sorted by score descending.
        """
        sorted_scores = sorted(self.capability_scores, key=lambda cs: cs.score, reverse=True)
        return tuple(sorted_scores[:n])

    def get_metadata(self, key: str, default: str = "") -> str:
        """Retrieve a metadata value by key.

        Args:
            key: The metadata key to look up.
            default: Value to return if key is not found.

        Returns:
            The metadata value, or ``default`` if not present.
        """
        for k, v in self.metadata:
            if k == key:
                return v
        return default

    def supports_language(self, language: str) -> bool:
        """Check if the model supports a specific programming language.

        Args:
            language: The language to check (e.g. "python", "sql").

        Returns:
            True if the model lists this language in supported_languages.
        """
        return language.lower() in self.supported_languages
