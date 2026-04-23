#!/usr/bin/env python3
"""Check README badge rails against release/badges.json truth."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

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


def _validate_http_link(errors: list[str], badge_id: str, link: str, timeout: float = 8.0) -> None:
    parsed = urlsplit(link)
    if parsed.scheme not in {"http", "https"}:
        return

    req = Request(link, method="HEAD", headers={"User-Agent": "alpha-nova-seeds-badge-check/1.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            if response.status >= 400:
                errors.append(f"badge {badge_id} link returned HTTP {response.status}: {link}")
    except HTTPError as exc:
        if exc.code in {405, 403}:
            # Some hosts block HEAD; retry with GET.
            get_req = Request(link, method="GET", headers={"User-Agent": "alpha-nova-seeds-badge-check/1.0"})
            try:
                with urlopen(get_req, timeout=timeout) as response:
                    if response.status >= 400:
                        errors.append(f"badge {badge_id} link returned HTTP {response.status}: {link}")
            except Exception as get_exc:  # pragma: no cover - defensive
                errors.append(f"badge {badge_id} link check failed for {link}: {get_exc}")
            return
        errors.append(f"badge {badge_id} link returned HTTP {exc.code}: {link}")
    except URLError as exc:
        errors.append(f"badge {badge_id} link check failed for {link}: {exc}")


def _validate_workflow_badge_link(errors: list[str], badge: dict) -> None:
    badge_id = badge["id"]
    workflow = badge["workflow"]
    link = badge.get("link", "")
    parsed = urlsplit(link)
    expected_path = f"/MontrealAI/alpha-nova-seeds/actions/workflows/{workflow}"

    if parsed.scheme != "https" or parsed.netloc != "github.com":
        errors.append(
            f"badge {badge_id} workflow link must be a GitHub Actions workflow URL for {workflow}: {link}"
        )
        return

    if parsed.path != expected_path:
        errors.append(
            f"badge {badge_id} workflow link path mismatch: expected {expected_path}, got {parsed.path}"
        )


def _expanded_demos_badges(cfg: dict) -> list[dict]:
    from scripts.generate_readme_badges import _expand_row_entries

    rows = cfg["demos_readme"].get("rows")
    if not rows:
        rows = [{"badges": cfg["demos_readme"].get("badges", [])}]

    merged: list[dict] = []
    for row in rows:
        merged.extend(_expand_row_entries(cfg, row["badges"]))
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-http-links",
        action="store_true",
        help="also validate HTTP/HTTPS badge targets with lightweight requests",
    )
    args = parser.parse_args()

    errors: list[str] = []

    config = json.loads(BADGE_CONFIG.read_text(encoding="utf-8"))
    required = set(config["readme"]["required_badges"])
    available = {badge["id"] for badge in config["readme"]["badges"]}

    missing = sorted(required - available)
    if missing:
        errors.append(f"release/badges.json missing required badge definitions: {', '.join(missing)}")

    rows = config["readme"].get("rows", [])
    if not rows:
        errors.append("release/badges.json readme.rows is missing or empty")
    else:
        expected_labels = {"Operational trust rail", "Orientation rail"}
        present_labels = {row.get("label", "") for row in rows}
        missing_labels = sorted(label for label in expected_labels if label not in present_labels)
        if missing_labels:
            errors.append(
                "release/badges.json readme.rows missing required row labels: "
                + ", ".join(missing_labels)
            )

        rendered_badge_ids: set[str] = set()
        for idx, row in enumerate(rows, start=1):
            if not row.get("badges"):
                errors.append(f"readme row {idx} has no badges")
                continue
            row_badge_ids: list[str] = []
            for entry in row["badges"]:
                badge_id = entry if isinstance(entry, str) else entry.get("id")
                if not badge_id:
                    errors.append(f"readme row {idx} contains a badge entry with no id")
                    continue
                if badge_id not in available:
                    errors.append(
                        f"readme row {idx} references unknown badge id: {badge_id}"
                    )
                    continue
                row_badge_ids.append(badge_id)
                rendered_badge_ids.add(badge_id)

            duplicates = sorted({badge_id for badge_id in row_badge_ids if row_badge_ids.count(badge_id) > 1})
            if duplicates:
                errors.append(
                    f"readme row {idx} contains duplicate badge ids: {', '.join(duplicates)}"
                )

        missing_from_rows = sorted(required - rendered_badge_ids)
        if missing_from_rows:
            errors.append(
                "release/badges.json readme.rows does not render all required_badges: "
                + ", ".join(missing_from_rows)
            )

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
        if args.check_http_links:
            _validate_http_link(errors, badge["id"], link)
        if badge["kind"] == "workflow":
            workflow = badge["workflow"]
            if not (WORKFLOW_DIR / workflow).exists():
                errors.append(f"badge {badge['id']} references missing workflow file: {workflow}")
            _validate_workflow_badge_link(errors, badge)

    demos_badges = _expanded_demos_badges(config)
    for badge in demos_badges:
        link = badge.get("link", "")
        if not link:
            errors.append(f"demos badge {badge['id']} missing link")
            continue
        _validate_local_link(errors, f"demos:{badge['id']}", ROOT / "demos", link)
        if args.check_http_links:
            _validate_http_link(errors, f"demos:{badge['id']}", link)

    from scripts.generate_readme_badges import (
        DEMOS_MARKERS as GEN_DEMOS_MARKERS,
        README_MARKERS as GEN_README_MARKERS,
        _load_config,
        _render_block,
        _render_rows,
    )

    repo = "MontrealAI/alpha-nova-seeds"
    style = config["style"]
    cfg = _load_config()

    readme_rows = cfg["readme"].get("rows")
    if not readme_rows:
        readme_rows = [{"badges": [badge["id"] for badge in cfg["readme"]["badges"]]}]
    try:
        expected_readme = _render_block(_render_rows(cfg, readme_rows, repo, style), *GEN_README_MARKERS)
    except KeyError as exc:
        errors.append(f"unable to render README badge rows due to unknown badge id: {exc}")
        expected_readme = ""

    demos_rows = cfg["demos_readme"].get("rows")
    if not demos_rows:
        demos_rows = [{"badges": cfg["demos_readme"].get("badges", [])}]
    try:
        expected_demos = _render_block(_render_rows(cfg, demos_rows, repo, style), *GEN_DEMOS_MARKERS)
    except KeyError as exc:
        errors.append(f"unable to render demos badge rows due to unknown badge id: {exc}")
        expected_demos = ""

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
    if args.check_http_links:
        print("PASS: badge HTTP/HTTPS link checks succeeded")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
