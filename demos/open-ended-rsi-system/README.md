# Open-Ended RSI System Demo (v2.8.0-rc.2 target)

This demo is a deterministic, repo-native **bounded proof-of-mechanism** for an early accelerating loop:

**bounded → expanding → increasingly autonomous**

It demonstrates controlled compounding under governance. It does **not** claim unrestricted autonomy.

## What this demo does

1. Runs a real Mandate 1 starting point in the protocol-correctness wedge.
2. Freezes a governed capability package with a manifest + hash.
3. Uses that package in an adjacent Mandate 2 treatment lane against a control lane.
4. Selects and executes Mandate 3 from a bounded frontier whitelist with less human intervention.
5. Emits board-ready scorecards, safety gates, provenance logs, and proof-docket outputs.

## Required folders and emitted artifacts

This demo includes:

- `00_manifest/`
- `01_frontier_queue/`
- `02_seed_genome/`
- `03_generation/`
- `04_assays/`
- `05_selection/`
- `06_archive/`
- `07_scorecard/`
- `08_proof_docket/`
- `out/`

Primary machine-readable outputs in `out/`:

- `capability_genome.json`
- `assay_bundle.json`
- `lineage.json`
- `frontier_queue.json`
- `intervention_log.json`
- `scorecard.json`
- `summary.md`
- `proof_docket.md`
- `provenance_manifest.json`
- `board_report.html`

## Run

```bash
python3 demos/open-ended-rsi-system/run_demo.py --assert
```

## Three generations

### Generation 0 (bounded)

- Domain: protocol correctness wedge.
- Uses a fixed reactive intermediate (`missing_provenance_surface`).
- Deterministically generates 48 candidates across DISCO + Arnold modes.
- Screens cheap → mid → expensive assays.
- Freezes winner as governed package with deterministic hash.

### Generation 1 (expanding)

- Domain: adjacent mandate in wedge.
- Runs explicit control vs treatment lanes.
- Emits AOY/speed/rework/evidence/safety/package-dependence metrics.
- Treatment lane wins and is attributable to the frozen package.

### Generation 2 (increasingly autonomous)

- Domain selection from fixed whitelist only.
- Selection scoring uses transfer, assay coverage, safety scope, evidence density.
- Runs DISCO discovery then Arnold local evolution.
- Emits `frontier_width`, `autonomy_delta`, `neighborhood_slope`, `archive_depth`.

## Demonstrated vs simulated vs unproven

### Demonstrated

- Bounded accelerating loop mechanics under governance.
- Package freeze/reuse with attributable control-vs-treatment uplift.
- Reduced operator intervention in Generation 2 without authority widening.

### Simulated

- Assay outcomes and scorecard values are synthetic deterministic replay values.
- No network calls, no external APIs, no live settlement.

### Unproven

- Unrestricted autonomy.
- Literal or general unbounded recursive self-improvement.
- Completed real-world broad cybersecurity sovereign operation.

## Demo ladder links

- Flagship synthetic wedge demo: [`../protocol_smart_contract_correctness_demo/`](../protocol_smart_contract_correctness_demo/)
- Adjacent synthetic proof demo: [`../adjacent_mandate_reuse_proof_demo/`](../adjacent_mandate_reuse_proof_demo/)
- Real-world proof pack: [`../adjacent_mandate_reuse_proof_real_v1/`](../adjacent_mandate_reuse_proof_real_v1/)
- Legacy accelerating-loop demo: [`../unbounded-rsi-system/`](../unbounded-rsi-system/)
- Demo ladder index: [`../README.md`](../README.md)
