# Verify a v2.7 release candidate

This guide verifies that the release artifacts were produced from repository source and include provenance signals.

## Prerequisites

- `gh` CLI authenticated
- `sha256sum`
- `jq`
- Python 3.11+

## 1) Reproduce local verification surfaces (recommended before downloading artifacts)

Run these commands from a clean checkout at the release tag:

```bash
git checkout <TAG>
python scripts/contracts/export_abi.py
python backend/scripts/export_openapi.py
python scripts/release/generate_provenance_manifest.py --tag <TAG> --output /tmp/provenance-manifest-<TAG>.json
pytest -q backend/tests
```

Expected outputs:
- ABI snapshots updated in `contracts/abi/`
- OpenAPI document at `dist/openapi-v2.6.0-rc.1.json`
- Local provenance manifest at `/tmp/provenance-manifest-<TAG>.json`
- Passing backend/schema regression tests

## 2) Download provenance artifact bundle

> Note: the workflow artifact name remains `v26-provenance-<TAG>` in `.github/workflows/release-provenance.yml`.

```bash
gh run download <RUN_ID> --name v26-provenance-<TAG> --dir ./verify-dist
```

Expected files in `verify-dist/`:
- `alpha-nova-seeds-<TAG>.tar.gz`
- `provenance-manifest-<TAG>.json`
- `sbom-<TAG>.spdx.json`
- `openapi-v2.6.0-rc.1.json`
- `SHA256SUMS`

## 3) Verify checksums

```bash
cd verify-dist
sha256sum -c SHA256SUMS
```

All entries must show `OK`.

## 4) Validate manifest structure

```bash
jq -e '.release_tag and .generated_at_utc and (.files | length > 0)' provenance-manifest-<TAG>.json
jq -e '.files[] | select(.path and .sha256 and .size_bytes)' provenance-manifest-<TAG>.json >/dev/null
```

## 5) Verify source tarball contains expected tracked files

```bash
tar -tzf alpha-nova-seeds-<TAG>.tar.gz | head -n 20
```

## 6) Validate OpenAPI release surface

```bash
jq -e '.info.version == "2.6.0-rc.1"' openapi-v2.6.0-rc.1.json
jq -e '.paths["/ready"] and .paths["/metrics"] and .paths["/governance/reviewer-ledger"]' openapi-v2.6.0-rc.1.json
```

## 7) Verify GitHub attestation exists

```bash
gh attestation verify alpha-nova-seeds-<TAG>.tar.gz --repo MontrealAI/alpha-nova-seeds
```

## Operator note

This verification flow proves artifact integrity/provenance signals for an RC. It does **not** claim final audit coverage.


## v2.7 demo-and-doctrine checks

```bash
python3 demos/protocol_smart_contract_correctness_demo/run_demo.py --assert
python3 demos/adjacent_mandate_reuse_proof_demo/run_demo.py
python3 scripts/check_math_markdown.py
python3 scripts/check_doctrine_consistency.py
```

These checks ensure demo determinism, cross-demo replayability, and canonical GitHub math rendering posture.
