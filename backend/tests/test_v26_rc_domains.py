import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_seed_identity_surface_exists_in_registry_abi():
    abi = json.loads((ROOT / "contracts/abi/NovaSeedRegistryV26RC.abi.json").read_text())
    names = {x.get("name") for x in abi}
    assert "draftSeed" in names
    assert "sealSeed" in names


def test_governance_accounting_docs_present():
    assert (ROOT / "docs/reviewer-stake-accounting.md").exists()
    assert (ROOT / "docs/council-seat-lifecycle.md").exists()


def test_threshold_attestation_docs_and_schemas_present():
    assert (ROOT / "docs/threshold-attestation-lifecycle.md").exists()
    assert (ROOT / "schemas/threshold/v2.6/decryption-attestation.schema.json").exists()
    assert (ROOT / "schemas/threshold/v2.6/threshold-binding-profile.schema.json").exists()


def test_reviewer_stake_and_council_lifecycle_views_in_migration():
    sql = (ROOT / "backend/migrations/002_v26_hardening.sql").read_text()
    assert "reviewer_stake_ledger_v26" in sql
    assert "council_seat_lifecycle_v26" in sql
