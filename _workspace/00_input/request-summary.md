# Request Summary

## Scope

Implement the post-v0.2 SDD progress review plan. The goal is to review the
current playable prototype state and organize the next development queue in
`SPEC.md` and related SDD documents without promoting a runtime feature into
active development.

Specific tasks:
1. Record the progress review as a completed patch-level SDD slice.
2. Keep `SPEC.md` `Present` empty.
3. Reorganize `SPEC.md` `Future` into a ranked, gated next-development queue.
4. Refresh stale companion docs that still point to completed competitive
   runtime slices as next work.
5. Update `CHANGELOG.md`, `LESSONS.md`, and Cargo package version to `0.2.1`.
6. Run standard Rust checks and targeted stale-status scans.

## Non-Goals

- No changes to simulation transition rules, command syntax, scenario schemas,
  replay formats, MCP DTOs, gameplay balance, or public product positioning.
- No promotion of a Future item into `Present`.
- No claims of empirical calibration, measured human learning, classroom
  effectiveness, or policy-forecasting validity.

## Sources

- `README.md`
- `SPEC.md`
- `ARCHITECTURE.md`
- `CHANGELOG.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.1.56.md`
- `docs/playtest-findings-v0.1.58.md`
- `LESSONS.md`

## Expected Files

- `SPEC.md`
- `CHANGELOG.md`
- `LESSONS.md`
- `Cargo.toml`
- `Cargo.lock`
- `docs/first-scenario-brief.md`
- `docs/phase5-scope-register.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/final/handoff.md`

## Validation Target

- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
- Targeted `rg` scan for stale competitive-runtime and SDD status phrases.

## Global Skills Needed

- `spec-driven-developer` for SDD index, changelog, and architecture/status
  synchronization.
- `plan-designer` for keeping the implementation bounded to the approved plan.
- `simple-code-writer` for minimal, scoped edits.
