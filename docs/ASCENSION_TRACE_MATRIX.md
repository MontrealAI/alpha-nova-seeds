# Ascension Trace Matrix (bounded local/devnet)

| Layer | Artifact | Event coverage | Verification note |
|---|---|---|---|
| Insight | `out/insight_packet.json` | `InsightEmitted` | Deterministic opportunity packet + rationale |
| Nova-Seeds | `out/nova_seed_registry_snapshot.json` | `NovaSeedRegistered` | Three-seed registry with lifecycle states |
| MARK | `out/mark_selection_report.json` | `MarkScored` | Deterministic ranking + simulated allocation |
| Sovereign | `out/sovereign_manifest.json` | `SovereignFormed` | Bounded authority scope and policies |
| Business | `out/business_operating_plan.json` | Included in runtime events | Mandate decomposition references job IDs |
| Marketplace | `out/marketplace_round.json` | `AgentApplied`, `AgentSelected` | Competing local bids and assignment |
| AGI Jobs | `out/jobs/job_receipt.json` | `JobCreated`, `CompletionRequested`, `JobFinalized` | Proof-bound job receipt with local settlement units |
| Agents | `out/agent_execution_log.json` | `AgentApplied`, `AgentSelected` | Strategy-diverse deterministic agent profiles |
| Validators/Council | `out/validation_round.json`, `out/council_ruling.json` | `ValidationSubmitted` | Explicit validation checks + council ratification |
| Value Reservoir | `out/reservoir_ledger.json` | `ReservoirCredited` | Placeholder-unit local accounting only |
| Archive | `out/archive_lineage.json` | `ArchiveUpdated` | Capability and receipt lineage |
| Architect | `out/architect_recommendation.json` | `ArchitectRecommended` | Next-loop recommendation + blocked proof list |

## Boundary reminder

All artifacts and events are for bounded local/devnet replay. They are not a claim of mainnet production proof.
