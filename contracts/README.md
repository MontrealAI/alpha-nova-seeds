# Nova-Seeds contracts map (v2.6 RC posture)

This package contains Solidity surfaces for the Nova-Seeds on-chain anchors.

Doctrine alignment:

1. **identity**
2. **proof**
3. **settlement**
4. **governance**

This is a release-candidate architecture surface, not an audited final deployment claim.

## Contract roles

- `AlphaNovaSeedV25.sol` — primary seed identity/formation anchor.
- `NovaSeedRegistryV25.sol` — registry of seed records and status transitions.
- `SignedAttestationVerifierV25.sol` — signature and attestation validation hooks.
- `ThresholdNetworkAdapterV25.sol` — threshold-network integration adapter surface.
- `NovaSeedWorkflowAdapterV25.sol` — workflow bridge between seed lifecycle and execution modules.
- `ChallengePolicyModuleV25.sol` — challenge/dispute policy mechanics.
- `ReviewerRewardTreasuryV25.sol` — reviewer reward/stake treasury mechanics.
- `CouncilGovernanceV25.sol` — council seat/governance decision mechanics.

## Interface package

- `interfaces/` contains typed contract interfaces used across modules and indexer/event decoding surfaces.

## ABI export surface

Stable ABI snapshots are kept in:

- `contracts/abi/`

Generate/update snapshots with:

```bash
python scripts/contracts/export_abi.py
```

## v2.6 RC hardening expectations

When modifying contract behavior:

- add or update NatSpec on public/external surfaces
- update corresponding tests and ABI snapshots
- document governance/settlement semantics changes in docs
- avoid hidden privileged paths
