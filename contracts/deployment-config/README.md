# Deployment configuration profiles

This folder stores operator-reviewed configuration profiles used by deployment scripts.

## Posture

- Fail-closed defaults.
- No automatic activation of creators, signers, threshold profiles, or challenge policies.
- Ownership is set to `ADMIN_OWNER_ADDRESS` at deploy time, then re-checked in postcheck.

## Files

- `mainnet.example.json` — conservative reference values.
- `sepolia.example.json` — testnet reference values.

Copy one of these files and adapt to your operation with evidence-backed governance approvals.
