# Open-Ended RSI System Runbook

This runbook explains how to run and verify the deterministic `demos/open-ended-rsi-system/` accelerating-loop demo.

## Scope and authority boundary

- This is a **bounded RC demo**.
- It is deterministic and local-only.
- It does not widen authority, perform settlement, or claim external real-world validation.

## Prerequisites

From repository root:

```bash
python3 --version
```

No network calls, external APIs, or model training are used by this demo.

## Primary command

```bash
python3 demos/open-ended-rsi-system/run_demo.py --assert
```

Expected result:

- CLI exits `0` with `PASS: open-ended-rsi-system artifacts generated ...`
- full deterministic output tree appears under `demos/open-ended-rsi-system/out/`

## Artifact contract check

```bash
python3 scripts/check_open_ended_rsi_artifacts.py
```

This checks required artifacts, threshold gates, descending operator touches, doctrine safety gate pass states, and mandate-3 execution/provenance constraints.

## Determinism replay check

```bash
python3 demos/open-ended-rsi-system/run_demo.py --assert
cp demos/open-ended-rsi-system/out/determinism_fingerprint.json /tmp/open-ended-rsi-fingerprint-a.json
python3 demos/open-ended-rsi-system/run_demo.py --assert
diff -u /tmp/open-ended-rsi-fingerprint-a.json demos/open-ended-rsi-system/out/determinism_fingerprint.json
```

No diff indicates deterministic replay for fixed config and local state.

## What is demonstrated vs simulated vs unproven

- Demonstrated: deterministic three-generation loop mechanics, governed package freeze/reuse, whitelist-bounded autonomous mandate-3 selection.
- Simulated: assay outcomes and scorecard values.
- Unproven: unrestricted autonomy, literal unbounded RSI, broad real-world sovereign completion.
