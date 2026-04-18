# Security Policy

## Release posture
Nova-Seeds v2.6 is a **release candidate** for proof and release hardening. It should not be represented as audited or production-final.

## Reporting a vulnerability
Please report vulnerabilities privately:
- Open a security advisory in GitHub (preferred), or
- Email the maintainers listed in `SUPPORT.md`.

Include:
1. affected component (`contracts/`, `backend/`, `dashboard/`, `sdk/`),
2. reproduction steps,
3. expected vs actual behavior,
4. severity assessment,
5. mitigation ideas if available.

## Response goals
- Initial acknowledgement: within 3 business days.
- Triage status update: within 7 business days.
- Fix timeline: communicated after triage.

## Hardening controls in v2.6 RC
- Static analysis in CI for Solidity.
- Release artifact checksums and attestations.
- Deterministic backend ingestion surfaces and readiness probes.

## Non-goals in v2.6 RC
- Declaring the system audited.
- Declaring final mainnet deployment safety.
