# Project Specification

This file is the lightweight spec-driven-development index for the Health
Policy Strategy Game. It tracks what is already true, what is being changed now,
and what is intentionally deferred.

Canonical product and domain direction lives in:

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Spec Maintenance Rule

Any active or incomplete item in `Present` must explicitly separate:

- `Done`: implemented, documented, or verified work that already exists on the
  active branch.
- `Not Yet Done`: planned goal or target scope for the active item that is not
  complete yet.
- `Deferred / Non-Goals`: excluded work, future work, or known limits that
  should not be mistaken for planned completion within the active item.

Do not rely only on summaries, verification lists, or out-of-scope notes for
active work; future contributors must be able to tell what exists versus what
is planned-but-incomplete versus what is deliberately out of scope without
reconstructing it from the diff.

## Past

- Project concept established as a Rust, CLI-first health-policy strategy game
  about leading a fictional nonprofit US health system.
- Canonical proposal, roadmap, and design principles created under `docs/`.
- Repo-local agent harness created for project-specific health-policy simulation
  workflow.
- Rust package scaffold and spec-driven documentation baseline established.
- Feature: Deterministic vertical-slice spine
  Status: Complete
  Started: 2026-06-23
  Branch: feat/deterministic-slice-spine

  Summary:
  Replace the placeholder CLI with a small deterministic architecture proof: a
  scripted health-system turn with explicit resolved inputs, validation,
  actor-specific observation, one commercial-insurer decision rationale,
  attributed effects, append-only history, and replay verification.

  Done:
  - Placeholder `Hello, world!` CLI replaced by a scripted deterministic demo
  - Package version bumped to `0.1.2`
  - Single-file Rust prototype added with typed world state, ruleset, resolved
    inputs, player command, validation errors, observation, actor decision
    record, events, attributed effects, transition, and history
  - Pure transition path added for the scripted slice:
    `prior state + command + resolved inputs + ruleset -> transition`
  - Commercial-insurer decision added with accept, counter, and reject outcomes
    plus inspectable rationale text
  - Append-only demo history and replay function added
  - State fingerprint string added for deterministic demo inspection
  - Focused tests added for deterministic repeatability, true-state versus
    observed-state separation, validation failures, unfavorable valid outcomes,
    accepted-rate handling, negative capital-spend rejection, and replay
  - Repo-local handoff artifacts added under `_workspace/`
  - `ARCHITECTURE.md`, `CHANGELOG.md`, and `LESSONS.md` updated for the slice
  - PR handoff opened as GitHub PR #2, and three review passes completed
  - PR #2 merged into `main`

  Deferred / Non-Goals:
  - No full campaign or multiple-turn playable scenario
  - No interactive CLI input or command parser
  - No scenario, ruleset, or save-file loader
  - No external data ingestion or official parameter ledger
  - No empirical calibration, validation against real data, or policy
    forecasting claim
  - No cryptographic state hash or durable replay artifact format
  - No module split; prototype remains in `src/main.rs` until another command or
    actor interaction justifies boundaries
  - No CI, release automation, or expanded contributor process

  Verification:
  - Identical prior state, command, resolved inputs, and ruleset produce the
    same transition
  - Observed access can differ from true access through explicit resolved inputs
  - Invalid commands fail validation separately from unfavorable modeled outcomes
  - Replay from genesis reproduces the committed final state
  - `cargo fmt`, `cargo test`, and `cargo run` pass

## Present

- Feature: State policy response slice
  Status: Active
  Started: 2026-06-23
  Branch: feat/state-policy-response-slice

  Summary:
  Extend the scripted deterministic demo from one payer negotiation into a
  two-turn history by adding one state-policy response command. The new command
  models a health system response to a state access mandate using explicit
  advocacy spend, access commitment, actor-specific observation, state-official
  decision rationale, attributed effects, and replay verification.

  Done:
  - Package version bumped to `0.1.3`
  - Added `RespondToStateAccessMandate` with validation for advocacy spend and
    access commitment
  - Added state policy decisions for flexibility, mandate continuation, and
    oversight escalation
  - Demo history now commits the existing capacity/payer turn followed by one
    state-policy response turn
  - Replay now verifies the final state of a two-transition history
  - Focused tests added for deterministic policy response, invalid advocacy
    spend, invalid access commitment, unfavorable valid policy outcome, and
    two-transition replay

  Not Yet Done:
  - Complete three code-reviewer passes and address findings
  - Merge after review and verification

  Deferred / Non-Goals:
  - No interactive CLI input or command parser
  - No scenario, ruleset, or save-file loader
  - No external data ingestion or empirical calibration
  - No full policy lifecycle framework
  - No module split yet

  Verification:
  - Existing payer negotiation behavior remains intact
  - Invalid operations remain separate from unfavorable modeled outcomes
  - Two-transition replay reproduces the committed final state
  - `cargo fmt`, `cargo test`, and `cargo run` pass

## Future

- Define glossary, decision-record conventions, and versioning policy from
  roadmap Phase 0.
- Convert Phase 1 research into an evidence registry and research-to-design
  implications memo.
- Define the initial conceptual model: system boundary, actor classes, ontology,
  observation model, and causal framework.
- Design the first narrow vertical slice with deterministic replay and
  educational debrief hooks.
- Split the prototype into stable module boundaries when the next slice needs
  more than one command or actor interaction.
- Add scenario data loading only after the conceptual model and first action
  vocabulary settle.
