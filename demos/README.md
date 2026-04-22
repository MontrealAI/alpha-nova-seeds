# Demo Ladder (v2.7.0-rc.2)

This folder contains the three demo surfaces for the protocol-and-smart-contract correctness wedge.

Use this ladder with explicit scope labels:
- **Synthetic flagship wedge demo** (primary front door)
- **Synthetic compact adjacent proof demo** (small replay)
- **Real-world experiment pack** (operator templates requiring blinded execution data)

## 1) Flagship synthetic wedge demo

- Path: [`protocol_smart_contract_correctness_demo/`](./protocol_smart_contract_correctness_demo/)
- Role: best public/operator entry point
- Run: `python3 demos/protocol_smart_contract_correctness_demo/run_demo.py --assert`
- Proves: deterministic synthetic wedge mechanics, winner selection, package freeze, adjacent control-vs-treatment scorecard, and synthetic sovereign gating
- Does not prove: real-world compounding correctness under live delivery

## 2) Adjacent synthetic proof demo

- Path: [`adjacent_mandate_reuse_proof_demo/`](./adjacent_mandate_reuse_proof_demo/)
- Role: compact synthetic replay
- Run: `python3 demos/adjacent_mandate_reuse_proof_demo/run_demo.py`
- Proves: minimal adjacent-mandate threshold gate structure
- Does not prove: real-world external validity

## 3) Real-world proof pack

- Path: [`adjacent_mandate_reuse_proof_real_v1/`](./adjacent_mandate_reuse_proof_real_v1/)
- Role: operator execution templates for controlled real-world proof
- Run (scorecard helper): `python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py`
- Proves: only when run with real blinded data and published proof-docket artifacts

## Doctrine context

- [`../docs/DOCTRINE_STACK.md`](../docs/DOCTRINE_STACK.md)
- [`../docs/THERMODYNAMIC_MODEL.md`](../docs/THERMODYNAMIC_MODEL.md)
- [`../docs/NATION_STATE_DOCTRINE.md`](../docs/NATION_STATE_DOCTRINE.md)
- [`../docs/DEMO_STRATEGY.md`](../docs/DEMO_STRATEGY.md)

## Claim boundary (explicit)

This demo ladder supports a narrow claim for this RC: protocol correctness can be staged and tested as compounding reusable capability under controlled synthetic conditions.

It does **not** claim that the broader cybersecurity sovereign is already proven in real-world operation.
