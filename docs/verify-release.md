# Verify a v2.6 release candidate

This guide verifies that the release artifacts were produced from repository source and include provenance signals.

## Prerequisites

- `gh` CLI authenticated
- `sha256sum`
- `jq`

## 1) Download provenance artifact bundle

```bash
gh run download <RUN_ID> --name v26-provenance-<TAG> --dir ./verify-dist
```

Expected files in `verify-dist/`:
- `alpha-nova-seeds-<TAG>.tar.gz`
- `provenance-manifest-<TAG>.json`
- `sbom-<TAG>.spdx.json`
- `SHA256SUMS`

## 2) Verify checksums

```bash
cd verify-dist
sha256sum -c SHA256SUMS
```

All entries must show `OK`.

## 3) Validate manifest structure

```bash
jq -e '.release_tag and .generated_at_utc and (.files | length > 0)' provenance-manifest-<TAG>.json
jq -e '.files[] | select(.path and .sha256 and .size_bytes)' provenance-manifest-<TAG>.json >/dev/null
```

## 4) Verify source tarball contains expected tracked files

```bash
tar -tzf alpha-nova-seeds-<TAG>.tar.gz | head -n 20
```

## 5) Verify GitHub attestation exists

```bash
gh attestation verify alpha-nova-seeds-<TAG>.tar.gz --repo MontrealAI/alpha-nova-seeds
```

## Operator note

This verification flow proves artifact integrity/provenance signals for an RC. It does **not** claim final audit coverage.
