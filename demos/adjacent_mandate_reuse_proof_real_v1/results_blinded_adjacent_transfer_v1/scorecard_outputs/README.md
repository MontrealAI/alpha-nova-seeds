# Scorecard outputs workspace

Populate these files from real blinded reviewer adjudication:

- `run_costs.csv`
- `output_scoring.csv`
- `package_dependence_ledger.csv`

Then run:

```bash
python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py --scorecard-dir demos/adjacent_mandate_reuse_proof_real_v1/results_blinded_adjacent_transfer_v1/scorecard_outputs
```
