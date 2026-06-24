# Request Summary

## Scope

Continue development under the preferred workflow by adding a seeded stochastic
input boundary to the existing deterministic two-turn playable CLI demo. Replace
per-path hard-coded `ResolvedInputs` with deterministic derivation from an
explicit seed and named random streams before the transition core runs.

## Roadmap Phase

Primary phase: Phase 4.3 stochastic input boundary completion.

Forward intent: keep strategy paths as command presets while moving exogenous
variation behind an inspectable seed boundary that preserves deterministic
replay.

## Sources

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `SPEC.md`
- `ARCHITECTURE.md`

## Expected Files

- Rust prototype and CLI boundary in `src/main.rs`
- Version bump in `Cargo.toml`
- Lightweight state updates in `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`,
  and `LESSONS.md`
- Handoff artifacts under `_workspace/`

## Validation Target

- `cargo fmt`
- `cargo test`
- `cargo run`

## Non-Goals

- No scenario or ruleset file format.
- No new Cargo dependency.
- No cryptographic state hash or durable replay artifact.
- No module split unless unavoidable.
- No interactive per-turn command entry.
- No CI, release automation, or contributor-process expansion.
- No empirical calibration or policy forecasting claim.

## Generic Global Skills Needed

- `preferred-workflow` for branch and delivery discipline.
- `simple-code-writer` for minimal implementation.
- `spec-driven-developer` for documentation state.
- `code-reviewer` after PR or diff handoff.
