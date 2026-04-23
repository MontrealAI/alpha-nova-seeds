#!/usr/bin/env python3
"""Check README badge rails against release/badges.json truth."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BADGE_CONFIG = ROOT / "release" / "badges.json"
README = ROOT / "README.md"
DEMOS_README = ROOT / "demos" / "README.md"
WORKFLOW_DIR = ROOT / ".github" / "workflows"

README_MARKERS = ("<!-- BADGE_RAIL_START -->", "<!-- BADGE_RAIL_END -->")
DEMOS_MARKERS = ("<!-- DEMO_BADGE_STRIP_START -->", "<!-- DEMO_BADGE_STRIP_END -->")


def _extract_marked_block(text: str, markers: tuple[str, str]) -> str:
    start, end = markers
    pattern = re.compile(re.escape(start) + r"(.*?)" + re.escape(end), re.S)
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing markers: {start} / {end}")
    return f"{start}{match.group(1)}{end}"


def _is_relative_link(link: str) -> bool:
    return (
        bool(link)
        and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link)
        and not link.startswith("#")
        and not link.startswith("//")
    )


def _validate_local_link(errors: list[str], badge_id: str, base_dir: Path, link: str) -> None:
    if not _is_relative_link(link):
        return

    parsed = urlsplit(link)
    local_path = parsed.path
    if not local_path:
        return

    target = (base_dir / local_path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        errors.append(f"badge {badge_id} resolves outside repository root: {link}")
        return

    if not target.exists():
        errors.append(f"badge {badge_id} has missing local link target: {link}")


def _expanded_demos_badges(cfg: dict) -> list[dict]:
    from scripts.generate_readme_badges import _find_badge

    merged: list[dict] = []
    for entry in cfg["demos_readme"]["badges"]:
        if isinstance(entry, str):
            badge = dict(_find_badge(cfg, entry))
        else:
            badge = dict(_find_badge(cfg, entry["id"]))
            if "link" in entry:
                badge["link"] = entry["link"]
        merged.append(badge)
    return merged


def main() -> int:
    errors: list[str] = []

    config = json.loads(BADGE_CONFIG.read_text(encoding="utf-8"))
    required = set(config["readme"]["required_badges"])
    available = {badge["id"] for badge in config["readme"]["badges"]}

    missing = sorted(required - available)
    if missing:
        errors.append(f"release/badges.json missing required badge definitions: {', '.join(missing)}")

    release_target = config["release_target"]
    release_badge = next(
        (badge for badge in config["readme"]["badges"] if badge.get("id") == "release-posture"),
        None,
    )
    if not release_badge:
        errors.append("release/badges.json missing release-posture badge definition")
    else:
        if release_badge.get("kind") != "static":
            errors.append("release-posture badge must be static")
        if release_badge.get("message") != release_target:
            errors.append(
                "release-posture badge message does not match release_target in release/badges.json"
            )
        if release_target not in release_badge.get("alt", ""):
            errors.append(
                "release-posture badge alt text does not include release_target in release/badges.json"
            )

    for badge in config["readme"]["badges"]:
        link = badge.get("link", "")
        if not link:
            errors.append(f"badge {badge['id']} missing link")
            continue
        _validate_local_link(errors, badge["id"], ROOT, link)
        if badge["kind"] == "workflow":
            workflow = badge["workflow"]
            if not (WORKFLOW_DIR / workflow).exists():
                errors.append(f"badge {badge['id']} references missing workflow file: {workflow}")

    demos_badges = _expanded_demos_badges(config)
    for badge in demos_badges:
        link = badge.get("link", "")
        if not link:
            errors.append(f"demos badge {badge['id']} missing link")
            continue
        _validate_local_link(errors, f"demos:{badge['id']}", ROOT / "demos", link)

    from scripts.generate_readme_badges import (
        DEMOS_MARKERS as GEN_DEMOS_MARKERS,
        README_MARKERS as GEN_README_MARKERS,
        _badge_markdown,
        _find_badge,
        _load_config,
        _render_block,
    )

    repo = "MontrealAI/alpha-nova-seeds"
    style = config["style"]
    cfg = _load_config()

    readme_lines = [
        _badge_markdown(repo, style, badge)
        for badge in cfg["readme"]["badges"]
        if badge["id"] != "latest-rc"
    ]
    readme_lines.append(_badge_markdown(repo, style, _find_badge(cfg, "latest-rc")))
    expected_readme = _render_block(readme_lines, *GEN_README_MARKERS)

    demos_lines = [_badge_markdown(repo, style, badge) for badge in _expanded_demos_badges(cfg)]
    expected_demos = _render_block(demos_lines, *GEN_DEMOS_MARKERS)

    try:
        actual_readme = _extract_marked_block(README.read_text(encoding="utf-8"), README_MARKERS)
        actual_demos = _extract_marked_block(DEMOS_README.read_text(encoding="utf-8"), DEMOS_MARKERS)
    except ValueError as exc:
        errors.append(str(exc))
        actual_readme = ""
        actual_demos = ""

    if actual_readme != expected_readme:
        errors.append("README.md badge rail drift detected (run: python scripts/generate_readme_badges.py --write)")
    if actual_demos != expected_demos:
        errors.append("demos/README.md badge strip drift detected (run: python scripts/generate_readme_badges.py --write)")

    readme_text = README.read_text(encoding="utf-8")
    if release_target not in readme_text:
        errors.append(f"README.md missing active release target marker: {release_target}")

    if errors:
        print("FAIL: README badge validation failed")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PASS: README badge rails are in sync with release/badges.json")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
