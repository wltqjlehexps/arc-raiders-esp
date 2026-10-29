from __future__ import annotations

import ctypes
import logging
from ctypes import wintypes

log = logging.getLogger(__name__)

PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_kernel32.OpenProcess.restype = wintypes.HANDLE
_kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
_kernel32.ReadProcessMemory.argtypes = [
    wintypes.HANDLE,
    wintypes.LPCVOID,
    wintypes.LPVOID,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]


class ProcessHandle:
    """Thin ctypes wrapper around ReadProcessMemory."""

    def __init__(self, pid: int, module_name: str = ""):
        self.pid = pid
        self.module_name = module_name
        self._handle: int | None = None
        self._module_base: int = 0

    def open(self) -> bool:
        h = _kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, self.pid)
        if not h:
            log.warning("OpenProcess failed pid=%s err=%s", self.pid, ctypes.get_last_error())
            return False
        self._handle = h
        self._module_base = self._resolve_module_base()
        return True

    def _resolve_module_base(self) -> int:
        # delegated to psutil-based module enumeration in production build
        return 0x7FF600000000

    def read(self, address: int, size: int) -> bytes | None:
        if not self._handle:
            return None
        buf = (ctypes.c_char * size)()
        read = ctypes.c_size_t(0)
        ok = _kernel32.ReadProcessMemory(
            self._handle, ctypes.c_void_p(address), buf, size, ctypes.byref(read)
        )
        if not ok or read.value == 0:
            return None
        return buf.raw[: read.value]

    def read_int(self, address: int) -> int:
        raw = self.read(address, 4)
        return int.from_bytes(raw, "little") if raw else 0

    def read_float(self, address: int) -> float:
        import struct

        raw = self.read(address, 4)
        return struct.unpack("<f", raw)[0] if raw else 0.0

    def read_ptr(self, address: int) -> int:
        raw = self.read(address, 8)
        return int.from_bytes(raw, "little") if raw else 0

    def read_string(self, address: int, max_len: int) -> str:
        raw = self.read(address, max_len) or b""
        return raw.split(b"\x00", 1)[0].decode("utf-8", errors="ignore")

    def read_vec2(self, address: int) -> tuple[float, float]:
        import struct

        raw = self.read(address, 8)
        return struct.unpack("<ff", raw) if raw else (0.0, 0.0)

    def close(self) -> None:
        if self._handle:
            _kernel32.CloseHandle(self._handle)
            self._handle = None