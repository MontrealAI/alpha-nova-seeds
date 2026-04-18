# Threshold Attestation Lifecycle (v2.6 RC)

This document describes the proof path for threshold decryption attestations.

## Scope
- This is an RC operational lifecycle for verifiable proof.
- It does not claim audited final deployment readiness.

## Lifecycle
1. **Seed identity established**: seed is drafted and sealed.
2. **Threshold profile bound**: `threshold-binding-profile.schema.json` payload is published and hash-linked.
3. **Decryption request opened**: request enters review term with deadline and policy hash.
4. **Committee execution**: threshold network returns plaintext commitment.
5. **Attestation signed**: decryption attestation payload is signed over EIP-712 domain.
6. **Indexing + visibility**: backend indexes attestation and exposes proof summary metrics.
7. **Settlement/governance follow-on**: unresolved or conflicting attestations route to governance challenge.

## Canonical schemas
- `schemas/threshold/v2.6/decryption-attestation.schema.json`
- `schemas/threshold/v2.6/threshold-binding-profile.schema.json`

## Operator checks
- Ensure attestation `seedId` and `requestId` match on-chain event records.
- Ensure signer belongs to approved threshold binding profile.
- Ensure deadline is not stale at ingest time.
