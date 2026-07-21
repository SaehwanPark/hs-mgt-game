# Request Summary — Visual/audio Phase 7.1 UI and event cue refinement v0.12.70

## Authorized outcome

Complete Milestone 7.1 of `docs/visual_audio_enhancement_roadmap.md` as a
bounded generated-audio standards and client-control slice. Existing optional
Web Audio playback remains presentation-only.

## Slice boundary

- Cover all 16 existing interface and event cue IDs.
- Add a pure per-cue contract for semantic purpose, priority class, duration,
  loudness target, peak ceiling, cooldown, text equivalent, distinction, and
  visible trigger source.
- Apply the shared normalization/peak metadata to the existing synthesis path.
- Add an explicit local cues-only mode that disables music/ambience while
  preserving interface/event cues and written equivalents.
- Add a fixture proof and tests for every cue, visible-only trigger mapping,
  cues-only behavior, unsupported audio, mute, and safe fallbacks.
- Do not add downloaded/recorded audio, change host DTOs, simulation state,
  commands, transitions, stochastic inputs, history, hashes, replay authority,
  or debrief behavior.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 7.1.
- `gui/audio.mjs` — existing generated Web Audio client and cue vocabulary.
- `gui/audio-catalog.json` — existing fixture catalog.
- `docs/design_principles.md` — optional audio and actor-visible boundaries.
- `assets/registry/audio-assets.json` — provenance and release gate.

## Validation target

Focused cue-contract/audio tests, fixture proof checks, registry/credits,
metadata, documentation links, full Python, full Rust, formatting, and diff
checks.

## Evidence limits

Contract metadata and generated-tone tests establish technical consistency only;
they do not establish loudness on baseline hardware, lived accessibility,
fatigue, musical quality, human comprehension, learning, calibration, or policy
validity.
