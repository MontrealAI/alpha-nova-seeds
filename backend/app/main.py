from fastapi import FastAPI, Response
from sqlalchemy import text
from .db import engine
from .schemas import DashboardSummary, ProofSummary, ReviewerStakeRow, CouncilSeatRow, ReadyStatus

app = FastAPI(title="Nova-Seeds v2.6 RC API", version="2.6.0-rc.1")


@app.get('/health')
def health():
    return {'ok': True, 'version': app.version}


@app.get('/ready', response_model=ReadyStatus)
def ready():
    with engine.begin() as conn:
        chain_events = conn.execute(text('SELECT count(*) FROM chain_events')).scalar_one_or_none() or 0
        cursor_block = conn.execute(text('SELECT last_safe_block FROM indexer_state WHERE id = 1')).scalar_one_or_none() or 0
    return ReadyStatus(ok=True, chain_events=chain_events, cursor_block=cursor_block)


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


@app.get('/proof/summary', response_model=ProofSummary)
def proof_summary():
    with engine.begin() as conn:
        chain_event_count = conn.execute(text('SELECT count(*) FROM chain_events')).scalar_one_or_none() or 0
        reviewer_ledger_rows = conn.execute(text('SELECT count(*) FROM reviewer_stake_ledger')).scalar_one_or_none() or 0
        council_lifecycle_rows = conn.execute(text('SELECT count(*) FROM council_seat_lifecycle')).scalar_one_or_none() or 0
        open_challenges = conn.execute(text('SELECT count(*) FROM seat_challenges WHERE resolved = false')).scalar_one_or_none() or 0
    return ProofSummary(
        chain_event_count=chain_event_count,
        reviewer_ledger_rows=reviewer_ledger_rows,
        council_lifecycle_rows=council_lifecycle_rows,
        open_challenges=open_challenges,
    )


@app.get('/governance/reviewer-ledger', response_model=List[ReviewerStakeRow])
def reviewer_ledger():
    with engine.begin() as conn:
        rows = conn.execute(text('SELECT reviewer, net_delta::float8 AS net_delta FROM reviewer_stake_balances ORDER BY reviewer ASC')).mappings().all()
    return [ReviewerStakeRow(**row) for row in rows]


@app.get('/governance/council-seats', response_model=List[CouncilSeatRow])
def council_seats():
    with engine.begin() as conn:
        rows = conn.execute(text('''
            SELECT term_id, seat_id, occupant, event_type, tx_hash, block_number
            FROM council_seat_lifecycle
            ORDER BY block_number DESC, log_index DESC
            LIMIT 200
        ''')).mappings().all()
    return [CouncilSeatRow(**row) for row in rows]


@app.get('/metrics')
def metrics():
    with engine.begin() as conn:
        chain_events = conn.execute(text('SELECT count(*) FROM chain_events')).scalar_one_or_none() or 0
        ledger_rows = conn.execute(text('SELECT count(*) FROM reviewer_stake_ledger')).scalar_one_or_none() or 0
        seats_rows = conn.execute(text('SELECT count(*) FROM council_seat_lifecycle')).scalar_one_or_none() or 0

    payload = (
        '# HELP nova_chain_events_total Indexed chain events\n'
        '# TYPE nova_chain_events_total gauge\n'
        f'nova_chain_events_total {chain_events}\n'
        '# HELP nova_reviewer_stake_rows_total Reviewer stake ledger rows\n'
        '# TYPE nova_reviewer_stake_rows_total gauge\n'
        f'nova_reviewer_stake_rows_total {ledger_rows}\n'
        '# HELP nova_council_lifecycle_rows_total Council seat lifecycle rows\n'
        '# TYPE nova_council_lifecycle_rows_total gauge\n'
        f'nova_council_lifecycle_rows_total {seats_rows}\n'
    )
    return Response(content=payload, media_type='text/plain; version=0.0.4')


@app.get('/openapi.json')
def openapi_export():
    return app.openapi()
