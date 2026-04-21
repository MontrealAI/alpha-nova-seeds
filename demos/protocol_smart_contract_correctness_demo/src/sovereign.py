from __future__ import annotations
from .utils import write_json, demo_timestamp


def emit_sovereign_or_ruling(scorecard: dict, protocol_pack: dict, out_dir):
    now = demo_timestamp()
    if scorecard["passes"]["adjacent_mandate_proof"]:
        artifact = {
            "id": "ProtocolAssuranceSovereign-v1.synthetic.json",
            "type": "synthetic_sovereign_artifact",
            "status": "emitted",
            "depends_on": protocol_pack["id"],
            "package_hash": protocol_pack["package_hash"],
            "constitutional_order": ["identity", "proof", "settlement", "governance"],
            "invariant": [
                "no value without evidence",
                "no autonomy without authority",
                "no settlement without validation"
            ],
            "timestamp": now,
            "disclaimer": "Synthetic local demo artifact; not a real-world proof."
        }
        write_json(out_dir / artifact["id"], artifact)
        return artifact

    ruling = {
        "id": "ProtocolAssuranceSovereign-v1.fail_closed.json",
        "type": "governance_ruling",
        "status": "blocked",
        "reason": "Adjacent-mandate proof thresholds not met.",
        "failed_thresholds": [k for k, ok in scorecard["passes"].items() if not ok],
        "timestamp": now,
        "disclaimer": "Fail-closed synthetic ruling for replayability."
    }
    write_json(out_dir / ruling["id"], ruling)
    return ruling
