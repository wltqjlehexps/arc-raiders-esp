from arc_esp.core.snapshot import PlayerEntity, WorldSnapshot
from arc_esp.memory.offsets import Offsets


class _FakeReader:
    def __init__(self):
        self._ptrs = {0x1000: 0x2000}
        self._ints = {0x2000 + 0x10: 3}

    def read_ptr(self, addr):
        return self._ptrs.get(addr, 0)

    def read_int(self, addr):
        return self._ints.get(addr, 0)

    def read_float(self, addr):
        return 0.0

    def read_string(self, addr, n):
        return ""

    def read_vec2(self, addr):
        return (0.0, 0.0)


def test_empty_snapshot_when_world_null():
    o = Offsets(world_pointer=0xDEAD, player_count=0x10, player_list=0x18)
    snap = WorldSnapshot.read(_FakeReader(), o)
    assert snap.players == []


def test_bone_lookup_head_vs_chest():
    p = PlayerEntity(
        name="raider", health=100, distance_m=42.0, is_teammate=False,
        visible=True, head_screen=(1.0, 2.0), chest_screen=(3.0, 4.0),
    )
    assert p.bone_screen("head") == (1.0, 2.0)
    assert p.bone_screen("chest") == (3.0, 4.0)