#!/usr/bin/env python3
"""Validate deterministic artifact contract for demos/open-ended-rsi-system outputs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos" / "open-ended-rsi-system"
OUT = DEMO / "out"

REQUIRED = [
    "capability_genome.json",
    "manifest.json",
    "generation_0.json",
    "generation_1.json",
    "generation_2.json",
    "assay_bundle.json",
    "lineage.json",
    "frontier_queue.json",
    "intervention_log.json",
    "scorecard.json",
    "claim_boundary.json",
    "determinism_fingerprint.json",
    "safety_gates.json",
    "summary.md",
    "proof_docket.md",
    "provenance_manifest.json",
    "board_report.html",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    missing = [name for name in REQUIRED if not (OUT / name).exists()]
    if missing:
        print("FAIL: missing required out artifacts:")
        for item in missing:
            print(f"  - {item}")
        return 1

    g0 = load_json(OUT / "generation_0.json")
    g1 = load_json(OUT / "generation_1.json")
    g2 = load_json(OUT / "generation_2.json")
    score = load_json(OUT / "scorecard.json")
    gates = load_json(OUT / "safety_gates.json")

    if not (g2["human_intervention_touches"] < g1["human_intervention_touches"] < g0["human_intervention_touches"]):
        print("FAIL: human intervention touches are not strictly descending g0 > g1 > g2")
        return 1

    observed = score["observed"]
    thresholds = score["thresholds"]
    checks = {
        "aoy_uplift": observed["aoy_uplift"] >= thresholds["aoy_uplift_min"],
        "speed_uplift": observed["speed_uplift"] >= thresholds["speed_uplift_min"],
        "rework_reduction": observed["rework_reduction"] >= thresholds["rework_reduction_min"],
        "evidence_completeness_uplift": observed["evidence_completeness_uplift"] >= thresholds["evidence_uplift_min"],
        "package_dependence": observed["package_dependence"] >= thresholds["package_dependence_min"],
        "no_safety_regression": observed["no_safety_regression"] is True,
    }
    failing = [k for k, ok in checks.items() if not ok]
    if failing:
        print(f"FAIL: threshold checks failed: {', '.join(failing)}")
        return 1

    bad_gates = [k for k, v in gates.items() if v.get("status") != "pass"]
    if bad_gates:
        print(f"FAIL: doctrine safety gates not all pass: {', '.join(bad_gates)}")
        return 1

    print("PASS: open-ended-rsi artifact contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
