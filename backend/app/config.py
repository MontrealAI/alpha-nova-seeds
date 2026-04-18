import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/nova")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RPC_URL = os.getenv("RPC_URL", "http://localhost:8545")
REGISTRY_ADDRESS = os.getenv("REGISTRY_ADDRESS", "0x0000000000000000000000000000000000000000")
CHAIN_ID = int(os.getenv("CHAIN_ID", "1"))
START_BLOCK = int(os.getenv("START_BLOCK", "0"))
CONFIRMATIONS = int(os.getenv("CONFIRMATIONS", "12"))
INDEXER_NAME = os.getenv("INDEXER_NAME", "registry_v25")
