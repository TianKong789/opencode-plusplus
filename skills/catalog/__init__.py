"""Skill catalog — defines and registers all known skills.

Each skill is a ``Skill`` dataclass instance with associated benchmarks.
Import this module to populate the global registry.
"""

from __future__ import annotations

from core.ids import BenchmarkId, SkillId
from core.models.benchmark import Benchmark
from core.models.skill import Skill

PYTHON_DATACLASS_MODELING = Skill(
    id=SkillId("skill-python-dataclass-modeling"),
    name="python-dataclass-modeling",
    description=(
        "Create immutable, validated domain models using "
        "@dataclass(slots=True, frozen=True) with typed IDs, "
        "comprehensive docstrings, and __post_init__ validation."
    ),
    proficiency=0.95,
    use_count=15,
)
"""Core modeling skill — mastered through building OpenCode++ domain models."""

ORCHESTRATOR_DESIGN = Skill(
    id=SkillId("skill-orchestrator-design"),
    name="orchestrator-design",
    description=(
        "Design pipeline coordinators that wire together Planner, "
        "Executor, Evaluator, Reflector, and MemoryProvider into "
        "a single run() loop."
    ),
    proficiency=0.7,
    use_count=3,
)
"""Pipeline orchestration — competent, needs more real-world runs."""

TYPED_IDENTIFIERS = Skill(
    id=SkillId("skill-typed-identifiers"),
    name="typed-identifiers",
    description=(
        "Implement type-safe identifiers using str subclasses "
        "with a common BaseEntityId base class for static and "
        "runtime type checking."
    ),
    proficiency=0.9,
    use_count=5,
)
"""Typed ID system — near mastery, validated across 10 domain models."""

ALL_SKILLS: tuple[Skill, ...] = (
    PYTHON_DATACLASS_MODELING,
    ORCHESTRATOR_DESIGN,
    TYPED_IDENTIFIERS,
)
"""Complete catalog of registered skills."""

# ── benchmarks ──────────────────────────────────────────────────────

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
