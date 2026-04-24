from __future__ import annotations

from pathlib import Path

from .utils import write_json


def run(cfg: dict, out: Path, jobs: list[dict], assignments: list[dict], claim_boundary: str) -> list[dict]:
    receipts = []
    for job in jobs:
        selection = next(a for a in assignments if a["job_id"] == job["job_id"])
        spec = {**job, "claim_boundary": claim_boundary}
        completion = {
            "job_id": job["job_id"],
            "selected_agent": selection["selected_agent"],
            "status": "completed",
            "proof_docket": [
                f"jobs/{job['job_id']}_spec.json",
                f"jobs/{job['job_id']}_completion.json",
            ],
            "claim_boundary": claim_boundary,
        }
        receipt = {
            "job_id": job["job_id"],
            "receipt_id": f"{job['job_id']}_receipt",
            "status": "pending_validation",
            "settlement_unit": cfg["bounty_unit"],
            "bounty_units": job["bounty_placeholder"]["units"],
            "claim_boundary": claim_boundary,
        }
        log = {
            "job_id": job["job_id"],
            "events": ["created", "assigned", "completed", "pending_validation"],
            "claim_boundary": claim_boundary,
        }
        write_json(out / "jobs" / f"{job['job_id']}_spec.json", spec)
        write_json(out / "jobs" / f"{job['job_id']}_completion.json", completion)
        write_json(out / "jobs" / f"{job['job_id']}_receipt.json", receipt)
        write_json(out / "jobs" / f"{job['job_id']}_event_log.json", log)
        receipts.append(receipt)
    return receipts
