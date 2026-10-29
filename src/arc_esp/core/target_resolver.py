from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import psutil

from arc_esp.config.loader import ProcessConfig
from arc_esp.memory.reader import ProcessHandle

log = logging.getLogger(__name__)


@dataclass
class AttachedProcess:
    pid: int
    name: str
    reader: ProcessHandle


class TargetResolver:
    """Locate the ARC Raiders process and hand back a memory reader."""

    def __init__(self, cfg: ProcessConfig):
        self._cfg = cfg

    def _find(self) -> psutil.Process | None:
        wanted = {n.lower() for n in self._cfg.exe_names}
        for p in psutil.process_iter(["pid", "name"]):
            try:
                if p.info["name"] and p.info["name"].lower() in wanted:
                    return p
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def attach(self, retries: int = 3) -> AttachedProcess | None:
        for attempt in range(retries):
            p = self._find()
            if p is not None:
                reader = ProcessHandle(p.pid, self._cfg.module)
                if reader.open():
                    log.info("attached to %s (pid=%s)", p.name(), p.pid)
                    return AttachedProcess(pid=p.pid, name=p.name() or "", reader=reader)
            time.sleep(self._cfg.poll_ms / 1000.0)
            log.debug("attach attempt %d/%d failed", attempt + 1, retries)
        return None