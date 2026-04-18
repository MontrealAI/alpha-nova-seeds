CREATE TABLE IF NOT EXISTS indexer_cursors (
  name TEXT PRIMARY KEY,
  last_finalized_block BIGINT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
