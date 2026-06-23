# Request Summary

## Scope

Continue development under the preferred workflow by adding the first minimal
playable CLI choice over the existing deterministic two-turn history and
educational debrief.

## Roadmap Phase

Primary phase: Phase 5 first vertical slice preparation.

Forward intent: move the architecture proof toward a narrow playable slice by
letting the player choose among three hard-coded strategy paths without
implementing scenario loading or a general command parser.

## Sources

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/phase1-lit-review.md`
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

- No full campaign.
- No general command parser.
- No scenario loader.
- No external data ingestion.
- No full policy lifecycle framework.
- No general debrief framework or instructor export format.
- No CI, release automation, or contributor-process expansion.
- No empirical calibration or policy forecasting claim.

## Generic Global Skills Needed

- `preferred-workflow` for branch and delivery discipline.
- `simple-code-writer` for minimal implementation.
- `spec-driven-developer` for documentation state.
- `code-reviewer` after PR or diff handoff.
