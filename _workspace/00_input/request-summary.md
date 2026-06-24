# Request Summary

## Scope

Continue development with a bounded Phase 5 playability slice: add per-turn
interactive command entry as the default CLI play mode while preserving preset
strategy paths 1–3.

## Roadmap Phase

Phase 5 first vertical slice — playable CLI with per-turn executive decisions,
without changing the deterministic core mechanics.

## Expected Outputs

- Updated `src/main.rs` with play-mode selection, per-turn parsers, interactive
  session loop, executive briefings, and turn-resolution summaries
- Preserved preset strategy paths with unchanged golden trajectories
- Version bump to `0.1.14`
- Updated README, architecture notes, changelog, lessons, domain QA, and final
  handoff artifacts

## Non-Goals

- No new commands, actors, metrics, or random streams
- No scenario or ruleset file loader
- No command parser framework, save format, or replay artifact export
- No changes to transition logic, resolved inputs, actor decisions, or replay
  hash semantics
- No empirical calibration or policy forecasting claim
- No module split

## Validation Target

- Interactive play completes four turns from `cargo run`
- Preset paths 1–3 reproduce pre-slice behavior
- Invalid per-turn input fails before committing partial history
- Turn briefings use observation data only
- `cargo fmt --check`, `cargo test`, and `cargo run` pass

## Generic Skills Needed

- `simple-code-writer` for the minimal implementation
- `code-reviewer` for the preferred-workflow review loop after PR handoff
