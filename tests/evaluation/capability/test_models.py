from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.models import CapabilityScore, ModelCapabilityProfile


def _make_profile() -> ModelCapabilityProfile:
    return ModelCapabilityProfile(
        model_id="test-model",
        provider="test-provider",
        model_name="Test Model",
        version="1.0",
        context_window=8_192,
        max_output_tokens=1_024,
    )


class TestCapabilityScore:
    def test_constructs_with_all_fields(self) -> None:
        score = CapabilityScore(
            capability=Capability.PYTHON,
            score=9.5,
            confidence=0.8,
            evidence=("benchmark", "code review"),
        )

        assert score == CapabilityScore(
            capability=Capability.PYTHON,
            score=9.5,
            confidence=0.8,
            evidence=("benchmark", "code review"),
        )

    def test_defaults_confidence_and_evidence(self) -> None:
        score = CapabilityScore(capability=Capability.SQL, score=7.0)

        assert (score.confidence, score.evidence) == (1.0, ())

    @pytest.mark.parametrize("value", (0.0, 10.0))
    def test_accepts_score_boundaries(self, value: float) -> None:
        score = CapabilityScore(capability=Capability.DEBUGGING, score=value)

        assert score.score == value

    @pytest.mark.parametrize("value", (-0.1, 10.1))
    def test_rejects_score_outside_valid_range(self, value: float) -> None:
        with pytest.raises(ValueError, match="score must be 0.0-10.0"):
            CapabilityScore(capability=Capability.DEBUGGING, score=value)

    @pytest.mark.parametrize("value", (-0.1, 1.1))
    def test_rejects_confidence_outside_valid_range(self, value: float) -> None:
        with pytest.raises(ValueError, match="confidence must be 0.0-1.0"):
            CapabilityScore(capability=Capability.DEBUGGING, score=5.0, confidence=value)

    def test_rejects_attribute_assignment(self) -> None:
        score = CapabilityScore(capability=Capability.PYTHON, score=8.0)

        with pytest.raises(FrozenInstanceError):
            score.score = 9.0

    def test_has_no_dict_for_attribute_assignment(self) -> None:
        score = CapabilityScore(capability=Capability.PYTHON, score=8.0)

        with pytest.raises(AttributeError):
            score.__dict__["score"] = 9.0


class TestModelCapabilityProfileConstruction:
    def test_constructs_with_required_fields_and_defaults(self) -> None:
        profile = _make_profile()

        assert (
            profile.supports_tools,
            profile.supports_function_calling,
            profile.supports_images,
            profile.supports_reasoning,
            profile.supported_languages,
            profile.supported_domains,
            profile.average_latency_ms,
            profile.tokens_per_second,
            profile.estimated_cost,
            profile.reliability,
            profile.capability_scores,
            profile.overall_score,
            profile.metadata,
        ) == (False, False, False, False, (), (), 0.0, 0.0, 0.0, 0.0, (), 0.0, ())

    def test_constructs_with_all_fields(self) -> None:
        scores = (
            CapabilityScore(Capability.PYTHON, 9.0, 0.9, ("suite",)),
            CapabilityScore(Capability.TOOL_USE, 8.5, 0.8, ("evaluation",)),
        )
        profile = ModelCapabilityProfile(
            model_id="provider/model",
            provider="provider",
            model_name="Model",
            version="2026-01-01",
            context_window=200_000,
            max_output_tokens=16_384,
            supports_tools=True,
            supports_function_calling=True,
            supports_images=True,
            supports_reasoning=True,
            supported_languages=("python", "sql"),
            supported_domains=("engineering", "analysis"),
            average_latency_ms=125.5,
            tokens_per_second=80.0,
            estimated_cost=0.003,
            reliability=0.99,
            capability_scores=scores,
            overall_score=8.75,
            metadata=(("region", "us-east"),),
        )

        assert (
            profile.model_id,
            profile.provider,
            profile.model_name,
            profile.version,
            profile.context_window,
            profile.max_output_tokens,
            profile.supports_tools,
            profile.supports_function_calling,
            profile.supports_images,
            profile.supports_reasoning,
            profile.supported_languages,
            profile.supported_domains,
            profile.average_latency_ms,
            profile.tokens_per_second,
            profile.estimated_cost,
            profile.reliability,
            profile.capability_scores,
            profile.overall_score,
            profile.metadata,
        ) == (
            "provider/model",
            "provider",
            "Model",
            "2026-01-01",
            200_000,
            16_384,
            True,
            True,
            True,
            True,
            ("python", "sql"),
            ("engineering", "analysis"),
            125.5,
            80.0,
            0.003,
            0.99,
            scores,
            8.75,
            (("region", "us-east"),),
        )

    @pytest.mark.parametrize("field_name", ("model_id", "provider", "model_name", "version"))
    def test_rejects_empty_required_text_fields(self, field_name: str) -> None:
        with pytest.raises(ValueError, match=f"{field_name} must not be empty"):
            replace(_make_profile(), **{field_name: ""})

    @pytest.mark.parametrize(
        ("field_name", "value", "message"),
        (
            ("context_window", 0, "context_window must be positive"),
            ("max_output_tokens", 0, "max_output_tokens must be positive"),
            ("average_latency_ms", -0.1, "average_latency_ms must not be negative"),
            ("tokens_per_second", -0.1, "tokens_per_second must not be negative"),
            ("estimated_cost", -0.1, "estimated_cost must not be negative"),
        ),
    )
    def test_rejects_invalid_operational_metrics(
        self, field_name: str, value: int | float, message: str
    ) -> None:
        with pytest.raises(ValueError, match=message):
            replace(_make_profile(), **{field_name: value})

    @pytest.mark.parametrize("value", (-0.1, 1.1))
    def test_rejects_reliability_outside_valid_range(self, value: float) -> None:
        with pytest.raises(ValueError, match="reliability must be 0.0-1.0"):
            replace(_make_profile(), reliability=value)

    @pytest.mark.parametrize("value", (-0.1, 10.1))
    def test_rejects_overall_score_outside_valid_range(self, value: float) -> None:
        with pytest.raises(ValueError, match="overall_score must be 0.0-10.0"):
            replace(_make_profile(), overall_score=value)

    def test_rejects_duplicate_capability_scores(self) -> None:
        scores = (
            CapabilityScore(Capability.PYTHON, 7.0),
            CapabilityScore(Capability.PYTHON, 8.0),
        )

        with pytest.raises(ValueError, match="Duplicate capability"):
            replace(_make_profile(), capability_scores=scores)


