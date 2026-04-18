import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]


def _load(path: str):
    return json.loads((ROOT / path).read_text())


def test_decryption_attestation_example_validates():
    schema = _load("schemas/threshold/v2.6/decryption-attestation.schema.json")
    example = _load("examples/v2.6/decryption_attestation.json")
    example.pop("schemaVersion", None)
    jsonschema.validate(instance=example, schema=schema)


def test_threshold_binding_example_validates():
    schema = _load("schemas/threshold/v2.6/threshold-binding-profile.schema.json")
    example = _load("examples/v2.6/threshold_binding_profile.json")
    example.pop("schemaVersion", None)
    jsonschema.validate(instance=example, schema=schema)
