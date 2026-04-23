# α‑AGI Nova‑Seeds (v2.8.0-rc.3 posture)

<!-- BADGE_RAIL_START -->
**Operational trust rail**
[![Release posture: v2.8.0-rc.3](https://img.shields.io/badge/release-v2.8.0-rc.3-1f6feb?style=flat-square)](./RELEASES.md) [![CI workflow status](https://github.com/MontrealAI/alpha-nova-seeds/actions/workflows/ci.yml/badge.svg?style=flat-square)](https://github.com/MontrealAI/alpha-nova-seeds/actions/workflows/ci.yml) [![Contracts security workflow status](https://github.com/MontrealAI/alpha-nova-seeds/actions/workflows/contracts-security.yml/badge.svg?style=flat-square)](https://github.com/MontrealAI/alpha-nova-seeds/actions/workflows/contracts-security.yml) [![Release provenance workflow status](https://github.com/MontrealAI/alpha-nova-seeds/actions/workflows/release-provenance.yml/badge.svg?style=flat-square)](https://github.com/MontrealAI/alpha-nova-seeds/actions/workflows/release-provenance.yml)
**Orientation rail**
[![Proof-first bounded release candidate posture](https://img.shields.io/badge/claim%20boundary-proof-first%20bounded%20RC-6f42c1?style=flat-square)](./docs/FRONTIER_LAB_POSTURE.md) [![Flagship protocol correctness demo](https://img.shields.io/badge/flagship%20demo-protocol%20correctness-0e8a16?style=flat-square)](./demos/protocol_smart_contract_correctness_demo/README.md) [![Demo ladder index](https://img.shields.io/badge/demo%20ladder-entry-0e8a16?style=flat-square)](./demos/README.md) [![Accelerating-loop demo](https://img.shields.io/badge/accelerating%20loop-open-ended%20RSI-0e8a16?style=flat-square)](./demos/open-ended-rsi-system/README.md) [![Doctrine stack](https://img.shields.io/badge/doctrine-stack-8250df?style=flat-square)](./docs/DOCTRINE_STACK.md)
<!-- BADGE_RAIL_END -->

Nova‑Seeds are **sealed venture blueprints for sovereign opportunity formation**. This repository is a **verifiable release candidate** for identity → proof → settlement → governance coordination infrastructure; it is **not** represented as an audited final deployment or default mainnet-safe system.

System framing: `α‑AGI Insight → Nova‑Seeds → MARK → Sovereigns`

## Front door (start in 90 seconds)

- **What this is:** a proof-first architecture spanning Solidity contracts, SDK bindings, FastAPI/Postgres indexing, operator dashboard surfaces, and deterministic demo evidence ladders.
- **What is real today:** deterministic synthetic flagship wedge replay, bounded accelerating-loop replay, release provenance workflows, and verifiable RC documentation.
- **What is not claimed:** audited-final deployment, completed broad sovereign realization, unrestricted autonomy, or external real-world validity by default.
- **Current RC target:** **v2.8.0-rc.3** (additive hardening cut; prior RC history remains in `CHANGELOG.md` / `RELEASES.md`).

## Immediate paths

1. **Flagship wedge (primary entry):** [`demos/protocol_smart_contract_correctness_demo/`](./demos/protocol_smart_contract_correctness_demo/)
2. **Demo ladder index:** [`demos/README.md`](./demos/README.md)
3. **Accelerating-loop demo (bounded):** [`demos/open-ended-rsi-system/`](./demos/open-ended-rsi-system/)
4. **Doctrine stack:** [`docs/DOCTRINE_STACK.md`](./docs/DOCTRINE_STACK.md)
5. **Release posture contract:** [`RELEASES.md`](./RELEASES.md)

Full ladder surfaces:
- [`demos/adjacent_mandate_reuse_proof_demo/`](./demos/adjacent_mandate_reuse_proof_demo/)
- [`demos/adjacent_mandate_reuse_proof_real_v1/`](./demos/adjacent_mandate_reuse_proof_real_v1/)
- [`demos/unbounded-rsi-system/`](./demos/unbounded-rsi-system/) *(legacy compatibility)*

## Doctrine stack

- [`docs/DOCTRINE_STACK.md`](./docs/DOCTRINE_STACK.md)
- [`docs/THERMODYNAMIC_MODEL.md`](./docs/THERMODYNAMIC_MODEL.md)
- [`docs/NATION_STATE_DOCTRINE.md`](./docs/NATION_STATE_DOCTRINE.md)
- [`docs/DEMO_STRATEGY.md`](./docs/DEMO_STRATEGY.md)
- [`docs/RELEASE_POSITIONING.md`](./docs/RELEASE_POSITIONING.md)
- [`docs/FRONTIER_LAB_POSTURE.md`](./docs/FRONTIER_LAB_POSTURE.md)

## Invariants (non-negotiable)

- no value without evidence
- no autonomy without authority
- no settlement without validation

## Release posture (April 23, 2026)

- Active release train: **v2.8.x verifiable release-candidate**.
- This cut advances front-door clarity, badge governance, and release-surface drift prevention.
- Proof remains bounded and explicit: synthetic deterministic evidence is strengthened; broad sovereign claims remain future-facing.

## Repository map

- `contracts/` — Solidity identity/registry/governance/workflow/challenge/treasury/council surfaces
- `sdk/` — threshold crypto bindings + typed payload helpers
- `backend/` — FastAPI + Postgres indexer and proof/governance APIs
- `dashboard/` — operator dashboard for proof, lineage, and release visibility
- `schemas/` — canonical versioned JSON schemas
- `docs/` — doctrine, trust/threat model, verification guides, proof-docket guidance
- `demos/` — flagship/synthetic/real-world proof ladder
- `release/` — RC checklists and release-hardening notes

## Verification-first docs

- [Verify release artifacts](./docs/verify-release.md)
- [Trust model](./docs/trust-model.md)
- [Threat model](./docs/threat-model.md)
- [Green path](./docs/green-path.md)
- [Proof docket template](./docs/proof-docket-template/)
- [Badge strategy](./docs/BADGE_STRATEGY.md)

## Quick local verification

```bash
pytest -q backend/tests
python backend/scripts/export_openapi.py
python scripts/contracts/export_abi.py
cd sdk && npm run build --if-present && cd -
python scripts/check_math_markdown.py
python scripts/check_doctrine_consistency.py
python scripts/check_demo_links.py
python scripts/check_release_surface_posture.py
python scripts/check_readme_badges.py
python scripts/check_open_ended_rsi_artifacts.py
python3 demos/protocol_smart_contract_correctness_demo/run_demo.py --assert
python3 demos/open-ended-rsi-system/run_demo.py --assert
python3 demos/unbounded-rsi-system/run_demo.py --assert  # legacy compatibility
```

For full provenance verification (checksums, SBOM, attestations), use [`docs/verify-release.md`](./docs/verify-release.md).
