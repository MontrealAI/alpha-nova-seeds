import json
from pathlib import Path
from web3 import Web3
from sqlalchemy import text
from .config import RPC_URL, REGISTRY_ADDRESS, START_BLOCK, CONFIRMATIONS, INDEXER_NAME
from .db import engine

ABI = json.loads(Path(__file__).with_name('abi').joinpath('NovaSeedRegistryV25.events.json').read_text())


def upsert_chain_event(conn, payload: dict):
    conn.execute(text("""
        INSERT INTO chain_events (block_number, tx_hash, log_index, contract_address, event_name, payload)
        VALUES (:block_number, :tx_hash, :log_index, :contract_address, :event_name, CAST(:payload AS JSONB))
        ON CONFLICT (tx_hash, log_index) DO NOTHING
    """), payload)


def load_cursor(conn) -> int:
    row = conn.execute(text("SELECT last_finalized_block FROM indexer_cursors WHERE name=:name"), {'name': INDEXER_NAME}).mappings().first()
    if row:
        return int(row['last_finalized_block'])
    conn.execute(
        text("INSERT INTO indexer_cursors(name, last_finalized_block, updated_at) VALUES (:name, :block, now()) ON CONFLICT (name) DO NOTHING"),
        {'name': INDEXER_NAME, 'block': START_BLOCK}
    )
    return START_BLOCK


def save_cursor(conn, block_number: int):
    conn.execute(text("""
        INSERT INTO indexer_cursors(name, last_finalized_block, updated_at)
        VALUES (:name, :block, now())
        ON CONFLICT (name)
        DO UPDATE SET last_finalized_block = EXCLUDED.last_finalized_block, updated_at = now()
    """), {'name': INDEXER_NAME, 'block': block_number})


def index_range(w3: Web3, from_block: int, to_block: int) -> int:
    if to_block < from_block:
        return from_block
    contract = w3.eth.contract(address=Web3.to_checksum_address(REGISTRY_ADDRESS), abi=ABI)
    with engine.begin() as conn:
        for event_abi in ABI:
            event = contract.events[event_abi['name']]
            logs = event.get_logs(fromBlock=from_block, toBlock=to_block)
            for log in logs:
                payload = {
                    'block_number': log['blockNumber'],
                    'tx_hash': log['transactionHash'].hex(),
                    'log_index': log['logIndex'],
                    'contract_address': REGISTRY_ADDRESS,
                    'event_name': event_abi['name'],
                    'payload': json.dumps(dict(log['args']), default=str),
                }
                upsert_chain_event(conn, payload)
        save_cursor(conn, to_block)
    return to_block


def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    latest = w3.eth.block_number
    finalized = max(START_BLOCK, latest - CONFIRMATIONS)
    with engine.begin() as conn:
        cursor = load_cursor(conn)
    from_block = cursor + 1
    indexed = index_range(w3, from_block, finalized)
    print(f"Indexed from {from_block} to {indexed} (latest={latest}, confirmations={CONFIRMATIONS})")


if __name__ == '__main__':
    main()
