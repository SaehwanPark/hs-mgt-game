# Final Handoff - Workforce Capacity Observation Context v0.12.6

## Result

- Added the exact competitive MCP `Staffing:` and `Physical capacity:` lines
  from existing typed `PlayerObservation` fields.
- Added a focused session-boundary regression test with seed-42 starting
  values.
- Replayed 75 compatible simulated-policy runs and 1,800 transitions.
- Confirmed exact history and state-hash equality against the immutable v0.11.11
  all-tier and v0.11.9 Expert controls.
- Confirmed all 1,800 trace observations contain both safe lines and no hidden
  marker from the excluded-field contract.
- Kept runtime difficulty, balance, scoring, transition, command, replay/hash,
  winnability, and human-learning promotion deferred.

## Version boundaries

- Package: `0.12.6`
- Change surface: MCP presentation, focused boundary test, evidence artifact,
  and project records
- Competitive and affiliation transitions, rulesets, state hashes, replay
  artifact semantics, command parsers, persistence, and debrief behavior:
  unchanged

## Branch and PR handoff

- Base branch: `main`
- Working branch: `feat/workforce-capacity-observation-v0.12.6`
- PR: to be opened after final local verification
- Domain QA: Pass for the bounded observation-only scope.
- Review passes: pending PR opening and post-open review.
- Merge state: pending PR review and merge.

## Verification

- Focused Rust boundary test: passed.
- Matrix artifact: 75/75 complete runs, 1,800 transitions, 1,800 staffing
  lines, 1,800 physical-capacity lines, zero hidden markers.
- Source comparison: 60/60 all-tier histories and 15/15 Expert histories match
  exactly; all state-hash sequences match exactly.
- Full Rust/Python suites, formatting, clippy, CLI smoke, golden, and diff
  checks: pending final verification.

## Next dependency

After merge, re-audit the affiliation-first design and produce the narrow
v0.12.7 runtime boundary proposal before implementing any new affiliation
mechanic. Keep acquisition breadth, deal finance, legal forecasting, and
difficulty/balance promotion deferred.
