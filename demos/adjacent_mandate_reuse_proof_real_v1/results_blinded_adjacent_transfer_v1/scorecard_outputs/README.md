# Scorecard outputs workspace

Fill these CSVs from real blinded adjudication outputs:

- `run_costs.csv`
- `output_scoring.csv`
- `package_dependence_ledger.csv`

Then run:

```bash
python3 demos/adjacent_mandate_reuse_proof_real_v1/07_scripts/calculate_q2_scorecard.py
```

The helper writes score summaries to:

- `demos/adjacent_mandate_reuse_proof_real_v1/04_scorecard/out/summary.json`
- `demos/adjacent_mandate_reuse_proof_real_v1/04_scorecard/out/summary.md`
