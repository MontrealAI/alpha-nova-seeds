# Changelog

## [Unreleased]

### Changed
- `scripts/check_release_surface_posture.py` stale RC detection now matches discovered RC markers as full tokens, preventing false stale-marker failures when the active target reaches two-digit RC values (for example `v2.8.0-rc.10`).
- `scripts/check_release_surface_posture.py` now reads the active RC target from `release/badges.json` and validates posture coherence across README/AGENTS/RELEASES plus `docs/FRONTIER_LAB_POSTURE.md`, `docs/DOCTRINE_STACK.md`, and `demos/README.md`.
- `scripts/check_readme_badges.py` now validates that every `readme.rows` badge id exists in `readme.badges` and reports structured errors instead of uncaught `KeyError` traces during expected-block rendering.
- `scripts/check_readme_badges.py` now enforces that `readme.rows` actually render every `required_badges` ID, preventing silent omission of mandatory trust-surface badges from README output.
- Badge rail generation now supports explicit row groups from `release/badges.json` so root README renders a two-tier trust/navigation rail instead of a single long badge line.
- `release/badges.json` upgraded to row-driven metadata (`version: 2`) and now requires doctrine-stack coverage while dropping the optional latest-pre-release badge from the default front-door rail to reduce noise and drift risk.
- `scripts/check_readme_badges.py` now validates row presence and supports optional HTTP/HTTPS link verification (`--check-http-links`) in addition to local-link and workflow-file checks.
- Root README and demo ladder badge markers were regenerated into calmer, grouped strips for faster first-screen scanning without changing claim boundaries.
- Added `release/v2.8.0-rc.3-front-door-badge-checklist.md` with acceptance, smoke, migration, rollback, and provenance notes for this coherence cut.

- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- Tightened demo-ladder coherence checks by extending `scripts/check_demo_links.py` with deterministic cross-link requirements between `demos/open-ended-rsi-system/README.md`, `demos/unbounded-rsi-system/README.md`, and the ladder index.
- Updated `release/v2.8.0-rc.2-open-ended-rsi-checklist.md` smoke checks to include `scripts/check_open_ended_rsi_artifacts.py` and `scripts/check_release_surface_posture.py`, and added explicit runbook pointer for deterministic operator execution.
- Added `scripts/check_release_surface_posture.py` and wired it into open-ended RSI repo-native probes/runbook/root verification commands to catch README/AGENTS/RELEASES active-RC drift deterministically.
- Open-ended RSI demo now emits a dedicated `mandate3_execution.json` artifact capturing deterministic Mandate 3 execution details (selector policy, DISCO/Arnold execution steps, and offline-only constraints) for clearer auditability of autonomous execution behavior.
- Open-ended RSI artifact checker now validates Mandate 3 execution logging, top-ranked frontier selection consistency, and provenance determinism guards for disabled network/external API paths.
- Open-ended RSI demo now emits additional board/governance/provenance outputs (`board_scorecard.json`, `board_scorecard.md`, `governance_ruling.json`, `chronicle_entry.json`) and documents deterministic operator procedure in `demos/open-ended-rsi-system/RUNBOOK.md`.
- Open-ended RSI artifact checker now requires the board/governance/chronicle artifact set and enforces board-scorecard contract parity with `scorecard.json`.
- Demo ladder and release contract docs now link the open-ended demo runbook and explicitly record `v2.8.0-rc.2` posture coherence across README/AGENTS/RELEASES surfaces.

## [v2.8.0-rc.3] - 2026-04-23

### Added
- Introduced disciplined badge governance with `release/badges.json` as a single source of truth plus `scripts/generate_readme_badges.py` and `scripts/check_readme_badges.py` for deterministic README badge generation and drift checks.
- Added `docs/BADGE_STRATEGY.md` documenting dynamic-vs-static badge policy, badge marker ownership, and release update workflow.

### Changed
- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- `scripts/check_release_surface_posture.py` now rejects same-train future markers (for example `v2.8.0-rc.4`) so premature RC posture strings cannot pass alongside required `v2.8.0-rc.3` markers.
- `scripts/check_readme_badges.py` now enforces `release_target` parity with the `release-posture` badge metadata (`message` and `alt`) so front-door release badge drift cannot pass validation.
- `scripts/check_release_surface_posture.py` now rejects stale active RC markers (including `v2.8.0-rc.2`) as disallowed drift while keeping `v2.9.0-rc.1` blocked as a future marker.
- `scripts/check_readme_badges.py` now validates all relative local badge links (including `../...` overrides used by `demos/README.md` badge entries), not only `./...` paths.
- Upgraded root README front door with an institutional badge rail, tighter orientation hierarchy, explicit “what is / what is not claimed” boundary, and direct paths to flagship demo, demo ladder, accelerating-loop demo, doctrine stack, and release posture surfaces.
- Added a compact status strip to `demos/README.md` and aligned it with the root badge strategy using marker-managed generation.
- Reconciled release-surface posture to `v2.8.0-rc.3` across README, AGENTS, RELEASES, doctrine posture docs, and release-surface validator patterns.
- Extended release acceptance surfaces to include README badge synchronization checks.

