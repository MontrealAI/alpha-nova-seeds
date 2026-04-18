# Council Seat Lifecycle (v2.6 RC)

## Seat statuses
- `ACTIVE`
- `INACTIVE`
- `RETIRED`

## Lifecycle operations
1. Election admin opens term.
2. Election admin assigns or updates seats.
3. Seat status can be changed explicitly with timestamps.
4. Bonded challenges can deactivate seats when upheld.

## Deterministic visibility
Each status transition records explicit timestamps to support review and dispute replay.

## Surfaces
- Contract: `contracts/CouncilGovernanceV25.sol`
- Dashboard page: council seats section
