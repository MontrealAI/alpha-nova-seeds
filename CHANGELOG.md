# Changelog

## [v2.8.0-rc.2] - 2026-04-22

### Added
- New flagship accelerating-loop demo: `demos/unbounded-rsi-system/` with deterministic phase A/B/C execution and board-ready artifacts (`manifest.json`, `package_manifest.json`, `package_hash.txt`, `provenance_log.json`, `safety_gates.json`, `governance_ruling.json`, `chronicle_entry.json`, `board_scorecard.json`, `board_scorecard.md`, `report.md`, `report.html`).
- New release checklist: `release/v2.8.0-rc.2-unbounded-rsi-demo-checklist.md` for acceptance criteria, smoke checks, provenance expectations, migration/rollback notes, and claim boundaries.

### Changed
- Demo ladder now includes four explicit roles: flagship wedge demo, compact synthetic adjacent demo, real-world proof pack, and accelerating-loop demo.
- Root front door and dashboard ladder surfaces now link the new accelerating-loop demo and promote v2.8.0-rc.2 checklist routing.
- Demo/doctrine link validation scripts now enforce `demos/unbounded-rsi-system/` presence and the `Accelerating-loop demo` role label.

### Notes
- This release remains a **verifiable release candidate**, not an audited final deployment.
- “Unbounded RSI” remains framed as a bounded proof-of-mechanism demonstration, not a literal unrestricted-autonomy claim.

## [v2.8.0-rc.1] - 2026-04-22

### Added
- Frontier posture doctrine doc: `docs/FRONTIER_LAB_POSTURE.md`.
- New RC release checklist: `release/v2.8.0-rc.1-frontier-ui-demo-release-checklist.md` with acceptance criteria, smoke checks, migration/rollback notes, and explicit claim boundaries.

### Changed
- Root front door upgraded to v2.8.0-rc.1 posture with clearer proof ladder, doctrine map, and non-claim boundaries.
- Demo ladder index (`demos/README.md`) tightened around three explicit roles: flagship synthetic wedge, compact synthetic adjacent replay, and real-world experiment pack.
- Dashboard operator UI polished with clearer status badges, artifact cards, proof boundary section, doctrine links, and checklist pointers.
- Flagship demo report UX (`run_demo.py` generated HTML) improved for operator readability and artifact discoverability while preserving deterministic behavior.
- Doctrine/release positioning surfaces aligned to v2.8.0-rc.1 naming and publication posture.

### Notes
- This release remains a **verifiable release candidate**, not an audited final deployment.
- Broader cybersecurity sovereign claims remain future-facing and conditional on controlled real-world adjacent-mandate proof.

## [v2.7.0-rc.2] - 2026-04-22

### Added
- New release checklist: `release/v2.7.0-rc.2-ui-demo-release-checklist.md` with acceptance criteria, smoke checks, migration/rollback notes, and explicit claim boundaries.
- Demo ladder validator `scripts/check_demo_links.py` to catch broken ladder links and missing role labels.

### Changed
- Root posture moved from `v2.7.0-rc.1` to `v2.7.0-rc.2` as the next additive RC cut.
- Dashboard UI polished for operator legibility: improved hierarchy, demo ladder cards, synthetic-vs-real labels, and RC2 snapshot naming.
- Flagship demo HTML report (`run_demo.py` output) refreshed for institutional readability with clearer wedge flow, deterministic winner criteria visibility, and operator artifact map.
- `RELEASES.md` acceptance surfaces generalized for v2.7.x RCs and now include demo ladder consistency checks.
- `demos/README.md` labeling clarified for flagship synthetic vs compact synthetic vs real-world pack roles.

### Notes
- This release remains a **verifiable release candidate**, not an audited final deployment.
- Broader cybersecurity sovereign claims remain future-facing; this RC only strengthens synthetic wedge proof surfaces and operator clarity.

## [v2.7.0-rc.1] - 2026-04-22

