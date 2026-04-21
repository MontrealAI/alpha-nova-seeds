# Releases

## v2.7 demo+doctrine RC release contract

Each release candidate must include:

1. **Acceptance criteria** tied to shipped features.
2. **Migration notes** with ordered SQL/API rollout.
3. **Provenance artifacts** (source archive hash, SHA256SUMS, attestations, SBOM).
4. **Rollback notes** with operator decision points.

## Immutable release asset naming

Use deterministic file names keyed by tag so operators can verify from a clean machine:

- `alpha-nova-seeds-<TAG>.tar.gz`
- `provenance-manifest-<TAG>.json`
- `sbom-<TAG>.spdx.json`
- `openapi-v2.6.0-rc.1.json`
- `SHA256SUMS`

Do not overwrite an existing release asset for the same `<TAG>`.
If regeneration is required, cut a new tag (for example, `v2.6.0-rc.2`) and produce a new immutable set.

## Release flow

1. Merge implementation changes and docs.
2. Run CI and local verification checks:
   - `pytest -q backend/tests`
   - `python backend/scripts/export_openapi.py`
   - `python scripts/contracts/export_abi.py`
   - `cd sdk && npm run build --if-present`
   - `python scripts/release/generate_provenance_manifest.py --tag <TAG> --output /tmp/provenance-manifest-<TAG>.json`
3. Trigger `release-provenance.yml` workflow.
4. Publish release notes referencing generated artifacts.
5. Validate `docs/verify-release.md` commands against the release assets.


## Demo-and-doctrine RC acceptance surfaces

For v2.7.0-rc.1, release publication additionally requires:

- Flagship demo replay command and assert mode passing.
- Cross-linked demo ladder (flagship synthetic, compact synthetic adjacent, real-world pack).
- Doctrine stack docs linked from root README.
- Math markdown validation helper run and passing.
- Explicit claim boundary: synthetic sovereign claim only; broader cybersecurity sovereign remains future-facing.
