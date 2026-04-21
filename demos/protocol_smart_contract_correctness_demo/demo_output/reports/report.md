# Protocol Smart-Contract Correctness Flagship Demo Report

**Synthetic disclaimer:** This report is synthetic, local, replayable, and falsifiable. It is not a real-world proof.

## Sector and parent business
- Sector: protocol and smart-contract correctness
- Parent business: Protocol Assurance Studio
- Why first wedge: objective, replayable, fast to review, reusable primitives, commercially legible.

## First mandate and assay setup
- Mandate 1 focus: governance/dispute correctness
- Contract fixtures: `CouncilGovernanceV25Fixture.sol`, `ChallengePolicyModuleV25Fixture.sol`
- Common harsh assay metrics: accepted usefulness points, time-to-first-accepted output, repair/rework, evidence completeness, unsupported claim rate, packageable artifact quality.

## Five sibling Nova-Seeds
| Seed | Mutation thesis | Operator workflow delta |
|---|---|---|
| audit_factory | Maximize breadth-first issue harvesting with strict triage templates. | Front-load contract surface enumeration and standardized triage queues. |
| exploit_replay | Map known exploit families onto current contracts to rapidly test inherited failure modes. | Run exploit-pattern replay passes before bespoke analysis. |
| fuzz_harness | Use seeded property fuzzing to find edge-case transition failures quickly. | Generate deterministic fuzz harnesses before manual deep-dive. |
| governance_parameter_simulator | Stress governance outcomes under parameter shifts (quorum, challenge windows, role thresholds). | Run deterministic parameter sweep before line-level issue extraction. |
| invariant_library | Start from reusable governance and settlement invariants, then map code paths against them. | Require each finding to link to broken invariant and state-transition path. |

## Nova-Seed assay (Mandate 1)
Winner: **invariant_library**

| Seed | AUP | First accepted step | Rework | Evidence | Unsupported claim rate | Package quality |
|---|---:|---:|---:|---:|---:|---:|
| audit_factory | 15 | 9 | 0.667 | 0.714 | 0.200 | 0.680 |
| exploit_replay | 12 | 10 | 0.500 | 0.786 | 0.333 | 0.620 |
| fuzz_harness | 23 | 9 | 0.333 | 0.857 | 0.000 | 0.720 |
| governance_parameter_simulator | 10 | 12 | 0.500 | 0.786 | 0.000 | 0.760 |
| invariant_library | 32 | 6 | 0.250 | 0.893 | 0.000 | 0.930 |


## Frozen capability packages
- Sub-pack: `GovernanceValidationPack-v1`
- Sector stepping stone: `ProtocolAssurancePack-v1`
- Distinction: sub-pack is first frozen reusable governance capability; stepping stone is promoted sector-level portability surface.

## Adjacent mandate (Mandate 2) control vs treatment
- Mandate 2 focus: threshold / attestation correctness
- Contract fixtures: `ThresholdNetworkAdapterV25Fixture.sol`, `SignedAttestationVerifierV25Fixture.sol`
- Control AOY: 1.067
- Treatment AOY: 1.667
- AOY uplift: 56.2%
- Speed uplift: 33.3%
- Repair/rework reduction: 100.0%
- Evidence completeness uplift: 27.2%
- Safety regression: NO
- Package dependence rate: 100.0%

## Threshold ruling (strict)
- AOY uplift ≥ 35%
- Speed uplift ≥ 30%
- Repair/rework reduction ≥ 40%
- Evidence completeness uplift ≥ 20%
- No safety regression
- Package dependence rate ≥ 30%
- Adjacent-mandate proof: **PASS**

## Sovereign emission
- Artifact: `ProtocolAssuranceSovereign-v1.synthetic.json`
- Status: `emitted`
- PASS interpretation: this emits the first compounding correctness sovereign in synthetic demo form, i.e., the α-AGI Protocol Assurance Sovereign.
- PASS interpretation: this is also the seed of a future broader cybersecurity sovereign.
- It does **not** claim a full cybersecurity sovereign already exists.
