# Blinded Adjacent-Transfer Experiment Record (v1)

This folder operationalizes the blinded adjacent-transfer protocol for:

- Stage A: adjacent transfer in the protocol-correctness wedge
- Stage B: conditional cross-domain transfer into backend/API correctness

Status today: **operationalized to the honest human boundary**.

No reviewer judgments, lane outcomes, or pass/fail results were fabricated.

## 1) What was frozen

- Preregistration freeze: `prereg_experiment_manifest.json`
- Environment and in-scope file hashes: `environment_lock.json`
- Stage A and Stage B lane budget symmetry and thresholds are locked in preregistration
- Scorecard inputs are pre-wired under `scorecard_outputs/`

## 2) What was blinded

- Public packets use lane IDs only: `lane_blue_packet_public/` and `lane_gold_packet_public/`
- Private assignment and reviewer identity maps are moved to git-ignored local storage:
  `../local_private_blinding_materials/results_blinded_adjacent_transfer_v1/`
- Private commitment hashes are generated locally with
  `../07_scripts/generate_private_commitment_hashes.py`

## 3) What passed / failed

- Stage A: **not yet adjudicated** (pending real human blinded execution)
- Stage B: **not run** (strictly conditional on a real Stage A pass)
- Scorecard status: calculator wiring verified; no real blinded inputs entered yet

## 4) What this supports

- A complete, reproducible execution harness for blinded adjacent transfer exists.
- The repository can now produce a public-safe record and separate private blinding materials without leaking assignment maps.

## 5) What this does not prove

- It does not prove a Stage A pass.
- It does not prove Stage B transfer.
- It does not prove unrestricted autonomy, unbounded RSI, or broad sovereign proof.

## Run sequence (honest execution)

1. Initialize scaffolding (if re-running fresh):
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/setup_blinded_adjacent_transfer_v1.py --force
   ```
2. Fill private-only files locally (outside git history).
3. Freeze private commitments:
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/generate_private_commitment_hashes.py \
     --private-dir demos/adjacent_mandate_reuse_proof_real_v1/local_private_blinding_materials/results_blinded_adjacent_transfer_v1
   ```
4. Execute Stage A lane work under blinded kits and collect packets.
5. Fill scorecard CSVs in `scorecard_outputs/` from real adjudication data.
6. Run scorecard helper:
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py
   ```
7. Lock scorecard and only then reveal blinded assignment map.
8. Run bundle completeness check:
   ```bash
   python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/validate_blinded_results_bundle.py
   ```

See `HUMAN_ACTION_REQUIRED.md` for unresolved role-separated steps.
