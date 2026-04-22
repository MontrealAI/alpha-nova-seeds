# Open-Ended RSI System Demo (v2.8.0-rc.2 target)

This demo is a **deterministic, bounded proof-of-mechanism** for a minimum viable accelerating loop:

**bounded → expanding → increasingly autonomous**.

It is repo-native and does not rely on network calls, external APIs, or model training.

## What this demo demonstrates

1. **Generation 0 (bounded, DISCO mode):**
   - Starts in the existing protocol-correctness wedge.
   - Uses one fixed reactive intermediate (`missing_proof_artifact`).
   - Builds and screens a deterministic candidate pool.
2. **Generation 1 (expanding):**
   - Freezes a governed capability package with manifest + hash + lineage.
   - Runs adjacent Mandate 2 in explicit control-vs-treatment lanes.
   - Emits AOY/speed/rework/evidence/safety/package-dependence thresholds.
3. **Generation 2 (increasingly autonomous):**
   - Selects the next domain only from a fixed whitelist.
   - Runs DISCO (first workable package) then Arnold (local neighborhood improvements).
   - Reduces operator intervention while preserving authority gates.

## Required demo directories

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

## Run

```bash
python3 demos/open-ended-rsi-system/run_demo.py --assert
```

## Outputs

Primary machine-readable artifacts in `out/`:

- `capability_genome.json`
- `assay_bundle.json`
- `lineage.json`
- `frontier_queue.json`
- `intervention_log.json`
- `scorecard.json`
- `provenance_manifest.json`

Board/operator artifacts in `out/`:

- `summary.md`
- `proof_docket.md`
- `report.html`

## Demonstrated vs simulated vs unproven

### Demonstrated

- Deterministic three-generation governed loop mechanics.
- Package freeze/hash with lineage and reusable asset ledger.
- Adjacent transfer win in bounded control-vs-treatment synthetic conditions.
- Bounded autonomous domain selection from a fixed whitelist.

### Simulated

- Mandate outcomes and blinded-rubric style adjudication metrics.
- Governance/board outputs as deterministic synthetic replay artifacts.

### Unproven

- Unrestricted autonomy.
- Fully general literal unbounded RSI.
- Completed real-world broad cybersecurity sovereign operation.

## Demo ladder links

- Flagship synthetic wedge demo: [`../protocol_smart_contract_correctness_demo/`](../protocol_smart_contract_correctness_demo/)
- Adjacent synthetic proof demo: [`../adjacent_mandate_reuse_proof_demo/`](../adjacent_mandate_reuse_proof_demo/)
- Real-world proof pack: [`../adjacent_mandate_reuse_proof_real_v1/`](../adjacent_mandate_reuse_proof_real_v1/)
- Prior accelerating-loop demo (compatibility): [`../unbounded-rsi-system/`](../unbounded-rsi-system/)
- Demo ladder index: [`../README.md`](../README.md)
