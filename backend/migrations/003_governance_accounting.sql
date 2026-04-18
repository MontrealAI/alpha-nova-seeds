ALTER TABLE reward_events
  ADD COLUMN IF NOT EXISTS accounting_kind TEXT DEFAULT 'reward';

ALTER TABLE seat_challenges
  ADD COLUMN IF NOT EXISTS seat_status TEXT DEFAULT 'active';

CREATE INDEX IF NOT EXISTS idx_chain_events_block ON chain_events (block_number);
CREATE INDEX IF NOT EXISTS idx_reward_events_reviewer ON reward_events (reviewer);
