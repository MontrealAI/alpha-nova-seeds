# Protocol reference — Blinded Adjacent Transfer + Cross-Domain Expansion v1

This public-safe reference summarizes the protocol used for `results_blinded_adjacent_transfer_v1/`.

## Purpose

The protocol tests whether a frozen capability package causally improves the next adjacent mandate under blinded conditions, and then whether the resulting lineage transfers into a second domain with less handholding.

## Stage A

Stage A tests blinded adjacent transfer inside the protocol-correctness wedge.

- **Mandate 1:** governance / dispute correctness
- **Frozen package:** `GovernanceValidationPack-v1`
- **Mandate 2:** threshold / attestation correctness
- **Comparison:** blinded control vs blinded treatment

A Stage A pass supports:

> Within the protocol-correctness wedge, a frozen capability package materially improved the next adjacent mandate under blinded control conditions.

## Stage B

Stage B runs only if Stage A passes.

- **Promoted lineage package:** `ProtocolCorrectnessLineage-v1`
- **Mandate 3 domain:** backend / API correctness
- **Comparison:** blinded control vs blinded treatment

A Stage A + Stage B pass supports:

> AGI ALPHA demonstrated bounded recursive self-improvement through blinded adjacent transfer and one cross-domain expansion under controlled evaluation.

## Boundary

This still does **not** prove unrestricted autonomy, literal/general unbounded RSI, independent external validation, or broad sovereign proof.

## Why it matters

The protocol adds three ingredients that weak rhetoric lacks:

- **causality:** package frozen first, then measured improvement;
- **blinding:** reviewers do not know which lane is which;
- **transfer:** success must survive one adjacent within-wedge transfer and one cross-domain expansion.
