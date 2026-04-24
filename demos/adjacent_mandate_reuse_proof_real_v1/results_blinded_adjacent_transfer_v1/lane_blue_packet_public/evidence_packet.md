# Lane Blue packet

## Scope
- contracts/ThresholdNetworkAdapterV25.sol
- contracts/SignedAttestationVerifierV25.sol

## Accepted outputs
### SA-204 — Configured threshold is never enforced at completion
- Code pointer: contracts/ThresholdNetworkAdapterV25.sol:78-96
- Broken condition / invariant: completeRequest can finalize without proving any threshold share count from the binding profile.
- Reproduction witness: Profile threshold=2 is configured; one globally trusted signer still finalizes the request after signature verification.
- Severity rationale: High: below-threshold completion defeats the profile’s declared multi-party requirement.
- Suggested fix: Require threshold satisfaction against a frozen profile snapshot before status transitions to FULFILLED.
- Replay artifact / trace: Request opened under threshold=2 profile -> single signer trusted -> completeRequest succeeds.

### SA-411 — Trusted signer scope is global rather than profile-bound
- Code pointer: contracts/SignedAttestationVerifierV25.sol:21,27-29; contracts/ThresholdNetworkAdapterV25.sol:90-92
- Broken condition / invariant: Signer trust is stored in a single global trustedSigners mapping with no profile/committee binding.
- Reproduction witness: A signer trusted for any purpose is accepted for all profiles because verify returns only (signer, trusted).
- Severity rationale: Medium: committee/profile isolation can be bypassed by global trust reuse.
- Suggested fix: Scope signer trust to profileId or committee root and include that binding in the attestation digest or verifier state.
- Replay artifact / trace: Set trusted signer once -> use same signer to satisfy any profile that calls verifier.verify.

### SA-583 — Request identity can collide on same-block duplicate opens
- Code pointer: contracts/ThresholdNetworkAdapterV25.sol:58-76
- Broken condition / invariant: The request identity pattern mirrors the timestamp-only challenge identity from Mandate 1.
- Reproduction witness: If two same-block opens use identical stable inputs, requestId collides and the later write overwrites the earlier request record.
- Severity rationale: Medium: lifecycle aliasing can corrupt request state and downstream evidence.
- Suggested fix: Add an anti-collision nonce or reject writes when requests[requestId] already exists.
- Replay artifact / trace: keccak(block.chainid, seedId, profileId, requester, ciphertextHash, manifestHash, block.timestamp).

### SA-667 — Completion is not bound to a frozen binding-profile snapshot
- Code pointer: contracts/ThresholdNetworkAdapterV25.sol:23-35; 78-96
- Broken condition / invariant: A request stores only profileId and completion never proves threshold, committeeRoot, relayerRoot, policyHash, or active state as frozen at open time.
- Reproduction witness: Profile parameters can change after openRequest; completeRequest reads none of them except through the global verifier path.
- Severity rationale: Medium: completion semantics can drift relative to the profile that governed request opening.
- Suggested fix: Store and verify a frozen snapshot hash (or the relevant fields) at open time and bind completion to it.
- Replay artifact / trace: openRequest records profileId only -> setBindingProfile can mutate underlying profile -> completeRequest still succeeds without snapshot comparison.
