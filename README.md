# α-AGI Nova-Seeds

**Verifiable release-candidate infrastructure for sovereign opportunity formation.**

> Current milestone focus: **proof hardening** over rhetoric expansion.

**Latest candidate:** `v2.6.0-rc1`  
**Previous architecture baseline:** `v2.5`

---

## System framing

`α-AGI Insight → Nova-Seeds → MARK → Sovereigns`

Constitutional stack order preserved in this repository:

1. identity
2. proof
3. settlement
4. governance

---

## Repository map

- `contracts/` — Solidity identity/proof/governance contracts
- `sdk/` — threshold cryptography bindings
- `backend/` — FastAPI + Postgres indexer/read API
- `dashboard/` — operator UI and snapshot exports
- `docs/` — release verification, trust model, threat model, proof docket shell

---

## v2.6 RC highlights

- Root repository contract docs (`CONTRIBUTING`, `SECURITY`, `SUPPORT`, `RELEASES`, `CHANGELOG`, `CODEOWNERS`).
- Release provenance workflow with source artifact, SBOM, attestations, and `SHA256SUMS`.
- Contract hardening for release metadata and deterministic reviewer/council accounting visibility.
- Canonical versioned threshold schemas and round-trip examples.
- Backend hardening: migrations, idempotent + reorg-safe cursoring, health/readiness/metrics/OpenAPI export, deterministic backfill command.
- Dashboard hardening for seeds/rounds/reviewer ledger/council seats/lineage/provenance/alerts plus JSON and PNG snapshot export.

---

## Quickstart

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Dashboard

Serve `dashboard/` with any static file server while backend runs on `localhost:8000`.

---

## Release verification

Use `docs/verify-release.md` for exact local verification commands.

---

## Release-candidate status

This repository state is for verifiable RC operation and review. It does not assert completed audit or final production deployment.
