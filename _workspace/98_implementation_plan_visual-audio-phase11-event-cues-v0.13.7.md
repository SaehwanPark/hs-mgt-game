# Implementation Plan — Visual/audio Phase 11.1 event-cue coverage v0.13.7

## Target slice

Close the Phase 11.1 `Event cue coverage complete` checklist item for the
current competitive presentation contract by proving exact parity between the
event-channel entries in `AUDIO_CUE_CONTRACT` and the host's eight visible
event-cue projection IDs. Preserve explicit-empty, legacy-browser, and
unknown-cue behavior.

## Selection rationale

The host projection and GUI fallback tests already exercise the eight current
event cues, but the campaign ledger still describes them only as a catalog.
Joining the catalog to the projection is the next smallest technical gap and
prevents a cue being documented without a host trigger or a host ID being
rendered without a documented text/source contract.

## Design

1. Add an event-cue coverage section to the Phase 11.1 ledger naming the
   event-channel IDs, host projection source, and explicit limits.
2. Extend the focused Phase 11.1 coverage test to load the live audio contract,
   require exact event-channel ID parity, require source/equivalent metadata,
   and verify the host projection test's visible-only boundary markers.
3. Add a Rust runtime fixture assertion with an explicit event-cue allowlist
   and exact emitted order so projection parity is exercised, not only read
   from source text.
4. Close only the current event-cue coverage checklist item. Retain broader
   event taxonomy, audio quality, music continuity, screenshot, device,
   compatibility, and human-evaluation gates as open.
4. Record the contract, SDD status, roadmap evidence, QA, changelog, lessons,
   and version projections for v0.13.7.

## Explicit boundary

This is a deterministic catalog/projection audit. It does not add cues,
recorded audio, host events, simulation rules, hidden-state data, browser-owned
authority, or a claim that every event in every campaign has a cue.

## Verification gate

Run focused event-cue/campaign coverage and asset checks, then the full Python
suite, `cargo fmt --check`, Clippy with warnings denied, Rust tests, and all
release, documentation, security, and visual/audio contract checks before one
code-reviewer handoff. Merge to `main`, remove all topic branches, and then
re-audit the next unchecked roadmap item.

## Acceptance criteria

- Event-channel catalog IDs equal the eight host-projected visible event-cue
  IDs exactly once.
- The Rust runtime fixture emits only the allowlisted IDs in the expected
  order.
- Every event cue has a visible trigger source, text equivalent, and cues-only
  contract.
- Explicit empty cue lists, legacy visible fallback, and unknown IDs remain
  covered.
- Only the Phase 11.1 event-cue coverage item is checked.

## Risk label

Risk: low

Reason: the change adds governance evidence and parity tests only; no runtime,
simulation, host DTO, audio asset, replay, or state behavior changes.
