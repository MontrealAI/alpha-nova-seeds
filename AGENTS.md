# AGENTS.md

## Scope
This file governs the entire repository unless a deeper `AGENTS.md` overrides it.

## Product doctrine
- Preserve the constitutional stack in this order: **identity → proof → settlement → governance**.
- Do not widen claims beyond what is implemented and testable.
- Prefer additive hardening and release engineering over architectural rewrites.
- Keep backend stack as **FastAPI + Postgres** and contract stack as **Solidity**.

## Release discipline
- For every release candidate, include:
  1. concrete acceptance criteria,
  2. explicit migration notes,
  3. provenance artifacts (hashes/manifests),
  4. rollback notes.
- Keep PRs implementation-ordered and small enough to review.

## Communication
- Use plain English for operator-facing docs.
- Clearly label assumptions, unknowns, and non-goals.
