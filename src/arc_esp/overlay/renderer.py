from __future__ import annotations

import logging
import time

from arc_esp.config.loader import RenderConfig
from arc_esp.core.esp_engine import EspEngine
from arc_esp.core.aimbot_engine import AimbotEngine
from arc_esp.overlay.draw import DrawList

log = logging.getLogger(__name__)


class OverlayRenderer:
    """Transparent overlay window that paints ESP frames and ticks the aimbot."""

    def __init__(self, cfg: RenderConfig):
        self._cfg = cfg
        self._esp: EspEngine | None = None
        self._aim: AimbotEngine | None = None
        self._running = False

    def attach_hooks(self, esp: EspEngine, aim: AimbotEngine) -> None:
        self._esp = esp
        self._aim = aim

    def _paint(self, draw: DrawList) -> None:
        if not self._esp or not self._esp.enabled:
            return
        frame = self._esp.build_frame()
        for p in frame.players:
            draw.box(p.head_screen, p.chest_screen, color=self._cfg.box_color)
            draw.text(p.head_screen, f"{p.name} {int(p.distance_m)}m")
        for (x, y, _kind) in frame.loot:
            draw.marker((x, y), color=self._cfg.loot_color)
        for (x, y, _kind) in frame.arcs:
            draw.marker((x, y), color=self._cfg.arc_color)

    def run(self) -> int:
        self._running = True
        draw = DrawList(backend=self._cfg.backend)
        log.info("overlay running backend=%s fps=%d", self._cfg.backend, self._cfg.target_fps)
        interval = 1.0 / max(self._cfg.target_fps, 1)
        try:
            while self._running:
                t0 = time.perf_counter()
                if self._aim:
                    self._aim.tick()
                self._paint(draw)
                draw.present()
                time.sleep(max(0.0, interval - (time.perf_counter() - t0)))
        except KeyboardInterrupt:
            pass
        finally:
            draw.close()
        return 0