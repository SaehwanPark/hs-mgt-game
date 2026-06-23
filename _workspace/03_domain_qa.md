# Domain QA

## Status

pass

## Reviewed Inputs

- User request to implement the approved playable CLI continuation plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- `_workspace/02_mechanism_design.md`
- `src/main.rs`

## Findings

- Scope remains narrow: a minimal CLI choice over three hard-coded two-turn
  strategy paths rather than a full campaign, parser framework, or scenario
  loader.
- Deterministic boundary is explicit: resolved inputs are provided to the
  transition function, and no hidden randomness, time, filesystem, or network
  state is used in core transition logic.
- CLI input is outside the transition core and only selects compiled strategy
  paths.
- True state and reported observation are distinct in both code and tests.
- Invalid commands are separated from unfavorable valid outcomes.
- Invalid CLI choice is separated from valid unfavorable modeled outcomes.
- The commercial-insurer and state-policy decisions include inspectable
  rationales, and the debrief reports those committed rationales.
- Prototype formulas are documented as abstractions, limiting false precision.

## Required Fixes

- Complete code-reviewer PR passes.

## Residual Risks

- Integer formulas are not empirically calibrated.
- State fingerprinting is human-readable and deterministic but not
  cryptographic.
- The prototype is still single-file; module boundaries should be revisited when
  repeated CLI behavior, scenario loading, reporting exports, or independent
  testing require it.

## Verification Evidence

- `cargo fmt --check` completed successfully.
- `cargo test` passed: 23 tests passed.
- Default `cargo run` selected access stabilization, replayed successfully, and
  printed the educational debrief.
- Strategy `2` selected fiscal caution, replayed successfully, and produced
  insurer accept plus mandate continuation.
- Strategy `3` selected aggressive bargaining, replayed successfully, and
  produced insurer rejection plus oversight escalation.
- Invalid strategy input exited nonzero with an explicit CLI error.
