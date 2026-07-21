# Implementation Plan — Visual/audio Phase 7.2 environmental ambience library v0.12.71

## 1. Task restatement

Define and register seven optional generated ambience recipes, expose them in
the existing audio catalog, keep the regional city bed as the active default,
and prove noise/loop/loudness/rights/speech/name/reduced-audio/fallback
contracts without adding recorded audio.

## 2. Current understanding

- `gui/audio.mjs` currently contains one generated ambience entry selected by a
  hard-coded active ID.
- Phase 7.1 established a project-generated Web Audio boundary and cues-only
  mode.
- Asset validation requires source hashes for modules referenced by registries.

## 3. Assumptions

- Generated recipe metadata is the authorized release artifact; there are no
  recorded files or external sources to license.
- The existing regional ambience remains the default active recipe so no new
  visible-context inference is introduced.
- If a setting requires true/private state or a recorded asset, stop and use the
  documented silent fallback instead.

## 4. Minimal implementation plan

1. Add `gui/ambience-contract.mjs` with seven filtered-noise setting entries, recipe/loop/
   noise/loudness/rights/speech/name/reduced-audio/equivalent fields, lookup,
   validation, and generic fallback helpers.
2. Update `gui/audio.mjs` to build `AUDIO_CATALOG.ambience` from the contract and
   schedule only the regional city-bed default, honoring full/cues-only/mute/
   focus/unsupported fallbacks.
3. Add `gui/ambience-proof.html`, focused tests, registry/credits metadata, and
   current GUI guidance.
4. Update roadmap, SPEC, architecture, README, CHANGELOG, lessons, and release
   metadata.

## 5. Files and functions likely to change

- `gui/ambience-contract.mjs`: new pure seven-entry contract.
- `gui/ambience-proof.html`: fixture proof.
- `gui/audio.mjs`: ambience catalog integration and active default selection.
- `tests/test_ambience_contract.py`: focused tests.
- `assets/registry/audio-assets.json`, `assets/ASSET_CREDITS.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `README.md`, `gui/README.md`, `CHANGELOG.md`, `LESSONS.md`, handoffs.
- `tests/test_release_metadata.py`, `Cargo.toml`, `Cargo.lock`.

## 6. Tests and checks

- `python3 -m unittest tests/test_ambience_contract.py tests/test_audio_cue_contract.py tests/test_gui_audio.py tests/test_asset_registry.py`
- `node --check gui/ambience-contract.mjs`
- `node --check gui/audio.mjs`
- `python3 scripts/validate_assets.py`
- `python3 scripts/generate_asset_credits.py --check`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `cargo fmt --check`
- `cargo test`
- `git diff --check`

## 7. Acceptance criteria

- Seven named settings are catalogued with all roadmap provenance, loop,
  loudness, speech/music/name exclusion, reduced-audio, equivalent, and
  fallback fields.
- Runtime audio exposes all seven recipes and keeps the regional city bed as
  the only default active ambience.
- Full/cues-only/mute/focus/unsupported paths never remove written information
  or create a hidden-state signal.
- Proof, tests, registry, credits, metadata, docs, and full checks pass.

## 8. Non-goals

- Do not add recorded/third-party audio, adaptive music, dynamic selection from
  hidden state, clinical alarms, real institution names, or spatial audio.
- Do not implement Phase 7.3 music stems or Phase 7.4 priority/fatigue manager.
- Do not change host/simulation/replay/debrief APIs or state.

## 9. Stop conditions

- Stop if an external asset/license or new dependency is required.
- Stop if a setting cannot be selected from an explicit visible context.
- Stop on unrelated test failures rather than expanding the slice.

## 10. Review checklist

- Seven entries cover the roadmap’s exact initial ambience targets.
- Every entry has deterministic filtered-noise recipe/loop/provenance and written fallback.
- The active default is visible context only and remains optional.
- Cues-only/mute/reduced-audio/focus behavior suppresses sound without losing
  text or events.
- No new registry hash or generated credit is stale.

## 11. Risk label

Risk: low

Reason: This is a local generated-recipe catalog and optional playback update;
it does not alter host, simulation, history, or replay authority.
