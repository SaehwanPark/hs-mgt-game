# Request Summary — External Playtest Protocol Refresh

## Scope

Continue development after v0.1.38 by adding a Phase 7 prep protocol for
informal external playtests of the current CLI game. The protocol should cover
both implemented flows: the five-turn `stabilization-v1` slice and the bounded
three-month `competitive-regional-v1` preview.

## Non-goals

- No Rust runtime behavior changes
- No scenario file loader
- No full 24-month competitive campaign
- No competitive autosave or replay artifact export
- No Medicare/Medicaid strategic actors
- No empirical calibration or policy-forecasting claim
- No formal human-subjects research workflow beyond cautioning when it is needed

## Sources

- User-approved plan for `feat/external-playtest-protocol`
- Canonical docs: `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`
- Harness spec: `docs/harness/health-policy-strategy-game/team-spec.md`
- Current state in `SPEC.md`, `CHANGELOG.md`, `docs/how-to-play.md`,
  `docs/first-scenario-brief.md`, and `docs/competitive-scenario-brief.md`

## Expected files

- `docs/external-playtest-protocol.md`
- `README.md`, `SPEC.md`, `CHANGELOG.md`
- `Cargo.toml`, `Cargo.lock`
- `_workspace/00_input/request-summary.md`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation target

- `cargo fmt --check`
- `cargo test`
- Manual documentation review for scope, campaign status accuracy, educational
  debrief framing, privacy caution, and no unsupported forecasting claims

## Roadmap phase

Phase 7 prep. This is a documentation and validation-readiness slice, not a
runtime expansion.
