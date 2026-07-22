from evolution.skill_evolver import SkillEvolver
from core.ids import SkillId
from core.models.skill import Skill


def _make_skill(proficiency: float = 0.5) -> Skill:
    return Skill(
        id=SkillId("s1"),
        name="python",
        description="test",
        proficiency=proficiency,
    )


class TestSkillEvolver:
    def test_adapt_increases_proficiency(self) -> None:
        evolver = SkillEvolver()
        skill = _make_skill(proficiency=0.3)
        adapted = evolver.adapt(skill, score=0.9)
        assert adapted.proficiency > skill.proficiency

    def test_adapt_clamps_at_one(self) -> None:
        evolver = SkillEvolver()
        skill = _make_skill(proficiency=0.95)
        adapted = evolver.adapt(skill, score=1.0)
        assert adapted.proficiency <= 1.0

    def test_adapt_increments_use_count(self) -> None:
        evolver = SkillEvolver()
        skill = _make_skill()
        adapted = evolver.adapt(skill, score=0.7)
        assert adapted.use_count == skill.use_count + 1

    def test_adapt_preserves_identity(self) -> None:
        evolver = SkillEvolver()
        skill = _make_skill()
        adapted = evolver.adapt(skill, score=0.8)
        assert adapted.id == skill.id
        assert adapted.name == skill.name
