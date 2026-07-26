# Implementation Plan — Visual/audio Phase 11.1 history view coverage v0.13.9

## Target slice

Close the Phase 11.1 `History view updated` checklist item by recording and
testing the current live history handoff: host `competitive-history-v1`, the
loopback route/adapter, text-first history rendering, aligned turn/hash rows,
and recoverable read failure that preserves the last valid view.

## Selection rationale

The live history route and browser client already exist and have focused tests,
but the campaign ledger still leaves the history checklist open. This is the
smallest next slice and strengthens a high-value explanation surface without
changing simulation, replay, or state authority.

## Design

1. Add a history-view coverage section to the Phase 11.1 ledger with exact
   host/schema/route/adapter/rendering sources and the failure boundary.
2. Extend the focused Phase 11.1 coverage test to require the live history
   handoff markers, aligned hash rendering, and failure-preserving behavior
   already exercised by `tests/test_phase11_live_history.py`.
3. Close only the history-view checklist item; retain debrief, save/load,
   replay continuity, screenshot, device, compatibility, and human gates.
4. Record contract, SDD status, roadmap evidence, QA, changelog, lessons, and
   v0.13.9 version projections.

## Explicit boundary

This is history presentation evidence only. It does not add a history store,
alter immutable records or hashes, expose true state, change commands or
transitions, or claim that save/load/replay continuity is complete.

## Verification gate

Run focused history/campaign coverage and asset checks, then the full Python
suite, `cargo fmt --check`, Clippy with warnings denied, Rust tests, and all
release, documentation, security, browser, and visual/audio contract checks
before one code-reviewer handoff. Merge to `main`, delete all topic branches,
and re-audit the next unchecked roadmap item.

## Acceptance criteria

- The ledger names the canonical history schema, host route, adapter, renderer,
  turn/hash alignment, and failure-preserving behavior.
- Focused tests prove valid rendering, incomplete/schema rejection, missing or
  throwing adapter recovery, and unchanged authority boundaries.
- Only the Phase 11.1 history-view item is checked.

## Risk label

Risk: low

Reason: the slice adds deterministic evidence and tests around existing
read-only history presentation; no runtime or simulation behavior changes.
