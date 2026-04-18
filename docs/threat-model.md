# Threat Model (v2.6 RC)

## In scope
- Event replay or duplicate ingestion attempts.
- Chain reorg effects on non-finalized blocks.
- Malicious reviewer behavior requiring slash accounting.
- Seat challenge manipulation attempts.

## Mitigations in this RC
- Idempotent ingestion via unique `(tx_hash, log_index)`.
- Finality buffer through configurable confirmations and indexer cursor.
- Deterministic slash/reward and seat lifecycle accounting.
- Release provenance workflow for source/hash/SBOM traceability.

## Out of scope
- Full cryptographic audit of threshold providers.
- Economic game-theory audit for governance incentives.
