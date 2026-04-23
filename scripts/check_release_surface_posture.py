#!/usr/bin/env python3
"""Validate release-surface posture coherence across primary RC-facing surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BADGE_CONFIG = ROOT / "release" / "badges.json"
FILES = {
    "README": ROOT / "README.md",
    "AGENTS": ROOT / "AGENTS.md",
    "RELEASES": ROOT / "RELEASES.md",
    "FRONTIER_LAB_POSTURE": ROOT / "docs" / "FRONTIER_LAB_POSTURE.md",
    "DOCTRINE_STACK": ROOT / "docs" / "DOCTRINE_STACK.md",
    "DEMOS_README": ROOT / "demos" / "README.md",
}
RELEASE_PROVENANCE_WORKFLOW = ROOT / ".github" / "workflows" / "release-provenance.yml"

RC_MARKER_PATTERN = re.compile(r"v(\d+)\.(\d+)\.(\d+)-rc\.(\d+)")


def _version_tuple(match: re.Match[str]) -> tuple[int, int, int, int]:
    return tuple(int(match.group(i)) for i in range(1, 5))


def _parse_target(target: str) -> tuple[int, int, int, int]:
    match = RC_MARKER_PATTERN.fullmatch(target)
    if not match:
        raise ValueError(f"invalid release target format in release/badges.json: {target}")
    return _version_tuple(match)


def _required_patterns(target: str) -> dict[str, list[re.Pattern[str]]]:
    escaped = re.escape(target)
    return {
        "README": [
            re.compile(rf"{escaped} posture"),
            re.compile(rf"Current RC target.*\*\*{escaped}\*\*"),
        ],
        "AGENTS": [
            re.compile(rf"tracks\s*\*\*{escaped}\*\*"),
        ],
        "RELEASES": [
            re.compile(rf"active target:\s*{escaped}"),
            re.compile(rf"retain `{escaped}` as the active unpublished RC target"),
        ],
        "FRONTIER_LAB_POSTURE": [
            re.compile(rf"{escaped}"),
        ],
        "DOCTRINE_STACK": [
            re.compile(rf"{escaped}"),
        ],
        "DEMOS_README": [
            re.compile(rf"{escaped} target"),
        ],
    }


def main() -> int:
    errors: list[str] = []
    try:
        config = json.loads(BADGE_CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: unable to read {BADGE_CONFIG.relative_to(ROOT)}: {exc}")
        return 1

    target = config.get("release_target", "")
    try:
        target_version = _parse_target(target)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1

    patterns = _required_patterns(target)
    for label, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")

        for pattern in patterns[label]:
            if not pattern.search(text):
                errors.append(
                    f"{path.relative_to(ROOT)} missing required posture marker: {pattern.pattern}"
                )

        for match in RC_MARKER_PATTERN.finditer(text):
            marker = match.group(0)
            version = _version_tuple(match)
            if version > target_version:
                errors.append(
                    f"{path.relative_to(ROOT)} contains premature future RC marker {marker}; expected active target {target}"
                )
            if version[:3] == target_version[:3] and version[3] < target_version[3]:
                errors.append(
                    f"{path.relative_to(ROOT)} contains disallowed stale RC marker {marker}; expected active target {target}"
                )

    if not RELEASE_PROVENANCE_WORKFLOW.exists():
        errors.append(
            f"missing file: {RELEASE_PROVENANCE_WORKFLOW.relative_to(ROOT)}"
        )
    else:
        workflow_text = RELEASE_PROVENANCE_WORKFLOW.read_text(encoding="utf-8")
        if "name: release-provenance-${{ inputs.release_tag }}" not in workflow_text:
            errors.append(
                "release-provenance workflow artifact upload name must be tag-generic: "
                "release-provenance-${{ inputs.release_tag }}"
            )

    if errors:
        print("FAIL: release-surface posture drift detected")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS: release-surface posture coherence is intact "
        f"(target {target}; README/AGENTS/RELEASES/docs/demos)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
