# Changelog

## [v2.6.0-rc.1] - 2026-04-18

### Added
- Root repository contract docs: contribution, security, support, release policy, changelog, and code owners.
- Release provenance workflows for source artifacts, SHA256SUMS, SBOM generation, and artifact attestations.
- Verification guide at `docs/verify-release.md`.
- Canonical threshold schemas and validation tests for decryption attestations and threshold bindings.
- Governance accounting docs and backend query surfaces for reviewer ledger and council seat lifecycle.
- Backend hardening: versioned migration, idempotent/reorg-safe indexer cursor, readiness, metrics, OpenAPI export, and deterministic backfill command.
- Dashboard hardening with proof/governance sections, alert views, and JSON/PNG snapshot export.
- Trust/proof docs and public proof docket template shell.

### Changed
- `README.md` updated for v2.6 RC verification and proof-first milestone framing.
- Contracts received NatSpec interface comments and release metadata surface constants.

### Notes
- This release is a **verifiable release candidate**, not an audited final deployment.
- Follow-up fixes applied after initial RC patch:
  - CI now uses `npm install` when no lockfile is present.
  - Reorg rewind now also clears derived governance rows.
  - Migration view DDL updated for PostgreSQL compatibility.
  - FastAPI `List` typing import fixed to avoid startup error.
