"""Skill catalog — defines and registers all known skills.

Each skill is a ``Skill`` dataclass instance. Benchmarks for these
skills live in ``benchmarks/definitions.py``.
"""

from __future__ import annotations

from core.ids import SkillId
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

ORCHESTRATOR_DESIGN = Skill(
    id=SkillId("skill-orchestrator-design"),
    name="orchestrator-design",
    description=(
        "Design pipeline coordinators that wire together Planner, "
        "Executor, Evaluator, Reflector, and ExperienceStore into "
        "a single run() loop."
    ),
    proficiency=0.7,
    use_count=3,
)

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

ALL_SKILLS: tuple[Skill, ...] = (
    PYTHON_DATACLASS_MODELING,
    ORCHESTRATOR_DESIGN,
    TYPED_IDENTIFIERS,
)
