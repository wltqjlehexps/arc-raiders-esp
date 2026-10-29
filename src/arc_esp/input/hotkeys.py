from __future__ import annotations

import logging
from typing import Callable

import keyboard

from arc_esp.config.loader import AppConfig

log = logging.getLogger(__name__)


class HotkeyBus:
    """Registers toggle / panic hotkeys via the `keyboard` library."""

    def __init__(self, cfg: AppConfig, on_panic: Callable[[], None] | None = None):
        self._cfg = cfg
        self._on_panic = on_panic or (lambda: None)
        self._callbacks: list[Callable[[], None]] = []

    def bind_toggle(self, cb: Callable[[], None]) -> None:
        self._callbacks.append(cb)
        keyboard.add_hotkey(self._cfg.hotkey_toggle, cb)
        log.info("hotkey toggle bound to %s", self._cfg.hotkey_toggle)

    def bind_panic(self) -> None:
        keyboard.add_hotkey(self._cfg.hotkey_panic, self._on_panic)
        log.info("panic hotkey bound to %s", self._cfg.hotkey_panic)