# α-AGI Nova-Seeds

**Sealed venture blueprints for sovereign opportunity formation.**

This repository now tracks **v2.6.0-rc.1**, a **verifiable release candidate** focused on proof surfaces and release provenance.

> System framing: **α-AGI Insight → Nova-Seeds → MARK → Sovereigns**

## Doctrine

Nova-Seeds implementation order remains:

1. **identity**
2. **proof**
3. **settlement**
4. **governance**

## Repository structure

- `contracts/` — Solidity identity/proof/governance contracts
- `sdk/` — threshold cryptography bindings + typed payload helpers
- `backend/` — FastAPI + Postgres indexer and proof/governance APIs
- `dashboard/` — operator dashboard and snapshots
- `schemas/` — versioned canonical JSON schemas (v2.6)
- `docs/` — trust, threat, verification, and proof docket guidance
- `release/` — release checklist and implementation plans

## v2.6 RC highlights

- Root repository contract docs (`CONTRIBUTING`, `SECURITY`, `SUPPORT`, `RELEASES`, `CHANGELOG`, `CODEOWNERS`).
- Release provenance workflow: source archive, SHA256SUMS, SBOM, and attestations.
- Canonical threshold schema surfaces + lifecycle documentation.
- Governance accounting visibility for reviewer stake and council seat lifecycle.
- Backend hardening: readiness, metrics, idempotent/reorg-safe indexing, deterministic backfill.
- Dashboard hardening: proof/governance/operator pages and snapshot export.
- Trust/proof documentation and docket templates.

## Verify release artifacts

Use `docs/verify-release.md` after running the release provenance workflow.

## Important posture

v2.6 is an RC hardening release. It does **not** claim to be audited final deployment.
