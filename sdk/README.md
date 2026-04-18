# Nova-Seeds v2.5 SDK bindings

This directory contains practical TypeScript adapters for threshold-cryptography network integration.

## Included adapters
- `lit/` — Lit Protocol bindings using the current package surface documented under `@lit-protocol/lit-client` and `@lit-protocol/auth`.
- `taco/` — TACo / Threshold Access Control bindings using `@nucypher/taco`, `@nucypher/taco-auth`, and `ethers@5` as required by TACo docs.
- `shared/` — common typed-data, attestation, and signature verification utilities.

## What is real vs placeholder
The adapters use the **real package names and documented setup paths**. Some functions remain opinionated wrappers around those SDKs and should be tested against your chosen environment before production.
