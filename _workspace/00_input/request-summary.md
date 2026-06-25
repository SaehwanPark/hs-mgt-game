# Request Summary — Competitive Multi-Month Loop

## Scope

Continue the competitive campaign runtime after v0.1.35 by replacing the
single-month interactive preview plus preset months 2-3 preview with one bounded
three-month competitive loop. The loop should reuse the existing deterministic
one-month resolver, AI batch generation, event/delay tick, institution phase,
Stata-like command parser, and executive report renderer.

## Non-goals

- No full 24-month campaign loop
- No competitive autosave or replay artifact export
- No syntax highlighting or autocomplete
- No scenario file loader
- No Medicare/Medicaid strategic actors
- No stabilization campaign behavior changes
- No new dependencies

## Sources

- User-approved plan for `feat/competitive-multi-month-loop`
- Canonical docs: `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`
- Harness spec: `docs/harness/health-policy-strategy-game/team-spec.md`
- Current runtime state in `SPEC.md`, `ARCHITECTURE.md`, and `CHANGELOG.md`
- Existing code in `src/cli/campaign.rs` and `src/competitive/month_loop.rs`

## Expected files

- `src/cli/campaign.rs`
- `src/competitive/month_loop.rs` if focused loop tests need adjustment
- `Cargo.toml`, `CHANGELOG.md`, `README.md`, `SPEC.md`, `ARCHITECTURE.md`
- `_workspace/00_input/request-summary.md`, `_workspace/final/handoff.md`
- `LESSONS.md` only if implementation reveals a reusable trap

## Validation target

- `cargo fmt --check`
- `cargo test`
- Competitive seed-42 golden remains deterministic; update only if the planned
  loop changes the committed golden scope with a changelog note.
- Stabilization golden hash remains unchanged.

## Roadmap phase

Phase 6.0 competitive campaign runtime continuation. This is a narrow runtime
slice after I8, not a broad MVP completion.
