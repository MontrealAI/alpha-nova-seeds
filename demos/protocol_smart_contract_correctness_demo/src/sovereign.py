from __future__ import annotations
from datetime import datetime, timezone
from .utils import write_json


def emit_sovereign_or_ruling(scorecard: dict, protocol_pack: dict, out_dir):
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if scorecard["passes"]["adjacent_mandate_proof"]:
        artifact = {
            "id": "ProtocolAssuranceSovereign-v1.synthetic",
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
        write_json(out_dir / "ProtocolAssuranceSovereign-v1.synthetic.json", artifact)
        return artifact

    ruling = {
        "id": "ProtocolAssuranceSovereign-v1.fail_closed_ruling",
        "type": "governance_ruling",
        "status": "blocked",
        "reason": "Adjacent-mandate proof thresholds not met.",
        "failed_thresholds": [k for k, ok in scorecard["passes"].items() if not ok],
        "timestamp": now,
        "disclaimer": "Fail-closed synthetic ruling for replayability."
    }
    write_json(out_dir / "ProtocolAssuranceSovereign-v1.fail_closed.json", ruling)
    return ruling
