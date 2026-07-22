from __future__ import annotations

from dataclasses import FrozenInstanceError
from math import inf

import pytest

from core.ids import ModelId
from src.opencode.evaluation.capability.models import ModelCapabilityProfile
from src.opencode.routing.policies import (
    BalancedPolicy,
    CloudPreferredPolicy,
    CostOptimizedPolicy,
    LatencyPolicy,
    LocalOnlyPolicy,
    QualityPolicy,
    RoutingContext,
    RoutingPolicy,
)


def _make_profile(
    model_id: str = "m1",
    provider: str = "anthropic",
    latency: float = 100.0,
    cost: float = 0.003,
    score: float = 7.0,
) -> ModelCapabilityProfile:
    return ModelCapabilityProfile(
        model_id=model_id,
        provider=provider,
        model_name=f"Model {model_id}",
        version="1.0",
        context_window=128_000,
        max_output_tokens=8_192,
        average_latency_ms=latency,
        estimated_cost=cost,
        overall_score=score,
    )


def _context(
    *profiles: ModelCapabilityProfile,
    max_latency_ms: float = inf,
    max_cost: float = inf,
) -> RoutingContext:
    return RoutingContext(
        profiles=profiles,
        task_description="Route this task",
        max_latency_ms=max_latency_ms,
        max_cost=max_cost,
    )


POLICIES: tuple[RoutingPolicy, ...] = (
    LatencyPolicy(),
    QualityPolicy(),
    LocalOnlyPolicy(),
    CloudPreferredPolicy(),
    CostOptimizedPolicy(),
    BalancedPolicy(),
)


def test_routing_context_constructs_when_required_fields_are_provided() -> None:
    profile = _make_profile()

    context = RoutingContext(
        profiles=(profile,),
        task_description="Summarize the report",
        required_capabilities=("summarization",),
        max_latency_ms=250.0,
        max_cost=0.004,
    )

    assert context.profiles == (profile,)
    assert context.task_description == "Summarize the report"
    assert context.required_capabilities == ("summarization",)
    assert context.max_latency_ms == 250.0
    assert context.max_cost == 0.004


def test_routing_context_uses_unconstrained_defaults_when_optional_fields_are_omitted() -> None:
    context = RoutingContext(profiles=(), task_description="Route this task")

    assert context.required_capabilities == ()
    assert context.max_latency_ms == inf
    assert context.max_cost == inf


def test_routing_context_rejects_mutation_when_constructed() -> None:
    context = RoutingContext(profiles=(), task_description="Route this task")

    with pytest.raises(FrozenInstanceError):
        setattr(context, "task_description", "Changed task")


@pytest.mark.parametrize("policy", POLICIES, ids=lambda policy: type(policy).__name__)
def test_filter_candidates_removes_models_over_latency_limit_when_limited(
    policy: RoutingPolicy,
) -> None:
    fast = _make_profile("fast", latency=50.0)
    slow = _make_profile("slow", latency=250.0)

    candidates = policy._filter_candidates(_context(fast, slow, max_latency_ms=100.0))

    assert candidates == (fast,)


@pytest.mark.parametrize("policy", POLICIES, ids=lambda policy: type(policy).__name__)
def test_filter_candidates_removes_models_over_cost_limit_when_limited(
    policy: RoutingPolicy,
) -> None:
    affordable = _make_profile("affordable", cost=0.002)
    expensive = _make_profile("expensive", cost=0.010)

    candidates = policy._filter_candidates(_context(affordable, expensive, max_cost=0.005))

    assert candidates == (affordable,)


@pytest.mark.parametrize("policy", POLICIES, ids=lambda policy: type(policy).__name__)
def test_filter_candidates_applies_both_constraints_when_both_are_set(
    policy: RoutingPolicy,
) -> None:
    eligible = _make_profile("eligible", latency=50.0, cost=0.002)
    slow = _make_profile("slow", latency=500.0, cost=0.002)
    expensive = _make_profile("expensive", latency=50.0, cost=0.020)

    candidates = policy._filter_candidates(
        _context(eligible, slow, expensive, max_latency_ms=100.0, max_cost=0.005)
    )

    assert candidates == (eligible,)


