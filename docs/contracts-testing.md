# Contracts testing guide (v2.6.0-rc.1)

This guide describes how to run contract security tests from a clean checkout.

## Prerequisites

- Node.js `22.10.0+`
- npm
- Foundry (`forge`)
- Slither (`slither`)
- Echidna (`echidna`)

Install contract dependencies:

```bash
npm --prefix contracts ci
```

## Compile

```bash
npm run contracts:build
```

## Unit tests (Foundry)

```bash
npm run test:contracts:unit
```

Coverage intent:

- ownership and role gates
- revert-path controls
- lifecycle transitions and terminal-state guards
- integration edges for registry + workflow + governance components

## Fuzz tests (Foundry)

```bash
npm run test:contracts:fuzz
```

Coverage intent:

- threshold/quorum boundaries
- arithmetic edge ranges
- seat assignment and governance coherence edges
- registry identity validation boundaries (`seedId`, `manifestHash`, `ciphertextHash`)
- malformed signature rejection for attestation verification

## Invariant tests (Foundry)

```bash
npm run test:contracts:invariant
```

Coverage intent:

- accounting monotonicity and no implicit value creation
- governance seat occupancy coherence
- threshold profile quorum-math coherence

## Echidna property tests

```bash
npm run test:contracts:echidna
```

Harnesses:

- `EchidnaTreasuryHarness.sol`
- `EchidnaGovernanceHarness.sol`
- `EchidnaThresholdHarness.sol`
- `EchidnaRegistryHarness.sol`

## Slither static analysis

```bash
npm run analyze:slither
```

The command fails on high-severity findings.

## CI expectations

Contracts security gates fail loud on:

- compile errors,
- unit/fuzz/invariant failures,
- Slither high-severity findings,
- malformed Echidna harness/config executions.

Echidna runs on `workflow_dispatch` and nightly schedule to keep PR latency bounded while preserving recurring stateful fuzz pressure.
