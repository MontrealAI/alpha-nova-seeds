# Stage B scorecard — blinded cross-domain expansion

## Result

- **Minimum pass:** PASS
- **Strong pass:** PASS

Stage B tested whether `ProtocolCorrectnessLineage-v1` transferred into backend / API correctness with reduced handholding.

## Lane reveal

Reveal occurred after score lock.

- `Lane Blue` = treatment
- `Lane Gold` = control

## Frozen lineage

- **Package:** `ProtocolCorrectnessLineage-v1`
- **Hash:** `85cdacce2067d759378c060c565d0fb2e5dc762fbf7c5a5975afac1396ac4bf8`
- **Freeze time:** `2026-04-23T22:07:23Z`

## Control

| Metric | Value |
|---|---:|
| Cost units | 12.0 |
| Accepted outputs | 2 |
| Usefulness points | 5.0 |
| AOY | 0.4167 |
| Time to first accepted output | 1.6 |
| Average rework | 2.0 |
| Evidence completeness | 0.7500 |
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

| Metric | Result | Minimum threshold | Strong threshold | Status |
|---|---:|---:|---:|---|
| AOY uplift | +80.00% | positive | >= +35.00% | PASS |
| Speed uplift | +43.75% | positive | >= +30.00% | PASS |
| Rework reduction | 50.00% | n/a | >= 40.00% | PASS |
| Evidence completeness uplift | +27.78% | >= +10.00% | >= +20.00% | PASS |
| Package dependence | 75.00% | >= 20.00% | >= 30.00% | PASS |
| Operator intervention reduction | 50.00% | >= 25.00% | n/a | PASS |
| Frontier width increase | +1 domain | >= 1 domain | n/a | PASS |
| Safety regression | none observed | none | none | PASS |

## Boundary

This is an internal controlled cross-domain expansion run. It is not independent external validation or proof of general unbounded recursive self-improvement.
