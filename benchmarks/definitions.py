"""Benchmark definitions for skill evaluation.

These benchmarks are domain-specific test cases that measure
skill proficiency. They belong to the benchmarks layer, not skills.
"""

from __future__ import annotations

from core.ids import BenchmarkId, SkillId
from core.models.benchmark import Benchmark

MODEL_CREATION_BENCHMARK = Benchmark(
    id=BenchmarkId("bench-model-creation"),
    skill_id=SkillId("skill-python-dataclass-modeling"),
    name="Create a frozen dataclass with typed ID and validation",
    input_data=(
        "Create an immutable dataclass 'Article' with fields: "
        "id (ArticleId), title (str), body (str), published (bool). "
        "Include __post_init__ validation and docstrings."
    ),
    expected_output=(
        "@dataclass(slots=True, frozen=True) class Article with "
        "ArticleId, validation, and docstrings"
    ),
    timeout_ms=30000.0,
)

TYPED_ID_BENCHMARK = Benchmark(
    id=BenchmarkId("bench-typed-id"),
    skill_id=SkillId("skill-typed-identifiers"),
    name="Create a new typed identifier inheriting from BaseEntityId",
    input_data=(
        "Create a typed ID class 'OrderId' that inherits from "
        "BaseEntityId and can be used as a field type in a dataclass."
    ),
    expected_output=("class OrderId(BaseEntityId) with docstring"),
    timeout_ms=15000.0,
)

ALL_BENCHMARKS: tuple[Benchmark, ...] = (
    MODEL_CREATION_BENCHMARK,
    TYPED_ID_BENCHMARK,
)
