# Request Summary

## Scope

Continue development under the preferred workflow by replacing the placeholder
CLI with the first deterministic vertical-slice spine.

## Roadmap Phase

Primary phase: Phase 4 technical architecture proof.

Forward intent: prepare a narrow Phase 5 vertical slice without implementing a
full campaign.

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

- Rust prototype in `src/main.rs`
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
- No interactive command parser.
- No scenario loader.
- No external data ingestion.
- No CI, release automation, or contributor-process expansion.
- No empirical calibration or policy forecasting claim.

## Generic Global Skills Needed

- `preferred-workflow` for branch and delivery discipline.
- `simple-code-writer` for minimal implementation.
- `spec-driven-developer` for documentation state.
- `code-reviewer` after PR or diff handoff.
