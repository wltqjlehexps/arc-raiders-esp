from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class DrawList:
    """Abstracted draw list — real implementation lives in the Qt overlay window."""

    def __init__(self, backend: str = "direct2d"):
        self._backend = backend
        self._items: list[tuple] = []

    def box(self, a: tuple[float, float], b: tuple[float, float], color: list[int]) -> None:
        self._items.append(("box", a, b, color))

    def marker(self, pos: tuple[float, float], color: list[int]) -> None:
        self._items.append(("marker", pos, color))

    def text(self, pos: tuple[float, float], text: str) -> None:
        self._items.append(("text", pos, text))

    def present(self) -> None:
        if self._items:
            log.debug("present %d draw items via %s", len(self._items), self._backend)
        self._items.clear()

    def close(self) -> None:
        log.info("draw list closed")