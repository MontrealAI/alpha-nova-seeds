from pathlib import Path
from fastapi import FastAPI, Response
from sqlalchemy import text
from .db import engine
from .schemas import DashboardSummary, OperationalStatus

APP_VERSION = "2.6.0-rc1"
app = FastAPI(title="Nova-Seeds API", version=APP_VERSION)


@app.get('/health', response_model=OperationalStatus)
def health():
    return OperationalStatus(ok=True, service='nova-seeds-backend', version=APP_VERSION)


@app.get('/readiness', response_model=OperationalStatus)
def readiness():
    with engine.begin() as conn:
        conn.execute(text('SELECT 1'))
    return OperationalStatus(ok=True, service='nova-seeds-backend', version=APP_VERSION)


@app.get('/metrics')
def metrics():
    with engine.begin() as conn:
        chain_events = conn.execute(text('SELECT count(*) FROM chain_events')).scalar_one_or_none() or 0
        open_decryptions = conn.execute(text('SELECT count(*) FROM decryption_requests WHERE status = 1')).scalar_one_or_none() or 0

    body = '\n'.join([
        '# HELP nova_chain_events_total Indexed chain event count',
        '# TYPE nova_chain_events_total gauge',
        f'nova_chain_events_total {chain_events}',
        '# HELP nova_decryption_requests_open Open decryption requests',
        '# TYPE nova_decryption_requests_open gauge',
        f'nova_decryption_requests_open {open_decryptions}',
        ''
    ])
    return Response(content=body, media_type='text/plain; version=0.0.4; charset=utf-8')


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


@app.get('/dashboard/reviewer-ledger')
def reviewer_ledger():
    with engine.begin() as conn:
        rows = conn.execute(text('''
            SELECT reviewer, sum(delta) as net_delta, count(*) as event_count
            FROM reward_events
            GROUP BY reviewer
            ORDER BY reviewer
        ''')).mappings().all()
    return {'items': [dict(r) for r in rows]}


@app.get('/dashboard/council-seats')
def council_seats():
    with engine.begin() as conn:
        rows = conn.execute(text('''
            SELECT seat_id, term_id, challenger, resolved, upheld, created_at
            FROM seat_challenges
            ORDER BY created_at DESC
            LIMIT 200
        ''')).mappings().all()
    return {'items': [dict(r) for r in rows]}


@app.get('/openapi/export')
def export_openapi():
    spec = app.openapi()
    target = Path(__file__).resolve().parents[1] / 'openapi.json'
    target.write_text(__import__('json').dumps(spec, indent=2))
    return {'ok': True, 'path': str(target)}
