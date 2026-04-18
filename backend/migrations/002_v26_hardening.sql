CREATE TABLE IF NOT EXISTS indexer_cursors (
  cursor_name TEXT PRIMARY KEY,
  last_scanned_block BIGINT NOT NULL,
  last_safe_block BIGINT NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS indexer_ingestion_runs (
  id BIGSERIAL PRIMARY KEY,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  from_block BIGINT NOT NULL,
  to_block BIGINT NOT NULL,
  ingested_events BIGINT NOT NULL DEFAULT 0,
  notes TEXT
);

CREATE VIEW IF NOT EXISTS reviewer_stake_ledger_v26 AS
SELECT
  reviewer,
  COALESCE(SUM(CASE WHEN kind = 'reward' THEN delta ELSE 0 END), 0) AS total_rewards,
  COALESCE(SUM(CASE WHEN kind = 'claim' THEN delta ELSE 0 END), 0) AS total_claimed,
  COALESCE(SUM(CASE WHEN kind IN ('clawback', 'slash') THEN delta ELSE 0 END), 0) AS total_slashed,
  GREATEST(
    COALESCE(SUM(CASE WHEN kind = 'reward' THEN delta ELSE 0 END), 0)
    - COALESCE(SUM(CASE WHEN kind = 'claim' THEN delta ELSE 0 END), 0)
    - COALESCE(SUM(CASE WHEN kind IN ('clawback', 'slash') THEN delta ELSE 0 END), 0),
    0
  ) AS claimable
FROM reward_events
GROUP BY reviewer;

CREATE VIEW IF NOT EXISTS council_seat_lifecycle_v26 AS
SELECT
  term_id,
  seat_id,
  COUNT(*) FILTER (WHERE resolved = false) AS open_challenges,
  COUNT(*) FILTER (WHERE resolved = true) AS resolved_challenges,
  MAX(updated_at) AS last_updated_at
FROM seat_challenges
GROUP BY term_id, seat_id;
