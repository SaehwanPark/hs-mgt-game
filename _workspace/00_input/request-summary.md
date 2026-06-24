# Request Summary

## Scope

Continue development with a bounded Phase 5 playability slice: add a starting
executive dashboard and strategy commitment previews to the existing CLI.

## Roadmap Phase

Phase 5 first vertical slice — playable CLI affordance and pre-run executive
context, without changing the deterministic core mechanics.

## Expected Outputs

- Updated `src/main.rs` with pure dashboard and strategy-preview helpers
- CLI output that shows starting state context and commitment previews before
  strategy selection
- Version bump to `0.1.13`
- Corrected `SPEC.md` state for the merged state-hash replay proof
- Updated README, architecture notes, changelog, lessons, domain QA, and final
  handoff artifacts

## Non-Goals

- No per-turn interactive command entry
- No scenario or ruleset file loader
- No command parser, save format, or replay artifact export
- No new commands, actors, metrics, random streams, or gameplay turns
- No changes to transition logic, actor decisions, resolved inputs, or replay
  hash semantics
- No empirical calibration or policy forecasting claim
- No module split

## Validation Target

- CLI shows a starting dashboard before strategy selection
- CLI previews all three compiled strategy paths using commitments only
- Previews do not describe future actor outcomes or replay results
- Existing deterministic strategy outcomes remain unchanged
- `cargo fmt --check`, `cargo test`, and default `cargo run` pass

## Generic Skills Needed

- `simple-code-writer` for the minimal implementation
- `code-reviewer` for the preferred-workflow review loop after PR handoff
