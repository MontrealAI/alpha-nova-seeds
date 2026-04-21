# Adjacent-Mandate Reuse Proof Demo

This is the **next milestone demo**:
one adjacent-mandate reuse proof under control conditions.

It is intentionally small, local, and reproducible.

## What it demonstrates

- Parent sector: **Protocol and smart-contract correctness**
- Mandate 1: review a first batch of smart-contract mandates
- Freeze the resulting reusable package as:
  - `ProtocolCybersecurityPack-v1` (legacy alias: `ProtocolAssurancePack-v1`)
- Mandate 2: review an **adjacent** batch twice:
  - **control** without the package
  - **treatment** with the frozen package
- Score the result against the adjacent-mandate proof gate

## How to run

```bash
python3 run_demo.py
```

No extra dependencies are required.

## Best files to open

- `demo_output/reports/report.html`
- `demo_output/reports/report.md`
- `demo_output/proof_docket/06_scorecard.md`

## Important note

This is a **synthetic local demo**, not a real-world proof.
It shows the structure of the milestone:
one completed mandate can create a frozen capability package that materially improves the next adjacent mandate under control conditions.

## Current synthetic result

- Adjacent-mandate proof: **PASS**
- Package hash: `467a32a99c0e16988e3085844b06f81f8fdf3e30815bb2aaf468155d1e85727b`

## Demo ladder

- Flagship synthetic wedge demo: `demos/protocol_smart_contract_correctness_demo/`
- Adjacent synthetic proof demo: `demos/adjacent_mandate_reuse_proof_demo/`
- Real-world experiment pack: `demos/adjacent_mandate_reuse_proof_real_v1/`
