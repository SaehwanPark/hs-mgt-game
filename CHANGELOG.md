# Changelog

All notable project changes should be recorded here.

The project follows lightweight semantic versioning during early development.

## [0.1.3] - 2026-06-23

### Added

- Added a deterministic state-policy response command to the scripted demo.
- Added state policy official decisions with inspectable rationales for
  flexibility, mandate continuation, and oversight escalation.
- Extended demo replay to cover a two-transition history.
- Added focused tests for policy response determinism, validation failures,
  unfavorable valid policy outcomes, and two-transition replay.

### Changed

- Bumped package version from `0.1.2` to `0.1.3`.
- Updated project state and handoff documentation for the policy-process slice.

## [0.1.2] - 2026-06-23

### Added

- Replaced the placeholder CLI with a scripted deterministic architecture proof.
- Added typed world state, player command validation, resolved inputs,
  actor-specific observation, commercial-insurer decision rationale, attributed
  effects, append-only history, replay, and focused unit tests.
- Added `_workspace/` handoff artifacts for request framing, evidence mapping,
  and mechanism design.

### Changed

- Bumped package version from `0.1.1` to `0.1.2`.
- Updated `SPEC.md` and `ARCHITECTURE.md` to reflect the implemented prototype
  instead of a placeholder executable.

## [0.1.1] - 2026-06-23

### Added

- Initiated root-level spec-driven-development documents:
  - `SPEC.md`
  - `ARCHITECTURE.md`
  - `CHANGELOG.md`
- Initiated `LESSONS.md` for durable development lessons.

### Changed

- Bumped package version from `0.1.0` to `0.1.1` for this PR-equivalent
  documentation change.

## [0.1.0] - Initial

### Added

- Initial Rust package scaffold.
- Canonical project proposal, roadmap, and design principles.
- Repo-local health-policy strategy game agent harness.
