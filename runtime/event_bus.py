from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from core.events.base import BaseEvent
from core.interfaces.event_bus import EventBus

# NullEventBus is the canonical null-object implementation.
# Re-exported here for backward compatibility; new code should
# import from ``core.null_objects`` directly.
from core.null_objects import NullEventBus  # noqa: F401


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


@dataclass(slots=True, frozen=True)
class NullEventBus(EventBus):
    """No-op event bus that discards all events.

    Use when event publication is not needed (tests, development stubs).
    """

    def publish(self, event: BaseEvent) -> None:
        """Discard the event (no-op).

        Args:
            event: The domain event (ignored).
        """

    def subscribe(self, event_type: type[BaseEvent], handler: Callable[[BaseEvent], None]) -> None:
        """Register a handler (silently ignored — events are never dispatched).

        Args:
            event_type: The event class to listen for.
            handler: Callback (never invoked).
        """
