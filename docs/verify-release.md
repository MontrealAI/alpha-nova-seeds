# Verify v2.6 Release Candidate Artifacts

This document verifies a **release candidate**. It does not claim audited final deployment.

## 1) Download workflow artifacts

From GitHub Actions, download artifact bundle named `release-provenance`.

Expected files:
- `alpha-nova-seeds-<tag-or-snapshot>.tar.gz`
- `SHA256SUMS`
- `sbom.spdx.json`

## 2) Verify SHA256 digest

```bash
sha256sum -c SHA256SUMS
```

Expected output:

```text
alpha-nova-seeds-<...>.tar.gz: OK
```

## 3) Verify source archive contents deterministically

```bash
mkdir -p /tmp/nova-release-check
cd /tmp/nova-release-check
tar -xzf /path/to/alpha-nova-seeds-<...>.tar.gz
find . -type f | sort > extracted-file-list.txt
sha256sum extracted-file-list.txt
```

Record `sha256(extracted-file-list.txt)` in release notes for reproducibility.

## 4) Inspect SBOM

```bash
jq '.spdxVersion, .creationInfo.created' sbom.spdx.json
jq '.packages | length' sbom.spdx.json
```

## 5) Validate canonical threshold schemas against examples

```bash
python3 -m json.tool docs/examples/v2.6/decryption-attestation.example.json >/dev/null
python3 -m json.tool docs/examples/v2.6/threshold-binding-profile.example.json >/dev/null
pytest -q tests/schemas/test_threshold_schemas.py
```

## 6) Verify backend operational surfaces

```bash
cd backend
python3 -m uvicorn app.main:app --port 8000
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/readiness
curl -s http://127.0.0.1:8000/metrics
curl -s http://127.0.0.1:8000/openapi.json | jq '.info.version'
```

## 7) Verify OpenAPI export command

```bash
cd backend
python3 scripts/export_openapi.py
ls -l openapi.json
```
