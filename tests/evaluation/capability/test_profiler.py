from __future__ import annotations

import pytest

from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.models import CapabilityScore
from src.opencode.evaluation.capability.profiler import Profiler


class TestProfilerRecordResult:
    def test_stores_score_for_model_and_capability(self) -> None:
        profiler = Profiler()

        profiler.record_result("model-1", Capability.PYTHON, 8.5)

        assert profiler.get_score("model-1", Capability.PYTHON) == 8.5

    def test_overwrites_previous_score_for_same_model_and_capability(self) -> None:
        profiler = Profiler()
        profiler.record_result("model-1", Capability.PYTHON, 6.0)

        profiler.record_result("model-1", Capability.PYTHON, 9.0)

        assert profiler.get_score("model-1", Capability.PYTHON) == 9.0

    @pytest.mark.parametrize("score", (-0.1, 10.1))
    def test_raises_for_score_outside_valid_range(self, score: float) -> None:
        profiler = Profiler()

        with pytest.raises(ValueError, match="score must be 0.0-10.0"):
            profiler.record_result("model-1", Capability.PYTHON, score)

    @pytest.mark.parametrize("confidence", (-0.1, 1.1))
    def test_raises_for_confidence_outside_valid_range(self, confidence: float) -> None:
        profiler = Profiler()

        with pytest.raises(ValueError, match="confidence must be 0.0-1.0"):
            profiler.record_result("model-1", Capability.PYTHON, 8.5, confidence)

    def test_stores_evidence_tuple(self) -> None:
        profiler = Profiler()
        evidence = ("passed benchmark", "reviewed output")

        profiler.record_result("model-1", Capability.PYTHON, 8.5, evidence=evidence)
        profile = profiler.build_profile("model-1", "acme", "Model One", "v1", 128000, 8192)

        assert profile.capability_scores[0].evidence == evidence


class TestProfilerScoreLookup:
    def test_returns_recorded_score(self) -> None:
        profiler = Profiler()
        profiler.record_result("model-1", Capability.SQL, 7.5)

        assert profiler.get_score("model-1", Capability.SQL) == 7.5

    def test_returns_none_for_unknown_model_id(self) -> None:
        profiler = Profiler()

        assert profiler.get_score("unknown-model", Capability.SQL) is None

    def test_returns_none_for_unknown_capability(self) -> None:
        profiler = Profiler()
        profiler.record_result("model-1", Capability.SQL, 7.5)

        assert profiler.get_score("model-1", Capability.PYTHON) is None


class TestProfilerAllScores:
    def test_returns_all_scores_for_model(self) -> None:
        profiler = Profiler()
        profiler.record_result("model-1", Capability.PYTHON, 8.5)
        profiler.record_result("model-1", Capability.SQL, 7.5)

        assert profiler.get_all_scores("model-1") == {
            Capability.PYTHON: 8.5,
            Capability.SQL: 7.5,
        }

    def test_returns_empty_dict_for_unknown_model(self) -> None:
        profiler = Profiler()

        assert profiler.get_all_scores("unknown-model") == {}

    def test_tracks_multiple_capabilities_independently(self) -> None:
        profiler = Profiler()
        profiler.record_result("model-1", Capability.PYTHON, 8.5)
        profiler.record_result("model-1", Capability.DEBUGGING, 9.0)
        profiler.record_result("model-1", Capability.WRITING, 6.5)

        assert profiler.get_all_scores("model-1") == {
            Capability.PYTHON: 8.5,
            Capability.DEBUGGING: 9.0,
            Capability.WRITING: 6.5,
        }


class TestProfilerBuildProfile:
    def test_creates_profile_with_correct_identifying_fields(self) -> None:
        profiler = Profiler()

        profile = profiler.build_profile(
            "model-1", "acme", "Model One", "2026.1", 128000, 8192
        )

        assert profile.model_id == "model-1"
        assert profile.provider == "acme"
        assert profile.model_name == "Model One"
        assert profile.version == "2026.1"
        assert profile.context_window == 128000
        assert profile.max_output_tokens == 8192

    def test_calculates_overall_score_as_average_of_capability_scores(self) -> None:
        profiler = Profiler()
        profiler.record_result("model-1", Capability.PYTHON, 9.0)
        profiler.record_result("model-1", Capability.SQL, 6.0)

        profile = profiler.build_profile("model-1", "acme", "Model One", "v1", 128000, 8192)

        assert profile.overall_score == 7.5

    def test_sets_overall_score_to_zero_when_no_results_recorded(self) -> None:
        profiler = Profiler()

        profile = profiler.build_profile("model-1", "acme", "Model One", "v1", 128000, 8192)

        assert profile.overall_score == 0.0

    def test_builds_capability_score_objects_from_recorded_results(self) -> None:
        profiler = Profiler()
        evidence = ("benchmark passed",)
        profiler.record_result("model-1", Capability.PYTHON, 8.5, 0.9, evidence)

        profile = profiler.build_profile("model-1", "acme", "Model One", "v1", 128000, 8192)

        assert profile.capability_scores == (
            CapabilityScore(Capability.PYTHON, 8.5, 0.9, evidence),
        )

    def test_passes_through_known_keyword_fields(self) -> None:
        profiler = Profiler()

        profile = profiler.build_profile(
            "model-1",
            "acme",
            "Model One",
            "v1",
            128000,
            8192,
            supports_tools=True,
            supports_function_calling=True,
            average_latency_ms=125.5,
            tokens_per_second=80.0,
            reliability=0.99,
            supported_languages=("python",),
            metadata=(("tier", "premium"),),
        )

        assert profile.supports_tools is True
        assert profile.supports_function_calling is True
        assert profile.average_latency_ms == 125.5
        assert profile.tokens_per_second == 80.0
        assert profile.reliability == 0.99
        assert profile.supported_languages == ("python",)
        assert profile.metadata == (("tier", "premium"),)

    def test_ignores_unknown_keyword_fields(self) -> None:
        profiler = Profiler()

        profile = profiler.build_profile(
            "model-1",
            "acme",
            "Model One",
            "v1",
            128000,
            8192,
            experimental_setting=True,
        )

        assert profile.supports_tools is False
        assert profile.average_latency_ms == 0.0
