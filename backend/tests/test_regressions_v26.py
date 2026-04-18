from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_migration_uses_postgres_compatible_view_statements():
    sql = (ROOT / 'backend/migrations/002_v26_hardening.sql').read_text()
    assert 'CREATE VIEW IF NOT EXISTS' not in sql
    assert 'DROP VIEW IF EXISTS reviewer_stake_balances;' in sql
    assert 'DROP VIEW IF EXISTS council_active_seat_count;' in sql


def test_indexer_reorg_rewind_deletes_derived_rows():
    source = (ROOT / 'backend/app/indexer.py').read_text()
    assert 'DELETE FROM chain_events WHERE block_number >= :start_block' in source
    assert 'DELETE FROM reviewer_stake_ledger WHERE block_number >= :start_block' in source
    assert 'DELETE FROM council_seat_lifecycle WHERE block_number >= :start_block' in source
    assert 'DELETE FROM seat_challenges WHERE block_number >= :start_block' in source


def test_fastapi_main_imports_list_typing():
    source = (ROOT / 'backend/app/main.py').read_text()
    assert 'from typing import List' in source
    assert 'response_model=List[ReviewerStakeRow]' in source
    assert 'response_model=List[CouncilSeatRow]' in source


def test_event_abis_include_governance_and_review_events():
    registry_abi = (ROOT / 'backend/app/abi/NovaSeedRegistryV25.events.json').read_text()
    governance_abi = (ROOT / 'backend/app/abi/CouncilGovernanceV25.events.json').read_text()
    assert 'ReviewSubmitted' in registry_abi
    assert 'SeedQuarantined' in registry_abi
    assert 'SeatAssigned' in governance_abi
    assert 'ChallengeOpened' in governance_abi
    assert 'ChallengeResolved' in governance_abi
