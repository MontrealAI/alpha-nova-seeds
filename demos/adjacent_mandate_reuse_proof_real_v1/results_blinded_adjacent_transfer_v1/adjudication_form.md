# Adjudication Form

## Experiment metadata
- Experiment ID: adjacent-mandate-reuse-real-v1-blinded-stage-a-solo-v1
- Repo SHA: 97907b70d86f44a5a3f31f71828a9360fd1f6744
- Reviewer pool ID: emulated-R1-R3
- Adjudication date: 2026-04-23T21:02:51Z

## Accepted outputs

| Blinded Output ID | Accepted | Usefulness points | Lane (revealed after adjudication) | Notes |
|---|---|---:|---|---|
| SA-102 | yes | 3 | control | Configured threshold is never enforced at completion |
| SA-317 | yes | 2 | control | Request identity can collide on same-block duplicate opens |
| SA-204 | yes | 3 | treatment | Configured threshold is never enforced at completion |
| SA-411 | yes | 2 | treatment | Trusted signer scope is global rather than profile-bound |
| SA-583 | yes | 2 | treatment | Request identity can collide on same-block duplicate opens |
| SA-667 | yes | 2 | treatment | Completion is not bound to a frozen binding-profile snapshot |

## Lane integrity checks
- Same scope across lanes? yes
- Same reviewer rubric across lanes? yes
- Same time budget across lanes? yes
- Same compute budget across lanes? yes
- Any unlogged intervention? no

## Final adjudication note
- Was the experiment valid? Partially: the blinded packet structure and delayed reveal were followed, but reviewer independence was emulated within one session and lane execution was sequential.
- Any contamination risks? Operator expectancy and single-session adjudication remain contamination risks; results should be treated as a protocol-conformant internal start, not final independent proof.