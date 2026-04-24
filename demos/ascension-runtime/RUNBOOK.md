# RUNBOOK — Ascension Runtime

1. Run deterministic demo:
   - `python3 demos/ascension-runtime/run_demo.py --assert`
2. Inspect key outputs under `demos/ascension-runtime/out/`.
   - `out/nova_seed_packet.json`
   - `out/agi_job_receipt.json`
   - `out/ascension_runtime_scorecard.json`
3. Verify claim boundaries in:
   - `out/ascension_runtime_scorecard.md`
   - `out/reports/ascension_runtime_report.md`
4. Use this runtime as a local replay surface only.
