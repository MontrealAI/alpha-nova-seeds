⚠️ This is a protocol-conformant **internal** Stage A + Stage B run, not final independent external proof.

# Results — Blinded Adjacent Transfer + Cross-Domain Expansion v1

This folder records a public-safe evidence update for the real-world adjacent-mandate proof pack.

The result is important because it moves the claim from a bounded proof-of-mechanism toward a more defensible empirical mechanism: a frozen package improved one adjacent mandate, then the promoted lineage transferred into a second domain under a blinded packet structure and delayed reveal discipline.

## Headline result

- **Stage A — blinded adjacent transfer:** PASS
- **Stage B — cross-domain output/evidence transfer:** PASS
- **Stage B strong output thresholds:** PASS
- **Stage B reduced-handholding gate:** NOT PASSED from public intervention logs
- **Public-safe status:** safe to publish
- **Private materials excluded:** answer keys, assignment maps, reviewer identity maps, and private commitments are not included

## Protocol-supported claim

> AGI ALPHA demonstrated blinded adjacent transfer and one cross-domain expansion under controlled internal evaluation.

This is the strongest safe claim supported by this public-safe folder. The stronger claim that Stage B also demonstrated **reduced handholding** remains pending because the public intervention log records two Stage B manual interventions for the treatment lane and two for the control lane.

## What was frozen

### Stage A package

- **Package:** `GovernanceValidationPack-v1`
- **Hash:** `7af9c5e920ccc2bcccea60714c412e1cf276a00728345be860a9eba40465afc1`
- **Mandate 1 scope:** governance / dispute correctness
  - `contracts/CouncilGovernanceV25.sol`
  - `contracts/ChallengePolicyModuleV25.sol`

### Stage B promoted lineage

- **Package:** `ProtocolCorrectnessLineage-v1`
- **Hash:** `85cdacce2067d759378c060c565d0fb2e5dc762fbf7c5a5975afac1396ac4bf8`
- **Freeze time:** `2026-04-23T22:07:23Z`
- **Mandate 3 scope:** backend / API correctness
  - `backend/app/main.py`
  - `backend/app/indexer.py`
  - `backend/app/schemas.py`
  - `backend/migrations/002_v26_hardening.sql`
  - directly coupled backend docs/tests

## What was blinded

Both stages used blinded lane labels:

- `Lane Blue`
- `Lane Gold`

Reveal occurred only after score lock.

Final revealed mapping:

- `Lane Blue` = treatment
- `Lane Gold` = control

## Stage A result

Stage A tested whether `GovernanceValidationPack-v1` improved the adjacent threshold / attestation mandate inside the protocol-correctness wedge.

| Metric | Result | Threshold | Status |
|---|---:|---:|---|
| AOY uplift | +80.00% | >= +35.00% | PASS |
| Speed uplift | +43.75% | >= +30.00% | PASS |
| Rework reduction | 50.00% | >= 40.00% | PASS |
| Evidence completeness uplift | +43.75% | >= +20.00% | PASS |
| Package dependence | 75.00% | >= 30.00% | PASS |
| Safety regression | none observed | none | PASS |

## Stage B result

Stage B tested whether the promoted `ProtocolCorrectnessLineage-v1` transferred into backend / API correctness.

| Metric | Result | Minimum threshold | Strong threshold | Status |
|---|---:|---:|---:|---|
| AOY uplift | +80.00% | positive | >= +35.00% | PASS |
| Speed uplift | +43.75% | positive | >= +30.00% | PASS |
| Rework reduction | 50.00% | n/a | >= 40.00% | PASS |
| Evidence completeness uplift | +27.78% | >= +10.00% | >= +20.00% | PASS |
| Package dependence | 75.00% | >= 20.00% | >= 30.00% | PASS |
| Operator intervention reduction | 0.00% | >= 25.00% | n/a | FAIL |
| Frontier width increase | +1 domain | >= 1 domain | n/a | PASS |
| Safety regression | none observed | none | none | PASS |

## What this supports

If read with the protocol caveats, this run supports the statement that AGI ALPHA demonstrated **blinded adjacent transfer and one cross-domain expansion under controlled internal evaluation**.

The result is meaningful because it adds:

- **causality:** package frozen first, then measured transfer;
- **blinding discipline:** reviewer-facing packets used lane labels and delayed reveal;
- **transfer:** one within-wedge adjacent mandate plus one cross-domain backend/API mandate.

## What this does not prove

This folder does **not** prove:

- reduced handholding in Stage B based on the public intervention logs;
- independent external reviewer validation;
- true end-to-end operator blinding;
- unrestricted autonomy;
- literal or general unbounded recursive self-improvement;
- broad sovereign proof;
- audited final deployment.

## Known deviations

- Role separation was partially emulated in one session.
- Reviewer independence was not external.
- Lane execution was sequential rather than truly parallel.

These deviations are why the result should be described as **strong internal controlled evidence**, not final independent proof.

## Recommended next validation

The next credibility upgrade is an independent rerun with:

- a separate blinding officer;
- separate lane operators;
- separate blinded reviewers;
- a clean checkout on a separate machine;
- explicit reduced-handholding instrumentation;
- public-safe results committed regardless of pass or fail.

## File map

- `summary_metrics.json` — normalized machine-readable summary
- `stage_a_scorecard.md` — Stage A scorecard
- `stage_b_scorecard.md` — Stage B scorecard
- `proof_docket_public.md` — public-safe proof docket
- `lane_blue_packet_public/` — Stage A public packet for Lane Blue
- `lane_gold_packet_public/` — Stage A public packet for Lane Gold
- `lane_blue_packet_stage_b_public/` — Stage B public packet for Lane Blue
- `lane_gold_packet_stage_b_public/` — Stage B public packet for Lane Gold
- `scorecard_outputs/` — Stage A scorecard outputs
- `scorecard_outputs_stage_b/` — Stage B scorecard outputs
- `verification_artifacts_stage_b/` — Stage B public verification artifacts
- `PROTOCOL_REFERENCE.md` — public-safe protocol reference summary
- `REPO_INTEGRATION.md` — suggested repo integration notes
