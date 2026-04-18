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
**Sealed venture blueprints for sovereign opportunity formation — enabling machine-driven evolution of enterprise systems at production scale.**

> AGI ALPHA evolves sovereign opportunities the way directed evolution evolves enzymes: from working parents, through variant generation, real-world selection, and compounding capability formation.

**Explore:** [🔮 α‑AGI MARK](./docs/alpha-agi-mark.md) · [📦 Latest release](https://github.com/MontrealAI/alpha-nova-seeds/releases/latest)

---

## What this is

Nova-Seeds are **cryptographically sealed enterprise embryos**:

- foresight genomes
- execution FusionPlans
- governance and validation pathways
- promotion into α-AGI Sovereigns

This repository contains the **production-grade architecture (v2.5)**.

---

## System Overview

`α-AGI Insight → Nova-Seeds → MARK → Sovereigns`

- **Insight** identifies high-leverage AGI opportunities
- **Nova-Seeds** encode them as sealed venture blueprints
- **MARK** evaluates, prices, and selects
- **Sovereigns** execute through real economic workflows

---

## Architecture

> 🎖️ **α‑AGI Insight** — identifies high‑leverage AGI opportunities<br>
> ↓<br>
> 🌱 **Nova‑Seeds** — sealed venture blueprints<br>
> ↓<br>
> 🔮 **MARK** — selection, pricing, and sovereign formation<br>
> ↓<br>
> 🔱 **Sovereigns** — execution-layer enterprises<br>
> ↓<br>
> 📜 **α‑AGI Jobs** → 👾 **Agents** → ✅ **Validators**<br>
> ↓<br>
> ⚙️ **Architect** — continuous optimisation

---

## Repository Structure

- **contracts/** — smart contracts (identity, registry, governance)
- **sdk/** — threshold cryptography bindings
- **backend/** — FastAPI + Postgres indexer
- **dashboard/** — operator interface

---

## Why this matters

This system enables:

- programmable formation of sovereign enterprises
- validator-gated economic execution
- compounding capability through iterative selection
- a new substrate for machine-driven innovation

Nova-Seeds are not ideas — they are **evolvable economic structures**.

---

## Version

Initial import of Nova-Seeds v2.5 architecture.
