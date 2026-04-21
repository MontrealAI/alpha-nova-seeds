# Protocol + Smart-Contract Correctness Flagship Demo

This demo is the **front door** for the protocol-correctness wedge in `alpha-nova-seeds`.

It demonstrates, end-to-end, a synthetic but replayable path:

1. **Sector:** Protocol and smart-contract correctness
2. **Parent business:** Protocol Cybersecurity Studio (legacy alias: Protocol Assurance Studio)
3. **Five Nova-Seeds:** audit-factory, invariant-library, fuzz-harness, exploit-replay, governance-parameter simulator
4. **Mandate 1 assay:** governance/dispute correctness across all five seeds
5. **First frozen sub-pack:** `GovernanceValidationPack-v1`
6. **First sector stepping stone:** `ProtocolCybersecurityPack-v1` (legacy alias: `ProtocolAssurancePack-v1`)
7. **Mandate 2 adjacent test:** threshold/attestation correctness, control vs treatment
8. **Threshold scorecard + ruling:** PASS/FAIL against explicit adjacent-mandate proof thresholds
9. **Conditional synthetic Sovereign artifact:** `ProtocolCybersecuritySovereign-v1.synthetic.json` (legacy alias retained)

> This is a **synthetic local flagship demo**, not a real-world proof pack.

---

## 3-minute doctrine map

- Why protocol correctness is still first: objective scoring + high replayability + archiveable primitives.
- Why language now says **Protocol Cybersecurity**: clearer public framing with less ambiguity than “assurance.”
- What the full-stack organism is: Insight → Nova-Seeds → MARK → AGI Jobs → Archive.
- Where AGI Jobs sits: identity, proof, settlement, governance convert candidate work into validated output.
- Why this is formal analogy: governance language with measurable proxies, not literal physics.
- Why this is nation-state legible: doctrine is explicit about what is proven now vs. still future-facing.

Canonical doctrine docs:

### Canonical math rendering policy

All doctrine equations are canonical in `docs/THERMODYNAMIC_MODEL.md` and use GitHub math delimiters (`$...$`, `$$...$$`).
Runtime validation fails closed if legacy `\[ ... \]` or bare `[ ... ]` pseudo-equation delimiters are detected.


- [`docs/DOCTRINE_STACK.md`](./docs/DOCTRINE_STACK.md)
- [`docs/THERMODYNAMIC_MODEL.md`](./docs/THERMODYNAMIC_MODEL.md)
- [`docs/NATION_STATE_DOCTRINE.md`](./docs/NATION_STATE_DOCTRINE.md)

---

## Why this sector is first

Protocol correctness is the first wedge because it is:

- objective enough to score
- replayable from contract fixtures and logs
- fast for operators and buyers to review
- rich in reusable primitives (invariants, evidence templates, release-gate checklists)
- commercially understandable for fixed-scope release-critical work

---

## Full-stack economic organism (demo interpretation)

The organism operates as a driven coordination loop:

1. **Insight** narrows search.
2. **Nova-Seeds** generate candidate fluctuations.
3. **MARK** applies selection pressure.
4. **AGI Jobs** validates and settles work (identity → proof → settlement → governance).
5. **Archive** freezes successful packets into reusable capability and lowers organizational entropy pressure.

In this flagship demo, 🌱💫 **α‑AGI Protocol Cybersecurity Sovereign 🔐** is the first narrow, high-verification production organ and compounding correctness wedge.

If stable over repeated adjacent proofs, it becomes the seed of a future 👑 **α‑AGI Cybersecurity Sovereign 🔱✨**.

### Explicitly not claimed

- a full cybersecurity sovereign already exists
- cybersecurity is solved once and for all
- the thermodynamic framing is literal physical law
- real-world proof is already complete

---


## Winner selection and freeze logic (non-hand-wavy)

Mandate 1 seed selection is deterministic. Each seed run emits a scored result file in `demo_output/mandate_1/` and the assay computes:

- accepted usefulness points (AUP),
- time to first accepted output,
- repair/rework ratio,
- evidence completeness,
- unsupported claim rate (penalty),
- package quality.

The winner is selected by a deterministic **lexicographic rank key** (not a single blended composite).
Ordering follows: usefulness points, time-to-first-accepted output, repair/rework, evidence completeness,
unsupported-claim rate, severity inflation count, then packageable artifact quality.
In the current deterministic run, `invariant_library` wins and is frozen as:

- first sub-pack: `GovernanceValidationPack-v1`
- promoted stepping-stone pack: `ProtocolCybersecurityPack-v1`

That pack is then injected into Mandate 2 treatment-only execution while control remains unassisted.

## Institutional evidence surfaces produced

The flagship run emits the full evidence set required by this RC framing:

- release-gate packet: `demo_output/scorecard/release_gate_packet.json`
- scorecard: `demo_output/scorecard/adjacent_mandate_scorecard.json`
- proof docket bundle: `demo_output/proof_docket/proof_docket.json` + supporting files
- chronicle entry: `demo_output/proof_docket/chronicle_entry.json`
- governance ruling: `demo_output/proof_docket/governance_ruling.json` and `08_governance_ruling.md`

## Adjacent-mandate thresholds (strict)

A scorecard is a PASS only if all are true:

- AOY uplift ≥ 35%
- speed uplift ≥ 30%
- repair/rework reduction ≥ 40%
- evidence completeness uplift ≥ 20%
- no safety regression
- package dependence rate ≥ 30%

---

## Run

```bash
cd demos/protocol_smart_contract_correctness_demo
python3 run_demo.py --assert
```

`--assert` runs deterministic integrity checks, including a two-run artifact hash comparison.
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
- `proof_docket/`
- `doctrine/`
- `reports/report.md`
- `reports/report.html`
- `sovereign/`

---

## Flagship conclusion (explicit)

If protocol correctness compounds through frozen reusable capability packages, this demo supports a narrow synthetic claim:

- 🌱💫 **α-AGI Protocol Cybersecurity Sovereign 🔐** is the first plausible compounding correctness sovereign form (in demo form).
- It is the seed of a future 👑 **α-AGI Cybersecurity Sovereign 🔱✨**.

But the demo is explicit about boundaries:

- It does **not** prove a full cybersecurity sovereign already exists.
- It does **not** claim cybersecurity is solved once and for all.


## Demo ladder

- Flagship synthetic wedge demo: `demos/protocol_smart_contract_correctness_demo/`
- Adjacent synthetic proof demo: `demos/adjacent_mandate_reuse_proof_demo/`
- Real-world experiment pack: `demos/adjacent_mandate_reuse_proof_real_v1/`
