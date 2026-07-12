# Request Summary - Workforce Capacity Difficulty Design Gate v0.12.5

## Scope

- Continue from merged PR #157 and the v0.12.4 candidate workforce-capacity
  pressure signal.
- Review the typed competitive observation, MCP formatter, transition events,
  and debrief boundary to decide whether the signal is sufficiently visible at
  decision time.
- Specify the smallest observation-only follow-up if safe typed staffing and
  capacity fields are omitted from MCP output.
- Keep difficulty values, balance, winnability, and transition semantics
  deferred until a separately justified implementation gate.

## Non-goals

- No runtime code, state, transition, ruleset, threshold, scoring, balance,
  difficulty, command, scenario, replay/hash, or GUI changes in this design
  gate.
- No hidden staffing targets, effective-capacity calculations, rival private
  workforce state, future hiring resolution, or actor utility exposure.
- No human-learning, calibration, legal-validity, policy-forecasting, or general
  Expert winnability claim.

## Sources

- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/proposal.md`.
- v0.12.4 difficulty-depth report and source artifact:
  `_workspace/experiments/v0.12.4-difficulty-depth-evidence/`.
- `src/model/campaign.rs` (`PlayerObservation`),
  `src/sim/observe_competitive.rs`, `src/mcp/session.rs`,
  `src/sim/transition_competitive.rs`, and `src/debrief/report.rs`.
- Existing competitive MCP/session tests and v0.11.11/v0.11.12 findings.

## Expected files

- `_workspace/experiments/v0.12.5-workforce-capacity-design/` deterministic
  design contract and diagnostics.
- `tests/test_workforce_capacity_design.py` for the design contract.
- `docs/playtest-findings-v0.12.5.md`, `docs/workforce-capacity-design-v0.12.5.md`,
  `SPEC.md`, `CHANGELOG.md`, README, architecture/roadmap/lesson notes, and
  workspace handoffs.
- `Cargo.toml` and `Cargo.lock` for version `0.12.5`.

## Validation target

- The design artifact names the v0.12.4 candidate signal and distinguishes
  existing visible fields from omitted typed fields.
- The proposal stays observation-only: render safe staffing/capacity fields at
  the MCP boundary using `PlayerObservation`, with no hidden-state inference.
- The artifact specifies focused tests and the unchanged v0.12.4 matrix as the
  next implementation gate, while keeping runtime promotion for mechanics and
  balance deferred.
- Domain QA returns `Pass`; full Rust/Python, formatting, clippy, golden, CLI,
  and diff checks pass under default parallel CI tests.