@pytest.mark.parametrize("policy", POLICIES, ids=lambda policy: type(policy).__name__)
def test_filter_candidates_preserves_all_models_when_no_constraints_are_set(
    policy: RoutingPolicy,
) -> None:
    first = _make_profile("first", latency=10.0, cost=0.001)
    second = _make_profile("second", latency=1_000.0, cost=0.050)

    assert policy._filter_candidates(_context(first, second)) == (first, second)


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        (_context(_make_profile("slow", latency=200.0), _make_profile("fast", latency=50.0)), ModelId("fast")),
        (_context(_make_profile("too-fast", latency=10.0), _make_profile("allowed", latency=50.0), max_latency_ms=100.0), ModelId("too-fast")),
        (_context(), None),
        (_context(_make_profile("slow", latency=200.0), max_latency_ms=100.0), None),
    ],
    ids=("lowest_latency", "latency_constraint", "no_candidates", "all_filtered"),
)
def test_latency_policy_selects_expected_model_when_candidates_vary(
    context: RoutingContext, expected: ModelId | None
) -> None:
    assert LatencyPolicy().select(context) == expected


def test_latency_policy_scores_zero_latency_as_maximum_when_profile_has_no_latency() -> None:
    assert LatencyPolicy().score(_make_profile(latency=0.0), _context()) == 1.0


def test_latency_policy_scores_lower_latency_higher_when_profiles_differ() -> None:
    policy = LatencyPolicy()

    assert policy.score(_make_profile(latency=500.0), _context()) > policy.score(
        _make_profile(latency=2_000.0), _context()
    )


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        (_context(_make_profile("good", score=8.0), _make_profile("best", score=9.0)), ModelId("best")),
        (_context(_make_profile("slow", latency=200.0, cost=0.001, score=10.0), _make_profile("costly", latency=10.0, cost=0.020, score=9.0), _make_profile("eligible", latency=50.0, cost=0.002, score=7.0), max_latency_ms=100.0, max_cost=0.005), ModelId("eligible")),
        (_context(), None),
    ],
    ids=("highest_quality", "constraints", "no_candidates"),
)
def test_quality_policy_selects_expected_model_when_candidates_vary(
    context: RoutingContext, expected: ModelId | None
) -> None:
    assert QualityPolicy().select(context) == expected


def test_quality_policy_returns_overall_score_when_scoring_profile() -> None:
    assert QualityPolicy().score(_make_profile(score=8.5), _context()) == 8.5


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        (_context(_make_profile("local-good", provider="Ollama", score=8.0), _make_profile("local-best", provider="local", score=9.0)), ModelId("local-best")),
        (_context(_make_profile("cloud", provider="anthropic", score=10.0), _make_profile("local", provider="ollama", score=6.0)), ModelId("local")),
        (_context(_make_profile("cloud", provider="openai", score=9.0)), None),
    ],
    ids=("best_local", "ignores_cloud", "no_local_models"),
)
def test_local_only_policy_selects_expected_model_when_candidates_vary(
    context: RoutingContext, expected: ModelId | None
) -> None:
    assert LocalOnlyPolicy().select(context) == expected


@pytest.mark.parametrize(
    ("profile", "expected"),
    [(_make_profile(provider="LMStudio", score=8.0), 8.0), (_make_profile(provider="anthropic", score=8.0), 0.0)],
    ids=("local_provider", "cloud_provider"),
)
def test_local_only_policy_scores_by_provider_when_profile_is_scored(
    profile: ModelCapabilityProfile, expected: float
) -> None:
    assert LocalOnlyPolicy().score(profile, _context()) == expected


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        (_context(_make_profile("local", provider="ollama", score=7.0), _make_profile("cloud", provider="anthropic", score=8.0)), ModelId("cloud")),
        (_context(_make_profile("cloud", provider="anthropic", latency=200.0, score=10.0), _make_profile("local", provider="ollama", latency=50.0, score=7.0), max_latency_ms=100.0), ModelId("local")),
        (_context(), None),
    ],
    ids=("cloud_available", "local_fallback", "no_candidates"),
)
def test_cloud_preferred_policy_selects_expected_model_when_candidates_vary(
    context: RoutingContext, expected: ModelId | None
) -> None:
    assert CloudPreferredPolicy().select(context) == expected


