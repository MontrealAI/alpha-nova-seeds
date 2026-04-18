# Threat Model (v2.6 RC)

## In scope
- Event replay/duplication attacks against ingestion.
- Reorg-induced cursor drift.
- Invalid threshold payload injection.
- Ambiguous reviewer reward/slash accounting.
- Release artifact tampering.

## Mitigations in v2.6 RC
- Idempotent chain event upserts.
- Reorg-safe indexed cursor with confirmation lag.
- JSON schema validation for threshold payloads.
- Deterministic SQL views for stake and seat lifecycle accounting.
- SHA256SUMS + provenance attestations + SBOM publication.

## Out of scope
- Formal economic audit.
- Final production-safe guarantees.
