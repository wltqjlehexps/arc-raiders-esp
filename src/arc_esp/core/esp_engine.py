from __future__ import annotations

import logging
from dataclasses import dataclass

from arc_esp.config.loader import EspConfig
from arc_esp.memory.reader import ProcessHandle
from arc_esp.memory.offsets import Offsets
from arc_esp.core.snapshot import WorldSnapshot, PlayerEntity

log = logging.getLogger(__name__)


@dataclass
class EspOverlayFrame:
    players: list[PlayerEntity]
    loot: list[tuple[int, int, int]]
    arcs: list[tuple[int, int, int]]
    extracts: list[tuple[int, int]]


class EspEngine:
    """Reads world state and produces an overlay frame for ESP rendering."""

    def __init__(self, cfg: EspConfig, reader: ProcessHandle):
        self._cfg = cfg
        self._reader = reader
        self._enabled = True
        self._offsets = Offsets.load()

    def toggle(self) -> None:
        self._enabled = not self._enabled
        log.info("esp %s", "enabled" if self._enabled else "disabled")

    @property
    def enabled(self) -> bool:
        return self._enabled

    def build_frame(self) -> EspOverlayFrame:
        if not self._enabled:
            return EspOverlayFrame(players=[], loot=[], arcs=[], extracts=[])

        snapshot = WorldSnapshot.read(self._reader, self._offsets)
        players = snapshot.players if self._cfg.players else []
        loot = snapshot.loot_screen if self._cfg.loot else []
        arcs = snapshot.arcs_screen if self._cfg.arcs else []
        extracts = snapshot.extracts_screen if self._cfg.extract else []
        return EspOverlayFrame(players=players, loot=loot, arcs=arcs, extracts=extracts)