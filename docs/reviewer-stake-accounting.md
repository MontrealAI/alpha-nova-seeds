# Reviewer Stake Accounting (v2.6 RC)

## What changed
Reviewer accounting now includes explicit stake, accrued rewards, claimed rewards, and slashed amounts in deterministic ledger fields.

## Accounting flow
1. Reviewer submits review.
2. Registry records temporary review stake weight.
3. Treasury accrues reward event for that review.
4. Finalization unstakes the review weight.
5. Slash actions reduce stake first, then accrued rewards.

## Why this matters
Operators can inspect deterministic accounting visibility and reconstruct slash/reward outcomes without inference.

## Surfaces
- Contract: `contracts/ReviewerRewardTreasuryV25.sol`
- Dashboard page: reviewer ledger section
