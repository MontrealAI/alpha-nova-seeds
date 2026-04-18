# Nova-Seeds v2.6 RC backend

FastAPI + Postgres indexer backend for proof and governance visibility.

## Services
- `api` — REST endpoints, health/readiness, metrics, OpenAPI
- `worker` — deterministic event indexer and backfill command
- `postgres` — state store and read-model views
- `redis` — optional cache/checkpoints

## Key v2.6 RC surfaces
- `GET /health`
- `GET /ready`
- `GET /dashboard/summary`
- `GET /governance/reviewer-ledger`
- `GET /governance/council-seats`
- `GET /metrics`

## Migrations
Apply in order:
1. `backend/migrations/001_init.sql`
2. `backend/migrations/002_v26_hardening.sql`

## Deterministic backfill
```bash
python -m app.indexer --from-block 0 --to-block 12345678
```

## Export OpenAPI
```bash
python -m app.export_openapi
```
