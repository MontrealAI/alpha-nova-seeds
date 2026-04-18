#!/usr/bin/env python3
"""Generate deterministic provenance manifest for release candidate artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

INCLUDE_GLOBS = [
    "contracts/*.sol",
    "contracts/interfaces/*.sol",
    "contracts/abi/*.json",
    "backend/migrations/*.sql",
    "backend/app/**/*.py",
    "sdk/**/*.ts",
    "docs/**/*.md",
    "schemas/**/*.json",
    "example_*_v25.json",
    "README.md",
    "CHANGELOG.md",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def iter_files() -> list[Path]:
    seen: set[Path] = set()
    files: list[Path] = []
    for pattern in INCLUDE_GLOBS:
        for p in sorted(REPO_ROOT.glob(pattern)):
            if p.is_file() and p not in seen:
                seen.add(p)
                files.append(p)
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    manifest = {
        "release_tag": args.tag,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/release/generate_provenance_manifest.py",
        "files": [],
    }

    for fp in iter_files():
        rel = fp.relative_to(REPO_ROOT).as_posix()
        manifest["files"].append(
            {
                "path": rel,
                "size_bytes": fp.stat().st_size,
                "sha256": sha256_file(fp),
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
