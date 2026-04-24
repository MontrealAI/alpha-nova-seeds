# Repo integration note

Recommended placement:

```text
demos/adjacent_mandate_reuse_proof_real_v1/results_blinded_adjacent_transfer_v1/
```

Do not upload private-only files such as:

- answer keys
- blinded assignment maps
- reviewer identity maps
- private commitment files
- full internal bundles

## Suggested link from `demos/adjacent_mandate_reuse_proof_real_v1/README.md`

```md
## Results

- [`results_blinded_adjacent_transfer_v1/`](./results_blinded_adjacent_transfer_v1/) — public-safe internal Stage A + Stage B evidence update. Stage A passed under a blinded packet structure and delayed reveal discipline. Stage B passed the cross-domain output/evidence transfer thresholds, but the public intervention logs do not support the reduced-handholding gate. This supports blinded adjacent transfer and one cross-domain expansion under controlled internal evaluation; it does not claim external validation or general unbounded RSI.
```

## Suggested PR title

```text
Add public-safe blinded adjacent-transfer Stage A+B results
```

## Suggested commit message

```text
docs(demo): add blinded adjacent-transfer Stage A+B results
```

## Suggested PR description

```text
Adds a public-safe Stage A + Stage B evidence update for the real-world adjacent-mandate proof pack.

Included:
- normalized README and metrics
- Stage A blinded adjacent-transfer scorecard
- Stage B blinded cross-domain expansion scorecard
- public proof docket
- public lane packets and scorecard outputs
- protocol reference and repo integration note

Claim boundary:
- supports blinded adjacent transfer and one cross-domain expansion under controlled internal evaluation
- Stage B passed cross-domain output/evidence thresholds but did not pass the reduced-handholding gate from the public intervention logs
- does not claim independent external validation, unrestricted autonomy, or general unbounded RSI

Private materials are intentionally excluded.
```
