import json
from pathlib import Path
from web3 import Web3
from sqlalchemy import text
from .config import RPC_URL, REGISTRY_ADDRESS, START_BLOCK, REORG_WINDOW, CONFIRMATIONS
from .db import engine

ABI = json.loads(Path(__file__).with_name('abi').joinpath('NovaSeedRegistryV25.events.json').read_text())


def _event_seed_id(args: dict) -> str:
    if 'seedId' in args:
        value = args['seedId']
        if hasattr(value, 'hex'):
            return value.hex()
        return str(value)
    return ''


def upsert_chain_event(conn, payload: dict):
    conn.execute(text("""
        INSERT INTO chain_events (block_number, tx_hash, log_index, contract_address, event_name, payload)
        VALUES (:block_number, :tx_hash, :log_index, :contract_address, :event_name, CAST(:payload AS JSONB))
        ON CONFLICT (tx_hash, log_index) DO NOTHING
    """), payload)


def upsert_governance_views(conn, payload: dict):
    event_name = payload['event_name']
    args = payload['args']

    if event_name == 'ReviewSubmitted':
        conn.execute(text("""
            INSERT INTO reviewer_stake_ledger (reviewer, delta, kind, reason_hash, tx_hash, log_index, block_number)
            VALUES (:reviewer, :delta, :kind, :reason_hash, :tx_hash, :log_index, :block_number)
            ON CONFLICT (tx_hash, log_index) DO NOTHING
        """), {
            'reviewer': args.get('reviewer', '').lower(),
            'delta': 1,
            'kind': 'accrual',
            'reason_hash': args.get('reasonHash', ''),
            'tx_hash': payload['tx_hash'],
            'log_index': payload['log_index'],
            'block_number': payload['block_number'],
        })

    if event_name in ('SeedGreenlit', 'SeedQuarantined'):
        conn.execute(text("""
            INSERT INTO council_seat_lifecycle (term_id, seat_id, occupant, event_type, tx_hash, log_index, block_number)
            VALUES (NULL, NULL, NULL, :event_type, :tx_hash, :log_index, :block_number)
            ON CONFLICT (tx_hash, log_index) DO NOTHING
        """), {
            'event_type': 'reassigned' if event_name == 'SeedGreenlit' else 'deactivated',
            'tx_hash': payload['tx_hash'],
            'log_index': payload['log_index'],
            'block_number': payload['block_number'],
        })


def _load_cursor(conn) -> int:
    return conn.execute(text('SELECT last_safe_block FROM indexer_state WHERE id = 1')).scalar_one_or_none() or 0


def _save_cursor(conn, block_number: int):
    conn.execute(text('''
        INSERT INTO indexer_state (id, last_safe_block, updated_at)
        VALUES (1, :block_number, now())
        ON CONFLICT (id) DO UPDATE SET last_safe_block = EXCLUDED.last_safe_block, updated_at = now()
    '''), {'block_number': block_number})


def run_once(start_override: int | None = None, end_override: int | None = None):
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=Web3.to_checksum_address(REGISTRY_ADDRESS), abi=ABI)
    latest = w3.eth.block_number
    safe_tip = max(0, latest - CONFIRMATIONS)

    with engine.begin() as conn:
        cursor = _load_cursor(conn)
        start_block = max(START_BLOCK, cursor - REORG_WINDOW)
        if start_override is not None:
            start_block = start_override

        end_block = safe_tip if end_override is None else min(end_override, safe_tip)

        if end_block < start_block:
            return {'indexed_to': cursor, 'safe_tip': safe_tip, 'events': 0}

        # Reorg-safe delete for mutable tail
        conn.execute(text('DELETE FROM chain_events WHERE block_number >= :start_block'), {'start_block': start_block})

        events = 0
        for event_abi in ABI:
            event = contract.events[event_abi['name']]
            logs = event.get_logs(fromBlock=start_block, toBlock=end_block)
            for log in logs:
                args = dict(log['args'])
                payload = {
                    'block_number': log['blockNumber'],
                    'tx_hash': log['transactionHash'].hex(),
                    'log_index': log['logIndex'],
                    'contract_address': REGISTRY_ADDRESS,
                    'event_name': event_abi['name'],
                    'payload': json.dumps(args, default=str),
                }
                upsert_chain_event(conn, payload)
                upsert_governance_views(conn, {
                    'event_name': event_abi['name'],
                    'args': args,
                    'tx_hash': payload['tx_hash'],
                    'log_index': payload['log_index'],
                    'block_number': payload['block_number'],
                    'seed_id': _event_seed_id(args),
                })
                events += 1

        _save_cursor(conn, end_block)

    return {'indexed_to': end_block, 'safe_tip': safe_tip, 'events': events}


def main():
    result = run_once()
    print(f"Indexed {result['events']} events through safe block {result['indexed_to']} (tip={result['safe_tip']})")


if __name__ == '__main__':
    main()
