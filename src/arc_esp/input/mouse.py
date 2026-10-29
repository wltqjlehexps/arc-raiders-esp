from __future__ import annotations

import ctypes
from ctypes import wintypes

MOUSEEVENTF_MOVE = 0x0001
INPUT_MOUSE = 0

_user32 = ctypes.WinDLL("user32", use_last_error=True)


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class _INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("mi", _MOUSEINPUT)]


class MouseInjector:
    """SendInput-based relative mouse movement used by the aimbot."""

    def move_relative(self, dx: int, dy: int) -> None:
        inp = _INPUT(type=INPUT_MOUSE)
        inp.mi = _MOUSEINPUT(dx=dx, dy=dy, mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0, dwExtraInfo=None)
        _user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(_INPUT))