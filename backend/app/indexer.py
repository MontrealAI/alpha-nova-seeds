import json
from pathlib import Path
from web3 import Web3
from sqlalchemy import text
from .config import RPC_URL, REGISTRY_ADDRESS, START_BLOCK
from .db import engine

ABI = json.loads(Path(__file__).with_name('abi').joinpath('NovaSeedRegistryV25.events.json').read_text())


def upsert_seed(conn, seed_id_hex: str, payload: dict):
    conn.execute(text("""
        INSERT INTO chain_events (block_number, tx_hash, log_index, contract_address, event_name, payload)
        VALUES (:block_number, :tx_hash, :log_index, :contract_address, :event_name, CAST(:payload AS JSONB))
        ON CONFLICT (tx_hash, log_index) DO NOTHING
    """), payload)


def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=Web3.to_checksum_address(REGISTRY_ADDRESS), abi=ABI)
    latest = w3.eth.block_number
    with engine.begin() as conn:
        for event_abi in ABI:
            event = contract.events[event_abi['name']]
            logs = event.get_logs(fromBlock=START_BLOCK, toBlock=latest)
            for log in logs:
                payload = {
                    'block_number': log['blockNumber'],
                    'tx_hash': log['transactionHash'].hex(),
                    'log_index': log['logIndex'],
                    'contract_address': REGISTRY_ADDRESS,
                    'event_name': event_abi['name'],
                    'payload': json.dumps(dict(log['args']), default=str),
                }
                upsert_seed(conn, log['args'].get('seedId').hex() if 'seedId' in log['args'] else '', payload)
    print(f"Indexed through block {latest}")


if __name__ == '__main__':
    main()
