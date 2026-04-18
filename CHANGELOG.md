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
  - Council lifecycle indexing now records real seat identifiers from governance events.
  - Reviewer/governance read-model indexing now includes required event ABIs.
  - Provenance manifest timestamp is deterministic (commit time / SOURCE_DATE_EPOCH), not wall-clock.
  - Registry ABI snapshot export now includes review/quarantine events used by governance indexing.
  - Challenge/deactivation lifecycle attribution now uses causal seat-occupant lookups.
  - Challenge resolution rewinds now remain reorg-safe by updating resolution block markers.
  - Release provenance workflow now archives the requested release tag ref instead of branch HEAD.
  - Challenge creation block is immutable; resolution uses a separate resolved block marker for rewind safety.
  - Release provenance checkout now uses the requested tag ref so manifest/SBOM match archived source.
  - Council active seat read-model now treats challenged seats as active until deactivation.
  - Release provenance bundle now includes deterministic OpenAPI export for API-surface verification.
