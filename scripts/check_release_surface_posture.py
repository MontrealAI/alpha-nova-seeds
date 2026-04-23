#!/usr/bin/env python3
"""Validate release-surface posture coherence across README/AGENTS/RELEASES."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = "v2.8.0-rc.2"
FILES = {
    "README": ROOT / "README.md",
    "AGENTS": ROOT / "AGENTS.md",
    "RELEASES": ROOT / "RELEASES.md",
}

PATTERNS = {
    "README": [
        re.compile(r"v2\.8\.0-rc\.2 posture"),
        re.compile(r"Current RC target:\s*\*\*v2\.8\.0-rc\.2\*\*"),
    ],
    "AGENTS": [
        re.compile(r"tracks\s*\*\*v2\.8\.0-rc\.2\*\*"),
    ],
    "RELEASES": [
        re.compile(r"active target:\s*v2\.8\.0-rc\.2"),
        re.compile(r"retain `v2\.8\.0-rc\.2` as the active unpublished RC target"),
    ],
}

FORBIDDEN = ["v2.8.0-rc.3", "v2.9.0-rc.1"]


def main() -> int:
    errors: list[str] = []

    for label, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")

        for pattern in PATTERNS[label]:
            if not pattern.search(text):
                errors.append(
                    f"{path.relative_to(ROOT)} missing required posture marker: {pattern.pattern}"
                )

        for disallowed in FORBIDDEN:
            if disallowed in text:
                errors.append(
                    f"{path.relative_to(ROOT)} contains future RC marker {disallowed}; expected active target {TARGET}"
                )

    if errors:
        print("FAIL: release-surface posture drift detected")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: release-surface posture coherence is intact (README/AGENTS/RELEASES)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
