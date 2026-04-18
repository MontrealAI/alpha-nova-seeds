# Nova-Seeds v2.5 backend

Production-oriented starter backend:
- **Postgres** for indexed state
- **Redis** for checkpoints/caching
- **FastAPI** for REST APIs
- **web3.py** event indexer

## Services
- `api` — REST + dashboard summary
- `worker` — event indexer / backfiller
- `postgres` — state store
- `redis` — offsets + cache

## Quick start
```bash
cp .env.example .env
# fill values

docker compose up --build
```

Then open:
- API docs: `http://localhost:8000/docs`
- Dashboard: `dashboard/index.html`
