# Green Path Operator Guide (v2.6 RC)

## Goal
Provide the shortest safe path to run and verify the release candidate.

## Steps
1. Apply migrations in order.
2. Start backend and verify `/health`, `/readiness`, `/metrics`.
3. Run indexer with confirmations enabled.
4. Open dashboard and check green-path page status cards.
5. Run release verification commands from `docs/verify-release.md`.

## Abort conditions
- Migration failure
- Cursor regression
- Unexpected metric drops
- Hash mismatch in release artifacts
