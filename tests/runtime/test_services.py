from __future__ import annotations

from core.events.experience import ExperienceStored
from core.ids import EvaluationId, ReflectionId
from core.models.experience import Experience
from core.models.reflection import Reflection
from memory.experience_store import ExperienceStore
from runtime.event_bus import SyncEventBus
from applications.services import ExperienceCapture


def _make_reflection(
    insights: tuple[str, ...] = ("lesson one",),
    root_cause: str = "because",
) -> Reflection:
    return Reflection(
        id=ReflectionId("refl-1"),
        evaluation_id=EvaluationId("eval-1"),
        insights=insights,
        improvements=(),
        root_cause=root_cause,
    )


def test_capture_stores_experience_in_memory() -> None:
    store = ExperienceStore()
    bus = SyncEventBus()
    svc = ExperienceCapture(memory=store, event_bus=bus)

    experience = svc.capture(_make_reflection())

    assert isinstance(experience, Experience)
    assert experience.reflection_id == "refl-1"
    assert experience.lesson == "lesson one"
    stored = store.get_experience(experience.id)
    assert stored is not None
    assert stored.lesson == "lesson one"


def test_capture_publishes_experience_stored_event() -> None:
    bus = SyncEventBus()
    events: list[ExperienceStored] = []
    bus.subscribe(ExperienceStored, lambda e: events.append(e))  # type: ignore[arg-type]
    svc = ExperienceCapture(memory=ExperienceStore(), event_bus=bus)

    svc.capture(_make_reflection())

    assert len(events) == 1
    assert events[0].experience_id.startswith("exp-")
    assert events[0].reflection_id == "refl-1"
    assert events[0].lesson == "lesson one"


def test_capture_uses_first_insight_as_lesson() -> None:
    svc = ExperienceCapture(memory=ExperienceStore(), event_bus=SyncEventBus())
    reflection = _make_reflection(insights=("first", "second"))

    experience = svc.capture(reflection)

    assert experience.lesson == "first"


def test_capture_falls_back_to_root_cause_when_no_insights() -> None:
    svc = ExperienceCapture(memory=ExperienceStore(), event_bus=SyncEventBus())
    reflection = _make_reflection(insights=(), root_cause="root issue")

    experience = svc.capture(reflection)

    assert experience.lesson == "root issue"
    assert experience.context == "root issue"


def test_capture_builds_context_from_insights_when_no_root_cause() -> None:
    svc = ExperienceCapture(memory=ExperienceStore(), event_bus=SyncEventBus())
    reflection = _make_reflection(insights=("a", "b"), root_cause="")

    experience = svc.capture(reflection)

    assert experience.context == "a; b"
