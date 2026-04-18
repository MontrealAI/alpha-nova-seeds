import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_registry_abi_exports_release_metadata_and_review_flow():
    abi = json.loads((ROOT / "contracts/abi/NovaSeedRegistryV26RC.abi.json").read_text())
    function_names = {entry["name"] for entry in abi if entry.get("type") == "function"}
    event_names = {entry["name"] for entry in abi if entry.get("type") == "event"}
    assert "RELEASE_VERSION" in function_names
    assert "RELEASE_METADATA_HASH" in function_names
    assert "draftSeed" in function_names
    assert "submitReview" in function_names
    assert "SovereignRegistered" in event_names
