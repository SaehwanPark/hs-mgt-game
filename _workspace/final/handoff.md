# Handoff — External Playtest Protocol Refresh (v0.1.39)

## Summary

Added a Phase 7 prep protocol for informal external playtests of the current CLI
game. The protocol gives facilitators setup steps, stabilization and competitive
preview session scripts, an observation rubric, post-session prompts, a note
template, privacy cautions, and synthesis guidance.

## Changed files

### Added documentation

- `docs/external-playtest-protocol.md`

### Updated project state

- `Cargo.toml`, `Cargo.lock`, `CHANGELOG.md`
- `README.md`, `SPEC.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Verification

- `cargo fmt --check`
- `cargo test` (201 library tests plus integration tests)

## Known limits

- No runtime behavior changed.
- The protocol is for informal playtesting, not formal human-subjects research
  or calibrated learning-outcome measurement.
- External playtest synthesis remains future work.
