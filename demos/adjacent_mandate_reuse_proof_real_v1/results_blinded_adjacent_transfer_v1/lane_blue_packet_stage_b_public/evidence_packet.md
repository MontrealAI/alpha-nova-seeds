# Lane Blue — Stage B packet

## Scope
- backend/app/main.py
- backend/app/indexer.py
- backend/app/schemas.py
- backend/migrations/002_v26_hardening.sql
- directly coupled docs/tests within backend proof surface

## Accepted outputs
### SB-104 — Council seats API omits log_index despite ordering by it
- Code pointer: backend/app/main.py:66-75; backend/app/schemas.py:25-31
- Broken condition / invariant: The API hides log_index even though replay ordering depends on it, so same-block event sequences cannot be deterministically reconstructed from API responses alone.
- Reproduction witness: OpenAPI CouncilSeatRow schema omits log_index while /governance/council-seats orders by log_index. Two rows in one block can swap relative order for API-only clients.
- Severity rationale: High for proof/read-model correctness because deterministic replay is a stated backend hardening goal.
- Suggested fix: Add log_index to CouncilSeatRow and include it in the SELECT projection returned by /governance/council-seats.
- Replay artifact / trace: SQL ORDER BY block_number DESC, log_index DESC in main.py; CouncilSeatRow fields in schemas.py do not include log_index.

### SB-231 — Dismissed challenge outcomes do not close the lifecycle stream
- Code pointer: backend/app/indexer.py:145-176; docs/council-seat-lifecycle.md:14-19
- Broken condition / invariant: Lifecycle replay completeness breaks for ChallengeResolved(false): the closure exists only in seat_challenges, not in council_seat_lifecycle.
- Reproduction witness: indexer.py always updates seat_challenges but inserts a lifecycle row only under if upheld:, so lifecycle-only consumers cannot observe dismissal closure.
- Severity rationale: Medium: operator checks require every challenged event to become deactivated or reassigned, but dismissed closure has no lifecycle witness.
- Suggested fix: Emit a closure lifecycle row for dismissed challenges or expose closure status in the council-seats/proof surfaces.
- Replay artifact / trace: ChallengeResolved(false) path updates status without _insert_council_lifecycle.

### SB-319 — Active seat count view is not bound to the actual active snapshot
- Code pointer: backend/migrations/002_v26_hardening.sql:49-57; docs/council-seat-lifecycle.md:16-19; contracts/CouncilGovernanceV25.sol:55-62
- Broken condition / invariant: council_active_seat_count infers active seats from latest event_type in {assigned,reassigned,challenged}, but the event stream omits the active flag and the contract assignment surface accepts active as an explicit state bit.
- Reproduction witness: The view never reads an active field because council_seat_lifecycle stores none; any inactive assignment encoded via assignSeat(..., active=false) is indistinguishable from an active assignment in the read model.
- Severity rationale: Medium: the backend operator check says active seat count should match governance snapshots for the current term, but the view is heuristic rather than bound to the authoritative active snapshot.
- Suggested fix: Persist active in the lifecycle/read model, or compute active seat count from a source that preserves the active bit and current-term binding.
- Replay artifact / trace: migration view filters latest.event_type IN (assigned,reassigned,challenged); SeatAssigned event and lifecycle schema carry no active field.

### SB-441 — Reviewer ledger amount and API precision are not bound to the canonical accrual source
- Code pointer: backend/app/indexer.py:43-56; backend/app/main.py:59-63; backend/app/schemas.py:21-23; docs/reviewer-stake-accounting.md:7-17; contracts/NovaSeedRegistryV25.sol:167-174
- Broken condition / invariant: The read model writes delta=1 for every accrual and the API coerces numeric net_delta to float, so the exposed ledger is not bound to the canonical treasury amount or precision.
- Reproduction witness: submitReview accrues 1 ether in the registry, reviewer_stake_accounting.md describes signed numeric deltas, yet _insert_reviewer_accrual writes delta=1 and reviewer_ledger casts net_delta::float8.
- Severity rationale: Medium: settlement-facing or treasury-facing consumers can misread both unit scale and exact precision.
- Suggested fix: Source accrual/clawback rows from the authoritative treasury amount surface (or store canonical wei units) and return net_delta as string/Decimal, not float.
- Replay artifact / trace: indexer.py sets delta: 1; main.py selects net_delta::float8; ReviewerStakeRow declares net_delta: float.
