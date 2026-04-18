# α-AGI Nova-Seeds

Nova-Seeds v2.6 is a **verifiable release candidate** focused on proof hardening.

> System framing: **α-AGI Insight → Nova-Seeds → MARK → Sovereigns**

## Release posture
- v2.5 established the foundational architecture.
- v2.6 RC strengthens proof, governance accounting visibility, and release provenance.
- v2.6 RC is **not** an audited final deployment.

## Constitutional order
All changes preserve this order:
1. identity
2. proof
3. settlement
4. governance

## Repository structure
- `contracts/` Solidity contracts and ABI exports
- `sdk/` threshold cryptography bindings
- `backend/` FastAPI + Postgres indexer and read models
- `dashboard/` operator pages and snapshot exports
- `schemas/` canonical versioned JSON schemas
- `docs/` operator and release runbooks

## v2.6 RC operator quickstart
1. Apply SQL migrations (`backend/migrations/001_init.sql`, `backend/migrations/002_v26_hardening.sql`).
2. Start backend and run deterministic indexer backfill.
3. Load dashboard and validate governance/proof pages.
4. Generate and verify release artifacts and attestations.

See:
- `docs/verify-release.md`
- `docs/threshold-attestation-lifecycle.md`
- `docs/reviewer-stake-accounting.md`
- `docs/council-seat-lifecycle.md`
- `docs/green-path.md`
