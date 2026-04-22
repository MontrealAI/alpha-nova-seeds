# α‑AGI Nova‑Seeds (v2.7.0-rc.2 posture)

Nova‑Seeds are **sealed venture blueprints for sovereign opportunity formation**.

This repository is maintained as a **verifiable release candidate** and **production-grade starter architecture** — not as an audited final deployment.

System framing:

`α‑AGI Insight → Nova‑Seeds → MARK → Sovereigns`

Operational doctrine:

1. identity
2. proof
3. settlement
4. governance

---

## What this repository contains

- `contracts/` — Solidity contracts for seed identity, registry, governance, workflow/challenge policy, reviewer treasury, and council mechanics.
- `sdk/` — threshold-cryptography bindings and typed payload helpers.
- `backend/` — FastAPI + Postgres indexer and proof/governance APIs.
- `dashboard/` — operator UI for seed, governance, and provenance visibility.
- `schemas/` — canonical versioned JSON schemas.
- `docs/` — trust model, threat model, green path, proof docket, and release verification guidance.
- `release/` — release-check surfaces and RC hardening notes.

---

## Release posture (April 22, 2026)

- Current target posture: **v2.7.0-rc.2 flagship demo + operator UI + doctrine verifiable release candidate**.
- SemVer target is **v2.7.0-rc.2** because `v2.7.0-rc.1` already exists and this batch adds new additive hardening surfaces (flagship UX polish, operator dashboard clarity, and release checklist refinement), not a stable GA cut.
- Latest generally referenced milestone in earlier docs: **v2.5 foundational architecture release**.
- This repo deliberately avoids claims such as “audited”, “final”, “mainnet-safe by default”, or “fully proven compounding substrate”.

What is currently represented as real:

- architectural substrate across contracts + SDK + backend + dashboard
- explicit governance and verification doctrine
- additive hardening for provenance, operator visibility, and deterministic indexing

What is not claimed as proven here:

- final security assurance from an external audit
- fully deployed production guarantees
- evidence of adjacent-mandate compounding reuse beyond the proof shells in this repo

---


## Front-door demo ladder (protocol correctness wedge)

Start here for the public/operator walkthrough of the first wedge:

- [`demos/protocol_smart_contract_correctness_demo/`](./demos/protocol_smart_contract_correctness_demo/)

This flagship demo is synthetic, deterministic, and replayable. It explains how a Protocol Cybersecurity Studio can freeze reusable capability packages and test adjacent-mandate uplift under strict control-vs-treatment thresholds.

Demo ladder index: [`demos/README.md`](./demos/README.md)

Complementary demos:
- [`demos/adjacent_mandate_reuse_proof_demo/`](./demos/adjacent_mandate_reuse_proof_demo/) — compact synthetic adjacent proof demo
- [`demos/adjacent_mandate_reuse_proof_real_v1/`](./demos/adjacent_mandate_reuse_proof_real_v1/) — real-world controlled experiment pack

Doctrine stack:
- [`docs/DOCTRINE_STACK.md`](./docs/DOCTRINE_STACK.md)
- [`docs/THERMODYNAMIC_MODEL.md`](./docs/THERMODYNAMIC_MODEL.md)
- [`docs/NATION_STATE_DOCTRINE.md`](./docs/NATION_STATE_DOCTRINE.md)
- [`docs/DEMO_STRATEGY.md`](./docs/DEMO_STRATEGY.md)
- [`docs/RELEASE_POSITIONING.md`](./docs/RELEASE_POSITIONING.md)

---

## Core operating docs

- [AGENTS.md](./AGENTS.md) — repository operating contract for maintainers and agents
- [CONTRIBUTING.md](./CONTRIBUTING.md) — contribution workflow and PR checklist
- [SECURITY.md](./SECURITY.md) — reporting and triage policy
- [SUPPORT.md](./SUPPORT.md) — support expectations
- [RELEASES.md](./RELEASES.md) — release contract and flow
- [CHANGELOG.md](./CHANGELOG.md) — version history

---

## Verification-first docs

- [Mainnet deployment runbook](./docs/mainnet-deployment.md)
- [Operator handoff checklist](./docs/operator-handoff.md)
- [Verify deployment artifacts](./docs/verify-deployment.md)
- [Verify release artifacts](./docs/verify-release.md)
- [Trust model](./docs/trust-model.md)
- [Threat model](./docs/threat-model.md)
- [Green path](./docs/green-path.md)
- [Proof docket template](./docs/proof-docket-template/)
- [Threshold attestation lifecycle](./docs/threshold-attestation-lifecycle.md)
- [Council seat lifecycle](./docs/council-seat-lifecycle.md)
- [Reviewer stake accounting](./docs/reviewer-stake-accounting.md)

---

## Quick local verification

```bash
# backend tests
pytest -q backend/tests

# backend OpenAPI export
python backend/scripts/export_openapi.py

# SDK typecheck/build
cd sdk && npm run build --if-present && cd -

# doctrine + equation consistency
python scripts/check_math_markdown.py
python scripts/check_doctrine_consistency.py
python scripts/check_demo_links.py
```

For full RC artifact verification (checksums + attestation + SBOM), follow [`docs/verify-release.md`](./docs/verify-release.md).
