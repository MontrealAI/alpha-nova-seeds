# Releases

## v2.6.0-rc1 (candidate)

### Acceptance criteria
- Root repository governance docs exist and are consistent.
- Release provenance workflow emits source bundle, hashes, SBOM, and attestations.
- Contracts expose release metadata, ABI export, and hardened governance/reviewer accounting surfaces.
- Threshold attestation and binding profile examples are promoted into canonical v2.6 schemas with validation tests.
- Backend includes versioned migrations, idempotent/reorg-safe ingestion cursoring, readiness/health/metrics endpoints, deterministic backfill command, and OpenAPI export path.
- Dashboard provides operator pages for seeds, rounds, reviewer ledger, council seats, lineage, provenance, and alerts/disputes plus JSON/PNG snapshot export.
- Trust and threat docs plus proof docket shell are present.

### Migration notes
1. Apply SQL migrations in order:
   - `backend/migrations/001_init.sql`
   - `backend/migrations/002_indexer_cursor.sql`
   - `backend/migrations/003_governance_accounting.sql`
2. Refresh backend ABI artifacts from `contracts/abi/` if contract interfaces change.
3. Update indexer env:
   - `CONFIRMATIONS` (default 12)
   - `INDEXER_NAME` (default `registry_v25`)

### Provenance artifacts
- GitHub Actions workflow: `.github/workflows/release-provenance.yml`
- Verification guide: `docs/verify-release.md`

### Rollback notes
- Revert deployment to prior immutable image/tag.
- Reset indexer cursor in `indexer_cursors` to the previous known-good block.
- Re-run deterministic backfill for the rollback window to restore materialized state.
