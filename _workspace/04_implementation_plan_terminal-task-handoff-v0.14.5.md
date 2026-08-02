# Implementation Plan — Terminal task handoff v0.14.5

## Target slice

Synchronize the existing browser-local first-session task rail with the host's
terminal session signal. A terminal competitive or campaign-coverage envelope
shows a final-debrief task; a subsequent nonterminal load returns to the normal
flow. Explicit End session uses the same state so Review is not paired with a
stale action instruction.

## Design

1. Add `sessionDone` to the first-month flow state and a final `terminal` stage
   in both existing flow variants.
2. Populate/reset `sessionDone` only at existing presentation/session handoffs:
   session loads, committed refreshes, campaign-coverage commits, and the
   explicit end-session result.
3. Keep the controller's Review routing and host APIs unchanged; the terminal
   task text is presentation-only and does not fabricate a result.
4. Add deterministic Node/Python contracts for terminal rendering and reset,
   update release/currentness projections to v0.14.5, and preserve historical
   records.

## In scope

- `gui/first-month.mjs`, `gui/app.mjs`, focused GUI tests.
- Current core docs, GUI/presentation contract, changelog, release metadata,
  generated credits, and append-only workspace handoff evidence.

## Out of scope

- Host routes, schemas, Rust simulation, commands, history/replay formats,
  checkpoint semantics, assets/audio, or non-default browser support.

## Exit criteria

- Terminal task state is driven by the existing host terminal field and is
  cleared by a nonterminal load.
- Both flow variants render explicit final-debrief wording with text-first
  semantics; no future workspace is unlocked by the rail.
- Focused and full automated checks, documentation currentness, and one
  medium-effort code review pass; merged PR and branch cleanup recorded.
