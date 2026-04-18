# Verify a v2.6 release candidate

These commands verify that release artifacts are reproducible and untampered.

## 1) Build local artifacts
```bash
./scripts/release/build_artifacts.sh
./scripts/release/generate_sha256sums.sh
```

## 2) Verify checksums
```bash
cd release/artifacts
sha256sum -c SHA256SUMS
```

## 3) Verify source archive maps to commit
```bash
tar -tzf source/alpha-nova-seeds-<commit-sha>.tar.gz | head
```

## 4) Verify canonical payloads are present
```bash
ls -1 canonical/
```
Expected files:
- `NovaSeedRegistryV26RC.abi.json`
- `decryption-attestation.schema.json`
- `threshold-binding-profile.schema.json`
- `001_init.sql`
- `002_v26_hardening.sql`
- `verify-release.md`

## 5) Verify GitHub attestations (from workflow run)
Use GitHub CLI with repository permissions:
```bash
gh attestation verify \
  --repo MontrealAI/alpha-nova-seeds \
  --owner MontrealAI \
  release/artifacts/source/*
```

Repeat for `release/artifacts/canonical/*` and `release/artifacts/sbom.spdx.json`.

## Migration notes
1. Apply SQL migrations in order: `001_init.sql`, then `002_v26_hardening.sql`.
2. Deploy backend image with new readiness/metrics endpoints.
3. Run deterministic backfill once (see `backend/app/indexer.py`).

## Rollback notes
1. Stop indexer and API.
2. Roll back application image to previous version.
3. Keep migration schema, but disable v2.6-only endpoints if rollback requires compatibility mode.
4. Re-run indexer from previous safe cursor.
