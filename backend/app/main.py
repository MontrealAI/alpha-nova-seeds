from fastapi import FastAPI
from sqlalchemy import text
from .db import engine
from .schemas import DashboardSummary

app = FastAPI(title="Nova-Seeds v2.5 API")

@app.get('/health')
def health():
    return {'ok': True}

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
