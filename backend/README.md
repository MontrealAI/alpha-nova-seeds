# Nova-Seeds Backend (FastAPI + Postgres)

## What this service does
- exposes operator API for dashboard views,
- indexes on-chain events from `NovaSeedRegistryV25`,
- maintains deterministic read models.

## v2.6 RC hardening
- versioned SQL migrations,
- idempotent event ingestion,
- reorg-safe cursor + confirmations,
- `/health`, `/readiness`, `/metrics`,
- OpenAPI export (`/openapi/export` and `scripts/export_openapi.py`),
- deterministic backfill (`scripts/backfill.py`).

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Migrations

Apply in order:
1. `migrations/001_init.sql`
2. `migrations/002_indexer_cursor.sql`
3. `migrations/003_governance_accounting.sql`
