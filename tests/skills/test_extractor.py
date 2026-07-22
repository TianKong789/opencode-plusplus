from core.ids import ExperienceId, ReflectionId
from core.models.experience import Experience
from skills.extractor import SkillExtractor


def test_extract_skill_from_experiences() -> None:
    extractor = SkillExtractor()
    experiences = (
        Experience(
            id=ExperienceId("e1"),
            reflection_id=ReflectionId("r1"),
            lesson="l1",
            context="c1",
            confidence=0.9,
        ),
        Experience(
            id=ExperienceId("e2"),
            reflection_id=ReflectionId("r1"),
            lesson="l2",
            context="c2",
            confidence=0.7,
        ),
    )
    skill = extractor.extract(experiences, name="python", description="Python programming")
    assert skill.name == "python"
    assert skill.proficiency == 0.8
    assert skill.use_count == 2
