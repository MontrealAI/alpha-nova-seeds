# Badge Strategy (v2.8.0-rc.3)

This document defines how badges are used in this repository so the front door stays useful, disciplined, and proof-first.

## Goals

The badge system is designed to answer high-value questions quickly:

1. What is the current release posture?
2. Are core workflows healthy?
3. Where are the canonical demo entry points?
4. What is the explicit claim boundary?

It is intentionally not a vanity wall.

## Source of truth

- Canonical badge metadata: `release/badges.json`
- Generator: `scripts/generate_readme_badges.py`
- Validator: `scripts/check_readme_badges.py`

README badge blocks are managed between markers:

- Root: `<!-- BADGE_RAIL_START --> ... <!-- BADGE_RAIL_END -->`
- Demo ladder: `<!-- DEMO_BADGE_STRIP_START --> ... <!-- DEMO_BADGE_STRIP_END -->`

## Dynamic vs static badge policy

### Dynamic badges (GitHub workflow state / latest prerelease)

Use dynamic badges only for surfaces that should reflect live platform state:

- `ci.yml`
- `contracts-security.yml`
- `release-provenance.yml`
- latest prerelease tag on GitHub releases

### Static/generated badges (repo truth)

Use generated static badges for bounded claims and navigation:

- active RC posture
- proof-first bounded claim boundary
- demo ladder entry
- flagship demo entry
- accelerating-loop demo entry
- doctrine stack entry

These values are generated from local repo truth and versioned with docs/release updates.

## Operating commands

Regenerate badge rails:

```bash
python scripts/generate_readme_badges.py --write
```

Validate badge rails and links:

```bash
python scripts/check_readme_badges.py
```

Recommended paired release-surface check:

```bash
python scripts/check_release_surface_posture.py
```

## Change discipline

When changing release posture or badge semantics:

1. Update `release/badges.json` first.
2. Regenerate README blocks.
3. Run both badge and release-surface validators.
4. Update `CHANGELOG.md` and `RELEASES.md` if posture/acceptance surfaces changed.

This keeps README/AGENTS/RELEASES aligned and prevents silent drift.
