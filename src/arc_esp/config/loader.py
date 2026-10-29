from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AppConfig:
    name: str = "arc-raiders-esp"
    version: str = "0.0.0"
    log_level: str = "info"
    hotkey_toggle: str = "f8"
    hotkey_panic: str = "end"


@dataclass
class ProcessConfig:
    exe_names: list[str] = field(default_factory=list)
    module: str = ""
    poll_ms: int = 250


@dataclass
class RenderConfig:
    overlay_class: str = "ArcRaidersEspOverlay"
    backend: str = "direct2d"
    target_fps: int = 144
    box_color: list[int] = field(default_factory=lambda: [255, 64, 64, 255])
    skeleton_color: list[int] = field(default_factory=lambda: [64, 255, 128, 255])
    loot_color: list[int] = field(default_factory=lambda: [255, 220, 0, 255])
    arc_color: list[int] = field(default_factory=lambda: [200, 64, 255, 255])


@dataclass
class AimbotConfig:
    enabled: bool = False
    fov_radius: int = 180
    smooth: float = 0.35
    bone: str = "head"
    visibility_check: bool = True
    team_filter: bool = True
    max_distance_m: int = 400


@dataclass
class EspConfig:
    players: bool = True
    loot: bool = True
    arcs: bool = True
    extract: bool = True
    show_distance: bool = True
    show_health: bool = True
    show_name: bool = False


@dataclass
class MemoryConfig:
    read_batch: int = 32
    cache_ttl_ms: int = 120


@dataclass
class RootConfig:
    app: AppConfig = field(default_factory=AppConfig)
    process: ProcessConfig = field(default_factory=ProcessConfig)
    render: RenderConfig = field(default_factory=RenderConfig)
    aimbot: AimbotConfig = field(default_factory=AimbotConfig)
    esp: EspConfig = field(default_factory=EspConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)


def _merge(inst: Any, raw: dict[str, Any]) -> Any:
    for k, v in raw.items():
        if not hasattr(inst, k):
            continue
        cur = getattr(inst, k)
        if isinstance(v, dict) and hasattr(cur, "__dataclass_fields__"):
            _merge(cur, v)
        else:
            setattr(inst, k, v)
    return inst


def load_config(argv: list[str] | None = None) -> RootConfig:
    argv = argv or []
    path = Path("config/default.yaml")
    for i, a in enumerate(argv):
        if a == "--config" and i + 1 < len(argv):
            path = Path(argv[i + 1])
    cfg = RootConfig()
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
        _merge(cfg, raw)
    return cfg