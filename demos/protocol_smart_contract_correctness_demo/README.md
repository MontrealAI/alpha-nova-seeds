# Protocol + Smart-Contract Correctness Flagship Demo

This demo is the **front door** for the protocol-correctness wedge in `alpha-nova-seeds`.

It demonstrates, end-to-end, a synthetic but replayable path:

1. **Sector:** Protocol and smart-contract correctness
2. **Parent business:** Protocol Assurance Studio
3. **Five Nova-Seeds:** audit-factory, invariant-library, fuzz-harness, exploit-replay, governance-parameter simulator
4. **Mandate 1 assay:** Governance/dispute correctness across all five seeds
5. **First frozen sub-pack:** `GovernanceValidationPack-v1`
6. **First sector stepping stone:** `ProtocolAssurancePack-v1`
7. **Mandate 2 adjacent test:** threshold/attestation correctness, control vs treatment
8. **Threshold scorecard + ruling:** PASS/FAIL against explicit adjacent-mandate proof thresholds
9. **Conditional synthetic Sovereign artifact:** `ProtocolAssuranceSovereign-v1.synthetic.json`

> This is a **synthetic local flagship demo**, not a real-world proof pack.

---

## 3-minute read map

- **Why this sector first:** objective, replayable, fast to review, reusable, commercially understandable.
- **What gets sold:** fixed-scope protocol assurance mandates (2–4 release-critical contracts) with replayable release-gate evidence.
- **How seeds are screened:** harsh common assay on one mandate with shared rubric and evidence completeness checklist.
- **What is promoted:** one frozen sub-pack, then a sector stepping stone.
- **What counts as progress:** adjacent-mandate treatment must beat control under strict thresholds.
- **What this is not:** audited production proof.

---

## Why this sector is first

Protocol correctness is the first wedge because it is:

- objective enough to score
- replayable from contract fixtures and logs
- fast for operators and buyers to review
- rich in reusable primitives (invariants, evidence templates, release-gate checklists)
- commercially understandable for fixed-scope release-critical work

The design-partner offer modeled here is narrow: 2–4 release-critical contracts, replayable evidence, failing tests/fuzz traces, and a release-gate packet.

---

## Adjacent-mandate thresholds (strict)

A scorecard is a PASS only if all are true:

- AOY uplift ≥ 35%
- speed uplift ≥ 30%
- repair/rework reduction ≥ 40%
- evidence completeness uplift ≥ 20%
- no safety regression
- package dependence rate ≥ 30%

## Deterministic winner selection (Mandate 1)

Nova-Seeds are ranked with a deterministic lexicographic order over shared assay metrics:

1. accepted usefulness points (higher is better)
2. time to first accepted output (lower is better)
3. repair/rework (lower is better)
4. evidence completeness (higher is better)
5. unsupported-claim rate (lower is better)
6. severity inflation count (lower is better)
7. packageable artifact quality (higher is better)

This keeps selection replayable and non-arbitrary: the same fixtures and seed packets always select the same winner.

---

## What this demo proves vs does not prove

### Proves (synthetically)

- The compounding loop is computationally explicit and falsifiable.
- Five Nova-Seeds can be screened under one harsh assay.
- A winning seed can be frozen into a reusable package.
- Adjacent-mandate control vs treatment can be scored against hard thresholds.
- Sovereign emission can be fail-closed.

### Does not prove

- Real-world buyer outcomes
- Audited production safety
- Mainnet readiness
- External legal/regulatory acceptance

For adjacent proof references:

- [`../adjacent_mandate_reuse_proof_demo/`](../adjacent_mandate_reuse_proof_demo/)
- [`../adjacent_mandate_reuse_proof_real_v1/`](../adjacent_mandate_reuse_proof_real_v1/)

This flagship demo is intentionally clearer and more operator-facing than those deeper proof packs.


## Flagship conclusion (explicit)

If protocol correctness compounds through frozen reusable capability packages, this demo supports a narrow synthetic claim:

- 🌱💫 **α-AGI Protocol Assurance Sovereign 🔐** is the first plausible compounding correctness sovereign form (in demo form).
- It is the seed of a future 👑 **α-AGI Cybersecurity Sovereign 🔱✨**.

But this demo is explicit about boundaries:

- It does **not** prove a full cybersecurity sovereign already exists.
- It does **not** claim cybersecurity is solved once and for all.

---

## Run

```bash
cd demos/protocol_smart_contract_correctness_demo
python3 run_demo.py --assert
```

No third-party dependency is required. `requirements.txt` is intentionally empty.

---

## Output map

Primary outputs are written under `demo_output/`:

- `parent_business/`
- `nova_seeds/`
- `mandate_1/`
- `capability_package/`
- `mandate_2_control/`
- `mandate_2_treatment/`
- `scorecard/`
- `proof_docket/` (includes compact sectioned markdown docket files `00_*` through `08_*` plus machine-readable JSON)
- `reports/report.md`
- `reports/report.html`
- `sovereign/`

---

## Constitutional and safety framing

- Constitutional order: **identity → proof → settlement → governance**
- Invariant: **no value without evidence; no autonomy without authority; no settlement without validation**

If any threshold fails, the demo emits a fail-closed governance ruling artifact instead of a sovereign artifact.
