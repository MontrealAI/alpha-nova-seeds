#!/usr/bin/env python3
"""Normalize lane output artifacts into public-safe blinded reviewer packets."""

from __future__ import annotations

import argparse
import json
import shutil
import hashlib
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = PACK_ROOT / "results_blinded_adjacent_transfer_v1"
DEFAULT_PRIVATE = PACK_ROOT / "local_private_blinding_materials" / "results_blinded_adjacent_transfer_v1"

ALLOWED_FILENAMES = {
    "findings.md",
    "tests.md",
    "evidence_index.json",
    "repro_steps.md",
    "notes.md",
}
DISALLOWED_PATTERNS = [
    "operator",
    "kit blue",
    "kit gold",
    "control",
    "treatment",
]


def sanitize_text(text: str) -> str:
    output = text
    for pattern in DISALLOWED_PATTERNS:
        output = output.replace(pattern, "[redacted]")
        output = output.replace(pattern.title(), "[redacted]")
        output = output.replace(pattern.upper(), "[redacted]")
    return output


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_lane(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    copied = 0
    for name in sorted(ALLOWED_FILENAMES):
        in_file = src / name
        if not in_file.exists():
            continue
        out_file = dst / name
        text = in_file.read_text(encoding="utf-8")
        out_file.write_text(sanitize_text(text), encoding="utf-8")
        copied += 1
    (dst / "README.md").write_text(
        "# Normalized blinded reviewer packet\n\n"
        "This packet intentionally excludes operator identity, explicit lane type labels, "
        "and private assignment metadata.\n",
        encoding="utf-8",
    )
    print(f"Normalized {copied} files from {src} -> {dst}")


def refresh_public_provenance(results_dir: Path) -> None:
    manifest_path = results_dir / "provenance_manifest.json"
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    hashes = []
    for item in manifest.get("file_hashes", []):
        rel = item.get("path")
        if not rel:
            continue
        p = results_dir / rel
        if p.exists():
            hashes.append({"path": rel, "sha256": sha256_file(p)})
    manifest["file_hashes"] = hashes
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS))
    parser.add_argument("--private-dir", default=str(DEFAULT_PRIVATE))
    parser.add_argument("--stage", choices=["stage_a", "stage_b"], default="stage_a")
    parser.add_argument("--force", action="store_true", help="overwrite existing normalized packet files")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    private_dir = Path(args.private_dir)

    if args.stage == "stage_a":
        src_blue = private_dir / "raw_packets" / "stage_a" / "lane_blue"
        src_gold = private_dir / "raw_packets" / "stage_a" / "lane_gold"
    else:
        src_blue = private_dir / "raw_packets" / "stage_b" / "lane_blue"
        src_gold = private_dir / "raw_packets" / "stage_b" / "lane_gold"

    dst_blue = results_dir / "lane_blue_packet_public" / args.stage
    dst_gold = results_dir / "lane_gold_packet_public" / args.stage

    if args.force:
        for dst in [dst_blue, dst_gold]:
            if dst.exists():
                shutil.rmtree(dst)

    for src in [src_blue, src_gold]:
        src.mkdir(parents=True, exist_ok=True)

    normalize_lane(src_blue, dst_blue)
    normalize_lane(src_gold, dst_gold)
    refresh_public_provenance(results_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
