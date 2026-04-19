# Nova-Seeds contracts map (v2.6 RC posture)

This package contains Solidity surfaces for the Nova-Seeds on-chain anchors.

Doctrine alignment:

1. **identity**
2. **proof**
3. **settlement**
4. **governance**

This is a verifiable release-candidate architecture surface, not an audited final deployment claim.

## Contract roles

- `AlphaNovaSeedV25.sol` — primary seed identity/formation anchor.
- `NovaSeedRegistryV25.sol` — registry of seed records and status transitions.
- `SignedAttestationVerifierV25.sol` — signature and attestation validation hooks.
- `ThresholdNetworkAdapterV25.sol` — threshold-network integration adapter surface.
- `NovaSeedWorkflowAdapterV25.sol` — workflow bridge between seed lifecycle and execution modules.
- `ChallengePolicyModuleV25.sol` — challenge/dispute policy mechanics.
- `ReviewerRewardTreasuryV25.sol` — reviewer reward/stake treasury mechanics.
- `CouncilGovernanceV25.sol` — council seat/governance decision mechanics.

## Hardhat deployment workspace

The contracts package now includes a Hardhat 3 deployment/verification workspace:

- `hardhat.config.ts` — network + compiler + verification setup.
- `ignition/modules/` — declarative module graph for repeatable deployment.
- `scripts/deploy/` — operator scripts for checklist, dry-run, deployment, verification, postcheck, and ownership handoff.
- `deployments/<network>/<timestamp>/` — generated manifest + addresses + checksums + postcheck + operator handoff pack.
- `deployment-config/` — conservative profile examples for rehearsals and governance review.

## Operator safety posture

Deployment scripts are fail-closed by default:

- no auto-broadcast to mainnet without explicit `--broadcast` plus env gate
- no auto-activation of creators/signers/profiles/policy knobs
- no private keys in source control (env only)
- explicit role ownership checks + manifest-driven handoff tooling

## Interface package

- `interfaces/` contains typed contract interfaces used across modules and indexer/event decoding surfaces.

## ABI export surface

Stable ABI snapshots are kept in:

- `contracts/abi/`

Generate/update snapshots with:

```bash
python scripts/contracts/export_abi.py
```

## Build and test

From repository root:

```bash
npm run contracts:build
npm run contracts:test
npm run contracts:test:fork
```

Before deployment scripts, create operator-reviewed deployment config files:

```bash
cp contracts/deployment-config/mainnet.example.json contracts/deployment-config/mainnet.json
cp contracts/deployment-config/sepolia.example.json contracts/deployment-config/sepolia.json
```

## v2.6 RC hardening expectations

When modifying contract behavior:

- add or update NatSpec on public/external surfaces
- update corresponding tests and ABI snapshots
- document governance/settlement semantics changes in docs
- avoid hidden privileged paths