def test_cloud_preferred_policy_applies_penalty_only_when_profile_is_local() -> None:
    policy = CloudPreferredPolicy()
    cloud = _make_profile(provider="anthropic", score=8.0)
    local = _make_profile(provider="ollama", score=8.0)

    assert policy.score(cloud, _context()) == 8.0
    assert policy.score(local, _context()) == pytest.approx(8.0 * (1 - policy.CLOUD_PENALTY))


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        (_context(_make_profile("ineligible", cost=0.0001, score=4.0), _make_profile("affordable", cost=0.001, score=7.0), _make_profile("costly", cost=0.002, score=8.0)), ModelId("affordable")),
        (_context(_make_profile("low-one", score=4.9), _make_profile("low-two", score=1.0)), None),
        (_context(_make_profile("constrained", cost=0.010, score=8.0), max_cost=0.005), None),
    ],
    ids=("cheapest_qualified", "no_qualified_model", "no_candidates_after_filtering"),
)
def test_cost_optimized_policy_selects_expected_model_when_candidates_vary(
    context: RoutingContext, expected: ModelId | None
) -> None:
    assert CostOptimizedPolicy().select(context) == expected


@pytest.mark.parametrize(
    ("profile", "expected"),
    [(_make_profile(cost=0.003, score=7.0), 7.0 / 0.004), (_make_profile(cost=0.0, score=7.0), 7.0)],
    ids=("positive_cost", "zero_cost"),
)
def test_cost_optimized_policy_scores_by_quality_to_cost_ratio_when_profile_varies(
    profile: ModelCapabilityProfile, expected: float
) -> None:
    assert CostOptimizedPolicy().score(profile, _context()) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        (_context(_make_profile("balanced", latency=100.0, cost=0.002, score=8.0), _make_profile("unbalanced", latency=900.0, cost=0.010, score=9.0)), ModelId("balanced")),
        (_context(_make_profile("slow", latency=200.0, cost=0.001, score=10.0), _make_profile("costly", latency=10.0, cost=0.020, score=10.0), _make_profile("eligible", latency=50.0, cost=0.002, score=6.0), max_latency_ms=100.0, max_cost=0.005), ModelId("eligible")),
        (_context(), None),
    ],
    ids=("highest_weighted_score", "constraints", "no_candidates"),
)
def test_balanced_policy_selects_expected_model_when_candidates_vary(
    context: RoutingContext, expected: ModelId | None
) -> None:
    assert BalancedPolicy().select(context) == expected


@pytest.mark.parametrize(
    ("profile", "expected"),
    [
        (_make_profile(score=8.0, cost=0.010, latency=1_000.0), 0.5 * 0.8),
        (_make_profile(score=0.0, cost=0.003, latency=1_000.0), 0.3 * 0.7),
        (_make_profile(score=0.0, cost=0.020, latency=1_000.0), 0.0),
        (_make_profile(score=0.0, cost=0.010, latency=200.0), 0.2 * 0.8),
        (_make_profile(score=0.0, cost=0.010, latency=2_000.0), 0.0),
    ],
    ids=("quality", "cost", "cost_clamped", "latency", "latency_clamped"),
)
def test_balanced_policy_calculates_weighted_components_when_profile_varies(
    profile: ModelCapabilityProfile, expected: float
) -> None:
    assert BalancedPolicy().score(profile, _context()) == pytest.approx(expected)
