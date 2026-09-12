#!/usr/bin/env python3
"""Verify raw data snapshots in data/ against research/data/checksums.txt.

Stdlib only. Run from the repo root:

    python3 research/data/verify.py

Exit 0 = every pinned file present with a matching hash and no unexpected
raw files in data/. Exit 1 = drift (a prereg that pins a snapshot must not
run against a file that changed underneath it).

This is the local half of the reproducibility rule; CI calls the same script.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKSUMS = REPO_ROOT / "research" / "data" / "checksums.txt"
DATA_DIR = REPO_ROOT / "data"
IGNORED = {"README.md"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    failures: list[str] = []
    pinned: dict[str, str] = {}

    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, rel = line.partition("  ")
        rel = rel.strip()
        pinned[rel] = digest.strip()

    for rel, expected in sorted(pinned.items()):
        path = REPO_ROOT / rel
        if not path.is_file():
            failures.append(f"MISSING   {rel} (pinned but not on disk)")
            continue
        actual = sha256(path)
        if actual != expected:
            failures.append(f"MISMATCH  {rel}\n          expected {expected}\n          actual   {actual}")
        else:
            print(f"OK        {rel}")

    if not DATA_DIR.is_dir():
        failures.append("MISSING   data/ directory does not exist")
    else:
        for path in sorted(DATA_DIR.iterdir()):
            if not path.is_file() or path.name in IGNORED:
                continue
            rel = f"data/{path.name}"
            if rel not in pinned:
                failures.append(f"UNPINNED  {rel} (in data/ but not in checksums.txt)")

    if failures:
        print("\nVERIFY FAILED:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1

    print(f"\nAll {len(pinned)} pinned snapshot(s) verified. No unpinned files in data/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
