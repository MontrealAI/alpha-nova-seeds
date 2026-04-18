import json
import argparse
from pathlib import Path
from web3 import Web3
from sqlalchemy import text
from .config import RPC_URL, REGISTRY_ADDRESS, START_BLOCK
from .db import engine

ABI = json.loads(Path(__file__).with_name('abi').joinpath('NovaSeedRegistryV25.events.json').read_text())
CURSOR_NAME = "registry"
CONFIRMATION_LAG = 3


def upsert_seed(conn, payload: dict):
    conn.execute(text("""
        INSERT INTO chain_events (block_number, tx_hash, log_index, contract_address, event_name, payload)
        VALUES (:block_number, :tx_hash, :log_index, :contract_address, :event_name, CAST(:payload AS JSONB))
        ON CONFLICT (tx_hash, log_index) DO NOTHING
    """), payload)


def get_cursor(conn):
    row = conn.execute(text("""
        SELECT last_scanned_block
        FROM indexer_cursors
        WHERE cursor_name = :cursor_name
    """), {"cursor_name": CURSOR_NAME}).mappings().first()
    if row:
        return int(row["last_scanned_block"])
    return START_BLOCK


def update_cursor(conn, latest_block: int, safe_block: int):
    conn.execute(text("""
        INSERT INTO indexer_cursors (cursor_name, last_scanned_block, last_safe_block, updated_at)
        VALUES (:cursor_name, :last_scanned_block, :last_safe_block, now())
        ON CONFLICT (cursor_name)
        DO UPDATE SET
          last_scanned_block = EXCLUDED.last_scanned_block,
          last_safe_block = EXCLUDED.last_safe_block,
          updated_at = now()
    """), {
        "cursor_name": CURSOR_NAME,
        "last_scanned_block": latest_block,
        "last_safe_block": safe_block,
    })


def run_indexer(from_block_override: int | None = None, to_block_override: int | None = None):
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=Web3.to_checksum_address(REGISTRY_ADDRESS), abi=ABI)
    latest = w3.eth.block_number
    with engine.begin() as conn:
        start_block = from_block_override if from_block_override is not None else get_cursor(conn)
        end_block = to_block_override if to_block_override is not None else latest
        safe_block = max(end_block - CONFIRMATION_LAG, 0)

        run_row = conn.execute(text("""
            INSERT INTO indexer_ingestion_runs (from_block, to_block)
            VALUES (:from_block, :to_block)
            RETURNING id
        """), {"from_block": start_block, "to_block": end_block}).first()
        run_id = int(run_row[0])

        ingested = 0
        for event_abi in ABI:
            event = contract.events[event_abi['name']]
            logs = event.get_logs(fromBlock=start_block, toBlock=end_block)
            for log in logs:
                payload = {
                    'block_number': log['blockNumber'],
                    'tx_hash': log['transactionHash'].hex(),
                    'log_index': log['logIndex'],
                    'contract_address': REGISTRY_ADDRESS,
                    'event_name': event_abi['name'],
                    'payload': json.dumps(dict(log['args']), default=str),
                }
                upsert_seed(conn, payload)
                ingested += 1
        conn.execute(text("""
            UPDATE indexer_ingestion_runs
            SET completed_at = now(), ingested_events = :ingested
            WHERE id = :run_id
        """), {"ingested": ingested, "run_id": run_id})
        update_cursor(conn, end_block, safe_block)
    print(f"Indexed through block {end_block} (safe block {safe_block})")


def main():
    parser = argparse.ArgumentParser(description="Nova-Seeds deterministic indexer/backfill")
    parser.add_argument("--from-block", type=int, default=None)
    parser.add_argument("--to-block", type=int, default=None)
    args = parser.parse_args()
    run_indexer(from_block_override=args.from_block, to_block_override=args.to_block)


if __name__ == '__main__':
    main()
