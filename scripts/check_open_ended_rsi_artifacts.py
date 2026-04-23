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
    "mandate3_execution.json",
    "assay_bundle.json",
    "lineage.json",
    "frontier_queue.json",
    "intervention_log.json",
    "scorecard.json",
    "board_scorecard.json",
    "board_scorecard.md",
    "governance_ruling.json",
    "chronicle_entry.json",
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
    execution = load_json(OUT / "mandate3_execution.json")
    score = load_json(OUT / "scorecard.json")
    board = load_json(OUT / "board_scorecard.json")
    governance_ruling = load_json(OUT / "governance_ruling.json")
    gates = load_json(OUT / "safety_gates.json")
    provenance = load_json(OUT / "provenance_manifest.json")

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

    ranked = g2.get("frontier_queue", [])
    if not ranked:
        print("FAIL: generation_2 frontier queue is empty")
        return 1
    if g2["selected_domain"]["domain"] != ranked[0]["domain"]:
        print("FAIL: selected domain does not match top-ranked frontier domain")
        return 1

    if execution.get("domain") != g2["selected_domain"]["domain"]:
        print("FAIL: mandate3_execution domain does not match generation_2 selected domain")
        return 1
    if execution.get("offline_only") is not True:
        print("FAIL: mandate3_execution offline_only must be true")
        return 1
    if execution.get("simulated") is not True:
        print("FAIL: mandate3_execution simulated flag must be true")
        return 1
    if len(execution.get("steps", [])) < 3:
        print("FAIL: mandate3_execution must include at least 3 execution steps")
        return 1

    guards = provenance.get("determinism_guards", {})
    if guards.get("network_calls") != "disabled" or guards.get("external_apis") != "disabled":
        print("FAIL: provenance determinism guards must disable network and external APIs")
        return 1

    board_observed = board.get("observed", {})
    observed_keys = [
        "aoy_uplift",
        "speed_uplift",
        "rework_reduction",
        "evidence_completeness_uplift",
        "no_safety_regression",
        "package_dependence",
    ]
    mismatched_observed = [
        key for key in observed_keys if board_observed.get(key) != observed.get(key)
    ]
    if mismatched_observed:
        print(
            "FAIL: board_scorecard observed metrics mismatch scorecard observed metrics:"
            f" {', '.join(mismatched_observed)}"
        )
        return 1

    expected_gates = [
        "no_value_without_evidence",
        "no_autonomy_without_authority",
        "no_settlement_without_validation",
    ]
    config = load_json(DEMO / "config.json")
    forbidden_from_config = config.get("authority_scope", {}).get("may_not", [])
    ruling_release = governance_ruling.get("release_target")
    score_release = score.get("release_target")
    if ruling_release != score_release:
        print("FAIL: governance_ruling release_target must match scorecard release_target")
        return 1
    if governance_ruling.get("decision") != "approved_for_rc_demo_surface":
        print("FAIL: governance_ruling decision must be approved_for_rc_demo_surface")
        return 1
    if governance_ruling.get("authority_scope_validated") is not True:
        print("FAIL: governance_ruling authority_scope_validated must be true")
        return 1
    gates_required = governance_ruling.get("safety_gates_required", [])
    if sorted(gates_required) != sorted(expected_gates):
        print("FAIL: governance_ruling safety_gates_required must match doctrine gate contract")
        return 1
    missing_gate_artifacts = [gate for gate in expected_gates if gate not in gates]
    if missing_gate_artifacts:
        print(
            "FAIL: governance_ruling references doctrine gates missing from safety_gates.json:"
            f" {', '.join(missing_gate_artifacts)}"
        )
        return 1
    forbidden_actions = governance_ruling.get("forbidden_actions", [])
    if sorted(forbidden_actions) != sorted(forbidden_from_config):
        print("FAIL: governance_ruling forbidden_actions must match config authority_scope.may_not")
        return 1
    if not str(governance_ruling.get("notes", "")).strip():
        print("FAIL: governance_ruling notes must be non-empty")
        return 1

    print("PASS: open-ended-rsi artifact contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
