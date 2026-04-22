# α‑AGI Nova‑Seeds (v2.8.0-rc.2 target posture)

Nova‑Seeds are **sealed venture blueprints for sovereign opportunity formation**.

This repository is maintained as a **verifiable release candidate** and **production-grade starter architecture** — not an audited final deployment.

System framing:

`α‑AGI Insight → Nova‑Seeds → MARK → Sovereigns`

Constitutional order:

1. identity
2. proof
3. settlement
4. governance

Invariant:

- no value without evidence
- no autonomy without authority
- no settlement without validation

---

## Release posture (April 22, 2026)

- Current RC target: **v2.8.0-rc.2** (promoted from active unpublished v2.8.0-rc.1 after additive accelerating-loop hardening).
- This is a **new release-candidate cut** after v2.7.0-rc.2, focused on front-door coherence, flagship/demo ladder polish, doctrine legibility, and operator UX hardening.
- This RC remains proof-first and bounded: synthetic flagship evidence is strengthened; broader sovereign claims remain future-facing.

### What is represented as real today

- Contracts + SDK + backend + dashboard architecture for identity/proof/settlement/governance.
- Deterministic synthetic flagship wedge with replayable artifact production.
- Release/doctrine surfaces that can be reviewed from a clean machine.

### What is explicitly not claimed

- audited final deployment
- default mainnet safety guarantees
- completed real-world adjacent-mandate external proof
- proven broad cybersecurity sovereign operation

---

## Front-door orientation (start here)

### 1) Flagship demo (primary front door)

- [`demos/protocol_smart_contract_correctness_demo/`](./demos/protocol_smart_contract_correctness_demo/)
- Why this wedge first: strongest verification, fastest replay, objective evidence density, commercially legible mandate category.
- Output: deterministic winner selection, frozen capability package, adjacent control-vs-treatment scorecard, PASS/FAIL sovereign gate.

### 2) Demo ladder index

- [`demos/README.md`](./demos/README.md)
- Clarifies role boundaries across:
  - [`demos/adjacent_mandate_reuse_proof_demo/`](./demos/adjacent_mandate_reuse_proof_demo/)
  - [`demos/adjacent_mandate_reuse_proof_real_v1/`](./demos/adjacent_mandate_reuse_proof_real_v1/)
  - [`demos/open-ended-rsi-system/`](./demos/open-ended-rsi-system/)
  - [`demos/unbounded-rsi-system/`](./demos/unbounded-rsi-system/)
  - flagship synthetic wedge demo
  - compact synthetic adjacent proof demo
  - real-world experiment pack
  - accelerating-loop demo

### 3) Accelerating-loop demo

- [`demos/open-ended-rsi-system/`](./demos/open-ended-rsi-system/)
- Purpose: bounded proof-of-mechanism for bounded → expanding → increasingly autonomous loop with explicit DISCO/Arnold mode alternation.
- Output: deterministic package freeze/hash, control-vs-treatment scorecard, bounded autonomous mandate-3 selection, board-ready report artifacts.
- Compatibility: prior surface remains at [`demos/unbounded-rsi-system/`](./demos/unbounded-rsi-system/).

### 4) Doctrine stack

- [`docs/DOCTRINE_STACK.md`](./docs/DOCTRINE_STACK.md)
- [`docs/THERMODYNAMIC_MODEL.md`](./docs/THERMODYNAMIC_MODEL.md)
- [`docs/NATION_STATE_DOCTRINE.md`](./docs/NATION_STATE_DOCTRINE.md)
- [`docs/DEMO_STRATEGY.md`](./docs/DEMO_STRATEGY.md)
- [`docs/RELEASE_POSITIONING.md`](./docs/RELEASE_POSITIONING.md)
- [`docs/FRONTIER_LAB_POSTURE.md`](./docs/FRONTIER_LAB_POSTURE.md)

---

## Proof ladder and next milestone

Protocol correctness is the first narrow organ:

🌱💫 **α‑AGI Protocol Cybersecurity Sovereign 🔐** (synthetic wedge claim)

Future-facing target (not yet proven by this RC):

👑 **α‑AGI Cybersecurity Sovereign 🔱✨**

Next real milestone remains unchanged:

- one completed mandate
- one frozen capability package
- one adjacent mandate
- control vs treatment
- scorecard with predeclared thresholds

Adjacent-mandate threshold gate:

- ≥35% AOY uplift
- ≥30% faster time to first accepted output
- ≥40% lower repair/rework
- ≥20% better evidence completeness
- no safety regression
- ≥30% accepted treatment outputs depending on the frozen package

---

## Repository map

- `contracts/` — Solidity identity/registry/governance/workflow/challenge/treasury/council surfaces
- `sdk/` — threshold crypto bindings + typed payload helpers
- `backend/` — FastAPI + Postgres indexer and proof/governance APIs
- `dashboard/` — operator dashboard for proof, lineage, and release visibility
- `schemas/` — canonical versioned JSON schemas
- `docs/` — doctrine, trust/threat model, verification guides, proof-docket guidance
- `demos/` — flagship/synthetic/real-world proof ladder
- `release/` — RC checklists and release-hardening notes

---

## Verification-first docs

- [Verify release artifacts](./docs/verify-release.md)
- [Trust model](./docs/trust-model.md)
- [Threat model](./docs/threat-model.md)
- [Green path](./docs/green-path.md)
- [Proof docket template](./docs/proof-docket-template/)

---

## Quick local verification

```bash
pytest -q backend/tests
python backend/scripts/export_openapi.py
python scripts/contracts/export_abi.py
cd sdk && npm run build --if-present && cd -
python scripts/check_math_markdown.py
python scripts/check_doctrine_consistency.py
python scripts/check_demo_links.py
python3 demos/protocol_smart_contract_correctness_demo/run_demo.py --assert
python3 demos/open-ended-rsi-system/run_demo.py --assert
python3 demos/unbounded-rsi-system/run_demo.py --assert
```

For full provenance verification (checksums, SBOM, attestations), use [`docs/verify-release.md`](./docs/verify-release.md).
