"""Regenerate offsets/current.yaml from a fresh module signature scan."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from arc_esp.config.loader import load_config
from arc_esp.core.target_resolver import TargetResolver
from arc_esp.memory.scanner import SignatureScanner

PATTERNS = {
    "world_pointer": bytes.fromhex("48 8B 05 ?? ?? ?? ?? 48 8B 88"),
    "player_list": bytes.fromhex("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ??"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="offsets/current.yaml")
    args = ap.parse_args()

    resolved = TargetResolver(load_config().process).attach()
    if not resolved:
        print("target not running", file=sys.stderr)
        return 1

    scanner = SignatureScanner(resolved.reader)
    results: dict[str, int] = {}
    for name, pat in PATTERNS.items():
        hit = scanner.scan(pat, start=0x7FF600000000, length=0x2000000)
        if hit:
            results[name] = hit.address
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.out).open("w", encoding="utf-8") as fh:
        yaml.safe_dump({k: hex(v) for k, v in results.items()}, fh)
    print(f"wrote {len(results)} offsets -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())