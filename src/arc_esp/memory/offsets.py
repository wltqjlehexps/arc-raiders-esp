from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

OFFSETS_PATH = Path("offsets/current.yaml")


@dataclass
class Offsets:
    world_pointer: int = 0x0
    player_count: int = 0x0
    player_list: int = 0x0
    player_distance: int = 0x0
    player_name: int = 0x0
    player_health: int = 0x0
    player_team_flag: int = 0x0
    player_visible_flag: int = 0x0
    player_head_screen: int = 0x0
    player_chest_screen: int = 0x0

    @classmethod
    def load(cls, path: Path | None = None) -> "Offsets":
        p = path or OFFSETS_PATH
        inst = cls()
        if not p.exists():
            return inst
        with p.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
        for k, v in raw.items():
            if hasattr(inst, k):
                setattr(inst, k, int(v, 16) if isinstance(v, str) else int(v))
        return inst