class TestModelCapabilityProfileQueries:
    def test_get_capability_score_returns_matching_score(self) -> None:
        score = CapabilityScore(Capability.PYTHON, 9.0)
        profile = replace(_make_profile(), capability_scores=(score,))

        assert profile.get_capability_score(Capability.PYTHON) is score

    def test_get_capability_score_returns_none_when_absent(self) -> None:
        profile = _make_profile()

        assert profile.get_capability_score(Capability.PYTHON) is None

    @pytest.mark.parametrize(
        ("capability", "expected"),
        (
            (Capability.PYTHON, True),
            (Capability.SQL, False),
            (Capability.DEBUGGING, False),
        ),
    )
    def test_has_capability_returns_expected_presence(
        self, capability: Capability, expected: bool
    ) -> None:
        profile = replace(
            _make_profile(),
            capability_scores=(
                CapabilityScore(Capability.PYTHON, 4.0),
                CapabilityScore(Capability.SQL, 0.0),
            ),
        )

        assert profile.has_capability(capability) is expected

    @pytest.mark.parametrize(
        ("capability", "expected"),
        ((Capability.PYTHON, 4.0), (Capability.DEBUGGING, 0.0)),
    )
    def test_capability_score_returns_score_or_zero(
        self, capability: Capability, expected: float
    ) -> None:
        profile = replace(
            _make_profile(), capability_scores=(CapabilityScore(Capability.PYTHON, 4.0),)
        )

        assert profile.capability_score(capability) == expected

    def test_top_capabilities_returns_highest_scores_in_descending_order(self) -> None:
        profile = replace(
            _make_profile(),
            capability_scores=(
                CapabilityScore(Capability.PYTHON, 7.0),
                CapabilityScore(Capability.SQL, 9.0),
                CapabilityScore(Capability.DEBUGGING, 8.0),
            ),
        )

        assert profile.top_capabilities(2) == (
            CapabilityScore(Capability.SQL, 9.0),
            CapabilityScore(Capability.DEBUGGING, 8.0),
        )

    def test_top_capabilities_returns_all_scores_when_n_exceeds_count(self) -> None:
        scores = (CapabilityScore(Capability.PYTHON, 7.0),)
        profile = replace(_make_profile(), capability_scores=scores)

        assert profile.top_capabilities(2) == scores

    def test_top_capabilities_defaults_to_five(self) -> None:
        scores = (
            CapabilityScore(Capability.PYTHON, 6.0),
            CapabilityScore(Capability.SQL, 5.0),
            CapabilityScore(Capability.ARCHITECTURE, 4.0),
            CapabilityScore(Capability.CODE_REVIEW, 3.0),
            CapabilityScore(Capability.DEBUGGING, 2.0),
            CapabilityScore(Capability.TESTING, 1.0),
        )
        profile = replace(_make_profile(), capability_scores=scores)

        assert profile.top_capabilities() == scores[:5]

    def test_get_metadata_returns_existing_value(self) -> None:
        profile = replace(_make_profile(), metadata=(("region", "us-east"),))

        assert profile.get_metadata("region") == "us-east"

    def test_get_metadata_returns_supplied_default_when_missing(self) -> None:
        profile = _make_profile()

        assert profile.get_metadata("region", "unknown") == "unknown"

    def test_get_metadata_defaults_to_empty_string_when_missing(self) -> None:
        profile = _make_profile()

        assert profile.get_metadata("region") == ""

    @pytest.mark.parametrize(
        ("language", "expected"), (("PyThOn", True), ("rust", False))
    )
    def test_supports_language_matches_case_insensitively(
        self, language: str, expected: bool
    ) -> None:
        profile = replace(_make_profile(), supported_languages=("python", "sql"))

        assert profile.supports_language(language) is expected

    def test_rejects_attribute_assignment(self) -> None:
        profile = _make_profile()

        with pytest.raises(FrozenInstanceError):
            profile.provider = "different-provider"
