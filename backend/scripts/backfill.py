import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.indexer import index_range  # noqa: E402
from app.config import RPC_URL, START_BLOCK  # noqa: E402
from web3 import Web3


def main() -> None:
    parser = argparse.ArgumentParser(description='Deterministic chain event backfill for Nova-Seeds indexer')
    parser.add_argument('--from-block', type=int, default=START_BLOCK)
    parser.add_argument('--to-block', type=int, required=True)
    args = parser.parse_args()

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    indexed = index_range(w3, args.from_block, args.to_block)
    print(f"Backfilled up to block {indexed}")


if __name__ == '__main__':
    main()
