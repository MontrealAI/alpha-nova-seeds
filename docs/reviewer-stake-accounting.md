# Reviewer Stake Accounting (v2.6 RC)

This document defines deterministic visibility for reviewer rewards and slashes.

## Ledger model
Reviewer accounting is represented as:
- reward accrual events,
- claim events,
- clawback/slash events,
- derived net balance projections.

## Deterministic accounting formula
For each reviewer:

`net_stake_delta = total_rewards - total_clawed_back`

`claimable = max(total_rewards - total_claimed - total_clawed_back, 0)`

These values are exposed through backend SQL views and dashboard tables.

## Settlement assumptions
- Rewards are emitted from review decisions.
- Clawback/slash entries must include a reason hash.
- Accounting is event-driven and idempotent by `(tx_hash, log_index)`.
