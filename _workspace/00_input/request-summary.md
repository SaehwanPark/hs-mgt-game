# Request Summary — Visual/audio Phase 9.2 audio playback fallback v0.12.83

## Authorized outcome

Add a deterministic presentation-only audio playback fallback so unsupported or
failed optional Web Audio behavior preserves visible cue meaning without
breaking the GUI or introducing a second source of simulation state.

## Target slice

- Add a pure audio presentation adapter over the existing cue/music/ambience
  catalog and shared availability contract.
- Make unsupported context creation and cue playback exceptions publish a
  stable local fallback descriptor/status while preserving the cue source and
  written equivalent.
- Add focused fake-context tests for unavailable setup, thrown playback, and
  successful recording; keep generated audio and all current assets unchanged.
- Keep pending portraits outside runtime and release authority.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 9.2 and the v0.12.83
  audio-fallback target slice.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `gui/audio.mjs`, `gui/asset-availability.mjs`, and current audio tests.
- `scripts/validate_assets.py`, release guidance, and current audio contracts.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not add recorded audio, decode files, or redesign the audio catalog.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Audio fallback contract/tests, existing asset security/manifest/registry/
generation/credits/release/documentation checks, full Python/Rust tests,
formatting, Clippy, JavaScript, and diff checks.

## Evidence limits

The fallback contract establishes deterministic local recovery behavior only; it
does not measure loudness, prove browser/Web Audio compatibility, establish
human accessibility, validate audio quality, or replace human review. Portrait
human decisions, approved local model/seed provenance, release derivatives, and
registry bridges remain explicit external gates.
