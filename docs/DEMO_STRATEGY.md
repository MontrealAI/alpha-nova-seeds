# Demo Strategy — v2.7.0-rc.1

This repository now presents a three-surface demo ladder for protocol correctness.

## 1) Flagship synthetic wedge demo (front door)

- Path: [`demos/protocol_smart_contract_correctness_demo/`](../demos/protocol_smart_contract_correctness_demo/)
- Role: public/operator flagship walkthrough
- Proves: deterministic synthetic control-vs-treatment protocol-correctness assay mechanics
- Does not prove: real-world compounding under live delivery conditions

## 2) Adjacent synthetic proof demo (compact)

- Path: [`demos/adjacent_mandate_reuse_proof_demo/`](../demos/adjacent_mandate_reuse_proof_demo/)
- Role: small proof-of-method replay
- Proves: minimal adjacent-mandate threshold gate structure
- Does not prove: real-world external validity

## 3) Real-world experiment pack

- Path: [`demos/adjacent_mandate_reuse_proof_real_v1/`](../demos/adjacent_mandate_reuse_proof_real_v1/)
- Role: execution templates for real controlled experiment
- Proves: only when operators run it with real blinded data and publish the proof docket

## Doctrine cross-links

- `docs/DOCTRINE_STACK.md`
- `docs/THERMODYNAMIC_MODEL.md`
- `docs/NATION_STATE_DOCTRINE.md`

- `docs/RELEASE_POSITIONING.md`

## Smoke-run commands

- `python3 demos/protocol_smart_contract_correctness_demo/run_demo.py --assert`
- `python3 demos/adjacent_mandate_reuse_proof_demo/run_demo.py`
- `python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py`

These commands are intentionally lightweight and deterministic where synthetic data is used.
