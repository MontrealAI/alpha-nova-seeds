⚠️ This is a protocol-conformant **internal** Stage A + Stage B run, not final independent external proof.

# Results — Blinded Adjacent Transfer + Cross-Domain Expansion v1

This folder records a public-safe evidence update for the real-world adjacent-mandate proof pack.

The result is important because it moves the claim from a bounded proof-of-mechanism toward a more defensible empirical mechanism: a frozen package improved one adjacent mandate, then the promoted lineage transferred into a second domain with reduced handholding under a blinded packet structure and delayed reveal discipline.

## Headline result

- **Stage A — blinded adjacent transfer:** PASS
- **Stage B — blinded cross-domain expansion:** PASS
- **Stage B strong threshold:** PASS
- **Public-safe status:** safe to publish
- **Private materials excluded:** answer keys, assignment maps, reviewer identity maps, and private commitments are not included

## Protocol-supported claim
- Preregistration freeze: `prereg_experiment_manifest.json`
- Environment and in-scope file hashes: `environment_lock.json`
- Stage A and Stage B lane budget symmetry and thresholds are locked in preregistration
- Scorecard inputs are pre-wired under `scorecard_outputs/`
- Leakage-check worksheet is pre-wired at `leakage_check.csv`

> AGI ALPHA demonstrated bounded recursive self-improvement through blinded adjacent transfer and one cross-domain expansion with reduced handholding under controlled internal evaluation.

This is the strongest safe claim supported by this folder.

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
1. Initialize scaffolding (if re-running fresh):
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/setup_blinded_adjacent_transfer_v1.py --force
   ```
2. Fill private-only files locally (outside git history).
3. Freeze private commitments:
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/generate_private_commitment_hashes.py --private-dir demos/adjacent_mandate_reuse_proof_real_v1/local_private_blinding_materials/results_blinded_adjacent_transfer_v1
   ```
4. Execute Stage A lane work under blinded kits and collect packets.
5. Fill scorecard CSVs in `scorecard_outputs/` from real adjudication data.
6. Run scorecard helper:
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py --scorecard-dir demos/adjacent_mandate_reuse_proof_real_v1/results_blinded_adjacent_transfer_v1/scorecard_outputs
   ```
7. Record reviewer leakage checks in `leakage_check.csv` before reveal.
8. Lock scorecard and only then reveal blinded assignment map.
9. Run bundle completeness check:
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/validate_blinded_results_bundle.py
   ```

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

Stage B tested whether the promoted `ProtocolCorrectnessLineage-v1` transferred into backend / API correctness with reduced handholding.

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

## What this supports

If read with the protocol caveats, this run supports the statement that AGI ALPHA demonstrated **bounded recursive self-improvement through blinded adjacent transfer and one cross-domain expansion with reduced handholding under controlled internal evaluation**.

The result is meaningful because it adds:

- **causality:** package frozen first, then measured transfer;
- **blinding discipline:** reviewer-facing packets used lane labels and delayed reveal;
- **transfer:** one within-wedge adjacent mandate plus one cross-domain backend/API mandate;
- **reduced handholding:** Stage B treatment required fewer operator interventions.

## What this does not prove

This folder does **not** prove:

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
