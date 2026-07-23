from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Callable

from core.events.base import BaseEvent


@runtime_checkable
class EventBus(Protocol):
    """Publish-subscribe event bus for decoupled component communication.

    Implementations decide how events are dispatched: in-process,
    across threads, or over a network boundary.
    """

    def publish(self, event: BaseEvent) -> None:
        """Emit an event to all registered subscribers.

        Args:
            event: The domain event to publish.
        """

    def subscribe(self, event_type: type[BaseEvent], handler: Callable[[BaseEvent], None]) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The event class to listen for.
            handler: Callback invoked when a matching event is published.
        """
