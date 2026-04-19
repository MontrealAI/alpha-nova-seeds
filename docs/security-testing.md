# Security testing posture (contracts)

This repository is a **verifiable release candidate** and remains hardening-in-progress.

## Security test layers

1. **Hardhat integration tests**
   - Deployment wiring and integration behavior.
2. **Foundry unit tests**
   - Contract-aware happy/revert/authorization paths.
3. **Foundry fuzz + invariants**
   - Arithmetic, lifecycle boundary, and state-coherence properties.
4. **Echidna stateful campaigns**
   - Adversarial transaction-sequence properties on treasury, governance, threshold, and registry surfaces.
5. **Slither static analysis**
   - Detector-based static regression checks with fail-high policy.

## Risks now covered by executable evidence

- unauthorized lifecycle mutation attempts,
- duplicate seed insertion and lifecycle misuse,
- adjudication-policy inactive/finalized bypass attempts,
- council seat/challenge authority boundaries,
- reward accrual/slash/claim conservation,
- malformed/untrusted signature rejection and digest domain separation,
- invalid threshold profile persistence and untrusted completion rejection,
- workflow adapter fail-closed behavior when downstream engine fails.

## Out of scope / still not proven

This does **not** prove:

- economic security under all market/game-theoretic conditions,
- threshold-network cryptographic correctness of external operators,
- exhaustive formal verification of all state transitions,
- audit-complete or production-final deployment safety.

High-stakes deployment still requires independent human security review and external audit.
