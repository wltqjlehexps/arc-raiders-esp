from __future__ import annotations

from dataclasses import dataclass, field

from arc_esp.memory.reader import ProcessHandle
from arc_esp.memory.offsets import Offsets


@dataclass
class PlayerEntity:
    name: str
    health: int
    distance_m: float
    is_teammate: bool
    visible: bool
    head_screen: tuple[float, float]
    chest_screen: tuple[float, float]

    def bone_screen(self, bone: str) -> tuple[float, float]:
        return self.head_screen if bone == "head" else self.chest_screen


@dataclass
class WorldSnapshot:
    screen_center: tuple[float, float] = (960.0, 540.0)
    players: list[PlayerEntity] = field(default_factory=list)
    loot_screen: list[tuple[int, int, int]] = field(default_factory=list)
    arcs_screen: list[tuple[int, int, int]] = field(default_factory=list)
    extracts_screen: list[tuple[int, int]] = field(default_factory=list)

    @classmethod
    def read(cls, reader: ProcessHandle, offsets: Offsets) -> "WorldSnapshot":
        snapshot = cls()
        base = reader.read_ptr(offsets.world_pointer)
        if not base:
            return snapshot
        count = reader.read_int(base + offsets.player_count)
        ents = reader.read_ptr(base + offsets.player_list)
        for i in range(min(count, 64)):
            entry = reader.read_ptr(ents + i * 0x8)
            if not entry:
                continue
            snapshot.players.append(
                PlayerEntity(
                    name=reader.read_string(entry + offsets.player_name, 32),
                    health=reader.read_int(entry + offsets.player_health),
                    distance_m=reader.read_float(base + offsets.player_distance + i * 0x4),
                    is_teammate=bool(reader.read_int(entry + offsets.player_team_flag)),
                    visible=bool(reader.read_int(entry + offsets.player_visible_flag)),
                    head_screen=reader.read_vec2(entry + offsets.player_head_screen),
                    chest_screen=reader.read_vec2(entry + offsets.player_chest_screen),
                )
            )
        return snapshot