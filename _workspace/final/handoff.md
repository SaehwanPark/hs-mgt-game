# Final Handoff - Workforce Capacity Difficulty Design Gate v0.12.5

## Result

- Reviewed the v0.12.4 workforce-capacity signal against the typed competitive
  observation, MCP formatter, staffing transition events, and debrief output.
- Confirmed existing visible context: workforce trust, nursing-vacancy wording,
  prior operations, labor-market guidance, consultant options, and debrief
  attribution.
- Identified a bounded decision-time gap: safe typed staffing and physical-
  capacity counts exist in `PlayerObservation` but are omitted by the MCP
  formatter.
- Specified the smallest next projection: `Staffing:` and `Physical capacity:`
  lines using only existing typed fields.
- Excluded hidden targets, effective allocations, future hires, rival private
  state, and all difficulty/balance/transition tuning.

## Version boundaries

- Package: `0.12.5`
- Change surface: design contract, source-boundary review, and focused tests
- Competitive and affiliation transitions, rulesets, state hashes, replay
  artifact semantics, command parsers, persistence, and MCP behavior: unchanged
- Runtime difficulty/balance/scoring/winnability promotion: deferred

## Branch and PR handoff

- Base branch: `main`
- Working branch: `feat/workforce-capacity-design-v0.12.5`
- PR: [#158](https://github.com/SaehwanPark/hs-mgt-game/pull/158)
- Domain QA: Pass.
- Review passes: three post-open passes completed; no actionable code, data,
  scope, or documentation findings.
- CI: `check` passed in run [29208148870](https://github.com/SaehwanPark/hs-mgt-game/actions/runs/29208148870).
- Merge state: open and ready for merge after this handoff update.

## Verification

- Focused design-contract tests: 5 passed.
- Design artifact: source markers supported; observation follow-up required;
  runtime difficulty change unauthorized.
- Full Rust/Python suites, formatting, clippy, CLI smoke, competitive golden,
  and diff checks: passed locally; the PR check also passed.

## Next dependency

After merge, implement only the observation-context projection if the next
slice can add focused MCP boundary tests and prove unchanged v0.12.4-compatible
history/state hashes. Keep runtime difficulty and balance promotion deferred.
