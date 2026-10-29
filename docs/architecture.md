# Architecture

`arc-raiders-esp` is a modular external overlay toolkit for ARC Raiders.

## Layers

- `arc_esp.bootstrap` — entry point; wires config, process attach, overlay, esp, aimbot, hotkeys.
- `arc_esp.config` — YAML → dataclass config loader (`config/default.yaml`).
- `arc_esp.core` — `TargetResolver`, `EspEngine`, `AimbotEngine`, `WorldSnapshot`.
- `arc_esp.memory` — `ProcessHandle` (ctypes ReadProcessMemory), `Offsets`, `SignatureScanner`.
- `arc_esp.input` — `MouseInjector` (SendInput), `HotkeyBus` (keyboard).
- `arc_esp.overlay` — `OverlayRenderer` + `DrawList` abstraction, Qt/D2D backend at runtime.

## Typical flow

1. `TargetResolver.attach()` finds `PioneerGame.exe` and opens a read handle.
2. `OverlayRenderer.run()` pumps frames; `AimbotEngine.tick()` runs each frame.
3. `EspEngine.build_frame()` reads a `WorldSnapshot` and returns entities for painting.
4. Hotkeys (`F8` toggle, `End` panic) come from `config/default.yaml`.

## Offsets

Offsets drift after patches. Run `python scripts/update_offsets.py` to re-scan
signatures and regenerate `offsets/current.yaml`.