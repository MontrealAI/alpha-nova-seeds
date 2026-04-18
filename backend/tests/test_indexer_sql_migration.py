from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_v26_migration_contains_cursor_and_views():
    sql = (ROOT / "backend/migrations/002_v26_hardening.sql").read_text()
    assert "CREATE TABLE IF NOT EXISTS indexer_cursors" in sql
    assert "CREATE VIEW IF NOT EXISTS reviewer_stake_ledger_v26" in sql
    assert "CREATE VIEW IF NOT EXISTS council_seat_lifecycle_v26" in sql