### Notes
- This release is an additive front-door and release-surface hardening cut.
- It does **not** widen proof claims beyond bounded synthetic deterministic evidence.

## [v2.8.0-rc.2] - 2026-04-22

### Added
- New deterministic accelerating-loop demo at `demos/open-ended-rsi-system/` with governed generation pipeline, DISCO/Arnold alternating modes, machine-readable artifact ladder, board-ready HTML scorecard, and `--assert` smoke mode.
- Lightweight deterministic validator `scripts/check_open_ended_rsi_artifacts.py` to verify required `demos/open-ended-rsi-system/out/` artifacts, threshold contract outcomes, intervention-touch descent, and doctrine gate pass states.
- New staged demo artifact directories under `demos/open-ended-rsi-system/` (`00_manifest` ... `08_proof_docket` + `out`) plus deterministic emission of `capability_genome.json`, `assay_bundle.json`, `lineage.json`, `frontier_queue.json`, `intervention_log.json`, `scorecard.json`, `summary.md`, `proof_docket.md`, and `provenance_manifest.json`.
- Added deterministic `claim_boundary.json` emission and schema-conformance checks for capability genome / assay bundle / lineage artifacts in `demos/open-ended-rsi-system/run_demo.py`.
- New canonical v2.8 schemas for accelerating-loop artifacts: `schemas/v2.8/capability_genome.schema.json`, `schemas/v2.8/assay_bundle.schema.json`, and `schemas/v2.8/lineage.schema.json`.
- New release checklist `release/v2.8.0-rc.2-open-ended-rsi-checklist.md` with acceptance criteria, smoke checks, provenance expectations, migration/rollback notes, and claim boundaries.
- Added deterministic replay fingerprint artifact `demos/open-ended-rsi-system/out/determinism_fingerprint.json` and corresponding assert checks for fixed selection path + configuration contract.

### Changed
- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- `scripts/check_release_surface_posture.py` now rejects same-train future markers (for example `v2.8.0-rc.4`) so premature RC posture strings cannot pass alongside required `v2.8.0-rc.3` markers.
- `scripts/check_readme_badges.py` now enforces `release_target` parity with the `release-posture` badge metadata (`message` and `alt`) so front-door release badge drift cannot pass validation.
- Root README posture updated to active target `v2.8.0-rc.2`, with the new open-ended demo as the accelerating-loop front door while retaining `demos/unbounded-rsi-system/` as a legacy compatibility surface.
- Demo ladder index now designates `demos/open-ended-rsi-system/` as the accelerating-loop demo and preserves explicit demonstrated/simulated/unproven boundaries.
- Demo/doctrine link checks now include `demos/open-ended-rsi-system/` in required release surfaces.
- Repo-level posture docs (`AGENTS.md`, `docs/FRONTIER_LAB_POSTURE.md`, `docs/DOCTRINE_STACK.md`, `RELEASES.md`) aligned to the v2.8.0-rc.2 train without widening public claims.
- Open-ended RSI Mandate 1 now logs deterministic repo-native probe execution (including `protocol_smart_contract_correctness_demo` replay `--assert`, plus demo-link/doctrine/math checks) as non-simulated evidence inputs before synthetic adjudication stages.
- Open-ended RSI Generation 2 now derives candidates directly from `config.json` whitelist entries and fails closed if a whitelisted domain lacks deterministic assay profiles.
- Open-ended RSI outputs now include `out/safety_gates.json` to make doctrine gate outcomes (`no value without evidence`, `no autonomy without authority`, `no settlement without validation`) auditable as machine-readable artifacts.
- Open-ended RSI safety-gate statuses are now computed from real run outcomes (probe return codes, threshold gates, schema validation, and authority-bound checks) rather than hardcoded pass labels.
- Open-ended RSI output tree now mirrors generation artifacts in `out/` (`manifest.json`, `generation_0.json`, `generation_1.json`, `generation_2.json`) and logs a Generation 1 package-dependence ledger keyed to the frozen manifest hash.
- Open-ended RSI real Mandate 1 seed genome now includes broader repo-native surfaces (flagship demo runner, backend tests, v2.8 schema artifact, proof-docket template, and provenance manifest script) so frozen package dependency is better rooted in code/test/schema/proof/release inputs.
- Open-ended RSI determinism fingerprint now uses artifact file digests for `scorecard_hash` and `lineage_hash` to align with provenance-manifest hash semantics.
- Open-ended RSI assert-mode frontier selection check now derives expected domain from configured deterministic scoring output instead of hardcoding one domain label.
- Open-ended RSI Generation 0 now tracks deterministic strategy-family diversity on the Pareto frontier before winner freeze, and Generation 2 now emits a deterministically ranked frontier queue for clearer autonomy auditability.

