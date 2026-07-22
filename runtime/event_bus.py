from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from core.events.base import BaseEvent
from core.interfaces.event_bus import EventBus

# NullEventBus canonical location: ``core.null_objects``.


@dataclass(slots=True, frozen=True)
class SyncEventBus(EventBus):
    """Synchronous in-process event bus.

    Subscribers are invoked in registration order on the calling thread
    when ``publish`` is called.  No buffering, no async.
    """

    _subscribers: dict[type[BaseEvent], list[Callable[[BaseEvent], None]]] = field(
        default_factory=dict, init=False, repr=False
    )

    def publish(self, event: BaseEvent) -> None:
        """Dispatch event to all subscribers of its exact type.

        Args:
            event: The domain event to publish.
        """
        handlers = self._subscribers.get(type(event), [])
        for handler in handlers:
            handler(event)

    def subscribe(self, event_type: type[BaseEvent], handler: Callable[[BaseEvent], None]) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The event class to listen for.
            handler: Callback invoked when a matching event is published.
        """
        self._subscribers.setdefault(event_type, []).append(handler)
