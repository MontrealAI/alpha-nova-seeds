from fastapi import FastAPI
from sqlalchemy import text
from .db import engine
from .schemas import (
    DashboardSummary,
    ReadinessStatus,
    MetricPoint,
    ReviewerStakeRow,
    CouncilSeatRow,
)

app = FastAPI(title="Nova-Seeds v2.6 RC API")

@app.get('/health')
def health():
    return {'ok': True}

@app.get('/ready', response_model=ReadinessStatus)
def ready():
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT COALESCE(last_scanned_block, 0) AS latest_block, COALESCE(last_safe_block, 0) AS safe_block
            FROM indexer_cursors
            WHERE cursor_name = 'registry'
        """)).mappings().first()
    if not row:
        return ReadinessStatus(ready=False, latest_block=0, safe_block=0)
    return ReadinessStatus(ready=True, latest_block=int(row["latest_block"]), safe_block=int(row["safe_block"]))

@app.get('/dashboard/summary', response_model=DashboardSummary)
def dashboard_summary():
    with engine.begin() as conn:
        seed_count = conn.execute(text('SELECT count(*) FROM seeds')).scalar_one_or_none() or 0
        greenlit_count = conn.execute(text('SELECT count(*) FROM seeds WHERE state = 4')).scalar_one_or_none() or 0
        sovereign_count = conn.execute(text('SELECT count(*) FROM seeds WHERE state = 6')).scalar_one_or_none() or 0
        open_decryption_requests = conn.execute(text('SELECT count(*) FROM decryption_requests WHERE status = 1')).scalar_one_or_none() or 0
        open_challenges = conn.execute(text('SELECT count(*) FROM seat_challenges WHERE resolved = false')).scalar_one_or_none() or 0
        total_delegations = conn.execute(text('SELECT count(*) FROM delegations')).scalar_one_or_none() or 0
        total_reward_events = conn.execute(text('SELECT count(*) FROM reward_events')).scalar_one_or_none() or 0
    return DashboardSummary(
        seed_count=seed_count,
        greenlit_count=greenlit_count,
        sovereign_count=sovereign_count,
        open_decryption_requests=open_decryption_requests,
        open_challenges=open_challenges,
        total_delegations=total_delegations,
        total_reward_events=total_reward_events,
    )

@app.get('/metrics')
def metrics():
    with engine.begin() as conn:
        seed_count = conn.execute(text('SELECT count(*) FROM seeds')).scalar_one_or_none() or 0
        chain_events = conn.execute(text('SELECT count(*) FROM chain_events')).scalar_one_or_none() or 0
        open_challenges = conn.execute(text('SELECT count(*) FROM seat_challenges WHERE resolved = false')).scalar_one_or_none() or 0
    return {
        "metrics": [
            MetricPoint(name="seed_count", value=float(seed_count)).model_dump(),
            MetricPoint(name="chain_events", value=float(chain_events)).model_dump(),
            MetricPoint(name="open_challenges", value=float(open_challenges)).model_dump(),
        ]
    }

@app.get('/governance/reviewer-ledger', response_model=list[ReviewerStakeRow])
def reviewer_ledger():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT reviewer, total_rewards, total_claimed, total_slashed, claimable
            FROM reviewer_stake_ledger_v26
            ORDER BY reviewer ASC
        """)).mappings().all()
    return [ReviewerStakeRow(**dict(row)) for row in rows]

@app.get('/governance/council-seats', response_model=list[CouncilSeatRow])
def council_seats():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT term_id, seat_id, open_challenges, resolved_challenges
            FROM council_seat_lifecycle_v26
            ORDER BY term_id DESC, seat_id ASC
        """)).mappings().all()
    return [CouncilSeatRow(**dict(row)) for row in rows]
