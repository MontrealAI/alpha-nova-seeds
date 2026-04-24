# Lane Gold — Stage B packet

## Scope
- backend/app/main.py
- backend/app/indexer.py
- backend/app/schemas.py
- backend/migrations/002_v26_hardening.sql
- directly coupled docs/tests within backend proof surface

## Accepted outputs
### SB-106 — Council seats API omits log_index despite ordering by it
- Code pointer: backend/app/main.py:66-75; backend/app/schemas.py:25-31
- Broken condition / invariant: /governance/council-seats orders rows by block_number, log_index but the response model omits log_index, so same-block replay order cannot be reconstructed from the API surface.
- Reproduction witness: Generated OpenAPI for CouncilSeatRow exposes term_id, seat_id, occupant, event_type, tx_hash, block_number only; no log_index is present while the SQL query orders by log_index.
- Severity rationale: High for proof/replay surfaces: same-block lifecycle events can become non-deterministic to clients that consume only the API payload.
- Suggested fix: Expose log_index (and ideally active / closure markers) in CouncilSeatRow and the /governance/council-seats query.
- Replay artifact / trace: main.py lines 69-73 ORDER BY block_number DESC, log_index DESC; schemas.py CouncilSeatRow omits log_index.

### SB-237 — Dismissed challenge outcomes do not close the lifecycle stream
- Code pointer: backend/app/indexer.py:145-176; docs/council-seat-lifecycle.md:14-19
- Broken condition / invariant: _handle_challenge_resolved writes a lifecycle event only when upheld=true; dismissed challenges update seat_challenges but emit no lifecycle closure row.
- Reproduction witness: A ChallengeResolved(false) path updates resolved/upheld on seat_challenges yet skips _insert_council_lifecycle, so lifecycle consumers cannot tell that a challenge closed without joining another table.
- Severity rationale: Medium: operator checks require lifecycle closure, but the event-sourced table cannot represent dismissed closure on its own.
- Suggested fix: Insert an explicit lifecycle closure event for dismissed challenges (e.g., resolved_not_upheld) or expose closure status directly in the API surface.
- Replay artifact / trace: indexer.py lines 155-176 gate lifecycle insertion on if upheld: only.
