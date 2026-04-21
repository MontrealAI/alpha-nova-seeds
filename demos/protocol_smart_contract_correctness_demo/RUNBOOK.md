# RUNBOOK — protocol_smart_contract_correctness_demo

## 1) Execute

```bash
python3 run_demo.py --assert
```

Optional fail-closed rehearsal:

```bash
python3 run_demo.py --assert --force-fail
```

This confirms conditional sovereign emission logic by forcing a threshold miss and producing `demo_output/sovereign/ProtocolAssuranceSovereign-v1.fail_closed.json`.

## 2) Inspect outputs

Open:

- `demo_output/reports/report.html`
- `demo_output/reports/report.md`
- `demo_output/scorecard/adjacent_mandate_scorecard.json`
- `demo_output/proof_docket/proof_docket.json`

## 3) Determinism check

Run twice and compare hashes:

```bash
python3 run_demo.py --assert
sha256sum demo_output/scorecard/adjacent_mandate_scorecard.json
python3 run_demo.py --assert
sha256sum demo_output/scorecard/adjacent_mandate_scorecard.json
```

Hash should remain stable.

## 4) Interpretation guardrails

This is a synthetic replayable assay. It is suitable for:

- process legibility
- operator training
- proof-surface review

It is not a replacement for a real mandate proof pack.
