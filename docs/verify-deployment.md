# Verify deployment artifacts and contract publication

## 1) Validate manifest structure

Inspect `contracts/deployments/<network>/<timestamp>/manifest.json` for:

- `chainId`
- `commitSha`
- `contracts[]` names and addresses
- `deployedBytecodeHash`
- artifact/build-info hints
- verification status entries

## 2) Validate checksums

Run:

```bash
cd contracts/deployments/<network>/<timestamp>
sha256sum -c checksums.txt
```

## 3) Verify on Etherscan

From repo root:

```bash
npm run deploy:verify
```

If any verification fails, treat deployment as incomplete until mismatch is explained and resolved.

## 4) Cross-check runtime links

From `postcheck-report.md` ensure:

- release metadata endpoint matches expected version/hash
- registry ↔ NFT and registry ↔ treasury distributor wiring are correct
- owner targets match operator intent

## 5) Record provenance

Archive together:

- deployment packet files
- `git rev-parse HEAD` output
- contract build-info references
- release provenance manifest from `scripts/release/generate_provenance_manifest.py`
