# Request Summary — Visual/audio Phase 7.2 environmental ambience library v0.12.71

## Authorized outcome

Complete Milestone 7.2 as a bounded, fixture-verifiable ambience recipe library
for seven fictional settings. Keep ambience subtle, optional, non-clinical, and
outside deterministic host/simulation state.

## Slice boundary

- Cover executive office, hospital lobby, hospital campus exterior, construction
  site, boardroom, press/policy event, and regional city bed.
- Define generation method, project-generated license, per-setting source hash
  records, and the explicit no-release-file derivative rule,
  noise floor, loop points, loudness, speech/music/institution-name exclusions,
  reduced-audio behavior, written equivalent, and generic fallback.
- Add all seven entries to the runtime ambience catalog while keeping the
  existing regional city bed as the only active default selection.
- Add a fixture proof and tests for catalog completeness, deterministic recipe
  metadata, optional/muted/cues-only behavior, and no hidden-state selection.
- Do not add recorded audio, network assets, clinical alarms, real institutions,
  adaptive music, or simulation/host/replay changes.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 7.2.
- `gui/audio.mjs` — existing optional generated ambience playback.
- `gui/audio-cue-contract.mjs` — shared generated-audio boundary.
- `assets/registry/audio-assets.json` — provenance and release gate.
- `docs/design_principles.md` — optional audio and information boundaries.

## Validation target

Focused ambience/audio tests, fixture proof checks, registry/credits, metadata,
documentation links, full Python, full Rust, formatting, and diff checks.

## Evidence limits

Generated filtered-noise recipe metadata, deterministic source hashes, and
static loop checks establish technical coverage only. They do not establish
audibility, atmospheric quality, fatigue, lived accessibility, classroom
suitability, human comprehension, or policy validity.
