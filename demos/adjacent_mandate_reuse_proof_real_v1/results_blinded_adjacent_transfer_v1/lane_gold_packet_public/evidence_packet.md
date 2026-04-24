# Lane Gold packet

## Scope
- contracts/ThresholdNetworkAdapterV25.sol
- contracts/SignedAttestationVerifierV25.sol

## Accepted outputs
### SA-102 — Configured threshold is never enforced at completion
- Code pointer: contracts/ThresholdNetworkAdapterV25.sol:78-96
- Broken condition / invariant: completeRequest verifies only one global signer and never reads profiles[r.profileId].threshold or committeeSize.
- Reproduction witness: contracts/test/threshold.adapter.ts:25-60 shows a profile with threshold=2 that completes once a single signer is marked trusted.
- Severity rationale: High: the adapter can finalize below the configured multi-party threshold.
- Suggested fix: Bind completion to a per-request or per-profile signer-share threshold check and record the share count / signer set.
- Replay artifact / trace: Open request -> set one signer trusted -> complete with one signature -> status FULFILLED.

### SA-317 — Request identity can collide on same-block duplicate opens
- Code pointer: contracts/ThresholdNetworkAdapterV25.sol:58-76
- Broken condition / invariant: requestId is built from stable inputs plus block.timestamp only, with no nonce or overwrite guard.
- Reproduction witness: Two same-block opens by the same requester with the same inputs can compute the same requestId and overwrite the mapping entry.
- Severity rationale: Medium: duplicate opens can alias identity and confuse lifecycle state.
- Suggested fix: Add a requester nonce or explicit existence check before writing requests[requestId].
- Replay artifact / trace: openRequest(seed, profile, cipher, manifest) twice in same block with same sender.
