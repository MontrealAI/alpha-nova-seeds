# Release Process

This project follows a release-candidate-first discipline.

## v2.6 RC gate
A v2.6 release candidate is valid only when it includes:
1. concrete acceptance criteria,
2. explicit migration notes,
3. provenance artifacts (manifest/checksums/attestations),
4. rollback notes.

## Steps
1. Run local tests and static checks.
2. Generate release artifacts and `SHA256SUMS`.
3. Verify artifacts using `docs/verify-release.md`.
4. Tag RC (`v2.6-rc.N`) after review.

## Artifacts
Artifacts are produced by GitHub Actions in `.github/workflows/release-provenance.yml` and include source bundle, ABI/schema bundle, checksums, and attestations.
