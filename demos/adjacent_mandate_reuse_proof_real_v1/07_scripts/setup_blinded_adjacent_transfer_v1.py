#!/usr/bin/env python3
"""Initialize blinded adjacent-transfer result scaffolding with prereg freeze metadata.

This script creates a public-safe results bundle and a local-private workspace
for blinding materials. It does not fabricate reviewer inputs or scores.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACK_ROOT = Path(__file__).resolve().parents[1]

MANDATE_1_SCOPE = [
    "contracts/CouncilGovernanceV25.sol",
    "contracts/ChallengePolicyModuleV25.sol",
]
MANDATE_2_SCOPE = [
    "contracts/ThresholdNetworkAdapterV25.sol",
    "contracts/SignedAttestationVerifierV25.sol",
]
MANDATE_3_SCOPE = [
    "backend/app/main.py",
    "backend/app/indexer.py",
    "backend/app/schemas.py",
]


def run(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd or ROOT), text=True).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_text(src: Path, dst: Path) -> None:
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir",
        default="results_blinded_adjacent_transfer_v1",
        help="results directory name under the proof-pack root",
    )
    parser.add_argument(
        "--private-dir",
        default="local_private_blinding_materials/results_blinded_adjacent_transfer_v1",
        help="private local-only directory under proof-pack root",
    )
    parser.add_argument("--force", action="store_true", help="overwrite existing results dir")
    args = parser.parse_args()

    results_dir = PACK_ROOT / args.results_dir
    private_dir = PACK_ROOT / args.private_dir

    if results_dir.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing {results_dir}; use --force to replace.")
    if results_dir.exists() and args.force:
        shutil.rmtree(results_dir)

    (results_dir / "lane_blue_packet_public").mkdir(parents=True)
    (results_dir / "lane_gold_packet_public").mkdir(parents=True)
    (results_dir / "scorecard_outputs").mkdir(parents=True)
    private_dir.mkdir(parents=True, exist_ok=True)

    repo_sha = run(["git", "rev-parse", "HEAD"])
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    freeze_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    scope_hashes: dict[str, str] = {}
    for rel in MANDATE_1_SCOPE + MANDATE_2_SCOPE + MANDATE_3_SCOPE:
        scope_hashes[rel] = sha256_file(ROOT / rel)

    experiment_manifest = {
        "experiment_id": "adjacent-mandate-reuse-real-v1-blinded-adjacent-transfer",
        "repo": "MontrealAI/alpha-nova-seeds",
        "repo_sha": repo_sha,
        "branch": branch,
        "target_path": "demos/adjacent_mandate_reuse_proof_real_v1",
        "execution_results_path": str(results_dir.relative_to(ROOT)),
        "vertical": "protocol-and-smart-contract-correctness",
        "publication_rule": "publish_result_whether_pass_or_fail",
        "stopping_rule": "stop_after_stage_a_if_any_threshold_fails_or_if_human_blinded_inputs_missing",
        "mandate_1": {
            "name": "Governance / dispute correctness",
            "scope": MANDATE_1_SCOPE,
            "goal": "Produce GovernanceValidationPack-v1",
        },
        "mandate_2": {
            "name": "Threshold / attestation correctness",
            "scope": MANDATE_2_SCOPE,
            "goal": "Measure adjacent-mandate reuse under blinded control vs treatment",
        },
        "mandate_3": {
            "name": "Backend / API correctness",
            "scope": MANDATE_3_SCOPE,
            "goal": "Conditional Stage B cross-domain transfer test",
            "status": "conditional_on_real_stage_a_pass",
        },
        "reviewers_blinded": True,
        "control_and_treatment_parallel": True,
        "human_intervention_logging_required": True,
        "wall_clock_budget_per_lane_minutes": 180,
        "compute_budget_per_lane": {
            "machine_class": "same-machine-class-required",
            "max_test_runs": "set-by-sponsor-before-run",
            "max_command_count": "set-by-sponsor-before-run",
            "network": "disallowed",
        },
        "out_of_scope_issue_types": [
            "non-deterministic cosmetic refactors",
            "out-of-scope architecture redesign",
            "claims beyond protocol-correctness wedge",
        ],
        "allowed_tools_and_commands": [
            "local shell tooling only",
            "repo-native scripts and tests",
            "scorecard helper: python3 07_scripts/calculate_q2_scorecard.py",
        ],
        "intervention_policy": "log all exceptions in intervention log; symmetry across lanes required",
        "pass_thresholds": {
            "aoy_uplift_min_pct": 35,
            "speed_uplift_min_pct": 30,
            "rework_reduction_min_pct": 40,
            "evidence_completeness_uplift_min_pct": 20,
            "safety_regression_allowed": False,
            "package_dependence_min_pct": 30,
        },
        "freeze_time_utc": freeze_time,
    }

    environment_lock = {
        "python_version": sys.version.split()[0],
        "os": platform.platform(),
        "tool_versions": {
            "slither": "NA",
            "foundry": "NA",
            "hardhat": "NA",
            "node": run(["node", "--version"]) if shutil.which("node") else "NA",
        },
        "repo_sha": repo_sha,
        "branch": branch,
        "scope_hashes": scope_hashes,
        "allowed_human_interventions": [
            "budget approval",
            "policy clarification",
            "exception handling only",
        ],
    }

    (results_dir / "prereg_experiment_manifest.json").write_text(
        json.dumps(experiment_manifest, indent=2) + "\n", encoding="utf-8"
    )
    (results_dir / "environment_lock.json").write_text(
        json.dumps(environment_lock, indent=2) + "\n", encoding="utf-8"
    )

    copy_text(PACK_ROOT / "02_execution" / "run_register.template.csv", results_dir / "run_register.csv")
    copy_text(
        PACK_ROOT / "02_execution" / "intervention_log.template.csv",
        results_dir / "intervention_log.csv",
    )

    copy_text(PACK_ROOT / "04_scorecard" / "run_costs.template.csv", results_dir / "scorecard_outputs" / "run_costs.csv")
    copy_text(
        PACK_ROOT / "04_scorecard" / "output_scoring.template.csv",
        results_dir / "scorecard_outputs" / "output_scoring.csv",
    )
    copy_text(
        PACK_ROOT / "04_scorecard" / "package_dependence_ledger.template.csv",
        results_dir / "scorecard_outputs" / "package_dependence_ledger.csv",
    )

    write_csv(
        private_dir / "blinded_assignment_map.private.csv",
        ["artifact_set", "blinded_lane_id", "actual_lane", "kit_variant", "revealed_after_score_lock"],
        [["stage_a_mandate_2", "Lane Blue", "REPLACE", "REPLACE", "false"]],
    )
    write_csv(
        private_dir / "reviewer_identity_map.private.csv",
        ["reviewer_id", "legal_name_or_org", "contact", "role_constraints"],
        [["R1", "REPLACE", "REPLACE", "cannot_be_blinding_officer_or_scorecard_custodian"]],
    )

    private_answer = (
        "# Private answer key\n\n"
        "This file is private and must not be committed publicly.\n\n"
        "## Mandate scope\n- REPLACE\n\n"
        "## Accept criteria\n- REPLACE\n"
    )
    for name in ["answer_key_m1.private.md", "answer_key_m2.private.md", "answer_key_m3.private.md"]:
        (private_dir / name).write_text(private_answer, encoding="utf-8")

    (private_dir / "private_commitment_hashes.txt").write_text(
        "# Run 07_scripts/generate_private_commitment_hashes.py after private files are finalized.\n",
        encoding="utf-8",
    )

    print(f"Initialized public-safe results scaffold: {results_dir}")
    print(f"Initialized private local-only scaffold: {private_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
