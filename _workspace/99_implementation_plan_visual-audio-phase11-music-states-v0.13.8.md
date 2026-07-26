# Implementation Plan — Visual/audio Phase 11.1 music-state coverage v0.13.8

## Target slice

Close the Phase 11.1 `Music-state coverage complete` checklist item for the
current presentation contract by proving parity between all seven music-state
catalog entries, the six host resolution states, and the browser-only menu
state. Exercise the host projection with a Rust runtime allowlist and preserve
the existing visible-only fallback.

## Selection rationale

The live music projection and browser classifier already cover the current
states independently, but the campaign ledger does not record their exact
split. A catalog/host/browser parity slice is the smallest next step and keeps
the menu stage honest: it is a local presentation state, not a host resolution
state.

## Design

1. Add a music-state coverage section to the Phase 11.1 ledger with all seven
   catalog IDs, six host IDs, and the browser-only menu ID.
2. Extend focused coverage tests to require catalog metadata and classifier
   parity, then add a Rust runtime fixture assertion with an explicit host
   allowlist and exact state cases.
3. Close only current music-state coverage. Retain campaign music taxonomy,
   continuity, audio quality, screenshot, device, compatibility, and human
   evaluation gates as open.
4. Record contract, SDD status, roadmap evidence, QA, changelog, lessons, and
   v0.13.8 version projections.

## Explicit boundary

This is deterministic catalog/projection evidence. It does not add stems,
audio assets, timing, host events, simulation rules, hidden state, browser-owned
authority, or claims about musical usefulness or fatigue.

## Verification gate

Run focused music/campaign coverage and asset checks, then the full Python
suite, `cargo fmt --check`, Clippy with warnings denied, Rust tests, and all
release, documentation, security, browser, and visual/audio contract checks
before one code-reviewer handoff. Merge to `main`, delete all topic branches,
and re-audit the next unchecked roadmap item.

## Acceptance criteria

- All seven catalog IDs have visible source, text equivalent, fallback, and
  stem metadata.
- The host runtime emits only the six allowlisted resolution states.
- The browser classifier covers all seven states, with `menu` explicitly
  browser-only.
- Only the Phase 11.1 music-state coverage item is checked.

## Risk label

Risk: low

Reason: the slice adds deterministic parity evidence and test assertions; no
runtime behavior, audio bytes, simulation, replay, or host state changes.
