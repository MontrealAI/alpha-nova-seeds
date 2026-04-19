# Contracts testing guide (v2.6.0-rc.1)

This guide explains the security-testing command surface for the contracts subsystem from a clean checkout.

## Prerequisites

- Node.js `22.10.0+`
- npm
- Foundry (`forge`)
- Slither (`slither`)
- Echidna (`echidna`)

Install dependencies:

```bash
npm --prefix contracts ci
```

## Compile

```bash
npm run contracts:build
```

## Run the full contracts gate

```bash
npm run test:contracts
```

This executes unit + fuzz + invariant suites through Foundry.

## Unit tests (contract-aware + adversarial)

```bash
npm run test:contracts:unit
```

The suite includes per-contract happy/revert/authorization paths for:

- `AlphaNovaSeedV25`
- `NovaSeedRegistryV25`
- `ChallengePolicyModuleV25`
- `CouncilGovernanceV25`
- `ReviewerRewardTreasuryV25`
- `SignedAttestationVerifierV25`
- `ThresholdNetworkAdapterV25`
- `NovaSeedWorkflowAdapterV25`

## Fuzz tests

```bash
npm run test:contracts:fuzz
```

Fuzz coverage targets:

- threshold/quorum boundary constraints,
- reviewer accrual/slash/claim accounting boundaries,
- seat-count coherence,
- registry seed uniqueness and duplicate insertion rejection.

## Invariant tests

```bash
npm run test:contracts:invariant
```

Invariant coverage targets:

- accounting conservation (`accrued = claimed + clawed + balance`),
- governance seat-map coherence,
- persisted threshold profile validity,
- unauthorized creator inability to draft registry records.

## Echidna campaigns

```bash
npm run test:contracts:echidna
```

Campaign harnesses:

- `contracts/echidna/harnesses/EchidnaTreasuryHarness.sol`
- `contracts/echidna/harnesses/EchidnaGovernanceHarness.sol`
- `contracts/echidna/harnesses/EchidnaThresholdHarness.sol`
- `contracts/echidna/harnesses/EchidnaRegistryHarness.sol`

## Slither static analysis

```bash
npm run analyze:slither
```

Policy:

- high severity = release-blocking,
- medium severity = review-required,
- low severity = triage-required.

## CI gates

Contracts security is enforced by `.github/workflows/contracts-security.yml`:

- compile,
- integration tests,
- Foundry unit/fuzz/invariant tests,
- Slither fail-high analysis,
- Echidna campaigns (scheduled and manual dispatch).
