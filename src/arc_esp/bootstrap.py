from __future__ import annotations

import logging
import sys

from arc_esp.config.loader import load_config
from arc_esp.core.target_resolver import TargetResolver
from arc_esp.overlay.renderer import OverlayRenderer
from arc_esp.core.esp_engine import EspEngine
from arc_esp.core.aimbot_engine import AimbotEngine
from arc_esp.input.hotkeys import HotkeyBus


def main(argv: list[str] | None = None) -> int:
    cfg = load_config(argv)
    logging.basicConfig(
        level=getattr(logging, cfg.app.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    log = logging.getLogger("arc_esp.bootstrap")

    resolver = TargetResolver(cfg.process)
    proc = resolver.attach()
    if proc is None:
        log.error("target process not found; is ARC Raiders running?")
        return 2

    renderer = OverlayRenderer(cfg.render)
    esp = EspEngine(cfg=cfg.esp, reader=proc.reader)
    aim = AimbotEngine(cfg=cfg.aimbot, reader=proc.reader)
    hotkeys = HotkeyBus(cfg.app, on_panic=lambda: sys.exit(0))
    hotkeys.bind_toggle(esp.toggle)
    hotkeys.bind_toggle(aim.toggle)

    renderer.attach_hooks(esp, aim)
    log.info("overlay attached pid=%s", proc.pid)
    return renderer.run()