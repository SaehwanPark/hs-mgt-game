# Request Summary — Visual/audio Phase 7.4 audio priority and fatigue manager v0.12.73

## Authorized outcome

Complete Milestone 7.4 as a bounded presentation-only audio manager. Keep
visible consequence cues understandable during dense resolution batches, keep
audio optional, and preserve written/UI equivalents and host authority.

## Target slice

- Add a pure priority policy for critical, major, routine, and ambient signals.
- Batch synchronous cue requests with at most one critical cue, duplicate
  suppression, routine/minor aggregation, deterministic priority order, and a
  bounded queue.
- Keep at most one transient cue voice active at a time; retain layered music
  stems and one ambience bed as separate background channels.
- Duck ambience under major/critical cues and music under critical cues using
  bounded local gain ramps.
- Persist only local audio preferences: mode, mute/music-only mute, reduced
  notifications, and channel volumes. Treat storage failure as session-local.
- Add rapid-input, month-resolution, fake-Web-Audio, preference, and
  screen-reader-equivalent coverage without changing host DTOs or simulation.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 7.4.
- `gui/audio.mjs` — current optional music, ambience, and cue runtime.
- `gui/audio-cue-contract.mjs` — 16 visible cue definitions and priority labels.
- `gui/music-stem-contract.mjs` and `gui/ambience-contract.mjs` — background
  audio layers and bounded release metadata.
- `gui/app.mjs` and `gui/index.html` — visible status, settings, and host-facing
  browser boundary.
- `assets/registry/audio-assets.json` — provenance and release gate.

## Non-goals

- No host/simulation/replay/history/hash changes, hidden-state inference, or
  browser-owned outcome logic.
- No new recorded/third-party assets, network dependency, speech, or automatic
  audio permission request.
- No claim of measured loudness, musical quality, fatigue reduction, lived
  accessibility, human comprehension, learning, calibration, or policy validity.
- Do not implement the later AI asset pipeline or broad platform audio work.

## Validation target

Focused priority/runtime tests, fake context/timer stress checks, preference
round-trip checks, visible fallback markers, registry/credits, metadata,
documentation links, full Python, full Rust, formatting, and diff checks.

## Evidence limits

Deterministic policy plans, bounded queue behavior, local ducking metadata,
storage round trips, and automated accessibility-equivalent checks establish
technical coverage only. Human listening, screen-reader, fatigue, classroom,
and educational evaluation remain open.
