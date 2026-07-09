# Final Handoff - Future Queue Re-ranking and SDD Alignment

## Summary

Implemented the `v0.10.32` Future queue re-ranking and SDD alignment slice. The
change restructures `SPEC.md` Future items around explicit promotion rules,
validation-first ranking, and cross-cutting SDD guardrails so future work can be
promoted into bounded `Present` slices without broadening scope.

This is a documentation and project-state slice. It does not change runtime
mechanics, command legality, scenario schemas, MCP DTOs, replay formats, state
hashes, ruleset values, difficulty values, scoring, balance, GUI code, or asset
files.

## Changed Files

- `SPEC.md`: adds the `v0.10.32` completion record, explicit Future promotion
  rules, a six-track ranked queue, and cross-cutting SDD guardrails.
- `CHANGELOG.md`, `Cargo.toml`, and `Cargo.lock`: record `v0.10.32` project
  state and package metadata.
- `LESSONS.md`: records the durable SDD lesson that Future queues should
  separate ranked work from promotion rules and cross-cutting guardrails.
- `_workspace/00_input/request-summary.md`, `_workspace/03_domain_qa.md`, and
  `_workspace/final/handoff.md`: record repo-local handoff bookkeeping.

## Verification

- `git diff --check`
- `rg` stale-queue/version scan over SDD and companion docs; remaining hits were
  expected historical references or current version records.
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`

## Known Limits

- The ranking is a planning posture, not a claim that lower-ranked work is less
  valuable in all future circumstances.
- Expert difficulty is not yet proven winnable; it is now a future validation
  target with explicit non-goals.
- Regional M&A is not yet a scenario or mechanic; domain review and a bounded
  design slice are still required.
- GUI work has no toolkit, asset manifest, packaging plan, or implementation;
  the accepted boundary is only that a future GUI must reuse the existing core.
