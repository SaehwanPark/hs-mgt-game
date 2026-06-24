# Request Summary

## Scope

Continue development with a bounded Phase 4 technical architecture proof: add
stable per-transition state hashes and replay verification that detects committed
hash drift.

## Roadmap Phase

Phase 4 technical architecture proof — deterministic transition kernel,
append-only history, replay verification, and reproducible state hashes.

## Expected Outputs

- Updated `src/main.rs` with canonical state records, stable state hashes, and
  replay hash verification
- Version bump to `0.1.12`
- Corrected `SPEC.md` state for the merged Phase 3 actor/scenario slice
- Updated README, architecture notes, changelog, lessons, domain QA, and final
  handoff artifacts

## Non-Goals

- No scenario or ruleset file loader
- No command parser, save format, or replay artifact export
- No cryptographic hash dependency or security guarantee
- No new commands, actors, metrics, random streams, or gameplay turns
- No module split
- No empirical calibration or policy forecasting claim

## Validation Target

- Each committed transition stores a stable hash derived from a canonical state
  record
- Replay recomputes and verifies every committed transition hash
- Tampered committed hashes produce an explicit replay error
- Existing deterministic strategy outcomes remain unchanged
- `cargo fmt --check`, `cargo test`, and default `cargo run` pass

## Generic Skills Needed

- `simple-code-writer` for a minimal implementation
- `code-reviewer` for the preferred-workflow review loop if PR handoff is
  requested