### Added
- Root doctrine stack docs: `docs/DOCTRINE_STACK.md`, `docs/THERMODYNAMIC_MODEL.md`, `docs/NATION_STATE_DOCTRINE.md`, `docs/DEMO_STRATEGY.md`, and `docs/RELEASE_POSITIONING.md`.
- Math validation helper `scripts/check_math_markdown.py` for canonical equation and delimiter checks.
- Doctrine consistency helper `scripts/check_doctrine_consistency.py` for README doctrine links and canonical equation drift checks between root and flagship docs.
- Release readiness checklist at `release/v2.7.0-rc.1-demo-doctrine-checklist.md`.
- Demo strategy now uses direct Markdown links to all ladder surfaces and includes smoke-run command references for release operators.

### Changed
- Added `demos/README.md` as a canonical demo ladder index and updated demo README cross-links to use valid relative Markdown links.
- Adjacent synthetic proof README now explicitly states ladder role (supporting compact synthetic surface) and clarifies non-claims alongside cross-links.
- Adjacent synthetic proof README demo ladder links now use clickable relative Markdown links and include explicit sovereign-boundary language.
- Flagship and adjacent demo integration language now consistently frames protocol correctness as the first wedge and distinguishes synthetic vs real-world proof surfaces.
- Public-facing naming now prefers Protocol Cybersecurity labels while retaining legacy Protocol Assurance compatibility aliases where needed.
- Root release posture and demo entry points updated to v2.7.0-rc.1 demo-and-doctrine framing.
- Doctrine consistency helper now validates root README demo-ladder links and required role labels in `demos/README.md`.
- Demo strategy doctrine references now use direct Markdown links for cleaner operator navigation.
- Release provenance workflow artifact upload name now matches v2.7 verification docs (`v27-provenance-<TAG>`), with legacy v2.6 naming noted for historical runs.

### Notes
- This release remains a **verifiable release candidate**, not an audited final deployment.
- Broader cybersecurity sovereign claims remain future-facing and conditional on real adjacent-mandate controlled proof.

## [v2.6.0-rc.1] - 2026-04-18

### Added
- Root repository contract docs: contribution, security, support, release policy, changelog, and code owners.
- Release provenance workflows for source artifacts, SHA256SUMS, SBOM generation, and artifact attestations.
- Verification guide at `docs/verify-release.md`.
- Canonical threshold schemas and validation tests for decryption attestations and threshold bindings.
- Governance accounting docs and backend query surfaces for reviewer ledger and council seat lifecycle.
- Backend hardening: versioned migration, idempotent/reorg-safe indexer cursor, readiness, metrics, OpenAPI export, and deterministic backfill command.
- Dashboard hardening with proof/governance sections, alert views, and JSON/PNG snapshot export.
- Trust/proof docs and public proof docket template shell.

### Changed
- `README.md` updated for v2.6 RC verification and proof-first milestone framing.
- Contracts received NatSpec interface comments and release metadata surface constants.

### Notes
- This release is a **verifiable release candidate**, not an audited final deployment.
- Follow-up fixes applied after initial RC patch:
  - CI now uses `npm install` when no lockfile is present.
  - Reorg rewind now also clears derived governance rows.
  - Migration view DDL updated for PostgreSQL compatibility.
  - FastAPI `List` typing import fixed to avoid startup error.
  - Council lifecycle indexing now records real seat identifiers from governance events.
  - Reviewer/governance read-model indexing now includes required event ABIs.
  - Provenance manifest timestamp is deterministic (commit time / SOURCE_DATE_EPOCH), not wall-clock.
  - Registry ABI snapshot export now includes review/quarantine events used by governance indexing.
  - Challenge/deactivation lifecycle attribution now uses causal seat-occupant lookups.
  - Challenge resolution rewinds now remain reorg-safe by updating resolution block markers.
  - Release provenance workflow now archives the requested release tag ref instead of branch HEAD.
  - Challenge creation block is immutable; resolution uses a separate resolved block marker for rewind safety.
  - Release provenance checkout now uses the requested tag ref so manifest/SBOM match archived source.
  - Council active seat read-model now treats challenged seats as active until deactivation.
  - Release provenance bundle now includes deterministic OpenAPI export for API-surface verification.
  - Root posture docs normalized to v2.6 RC framing; added contracts package map and CODEOWNERS baseline.
  - SDK package/version now align to v2.6.0-rc.1 metadata while EIP-712 attestation domain remains at verifier-compatible `2.5`.