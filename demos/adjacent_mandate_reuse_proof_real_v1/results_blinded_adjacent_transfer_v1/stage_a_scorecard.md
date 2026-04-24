# Stage A scorecard — blinded adjacent transfer

## Result

**PASS**

Stage A tested whether `GovernanceValidationPack-v1` improved the adjacent threshold / attestation mandate inside the protocol-correctness wedge.

## Lane reveal

Reveal occurred after score lock.

- `Lane Blue` = treatment
- `Lane Gold` = control

## Control

| Metric | Value |
|---|---:|
| Cost units | 12.0 |
| Accepted outputs | 2 |
| Usefulness points | 5.0 |
| AOY | 0.4167 |
| Time to first accepted output | 1.6 |
| Average rework | 2.0 |
| Evidence completeness | 0.6667 |
| Safety incidents | 0 |
| Unsupported claims | 0 |
| Hallucinated references | 0 |
| Package dependence | 0.0 |

## Treatment

| Metric | Value |
|---|---:|
| Cost units | 12.0 |
| Accepted outputs | 4 |
| Usefulness points | 9.0 |
| AOY | 0.7500 |
| Time to first accepted output | 0.9 |
| Average rework | 1.0 |
| Evidence completeness | 0.9583 |
| Safety incidents | 0 |
| Unsupported claims | 0 |
| Hallucinated references | 0 |
| Package dependence | 0.75 |

## Comparisons

| Metric | Result | Threshold | Status |
|---|---:|---:|---|
| AOY uplift | +80.00% | >= +35.00% | PASS |
| Speed uplift | +43.75% | >= +30.00% | PASS |
| Rework reduction | 50.00% | >= 40.00% | PASS |
| Evidence completeness uplift | +43.75% | >= +20.00% | PASS |
| Package dependence | 75.00% | >= 30.00% | PASS |
| Safety regression | none observed | none | PASS |

## Boundary

This is an internal blinded-packet protocol run. It is not independent external validation.
