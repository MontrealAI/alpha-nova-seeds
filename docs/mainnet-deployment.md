# Mainnet Deployment Guide

## Purpose

This guide describes how to deploy the `alpha-nova-seeds` smart-contract stack to **Ethereum mainnet** under a **fail-closed, operator-reviewed posture**.

This guide is for the current public repository shape:

- `contracts/`
- `sdk/`
- `backend/`
- `dashboard/`

and is intended for the next **verifiable release-candidate** phase, not for a claim of audited or unrestricted production safety.

## What this deploys

The mainnet deployment should cover the repo’s on-chain governance and seed-formation surfaces, as actually present in `contracts/` after local inspection.

Expected logical modules:

- Nova-Seed identity / registry
- threshold-attestation / encrypted review round layer
- reviewer stake / reward accounting
- council seat governance
- challenge / dispute policy

> Replace logical module names with the exact contract names found under `contracts/` before broadcast.

---

## Safety posture

Mainnet deployment for `alpha-nova-seeds` is **fail-closed by default**.

That means:

- contracts deploy **paused**
- open enrollment is **off**
- public rounds are **off**
- allowlists are **on**
- thresholds are conservative
- ownership / admin rights are handed to a reviewed operator address or multisig
- no broadcast happens by default
- no activation happens without a separate review step

---

## Prerequisites

### Tooling

- Node.js (repo-supported version)
- npm or pnpm (match repo choice after local inspection)
- Hardhat 3
- Hardhat Ignition
- GitHub CLI (`gh`) for artifact attestation verification if configured
- Docker (if backend/dashboard postchecks use containers)

### Secrets and environment variables

Set these before deployment:

- `MAINNET_RPC_URL`
- `MAINNET_RPC_URL_SECONDARY` (recommended)
- `MAINNET_FORK_RPC_URL` (for dry-runs)
- `DEPLOYER_PRIVATE_KEY`
- `ETHERSCAN_API_KEY`

Optional / recommended:

- `ADMIN_OWNER_ADDRESS`
- `PAUSER_ADDRESS`
- `TREASURY_ADDRESS`
- `COUNCIL_ADMIN_ADDRESS`
- `EMERGENCY_GUARDIAN_ADDRESS`

> Never commit private keys or real production secrets.

---

## Configuration file

Use:

`deployment-config/mainnet.example.json`

as the template for your real deployment config.

Create a real file such as:

`deployment-config/mainnet.json`

and fill in:

- owner/admin addresses
- treasury addresses
- dependency addresses
- threshold/quorum values
- ENS settings if used

Do not edit code for environment-specific values unless absolutely necessary.

---

## Recommended deployment flow

### 1. Inspect the contracts layer

From repo root:

```bash
cd contracts
ls
```

Confirm:

- actual contract names
- actual module names
- whether Hardhat is already initialized
- whether Ignition modules already exist
- whether deployment scripts already exist

### 2. Install dependencies

```bash
cd contracts
npm ci
```

### 3. Compile

```bash
npm run build
# or
npx hardhat compile
```

### 4. Run contract tests

```bash
npm test
# or
npx hardhat test
```

### 5. Run static analysis (if configured)

```bash
npm run analyze
# or
npx slither .
```

### 6. Run a mainnet-fork dry-run

```bash
npm run deploy:fork
# or expected equivalent:
npx hardhat run scripts/deploy/dryrun-mainnet-fork.ts --network hardhat
```

The dry-run should:

- deploy the full contract graph
- write a deployment manifest
- emit a postcheck report
- confirm ownership / pause state / role assignments
- confirm thresholds match config
- confirm no unexpected open enrollment or unpaused state

### 7. Review the dry-run artifacts

Expected output directory:

`contracts/deployments/mainnet-fork/<timestamp>/`

Review at minimum:

- `manifest.json`
- `addresses.json`
- `postcheck-report.md`
- `operator-handoff.md`

Do not proceed if:
- ownership is wrong
- pause flags are wrong
- threshold values differ from config
- unresolved warnings remain in the postcheck report

### 8. Optional testnet rehearsal

If supported:

```bash
npm run deploy:sepolia
npm run deploy:verify -- --network sepolia
npm run deploy:postcheck -- --network sepolia
```

### 9. Mainnet deployment

Broadcast only after dry-run review:

```bash
npm run deploy:mainnet
# or expected equivalent:
npx hardhat ignition deploy ./ignition/modules/CompositeMainnet.ts --network mainnet --parameters deployment-config/mainnet.json
```

### 10. Verify deployed contracts

```bash
npm run deploy:verify
# or expected equivalent:
npx hardhat verify --network mainnet <contract-address> <constructor-args...>
```

### 11. Run post-deploy checks

```bash
npm run deploy:postcheck
```

### 12. Transfer ownership / admin roles

If deployment used a hot deployer account first, complete the handoff:

```bash
npm run deploy:handoff
# or expected equivalent:
npx hardhat run scripts/deploy/transfer-ownership.ts --network mainnet
```

Review that:

- owner = multisig / reviewed admin
- pauser = expected guardian
- treasury = expected address
- deployer retains no unnecessary privileged role

---

## Expected deployment artifacts

Each mainnet deployment should write:

`contracts/deployments/mainnet/<timestamp>/`

including:

- `manifest.json`
- `addresses.json`
- `checksums.txt`
- `postcheck-report.md`
- `operator-handoff.md`

Recommended additional files:

- `build-info.json`
- `verification.json`
- `sbom.spdx.json`
- `attestation.json`

---

## Mainnet review checklist

Before any unpause or public activation, verify:

- [ ] all contracts compiled from the expected commit
- [ ] deployment manifest matches the reviewed config
- [ ] contracts are paused
- [ ] open/public enrollment is off
- [ ] allowlists are active where intended
- [ ] threshold and quorum values are conservative
- [ ] ownership has been transferred correctly
- [ ] Etherscan verification succeeded
- [ ] no unresolved warnings remain in postcheck report
- [ ] operator handoff packet has been archived

---

## Optional ENS publication

If ENS integration is part of the current contracts layer, publish only after core deployment review.

Possible publication step:

```bash
npm run deploy:publish-ens
```

Only publish:

- stable names
- canonical pointers
- metadata / API references

Do not use ENS publication as a substitute for deployment verification.

---

## Post-deploy activation policy

Activation should be a **separate** step from deployment.

Recommended order:

1. deploy paused
2. verify contracts
3. hand off ownership
4. review manifests and reports
5. activate specific allowlists and council seats
6. unpause only the minimum required surface
7. observe metrics and logs before widening access

---

## Emergency controls

Document and test:

- pause
- partial pause if supported
- reviewer enrollment freeze
- council seat suspension
- ownership emergency escalation

If any emergency control is missing or untested, do not widen usage.

---

## What this guide does not claim

This guide does **not** claim that the repo is:

- audited
- risk-free
- unrestricted for open public use
- ready for broad autonomous market exposure

It is a deployment guide for an operator-reviewed, policy-bounded mainnet posture.

---

## Suggested first operator command set

```bash
cd contracts
npm ci
npm run build
npm test
npm run deploy:fork
npm run deploy:mainnet
npm run deploy:verify
npm run deploy:postcheck
npm run deploy:handoff
```

Adjust command names to match the final scripts implemented in this repo.
