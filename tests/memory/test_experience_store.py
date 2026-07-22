from core.ids import ExperienceId, ReflectionId
from core.models.experience import Experience
from memory.experience_store import ExperienceStore


def test_store_and_retrieve_experience() -> None:
    store = ExperienceStore()
    exp = Experience(
        id=ExperienceId("e1"),
        reflection_id=ReflectionId("r1"),
        lesson="test lesson",
        context="test",
    )
    store.store_experience(exp)
    assert store.get_experience("e1") == exp
    assert len(store.list_experiences()) == 1
