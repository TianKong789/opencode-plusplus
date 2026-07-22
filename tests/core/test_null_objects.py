from core.null_objects import NullEventBus
from core.events.base import BaseEvent


class TestNullEventBus:
    def test_publish_is_noop(self) -> None:
        bus = NullEventBus()
        event = BaseEvent(source="test")
        bus.publish(event)

    def test_subscribe_is_noop(self) -> None:
        bus = NullEventBus()
        bus.subscribe(BaseEvent, lambda e: None)
