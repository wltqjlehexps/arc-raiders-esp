from __future__ import annotations

import logging
from dataclasses import dataclass

from arc_esp.memory.reader import ProcessHandle

log = logging.getLogger(__name__)


@dataclass
class ScanHit:
    address: int
    pattern: bytes


class SignatureScanner:
    """Simple pattern scanner for locating the world pointer after patches."""

    def __init__(self, reader: ProcessHandle):
        self._reader = reader

    def scan(self, pattern: bytes, start: int, length: int, step: int = 0x1000) -> ScanHit | None:
        log.debug("scan start=0x%x len=0x%x", start, length)
        for addr in range(start, start + length, step):
            chunk = self._reader.read(addr, step)
            if not chunk:
                continue
            idx = chunk.find(pattern)
            if idx >= 0:
                return ScanHit(address=addr + idx, pattern=pattern)
        return None