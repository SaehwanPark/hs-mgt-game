# Implementation Plan — Host autosave after committed GUI decisions v0.13.68

## Target slice

Close the next explicit Phase 11.1 technical gate: automatically request the
existing host checkpoint after every accepted GUI decision for competitive,
stabilization, and regional-affiliation sessions.

## Design

1. Reuse `saveSession` and the configured host-only durable checkpoint path;
   add no route, schema, browser serialization, or second state store.
2. Invoke autosave only after the host accepts a transition. A checkpoint
   failure is written and recoverable, but never rolls back or hides the
   already committed host transition.
3. Keep manual Save/Restore controls as explicit retry and recovery paths.
4. Keep the browser limited to the opaque session ID and save metadata; all
   state, history, verification, and file I/O remain host-owned.

## Files and boundaries

- `gui/app.mjs`: shared autosave callback for competitive and campaign
  coverage submissions, written success/failure status, and the existing
  `ui.save-complete` cue.
- `gui/index.html`, `gui/README.md`, and `docs/guides/gui-how-to-play.md`:
  explain automatic checkpointing and manual retry behavior.
- `tests/test_phase11_live_checkpoint.py` and campaign coverage checks:
  verify autosave capability, call placement, error handling, and authority
  exclusions.
- Phase 11.1 ledger, roadmap, SPEC, changelog, README, lessons, and
  request/contract/QA/handoff records: record the bounded technical closure.

## Validation target

- Node syntax and focused checkpoint/autosave tests.
- Full Rust and Python suites, Clippy, formatting, release metadata, docs,
  asset/security/generation/credits, device/offline/browser/audio/raster/
  loading/visual-audio gates, and diff checks.
- Exactly one medium-effort code review, then PR, merge, and local/remote
  temporary-branch cleanup.

## Explicit non-goals

- No new save format, route, DTO/schema, simulation transition, browser state
  serialization, service worker, asset, audio file, screenshot, fresh AI
  search, human review, device certification, legal/provenance approval, or
  public-release claim.

## Exit criteria

- All three supported GUI campaigns request host autosave only after an
  accepted decision.
- Autosave success and failure remain written, recoverable, and non-authority-
  expanding; manual checkpoint controls remain available.
- Existing host restart, replay, history, debrief, and browser-refresh tests
  remain green.

