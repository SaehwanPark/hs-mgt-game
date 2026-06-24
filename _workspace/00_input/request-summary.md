# Request Summary

## Scope

Extend the seeded three-turn playable demo with a fourth turn modeling a regional
access coalition cooperative opportunity.

## Roadmap Phase

Phase 5 first vertical slice — interaction breadth (coalition/cooperative
opportunity per roadmap §5.2).

## Expected Outputs

- `PlayerCommand::JoinRegionalAccessCoalition` with validation
- Regional provider coalition liaison decision with inspectable rationale
- Four-transition history, replay, and educational debrief coverage
- Focused tests and golden-trajectory pinning for seed `42`
- Package version `0.1.8`

## Non-Goals

- No full campaign or per-turn interactive command entry
- No scenario or ruleset file loader
- No Medicare/Medicaid/competitor actors
- No module split unless unavoidable
- No new Cargo dependencies
- No CI or release automation

## Validation Target

- Four committed transitions replay deterministically from genesis
- `transition()` contains no RNG, time, or I/O
- Coalition liaison rationale appears in history and debrief
- Invalid coalition inputs fail validation separately from unfavorable outcomes
- `cargo fmt`, `cargo test`, and `cargo run` pass

## Generic Skills Needed

- `simple-code-writer` for implementation
- `code-reviewer` for PR review loop
- `spec-driven-developer` for project state sync