### Notes
- This RC strengthens deterministic bounded mechanism evidence and operator presentation quality.
- It does **not** claim unrestricted autonomy, literal unbounded RSI, or completed broad real-world sovereign operation.

## [v2.8.0-rc.1] - 2026-04-22

### Added
- New flagship-class accelerating-loop demo: `demos/unbounded-rsi-system/` with deterministic Phase A/B/C execution, package freeze/hash, bounded mandate-3 selector, and board-ready outputs (`board_scorecard.*`, `report.*`, governance/provenance/safety artifacts).
- Deterministic Phase C selection artifact: `demos/unbounded-rsi-system/demo_output/mandate3_selection.json` capturing bounded-candidate scoring policy and ranked outcomes.
- Parent wedge board artifact: `demos/unbounded-rsi-system/demo_output/parent_wedge_brief.md` generated from deterministic Phase A business/wedge rationale.
- New release checklist: `release/v2.8.0-rc.1-unbounded-rsi-demo-checklist.md` covering acceptance criteria, smoke checks, provenance, migration/rollback notes, and claim boundaries.
- Frontier posture doctrine doc: `docs/FRONTIER_LAB_POSTURE.md`.
- New RC release checklist: `release/v2.8.0-rc.1-frontier-ui-demo-release-checklist.md` with acceptance criteria, smoke checks, migration/rollback notes, and explicit claim boundaries.
- Demo-local doctrine appendix: `demos/unbounded-rsi-system/DOCTRINE_APPENDIX.md` with canonical GitHub-compatible math rendering and bounded claim framing.

### Changed
- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- `scripts/check_release_surface_posture.py` now rejects same-train future markers (for example `v2.8.0-rc.4`) so premature RC posture strings cannot pass alongside required `v2.8.0-rc.3` markers.
- `scripts/check_readme_badges.py` now enforces `release_target` parity with the `release-posture` badge metadata (`message` and `alt`) so front-door release badge drift cannot pass validation.
- Demo ladder index now includes four coherent roles: flagship synthetic wedge, compact adjacent synthetic replay, real-world proof pack, and accelerating-loop demo.
- Root README front-door guidance links directly to the accelerating-loop demo and its bounded claim boundary.
- Demo-link and doctrine-consistency validators enforce presence of `demos/unbounded-rsi-system/` in ladder and root front-door surfaces.
- Dashboard ladder cards and artifact/release pointers include the accelerating-loop demo as a first-class operator surface.
- Flagship demo report UX (`run_demo.py` generated HTML) improved for operator readability and artifact discoverability while preserving deterministic behavior.
- Doctrine/release positioning surfaces aligned to v2.8.0-rc.1 naming and publication posture.

### Notes
- This accelerating-loop surface is a bounded proof-of-mechanism; it does not claim unrestricted autonomy or literal unbounded recursive self-improvement.
- This release remains a **verifiable release candidate**, not an audited final deployment.
- Broader cybersecurity sovereign claims remain future-facing and conditional on controlled real-world adjacent-mandate proof.

## [v2.7.0-rc.2] - 2026-04-22

### Added
- New release checklist: `release/v2.7.0-rc.2-ui-demo-release-checklist.md` with acceptance criteria, smoke checks, migration/rollback notes, and explicit claim boundaries.
- Demo ladder validator `scripts/check_demo_links.py` to catch broken ladder links and missing role labels.

### Changed
- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- `scripts/check_release_surface_posture.py` now rejects same-train future markers (for example `v2.8.0-rc.4`) so premature RC posture strings cannot pass alongside required `v2.8.0-rc.3` markers.
- `scripts/check_readme_badges.py` now enforces `release_target` parity with the `release-posture` badge metadata (`message` and `alt`) so front-door release badge drift cannot pass validation.
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
- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- `scripts/check_release_surface_posture.py` now rejects same-train future markers (for example `v2.8.0-rc.4`) so premature RC posture strings cannot pass alongside required `v2.8.0-rc.3` markers.
- `scripts/check_readme_badges.py` now enforces `release_target` parity with the `release-posture` badge metadata (`message` and `alt`) so front-door release badge drift cannot pass validation.
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
- `scripts/check_release_surface_posture.py` now compares all discovered `vX.Y.Z-rc.N` markers against the active target and rejects any premature future RC marker (for example `v2.9.0-rc.2` or `v3.0.0-rc.1`).
- `scripts/check_release_surface_posture.py` now rejects same-train future markers (for example `v2.8.0-rc.4`) so premature RC posture strings cannot pass alongside required `v2.8.0-rc.3` markers.
- `scripts/check_readme_badges.py` now enforces `release_target` parity with the `release-posture` badge metadata (`message` and `alt`) so front-door release badge drift cannot pass validation.
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
