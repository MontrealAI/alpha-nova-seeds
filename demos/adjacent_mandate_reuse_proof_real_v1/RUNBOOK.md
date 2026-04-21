# Runbook

## Phase 0 — Freeze
Complete:
- `00_manifest/experiment_manifest.template.json`
- `00_manifest/environment_lock.template.json`
- `00_manifest/package_hash_record.template.json` (initial placeholders only)
- `02_execution/run_register.template.csv`
- private answer key + blinded assignment map

## Phase 1 — Mandate 1
Use:
- `01_mandate_specs/mandate_1_governance_dispute_correctness.md`
- `03_review/reviewer_form_mandate_1.template.md`

Output:
- accepted findings
- accepted harnesses/tests
- `GovernanceValidationPack-v1`
- settlement receipts
- chronicle entry draft

## Phase 2 — Freeze package
Record:
- package hash
- exact included files
- no-edit attestation

## Phase 3 — Mandate 2
Run both:
- control lane with `02_execution/control_lane_instructions.md`
- treatment lane with `02_execution/treatment_lane_instructions.md`

## Phase 4 — Review
Use:
- `03_review/reviewer_form_mandate_2_control.template.md`
- `03_review/reviewer_form_mandate_2_treatment.template.md`
- `03_review/adjudication_form.template.md`

## Phase 5 — Score
Fill:
- `04_scorecard/run_costs.template.csv`
- `04_scorecard/output_scoring.template.csv`

Then run:

```bash
python3 07_scripts/calculate_q2_scorecard.py
```

## Phase 6 — Publish
Complete the proof docket templates in `06_proof_docket/` using the calculated outputs.
