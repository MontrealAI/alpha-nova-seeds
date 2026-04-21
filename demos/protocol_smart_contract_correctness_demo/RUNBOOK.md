# RUNBOOK — protocol_smart_contract_correctness_demo

## 1) Execute

```bash
python3 run_demo.py --assert
```

## 2) Inspect outputs

Open:

- `demo_output/reports/report.html`
- `demo_output/reports/report.md`
- `demo_output/scorecard/adjacent_mandate_scorecard.json`
- `demo_output/proof_docket/proof_docket.json`
- `demo_output/mandate_1/accepted_usefulness_rubric.json`
- `demo_output/mandate_1/evidence_completeness_checklist.json`

## 3) Determinism check

Automatic mode:

```bash
python3 run_demo.py --assert
```

The command performs two back-to-back runs and verifies tracked artifact hashes are identical.

Manual mode:

```bash
python3 run_demo.py
sha256sum demo_output/scorecard/adjacent_mandate_scorecard.json
python3 run_demo.py
sha256sum demo_output/scorecard/adjacent_mandate_scorecard.json
```

Manual hash should remain stable as well.

## 4) Scoring source of truth

The deterministic engine loads scoring/evidence thresholds from:

- `config/accepted_usefulness_rubric.json`
- `config/evidence_completeness_checklist.json`
- `config/adjacent_mandate_thresholds.json`

This keeps thresholds operator-visible and reviewable without code edits.

## 5) Interpretation guardrails

This is a synthetic replayable assay. It is suitable for:

- process legibility
- operator training
- proof-surface review

It is not a replacement for a real mandate proof pack.
