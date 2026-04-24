#!/usr/bin/env python3
"""Assemble a reveal-time receipt after score lock for blinded adjacent-transfer runs.

This helper is intentionally narrow:
- reads private blinded assignment map and commitment hashes from local-private storage
- emits a public-safe reveal receipt with only hashes + lane mapping metadata
- never publishes reviewer identity map or answer keys
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = PACK_ROOT / "results_blinded_adjacent_transfer_v1"
DEFAULT_PRIVATE = PACK_ROOT / "local_private_blinding_materials" / "results_blinded_adjacent_transfer_v1"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_assignment_map(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS))
    parser.add_argument("--private-dir", default=str(DEFAULT_PRIVATE))
    parser.add_argument(
        "--confirm-score-lock",
        action="store_true",
        help="required safety flag; indicates scorecard adjudication has been locked",
    )
    args = parser.parse_args()

    if not args.confirm_score_lock:
        raise SystemExit("Refusing reveal assembly without --confirm-score-lock")

    results_dir = Path(args.results_dir)
    private_dir = Path(args.private_dir)

    assignment_map = private_dir / "blinded_assignment_map.private.csv"
    commitment_hashes = private_dir / "private_commitment_hashes.txt"

    missing = [str(p) for p in [assignment_map, commitment_hashes] if not p.exists()]
    if missing:
        raise SystemExit("Missing required private files:\n- " + "\n- ".join(missing))

    mapping_rows = load_assignment_map(assignment_map)
    lanes_only = []
    for row in mapping_rows:
        lanes_only.append(
            {
                "lane_id": row.get("lane_id", ""),
                "assigned_kit": row.get("assigned_kit", ""),
                "assignment_role": row.get("assignment_role", ""),
            }
        )

    receipt = {
        "receipt_type": "blinded_adjacent_transfer_reveal_receipt",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "score_lock_confirmed": True,
        "private_assignment_map_sha256": sha256_file(assignment_map),
        "private_commitment_hashes_sha256": sha256_file(commitment_hashes),
        "lane_assignments": lanes_only,
        "notes": [
            "This receipt intentionally excludes reviewer identities and answer keys.",
            "Reveal should happen only after adjudication and scorecard lock.",
        ],
    }

    out_path = results_dir / "scorecard_outputs" / "reveal_receipt_public.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
