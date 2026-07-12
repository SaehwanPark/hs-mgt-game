# Final Handoff - Release Metadata Check v0.12.13

## Result

- Added a read-only version-consistency check for `Cargo.toml`, `Cargo.lock`,
  README, and the latest changelog heading.
- Documented the local command and added the same command to GitHub Actions.
- Added focused tests for the current repository and a deliberate mismatch.
- No Rust runtime, scenario, replay, ruleset, or debrief behavior changed.

## Version boundaries

- Package: `0.12.13`
- Change surface: metadata checker, focused Python tests, CI command, docs, and
  queue status
- Publication, packaging, tag automation, registry access, and deployment:
  out of scope

## Branch and PR handoff

- Base branch: `main`
- Working branch: `feat/release-metadata-check-v0.12.13`
- PR: [#166](https://github.com/SaehwanPark/hs-mgt-game/pull/166)
- Domain QA: Pass for bounded contributor-readiness scope.
- Review passes: three clean post-open passes covering scope, checker behavior,
  and docs/version/queue boundaries.
- CI: [run #29210513712](https://github.com/SaehwanPark/hs-mgt-game/actions/runs/29210513712)
  passed.
- Merge state: pending PR review and merge.

## Verification

- `python3 scripts/check_release_metadata.py`: passed.
- Focused release metadata tests: 4 passed.
- Full Rust (308) and Python (230) suites, formatting, clippy, CLI smoke,
  golden, and diff checks: passed.

## Stop condition

After this check merges, the SPEC Future queue has no remaining item. Further
packaging, publication, licensing, deployment, or contributor workflow work
requires a new explicitly authorized requirement.
