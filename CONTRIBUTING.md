# Contributing to alpha-nova-seeds

Thanks for helping harden Nova-Seeds.

## Scope for v2.6 release candidate
This repository is currently shipping **v2.6 as a release candidate (RC)** focused on proof hardening. It is not an audited or final deployment release.

## Doctrine (must preserve)
When proposing changes, keep the stack and order intact:
1. **identity**
2. **proof**
3. **settlement**
4. **governance**

If your change touches multiple layers, call out impact in this order in your PR description.

## Development workflow
1. Create small, implementation-ordered commits.
2. Update docs and tests in the same PR.
3. Run local verification commands before opening a PR.
4. Do not remove a working component without documenting and shipping a replacement.

## Pull request checklist
- [ ] Acceptance criteria are explicit and testable.
- [ ] Migration notes are included if schema/API/contract behavior changed.
- [ ] Provenance artifacts are updated (manifest, checksums, attestations where relevant).
- [ ] Rollback notes are included for operators.
- [ ] Claims are scoped to what is implemented and verifiable.

## Coding conventions
- Backend stack remains **FastAPI + Postgres**.
- Contract stack remains **Solidity**.
- Operator docs should be plain-English first, technical second.
- Avoid TODOs unless absolutely unavoidable; ship complete paths when possible.

## Local verification quickstart
See `docs/verify-release.md` for full commands.
