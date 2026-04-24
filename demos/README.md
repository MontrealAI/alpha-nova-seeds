# Demo Ladder (v2.8.0-rc.7 target)

<!-- DEMO_BADGE_STRIP_START -->
**Demo ladder strip**
[![Release posture: v2.8.0-rc.7](https://img.shields.io/badge/release-v2.8.0-rc.7-1f6feb?style=flat-square)](../RELEASES.md) [![Flagship protocol correctness demo](https://img.shields.io/badge/flagship%20demo-protocol%20correctness-0e8a16?style=flat-square)](./protocol_smart_contract_correctness_demo/README.md) [![Ascension runtime local/devnet demo](https://img.shields.io/badge/ascension%20runtime-local%2Fdevnet%20MVA-0e8a16?style=flat-square)](./ascension-runtime/README.md) [![Proof-first bounded release candidate posture](https://img.shields.io/badge/claim%20boundary-proof-first%20bounded%20RC-6f42c1?style=flat-square)](../docs/FRONTIER_LAB_POSTURE.md)
<!-- DEMO_BADGE_STRIP_END -->

This folder is the canonical demo ladder for the protocol-correctness wedge and its adjacent expansion surfaces.

The four surfaces are intentionally separated so reviewers can distinguish:
- **what is flagship synthetic wedge evidence**
- **what is compact adjacent synthetic replay**
- **what is real-world experiment material**
- **what is accelerating-loop demonstration across bounded autonomy phases**


## 0) Ascension runtime (organism reference runtime)

- Path: [`./ascension-runtime/`](./ascension-runtime/)
- Role: bounded local/devnet organism reference runtime across Insight → Archive/next loop
- Run: `python3 demos/ascension-runtime/run_demo.py --assert`
- Proves: deterministic local replay with machine-readable artifacts for each Ascension layer
- Does not prove: audited-final deployment, live DEX/marketplace, mainnet settlement, or completed live Ascension

## 1) Flagship synthetic wedge demo (primary front door)

- Path: [`./protocol_smart_contract_correctness_demo/`](./protocol_smart_contract_correctness_demo/)
- Role: best public/operator entry point
- Run: `python3 demos/protocol_smart_contract_correctness_demo/run_demo.py --assert`
- Proves: deterministic wedge mechanics (winner selection, frozen package, adjacent control-vs-treatment gate, sovereign PASS/FAIL emission)
- Does not prove: live external validity or broad cybersecurity sovereign realization

## 2) Adjacent synthetic proof demo (compact replay)

- Path: [`./adjacent_mandate_reuse_proof_demo/`](./adjacent_mandate_reuse_proof_demo/)
- Role: compact synthetic adjacent proof replay
- Run: `python3 demos/adjacent_mandate_reuse_proof_demo/run_demo.py`
- Proves: minimal threshold-gate structure and synthetic measurement pattern
- Does not prove: real-world compounding correctness

## 3) Real-world proof pack (operator execution)

- Path: [`./adjacent_mandate_reuse_proof_real_v1/`](./adjacent_mandate_reuse_proof_real_v1/)
- Role: controlled real-world experiment templates
- Run (scorecard helper): `python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py`
- Proves: only when executed with blinded real-world data and published proof-docket artifacts

## 4) Accelerating-loop demo (bounded-to-expanding-to-more-autonomous)

- Path: [`./open-ended-rsi-system/`](./open-ended-rsi-system/)
- Role: flagship-class accelerating-loop demonstration with governed package heredity, frontier queue autonomy, and board-ready proof outputs
- Run: `python3 demos/open-ended-rsi-system/run_demo.py --assert`
- Operate: [`./open-ended-rsi-system/RUNBOOK.md`](./open-ended-rsi-system/RUNBOOK.md)
- Proves: deterministic three-generation loop mechanics with frozen package reuse and bounded autonomous adjacent selection
- Does not prove: unrestricted autonomy, literal unbounded RSI, or full broad sovereign realization

Legacy compatibility surface:
- [`./unbounded-rsi-system/`](./unbounded-rsi-system/) remains available for historical replay.

## Doctrine context

- [`../docs/DOCTRINE_STACK.md`](../docs/DOCTRINE_STACK.md)
- [`../docs/THERMODYNAMIC_MODEL.md`](../docs/THERMODYNAMIC_MODEL.md)
- [`../docs/NATION_STATE_DOCTRINE.md`](../docs/NATION_STATE_DOCTRINE.md)
- [`../docs/DEMO_STRATEGY.md`](../docs/DEMO_STRATEGY.md)
- [`../docs/FRONTIER_LAB_POSTURE.md`](../docs/FRONTIER_LAB_POSTURE.md)

## Claim boundary

This ladder supports narrow RC claims:

- protocol correctness can be formalized, replayed, settled, and archived as compounding capability under controlled synthetic conditions.
- an early accelerating loop can be demonstrated in bounded synthetic conditions with explicit governance gates.

It does **not** claim:

- a completed broad cybersecurity sovereign,
- final real-world external proof,
- audited-final deployment posture,
- unrestricted autonomy or literal unbounded recursive self-improvement.

Compatibility label: Real-world experiment pack.


## 5) Ascension live runtime demo (bounded local/devnet, legacy compatibility surface)

- Path: [`./ascension-live-runtime/`](./ascension-live-runtime/)
- Role: end-to-end bounded organism loop across Insight → Archive with machine-readable receipts
- Run: `python3 demos/ascension-live-runtime/run_demo.py --assert`
- Proves: deterministic local/devnet loop with seed selection, job competition, validation, settlement ledgering, archive lineage, and architect recommendation
- Does not prove: audited-final deployment, mainnet safety, real external-market settlement, or completed α‑AGI Ascension
