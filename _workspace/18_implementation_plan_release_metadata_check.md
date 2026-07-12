# Implementation Plan — Release Metadata Check v0.12.13

## Target slice

Add one dependency-free repository check that confirms the package version is
consistent across `Cargo.toml`, `Cargo.lock`, the README milestone line, and
the latest changelog heading. Document the local command and run the same
check in GitHub Actions.

## Files

- `scripts/check_release_metadata.py`: read-only metadata checker.
- `tests/test_release_metadata.py`: checker behavior and current-repository
  contract tests.
- `.github/workflows/ci.yml`: run the check in CI.
- `docs/contributor-release-check.md` and `README.md`: local usage and scope.
- `Cargo.toml`, `Cargo.lock`, `CHANGELOG.md`, `SPEC.md`: v0.12.13 release
  metadata and queue status.
- `ARCHITECTURE.md`, `docs/roadmap.md`, `LESSONS.md`, and SDD handoff files:
  record the bounded governance change.

## Non-goals

- No package publication, tag automation, release upload, or registry access.
- No dependency installation or broad CI restructuring.
- No simulation, command, scenario, ruleset, replay, state hash, or debrief
  behavior change.
- No release convention beyond the existing versioning policy.

## Acceptance criteria

- `python3 scripts/check_release_metadata.py` passes locally.
- A deliberately mismatched version is reported by the checker test.
- CI runs the same local command before Rust checks.
- Contributor documentation explains what is checked and what is not.
- Package metadata is bumped to `0.12.13` and the release Future item is
  removed from `SPEC.md`.
- The final SPEC audit has no numbered Future queue item remaining.
