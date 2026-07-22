from benchmarks.definitions import ALL_BENCHMARKS
from skills.catalog import ALL_SKILLS, PYTHON_DATACLASS_MODELING
from skills.registry import SkillRegistry


def test_skill_properties() -> None:
    assert PYTHON_DATACLASS_MODELING.name == "python-dataclass-modeling"
    assert PYTHON_DATACLASS_MODELING.proficiency == 0.95
    assert PYTHON_DATACLASS_MODELING.is_mastered() is True


def test_all_skills_have_unique_ids() -> None:
    ids = [s.id for s in ALL_SKILLS]
    assert len(ids) == len(set(ids))


def test_all_benchmarks_reference_valid_skills() -> None:
    skill_ids = {s.id for s in ALL_SKILLS}
    for bench in ALL_BENCHMARKS:
        msg = f"Benchmark {bench.id} references unknown skill {bench.skill_id}"
        assert bench.skill_id in skill_ids, msg


def test_registry_register_and_promote() -> None:
    registry = SkillRegistry()
    registry.register(PYTHON_DATACLASS_MODELING, experimental=True)
    assert registry.get_experimental(PYTHON_DATACLASS_MODELING.id) is not None
    assert registry.get_production(PYTHON_DATACLASS_MODELING.id) is None

    promoted = registry.promote(PYTHON_DATACLASS_MODELING.id)
    assert promoted is not None
    assert registry.get_experimental(PYTHON_DATACLASS_MODELING.id) is None
    assert registry.get_production(PYTHON_DATACLASS_MODELING.id) is not None
