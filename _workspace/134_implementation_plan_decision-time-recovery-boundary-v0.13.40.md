# Implementation Plan — Phase 12.3 decision-time recovery boundary v0.13.40

## Task restatement

Close the current Phase 12.3 evidence item for decision-time information
recoverability by documenting the existing immutable core/CLI record, host
history/replay summaries, and current browser recovery boundary. Keep a
browser-native per-decision observation timeline as separately open work.

## Current understanding

- The core `Transition` record retains the prior world state, command,
  resolved inputs, actor observation, actor decision, effects, next state, and
  state hash.
- The debrief tells reviewers to use observations recorded before each command
  and preserves prior committed observations when a later estimate is revised.
- Host history/replay envelopes expose immutable transition summaries, command
  text, effects/events, counts, and hashes; the browser renders that summary as
  a text-first history view.
- The current browser history view does not replay the full per-decision
  observation from each core transition, so a complete browser timeline remains
  open.

## Target slice

Add `docs/evaluation/phase12-decision-time-recovery-boundary.json` and a parity
test that record:

- core/CLI decision-time observation retention and debrief recovery language;
- host history/replay summary alignment and hash continuity;
- current browser text-first recovery and its missing full-observation boundary;
- written fallback and read-only authority; and
- explicit non-goals for new history fields, routes, persistence, hidden-state
  exposure, and human educational conclusions.

## Assumptions

- “Recoverable” means technically recoverable from the existing core/CLI
  history contract; it does not claim browser-native per-decision playback or
  human comprehension.
- Current host summaries remain intentionally narrower than core history and do
  not authorize promotion of resolved inputs or private rationale.
- The source-linked boundary is sufficient evidence for this checklist item;
  the browser timeline is a later implementation slice if the roadmap still
  requires it after adjacent debrief design work.

## Minimal implementation plan

1. Add the decision-time recovery boundary ledger and source-parity test.
2. Check the Phase 12.3 item and synchronize canonical docs, lessons, version
   metadata, generated credits, and additive request/contract/QA/handoff
   records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next Phase 12.3 item.

## Non-goals

- Do not add browser timeline controls, observation fields, routes, persistence,
  screenshots, assets, audio files, true-state views, causal graphs,
  counterfactuals, distributional views, exports, or educational claims.
- Do not expose resolved inputs, hidden state, or private actor rationale in
  live player history.

## Stop conditions

Stop if the existing core observation/command pairing cannot be distinguished
from the narrower host/browser summary without changing authority or implying a
complete visual timeline.

## Risk label

Risk: low

Reason: The slice records existing recovery boundaries only; it adds no runtime
fields or presentation authority.
