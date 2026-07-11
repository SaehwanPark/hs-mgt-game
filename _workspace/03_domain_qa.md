# Domain QA - ASC Project Observation Coverage

## Status

pass

## Reviewed Inputs

- `src/sim/observe_competitive.rs` and the ASC observation regression test.
- v0.10.55 deterministic capture and generated diagnostics.
- v0.10.54 source capture and project-limit findings.
- `docs/playtest-findings-v0.10.55.md`, `SPEC.md`, and the project handoffs.
- `README.md`, `docs/roadmap.md`, `docs/design_principles.md`, and the harness
  team specification.

## Findings

- The change is limited to an existing actor-visible observation boundary.
- True pending effects, active-project counters, validation, and transition
  history remain unchanged.
- The capture verifies that accepted ASC projects are visible before and after
  a rejected third-project command.
- The project ceiling remains labeled as a game abstraction rather than an
  empirical health-system constraint.
- No new actor, policy mechanism, social-welfare claim, or educational scoring
  rule was introduced.

## Required Fixes

None.

## Residual Risks

- Deterministic simulated-policy traces are not human or classroom evidence.
- Visibility and hash continuity do not establish comprehension, learning,
  balance, winnability, calibration, or policy validity.
- Structured project validation hints and broader guidance remain deferred.

## Verification Evidence

- Focused ASC evidence tests pass.
- Three Hard runs complete 24 transitions with expected rejection and safe
  retry behavior.
- v0.10.54 state-hash sequences remain identical.
- Full Python/Rust checks, formatting, clippy, automated playtests, and diff
  checks pass.
