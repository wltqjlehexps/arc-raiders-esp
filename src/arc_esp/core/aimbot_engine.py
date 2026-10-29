from __future__ import annotations

import logging
import math

from arc_esp.config.loader import AimbotConfig
from arc_esp.memory.reader import ProcessHandle
from arc_esp.memory.offsets import Offsets
from arc_esp.core.snapshot import WorldSnapshot
from arc_esp.input.mouse import MouseInjector

log = logging.getLogger(__name__)


class AimbotEngine:
    """Bone-target aimbot with FOV gating and visibility check."""

    def __init__(self, cfg: AimbotConfig, reader: ProcessHandle):
        self._cfg = cfg
        self._reader = reader
        self._offsets = Offsets.load()
        self._mouse = MouseInjector()
        self._enabled = cfg.enabled

    def toggle(self) -> None:
        self._enabled = not self._enabled
        log.info("aimbot %s", "enabled" if self._enabled else "disabled")

    def _pick_target(self, snapshot: WorldSnapshot) -> tuple[float, float] | None:
        best: tuple[float, tuple[float, float]] | None = None
        cx, cy = snapshot.screen_center
        for p in snapshot.players:
            if self._cfg.team_filter and p.is_teammate:
                continue
            if p.distance_m > self._cfg.max_distance_m:
                continue
            if self._cfg.visibility_check and not p.visible:
                continue
            sx, sy = p.bone_screen(self._cfg.bone)
            dx, dy = sx - cx, sy - cy
            dist = math.hypot(dx, dy)
            if dist > self._cfg.fov_radius:
                continue
            if best is None or dist < best[0]:
                best = (dist, (dx, dy))
        return best[1] if best else None

    def tick(self) -> None:
        if not self._enabled:
            return
        snap = WorldSnapshot.read(self._reader, self._offsets)
        delta = self._pick_target(snap)
        if delta is None:
            return
        dx = delta[0] * self._cfg.smooth
        dy = delta[1] * self._cfg.smooth
        self._mouse.move_relative(int(dx), int(dy))