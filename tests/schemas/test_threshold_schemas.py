import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HEX32 = re.compile(r"^0x[a-fA-F0-9]{64}$")


def _load(path: str):
    return json.loads((ROOT / path).read_text())


def test_decryption_example_round_trip_fields():
    example = _load("docs/examples/v2.6/decryption-attestation.example.json")
    assert HEX32.match(example["requestId"])
    assert HEX32.match(example["seedId"])
    assert HEX32.match(example["plaintextHash"])
    assert HEX32.match(example["completionHash"])
    assert example["termId"].isdigit()
    assert example["deadline"].isdigit()
    assert example["signer"].startswith("0x") and len(example["signer"]) == 42


def test_threshold_profile_example_round_trip_fields():
    example = _load("docs/examples/v2.6/threshold-binding-profile.example.json")
    assert HEX32.match(example["profileId"])
    assert example["committeeSize"] >= example["threshold"] >= 1
    assert example["timeoutSeconds"] > 0


def test_schema_files_present_and_versioned():
    d_schema = _load("docs/schemas/v2.6/decryption-attestation.schema.json")
    p_schema = _load("docs/schemas/v2.6/threshold-binding-profile.schema.json")
    assert d_schema["title"].endswith("V26")
    assert p_schema["title"].endswith("V26")
