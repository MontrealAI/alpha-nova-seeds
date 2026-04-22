# Releases

## v2.8 RC release contract

Each release candidate must include:

1. **Acceptance criteria** tied to shipped features.
2. **Migration notes** with ordered rollout guidance.
3. **Provenance artifacts** (source archive hash, SHA256SUMS, attestations, SBOM).
4. **Rollback notes** with operator decision points.

## Immutable release asset naming

Use deterministic file names keyed by tag:

- `alpha-nova-seeds-<TAG>.tar.gz`
- `provenance-manifest-<TAG>.json`
- `sbom-<TAG>.spdx.json`
- `openapi-<API_VERSION>.json` (currently `openapi-v2.6.0-rc.1.json`)
- `SHA256SUMS`

Do not overwrite assets for an existing `<TAG>`.
If regeneration is required, cut a new RC tag.

## Release flow

1. Merge implementation and docs.
2. Run verification checks:
   - `pytest -q backend/tests`
   - `python backend/scripts/export_openapi.py`
   - `python scripts/contracts/export_abi.py`
   - `cd sdk && npm run build --if-present`
   - `python scripts/release/generate_provenance_manifest.py --tag <TAG> --output /tmp/provenance-manifest-<TAG>.json`
3. Trigger `release-provenance.yml`.
4. Publish release notes with generated artifacts.
5. Validate `docs/verify-release.md` commands against published assets.

## Demo-and-doctrine RC acceptance surfaces

For v2.8.x publication:

- Flagship demo replay + assert mode passing.
- Demo ladder cross-links and role labels passing validation.
- Root README links to flagship, ladder, doctrine, and release posture docs.
- Math markdown validation helper passing.
- Doctrine consistency helper passing.
- Explicit synthetic-vs-real boundary language present on flagship, ladder, and release docs.
- Dashboard operator UI labels synthetic surfaces clearly and links to doctrine/release verification pointers.
