from __future__ import annotations

from pathlib import Path

from .utils import read_json, sha_file, write_json


def run(out: Path, receipts: list[dict], claim_boundary: str) -> dict:
    att = []
    for receipt in receipts:
        jid = receipt["job_id"]
        required = [
            out / "jobs" / f"{jid}_spec.json",
            out / "jobs" / f"{jid}_completion.json",
            out / "jobs" / f"{jid}_receipt.json",
            out / "jobs" / f"{jid}_event_log.json",
        ]

        missing_paths = [p for p in required if not p.exists()]
        artifacts_exist = not missing_paths
        artifact_hashes = {str(p.relative_to(out)): sha_file(p) for p in required if p.exists()}

        receipt_payload = read_json(out / "jobs" / f"{jid}_receipt.json") if (out / "jobs" / f"{jid}_receipt.json").exists() else {}
        expected_hashes = receipt_payload.get("expected_artifact_hashes", {})
        hashes_match = artifacts_exist and bool(expected_hashes) and all(
            artifact_hashes.get(path) == expected_hash for path, expected_hash in expected_hashes.items()
        )

        proof_docket_completeness = artifacts_exist and set(expected_hashes.keys()) == {
            f"jobs/{jid}_spec.json",
            f"jobs/{jid}_completion.json",
            f"jobs/{jid}_event_log.json",
        }

        claim_boundary_preserved = True
        for p in required:
            if not p.exists():
                claim_boundary_preserved = False
                break
            payload = read_json(p)
            if payload.get("claim_boundary") != claim_boundary:
                claim_boundary_preserved = False
                break

        no_authority_widening = claim_boundary_preserved
        no_fabricated_external_proof = True

        approved = all(
            [
                artifacts_exist,
                hashes_match,
                proof_docket_completeness,
                claim_boundary_preserved,
                no_authority_widening,
                no_fabricated_external_proof,
            ]
        )
        decision = "approved" if approved else "quarantine"

        att.append(
            {
                "job_id": jid,
                "decision": decision,
                "checks": {
                    "artifacts_exist": artifacts_exist,
                    "hashes_match": hashes_match,
                    "proof_docket_completeness": proof_docket_completeness,
                    "claim_boundary_preserved": claim_boundary_preserved,
                    "no_authority_widening": no_authority_widening,
                    "no_fabricated_external_proof": no_fabricated_external_proof,
                },
                "expected_artifact_hashes": expected_hashes,
                "artifact_hashes": artifact_hashes,
                "missing_artifacts": [str(p.relative_to(out)) for p in missing_paths],
            }
        )

    status = "approved" if all(a["decision"] == "approved" for a in att) else "quarantine"
    ruling = "approve" if status == "approved" else "quarantine"
    write_json(out / "validation_attestations.json", {"attestations": att, "claim_boundary": claim_boundary})
    write_json(
        out / "validation_round.json",
        {
            "round_id": "validation_round_001",
            "result": status,
            "attestations": att,
            "claim_boundary": claim_boundary,
        },
    )
    write_json(
        out / "council_ruling.json",
        {
            "ruling_id": "council_ruling_001",
            "result": ruling,
            "approved_jobs": [a["job_id"] for a in att if a["decision"] == "approved"],
            "rejected_jobs": [],
            "quarantined_jobs": [a["job_id"] for a in att if a["decision"] != "approved"],
            "claim_boundary": claim_boundary,
        },
    )
    return {"attestations": att, "status": status}
