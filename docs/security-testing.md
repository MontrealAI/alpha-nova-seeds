# Security testing posture (contracts)

This repository is a **verifiable release candidate** and should be treated as hardening-in-progress.

## Security test stack

The contracts subsystem uses layered testing:

1. Hardhat integration tests for deployment posture and integration wiring.
2. Foundry Solidity tests for unit, fuzz, and invariant checks.
3. Echidna transaction-sequence property tests for high-risk surfaces.
4. Slither static analysis for detector-based regression catching.

## Risk surfaces covered

- unauthorized lifecycle mutation,
- reviewer reward accounting regressions,
- threshold profile misconfiguration,
- governance seat/challenge lifecycle misuse,
- registry lifecycle ordering failures.

## What this does not claim

This testing layer does not claim the contracts are:

- audited,
- production-final,
- proven under all adversarial market conditions.

Independent review and formal audit remain required for high-stakes deployment decisions.
