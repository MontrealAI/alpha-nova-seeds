# Threshold Attestation Lifecycle (v2.6 RC)

## Purpose
This document describes the proof path for threshold decryption attestations in plain English.

## Lifecycle
1. **Binding profile published**: operator sets provider/network/committee/threshold policy.
2. **Request opened**: a decryption request links seed identity and ciphertext hashes.
3. **Committee attests**: threshold service signs the EIP-712 attestation payload.
4. **On-chain completion**: adapter verifies signer trust and records plaintext/completion hashes.
5. **Challenge window**: governance can challenge or cancel request if proof is disputed.

## Canonical schemas
- `docs/schemas/v2.6/threshold-binding-profile.schema.json`
- `docs/schemas/v2.6/decryption-attestation.schema.json`

## Round-trip examples
- `docs/examples/v2.6/threshold-binding-profile.example.json`
- `docs/examples/v2.6/decryption-attestation.example.json`

## Assumptions
- Signer trust list is managed through `SignedAttestationVerifierV25`.
- Deadline and term IDs are validated by contract logic, not JSON schema alone.

## Non-goals
- Defining cryptography internals of Lit/Taco networks.
- Replacing provider-level attestation mechanisms.
