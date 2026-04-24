# Public proof docket — Blinded Adjacent Transfer + Cross-Domain Expansion v1

## 1. What was frozen

- Repo SHA: `97907b70d86f44a5a3f31f71828a9360fd1f6744`
- Stage A package: `GovernanceValidationPack-v1`
- Stage A hash: `7af9c5e920ccc2bcccea60714c412e1cf276a00728345be860a9eba40465afc1`
- Stage B promoted lineage: `ProtocolCorrectnessLineage-v1`
- Stage B lineage hash: `85cdacce2067d759378c060c565d0fb2e5dc762fbf7c5a5975afac1396ac4bf8`
- Stage B freeze time: `2026-04-23T22:07:23Z`

## 2. What was blinded

- Stage A and Stage B used matched kits with the same filenames and folder shape.
- Reviewer-facing packets used only `Lane Blue` / `Lane Gold` labels.
- Reveal occurred only after score lock.
- Final reveal: `Lane Blue` = treatment; `Lane Gold` = control.

## 3. What passed / failed

### Stage A

- Overall result: **PASS**
- AOY uplift: `+80.00%` -> PASS
- Speed uplift: `+43.75%` -> PASS
- Rework reduction: `50.00%` -> PASS
- Evidence completeness uplift: `+43.75%` -> PASS
- Package dependence: `75.00%` -> PASS
- Safety regression: none observed -> PASS

### Stage B

- Cross-domain output / evidence result: **PASS**
- Strong output threshold result: **PASS**
- Minimum reduced-handholding gate: **FAIL**
- AOY uplift: `+80.00%` -> PASS
- Speed uplift: `+43.75%` -> PASS
- Rework reduction: `50.00%` -> PASS
- Evidence completeness uplift: `+27.78%` -> PASS
- Package dependence: `75.00%` -> PASS
- Operator intervention reduction: `0.00%` -> FAIL
- Frontier width increase: `+1 domain` -> PASS
- Safety regression: none observed -> PASS

## 4. What this supports

If read with the protocol caveats, this run supports the statement that AGI ALPHA demonstrated **blinded adjacent transfer and one cross-domain expansion under controlled internal evaluation**.

## 5. What this does not prove

- reduced handholding in Stage B based on public intervention logs
- independent external reviewer validation
- true end-to-end operator blinding
- unrestricted autonomy
- literal or general unbounded recursive self-improvement
- broad sovereign proof
- audited final deployment

## 6. Deviations

- Role separation was partially emulated in one session.
- Reviewer independence was not external.
- Lane execution was sequential rather than truly parallel.

## 7. Next validation

Run the same protocol with separate people for blinding, lane execution, and adjudication, ideally on a clean checkout / separate machine. Add explicit reduced-handholding instrumentation and publish the result regardless of pass or fail.
