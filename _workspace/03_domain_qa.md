# Domain QA

## Status

pass

## Reviewed Inputs

- User request to implement the seeded stochastic input boundary plan.
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

- Scope remains narrow: seed-scoped input resolution over the existing two-turn
  demo rather than a full campaign, parser framework, or scenario loader.
- Stochasticity is explicit and outside the transition core: `resolve_inputs`
  derives `ResolvedInputs` from seed, turn, and prior state using named streams.
- `transition()` contains no RNG, time, filesystem, or network access.
- True state and reported observation remain distinct in both code and tests.
- Invalid commands remain separate from unfavorable valid outcomes.
- Invalid CLI strategy choice and invalid seed input remain separate from modeled
  outcomes.
- Commercial-insurer and state-policy decisions still include inspectable
  rationales, and the debrief reports those committed rationales.
- Prototype formulas remain abstractions, limiting false precision.
- Default seed `42` pins a canonical demo trajectory in tests without claiming
  empirical calibration.

## Required Fixes

- None before merge.

## Residual Risks

- Integer formulas are not empirically calibrated.
- State fingerprinting is human-readable and deterministic but not
  cryptographic.
- The prototype is still single-file; module boundaries should be revisited when
  repeated CLI behavior, scenario loading, reporting exports, or independent
  testing require it.
- Removing per-path hard-coded inputs changes default demo outcomes relative to
  earlier releases; this is documented through seed-pinned tests rather than
  hidden behavior drift.

## Verification Evidence

- `cargo fmt --check` completed successfully.
- `cargo test` passed: 30 tests passed.
- Default `cargo run` selected access stabilization and seed `42`, replayed
  successfully, and printed resolved inputs plus the educational debrief.
- Invalid seed input exits nonzero with an explicit CLI error.
- Different seeds change resolved inputs while identical seeds remain
  deterministic.
