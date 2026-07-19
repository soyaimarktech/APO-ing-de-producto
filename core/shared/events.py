"""
Simple Event Bus.

Version 0.1 keeps events in memory.
Future versions will support plugins.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable


EventHandler = Callable[..., None]


class EventBus:

    def __init__(self) -> None:
        self._listeners = defaultdict(list)

    def subscribe(
        self,
        event: str,
        handler: EventHandler,
    ) -> None:

        self._listeners[event].append(handler)

    def publish(
        self,
        event: str,
        *args,
        **kwargs,
    ) -> None:

        for handler in self._listeners[event]:
            handler(*args, **kwargs)
