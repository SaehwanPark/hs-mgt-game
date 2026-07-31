# Implementation Plan — Host-envelope replay playback rail v0.13.66

## Target slice

Close the next narrow replay gate: let a player review committed replay rows
through a local written playback rail driven only by the existing host
`ReplayEnvelope`.

## Risk and scope

- Risk: medium. The change is a browser presentation controller and its typed
  tests; it must not become a second simulation or state boundary.
- In scope: previous/next/play/pause replay-row review for the existing visible
  transition summaries, keyboard/native control semantics, empty and failed
  states, and synchronized evidence/docs/version metadata.
- Out of scope: replay regeneration, new host routes or schemas, true-state or
  resolved-input exposure, simulation changes, durable persistence, autosave,
  assets/audio, screenshots, human review, and public release.

## Design contract

1. `getReplay` remains the only source. The browser validates the existing
   `competitive-replay-v1` envelope and stores only visible summaries already
   authorized for the replay/history surface.
2. Playback is a local review cursor over immutable rows. Previous, next, play,
   pause, and selected-row status never call `submitTurn`, mutate host state,
   regenerate a trace, or invent missing outcomes.
3. The rail has a complete written equivalent: active transition number,
   command/observation/effects/events/hash text, empty-state text, and
   recoverable failure text. Reduced motion and audio-off behavior remain
   valid because no semantic meaning depends on animation or sound.
4. Failed or malformed reads preserve the last valid envelope and playback
   cursor; an empty replay disables movement and reports that no committed rows
   exist.
5. The existing history list and host route remain backward compatible. No
   browser serialization, new DTO, service worker, or true-state field is
   introduced.

## Implementation steps

1. Add a small local replay playback controller and bind it to the existing
   replay client and history panel controls.
2. Add focused Node/browser-source tests for validation, cursor movement,
   play/pause, empty/failure preservation, keyboard semantics, and authority
   exclusions; preserve existing host replay tests.
3. Update the Phase 11.1 ledger, roadmap, GUI guide/README, SPEC, changelog,
   lessons, request/contract/QA/handoff records, and release metadata to
   v0.13.66.

## Verification and handoff

- `cargo fmt --check`, `cargo test`, and Clippy with warnings denied
- full Python suite plus release metadata, docs links, asset/security/
  generation/credits, device/offline/browser/audio/raster/loading, visual/audio
  contract, and diff checks
- exactly one medium-effort read-only code reviewer
- commit, push, PR checks, merge to `main`, and local/remote branch cleanup

## Exit evidence

The replay panel must allow a player to move through committed visible rows and
read the selected command, observation, effects/events, and state hash while a
host read failure preserves the last valid view and no client-side transition
or regenerated trace occurs.
