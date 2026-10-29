from pathlib import Path

from arc_esp.memory.offsets import Offsets


def test_load_default_offsets_when_missing(tmp_path: Path):
    o = Offsets.load(tmp_path / "missing.yaml")
    assert o.world_pointer == 0
    assert o.player_count == 0


def test_load_hex_offsets(tmp_path: Path):
    p = tmp_path / "o.yaml"
    p.write_text("world_pointer: '0x7FF600100000'\nplayer_count: '0x1A0'\n", encoding="utf-8")
    o = Offsets.load(p)
    assert o.world_pointer == 0x7FF600100000
    assert o.player_count == 0x1A0