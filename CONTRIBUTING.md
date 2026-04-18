# Contributing to alpha-nova-seeds

Thanks for helping with Nova-Seeds.

## Branch and commit rules

1. Keep pull requests small and implementation-ordered.
2. Match the constitutional stack order in code and docs changes:
   - identity
   - proof
   - settlement
   - governance
3. Do not claim audited, production-safe, or fully deployed status unless repository evidence exists.

## Development setup

### Contracts
- Language: Solidity (`contracts/`)
- Keep ABI and release metadata updated when public interfaces change.

### Backend
- Stack: FastAPI + Postgres (`backend/`)
- Add forward-only SQL migrations under `backend/migrations/`.
- Preserve idempotent indexing and reorg-safe behavior.

### Dashboard
- Keep operator pages plain-English first.
- Add deterministic JSON exports for operational snapshots.

## Pull request checklist

- [ ] Acceptance criteria listed in PR body.
- [ ] Migration notes listed (or “no migration required”).
- [ ] Rollback notes included.
- [ ] Provenance artifacts updated (hashes, manifests, attestations).
- [ ] Tests run locally and commands posted.

## Non-goals for release candidates

- Security audit declarations
- Mainnet deployment guarantees
- Marketing claims beyond implemented behavior
