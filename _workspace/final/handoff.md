# Final Handoff - Regional Affiliation Playtest Validation v0.12.1

## Result

- Captured and audited the opt-in `regional-affiliation-v1` campaign across
  independent, deferred, and pursuit policies at seeds 42, 43, and 44.
- Validated 9/9 complete six-stage runs, 54 observation-before-command links,
  54 transition/state-hash links, and 54 debrief stage lines.
- Preserved the affiliation runtime transition/replay/hash boundary and the
  competitive seed-42 golden path.
- Identified one concrete bounded gap: typed alternatives, assumptions, and
  commitments are not rendered in MCP affiliation observations.

## Version boundaries

- Package: `0.12.1`
- Affiliation transitions, ruleset, state hash, replay artifact, scenario, and
  command parser: unchanged
- Competitive ruleset, state hash, and golden trajectory: unchanged
- Runtime promotion: deferred for balance, ruleset, legal, and educational
  effect claims

## Branch and PR handoff

- Base branch: `main`
- Working branch: `feat/affiliation-playtest-validation-v0.12.1`
- PR: to be opened after local verification
- Domain QA: Pass.
- Review passes: pending implementation completion
- Merge state: pending PR review and merge

## Verification

- Focused artifact tests: 6 passed.
- Deterministic capture: 9 runs, 54 committed stages, 0 validation failures.
- Full Rust suite: 306 tests passed.
- Full Python suite: 169 tests passed.
- Formatting, clippy, competitive golden (2 tests), and diff checks passed.

## Next dependency

The next Present item is the bounded v0.12.2 MCP observation-context slice.
It should render only safe typed context, add focused observation tests, rerun
this exact matrix, and avoid transition/ruleset/balance changes.
