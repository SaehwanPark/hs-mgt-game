# Implementation Plan — v0.13.106 Automatic Resume Policy

## Target slice

Close the roadmap's automatic-resume-policy gap without moving save authority
into the browser. The policy is limited to a stored opaque session ID recovered
at browser-refresh initialization; only the host may restore the durable
checkpoint, and the browser performs one bounded retry.

## Design

1. Add a small, versioned browser policy constant describing the allowed source,
   one-retry limit, opaque-ID-only storage, transient-failure retention, and
   confirmed-unknown cleanup behavior.
2. Refine `createActionClient.load` so automatic durable recovery is opt-in via
   an explicit refresh option. Manual launcher loads and ordinary internal
   refreshes do not hydrate an unknown session automatically.
3. Keep the existing host adapter `loadSession` boundary and use the current
   presentation/action/history/replay refresh path after recovery. Do not add a
   browser artifact path or client-side state reconstruction.
4. Add runtime/static tests for refresh recovery, manual-load non-recovery,
   one-attempt behavior, transient ID retention, and unknown-ID cleanup.
5. Synchronize the roadmap addendum, `SPEC.md`, player guide/UI copy, campaign
   coverage ledger, remaining-gate technical audit, release metadata, and
   lessons learned.

## Verification

- `cargo fmt`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets --all-features -- -D warnings`
- full Python test suite and focused resume-policy tests
- remaining-gate and release validators
- device-performance proxy and `git diff --check`
- one medium-effort review by the existing reviewer, Archimedes

## Non-goals and safety boundaries

- No browser-owned save serialization/parsing/loading/storage.
- No automatic checkpoint discovery, session replacement, or retry loop.
- No changes to simulation, stochastic inputs, replay regeneration, assets, or
  audio.
- Human/runtime gates remain pending and promotion remains blocked.

## Handoff

Commit and push the bounded slice on the temporary branch, update PR #352's
successor workflow only through a new PR, obtain the same single medium-effort
reviewer approval, merge to `main`, delete local/remote temporary branches, and
re-audit before selecting another unmet roadmap item.
