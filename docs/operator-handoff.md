# Operator handoff checklist

Use this checklist after deployment artifacts are generated.

## Artifact packet to archive

From `contracts/deployments/<network>/<timestamp>/` archive:

- `manifest.json`
- `addresses.json`
- `checksums.txt`
- `postcheck-report.md`
- `operator-handoff.md`

## What operators must confirm

- Deployed addresses match expected module graph.
- Owner/admin for all contracts is the intended multisig or approved control address.
- No unauthorized signer or creator has been pre-authorized.
- Challenge and governance settings are conservative and evidence-backed.
- Verification links are attached and reproducible from the manifest.

## Transfer and acceptance

- If deployment used a temporary owner, run `npm run deploy:handoff` with `ALLOW_OWNERSHIP_TRANSFER=true`.
- Require two-person review of final owner state and checksum file.
- Store artifact packet in release provenance storage together with commit SHA.

## Caveat

This repo is a release candidate with hardening surfaces. Operator acceptance does not imply audited-final posture.
