# Releases

## v2.6-rc release contract

Each release candidate must include:

1. **Acceptance criteria** tied to shipped features.
2. **Migration notes** with ordered SQL/API rollout.
3. **Provenance artifacts** (source archive hash, SHA256SUMS, attestations, SBOM).
4. **Rollback notes** with operator decision points.

## Release flow

1. Merge implementation changes and docs.
2. Run CI and local verification checks.
3. Trigger `release-provenance.yml` workflow.
4. Publish release notes referencing generated artifacts.
5. Validate `docs/verify-release.md` commands against the release assets.
