# Unbounded RSI System Demo (v2.8.0-rc.2)

This is the **accelerating-loop demo** for the current release candidate.

It demonstrates a **minimum viable accelerating loop** in three bounded phases:

1. **Bounded** (Mandate 1 in protocol-correctness wedge)
2. **Expanding** (frozen package + Mandate 2 control vs treatment)
3. **Increasingly autonomous** (rule-based Mandate 3 selection/execution in a second domain)

## Why this demo exists

This surface shows how compounding capability can start in a strict proof-first wedge and then transfer to adjacent work with less human intervention, while keeping safety and governance explicit.

## Run

```bash
python3 demos/unbounded-rsi-system/run_demo.py --assert
```

## Artifact outputs

The run writes deterministic artifacts under `demo_output/`:

- `manifest.json`
- `package_manifest.json`
- `package_hash.txt`
- `provenance_log.json`
- `safety_gates.json`
- `governance_ruling.json`
- `chronicle_entry.json`
- `board_scorecard.json`
- `board_scorecard.md`
- `report.html`
- `report.md`

Phase-specific artifacts:

- `phase_a/mandate_1_review.json`
- `phase_b/mandate_2_scorecard.json`
- `phase_c/mandate_3_execution.json`

## Demonstrated vs simulated vs unproven

### Demonstrated

- Repo-native protocol fixtures are used in phase A review evidence.
- A governed capability package is frozen with deterministic manifest/hash.
- Mandate 2 control-vs-treatment passes declared thresholds.
- Mandate 3 selection uses explicit bounded scoring and lower intervention.

### Simulated

- Lane-level productivity metrics are deterministic simulation constants for reproducibility.
- Governance ruling is a demo packet, not a legal or on-chain ruling.

### Unproven

- Literal unbounded recursive self-improvement.
- Unrestricted open-world autonomy.
- Fully realized broad sovereign system operation.

## Claim boundary

This demo supports only a bounded claim:

- an early accelerating mechanism can be demonstrated under governance and policy bounds.

It does **not** claim unrestricted autonomy, fully generalized compounding in the wild, or audited-final production status.

## Demo ladder links

- Flagship wedge demo: [`../protocol_smart_contract_correctness_demo/`](../protocol_smart_contract_correctness_demo/)
- Compact adjacent synthetic proof demo: [`../adjacent_mandate_reuse_proof_demo/`](../adjacent_mandate_reuse_proof_demo/)
- Real-world proof pack: [`../adjacent_mandate_reuse_proof_real_v1/`](../adjacent_mandate_reuse_proof_real_v1/)
- Ladder index: [`../README.md`](../README.md)
