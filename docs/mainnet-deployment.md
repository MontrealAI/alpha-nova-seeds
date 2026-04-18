# Mainnet deployment runbook (v2.6.0-rc.1)

> Warning: this repository is a **verifiable release candidate**. It is experimental software and requires operator review before any production action.

This runbook is for **operator-reviewed deployment tooling**, not automatic transaction broadcast.

## Doctrine and safety constraints

- identity → proof → settlement → governance
- no value without evidence
- no autonomy without authority
- no settlement without validation

Operational defaults:

- policy-bounded by default
- fail-closed scripts
- reproducible artifacts
- auditable manifests

## 1) Configure environment

Copy and edit:

```bash
cp contracts/.env.example contracts/.env
```

Required values before deployment:

- `MAINNET_RPC_URL`
- `SEPOLIA_RPC_URL`
- `DEPLOYER_PRIVATE_KEY`
- `ADMIN_OWNER_ADDRESS`
- `AGI_TOKEN_ADDRESS`
- `AGIJOBMANAGER_ADDRESS`
- `ETHERSCAN_API_KEY` (for verification)

Safety gates (all default false):

- `ALLOW_DEPLOY_TO_SEPOLIA`
- `ALLOW_DEPLOY_TO_MAINNET`
- `ALLOW_OWNERSHIP_TRANSFER`
- `ALLOW_ENS_PUBLISH`

## 2) Install + compile

```bash
npm --prefix contracts install
npm run contracts:build
npm run contracts:test
```

## 3) Checklist before any broadcast

```bash
npm run deploy:checklist
```

This confirms env shape and reminds operators that no permissive policy is enabled automatically.

## 4) Mainnet fork dry-run (required)

```bash
npm run deploy:fork
```

Dry-run output pack is written to:

- `contracts/deployments/mainnet-fork/<timestamp>/manifest.json`
- `contracts/deployments/mainnet-fork/<timestamp>/addresses.json`
- `contracts/deployments/mainnet-fork/<timestamp>/checksums.txt`
- `contracts/deployments/mainnet-fork/<timestamp>/postcheck-report.md`
- `contracts/deployments/mainnet-fork/<timestamp>/operator-handoff.md`

## 5) Sepolia rehearsal (recommended)

```bash
npm run deploy:sepolia
```

## 6) Mainnet deployment (explicit broadcast step)

```bash
npm run deploy:mainnet
```

This command is intentionally guarded and requires both:

- `ALLOW_DEPLOY_TO_MAINNET=true`
- explicit `--broadcast` flag from the root script wiring

## 7) Etherscan verification

```bash
npm run deploy:verify
```

## 8) Post-deploy checks and handoff

```bash
npm run deploy:postcheck
npm run deploy:handoff
```

## What remains paused/closed by default

The deployment layer does **not** auto-enable:

- registry creator allowlists
- attestation trusted signers
- threshold decryption profiles
- challenge policies

These must be configured via explicit governance-approved transactions after reviewing deployment reports.

## Manual review required before any activation

1. Confirm owner/admin addresses and multisig/Safe control.
2. Confirm external dependency addresses (`AGI_TOKEN_ADDRESS`, `AGIJOBMANAGER_ADDRESS`).
3. Confirm manifest and checksum consistency.
4. Confirm Etherscan verification status for each deployed contract.
5. Record governance approval for each policy opening step.
