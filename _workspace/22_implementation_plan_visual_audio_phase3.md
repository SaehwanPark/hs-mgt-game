# Implementation Plan — Visual and Audio Phase 3 Contextual Action Submission v0.12.19

Status: Design approved for implementation.

Branch: `feat/visual-audio-phase3-contextual-actions-v0.12.19`

## User request and context

Continue the visual/audio Future track after the merged Phase 2 read-only
projection. Phase 3 must let an executive complete one competitive month from
the browser while preserving canonical CLI/MCP commands, host validation,
rejection atomicity, and explicit stochastic uncertainty.

## Goal

Add a bounded graphical action workflow for `competitive-regional-v1`:

- host-supplied action catalog for all existing competitive command families;
- contextual parameter forms that construct canonical command text;
- local draft batch add, revision, and removal;
- host-owned non-mutating validation preview with exact aggregate costs,
  constraints, delay labels, and uncertainty labels;
- submit only a validated canonical batch through the existing transition
  boundary; and
- preserve the Phase 2 read-only viewer and show rejected submissions without
  changing the current envelope, turn, history, or hashes.

## Assumptions

- The first graphical month targets the current competitive human system only.
- Existing `parse_competitive_batch`, `validate_competitive_batch`,
  `CompetitiveCommand::action_cost`, and `submit_turn` remain authoritative.
- The client may own draft form values and a draft batch, but it may not own
  action costs, legal constraints, transitions, randomness, or outcomes.
- Action catalog labels for delay/uncertainty/constraint are presentation
  metadata supplied by the host and are not outcome predictions.
- Phase 4 owns monthly resolution animation and causal overlays; Phase 3 only
  displays the committed response returned by the host.

## Exact implementation targets

1. `src/mcp/action.rs`
   - Add versioned typed action-catalog, parameter, preview, validation, and
     cost DTOs for all seven existing competitive command families:
     `hold`, `invest`, `recruit`, `monitor`, `negotiate`, `commit`, and
     `project`.
   - Build catalog templates from existing command vocabulary and expose no
     hidden state or guessed rival/private outcomes.
   - Return host-supplied delay, constraint, and uncertainty labels as
     presentation metadata.

2. `src/mcp/session.rs`, `src/mcp/server.rs`, `src/mcp/mod.rs`
   - Add `GetActionCatalogRequest`, `ValidateTurnRequest`,
     `ActionCatalogEnvelope`, and `ValidateTurnEnvelope`.
   - Add non-mutating `get_action_catalog` and `validate_turn` MCP tools for
     `competitive-regional-v1`.
   - Reuse the existing parser and validator; return invalid validation results
     as data so the client can revise/retry without a transition.
   - Leave `submit_turn` as the only transition path and preserve its existing
     rejection atomicity.

3. `gui/app.mjs`, `gui/index.html`, `gui/README.md`
   - Add a Phase 3 action client using `getActionCatalog`, `validateTurn`, and
     the existing `submitTurn` adapter boundary.
   - Render generic host-supplied parameter forms, canonical previews, exact
     host-returned costs, delay/constraint/uncertainty labels, draft rows, and
     validation errors.
   - Support add, revise, remove, validate, retry, and submit controls with
     keyboard labels and no command text input requirement.
   - Keep the read-only client as the default when no action adapter is
     configured; action controls must fail closed when the adapter is absent.

4. Tests and evidence
   - Add Rust tests for catalog coverage, canonical template parity, exact cost
     calculation through existing model methods, valid/invalid validation, and
     unchanged session state after validation/rejection.
   - Add Python/Node GUI contract tests for form generation, draft
     add/revise/remove, host validation, no local cost formula, no-submit-before
     validation, rejection/error recovery, and no-network/no-asset behavior.
   - Add `docs/visual-audio-phase3-contextual-actions-v0.12.19.md` with source
     mapping, command equivalence, user checklist, evidence limits, and Phase 4
     gate.

5. Project records
   - Promote Phase 3 in `SPEC.md`, refresh `ARCHITECTURE.md`, `README.md`,
     `CHANGELOG.md`, `LESSONS.md`, workspace evidence/mechanism notes, domain
     QA, final handoff, and version metadata to `0.12.19`.

## Acceptance criteria

- A player can build and revise a batch using graphical controls without typing
  CLI syntax.
- Every generated command is one of the existing canonical competitive command
  forms and is submitted unchanged to the host adapter.
- Exact aggregate AP/cash/political-capital cost and validation constraints come
  from the host; the browser contains no cost or transition formula.
- Invalid validation and rejected submission show recoverable errors while the
  current turn/history/hash/envelope remains unchanged.
- A successful submit calls only the existing host transition path and renders
  its committed response; no stochastic result is promised before resolution.
- Existing Phase 0/1/2, MCP, CLI, golden, replay, and metadata checks remain
  green.
- The diff changes no core transition, randomness, replay verification,
  scenario, audio, asset, or network-dependent behavior.

## Non-goals

- No resolution animation, causal overlay, replay playback, audio, assets,
  mobile support, campaign expansion, instructor true-state view, or human
  usability claim.
- No browser-side validation beyond field-shape/required-input checks needed to
  construct a host request; legality remains host-owned.
- No new command family, command alias, hidden outcome forecast, client
  resource mutation, or GUI-only transition.

## Stop conditions

Stop and narrow the phase if the action workflow requires a second parser,
client-side cost formulas, hidden rival/private fields, a transition outside
`submit_turn`, a new simulation rule, or a deployment/network convention.

## Review and handoff checks

- Use exactly one code-reviewer pass, per the user’s workflow instruction.
- Treat action-task checks as technical/interface proxies, not human usability
  or educational evidence.
- Merge only after focused/full verification, one review, CI, and explicit
  rejection-atomicity evidence; then return to Phase 4 design.
