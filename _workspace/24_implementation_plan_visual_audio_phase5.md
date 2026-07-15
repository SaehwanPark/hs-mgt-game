# Implementation Plan — Visual and Audio Phase 5 Foundational Audio v0.12.21

Status: Implemented and ready for the single code-review pass.

## Task restatement

Implement one optional, browser-only audio layer for the existing competitive
action/resolution page. Map explicit UI outcomes and actor-visible committed
conditions to generated Web Audio music/cues, while preserving complete visual
and textual play, unchanged simulation/replay state, and no external asset or
network dependency.

## Current understanding

- Phase 0 already defines four music states and sixteen interface/event cue IDs,
  visible equivalents, and hidden-state exclusions.
- Phase 4 supplies the typed resolution envelope and the action client has
  explicit successful-submit, validation, and refresh boundaries.
- ADR-0011 permits optional browser Web Audio while keeping cue classification
  deterministic and outside the Rust core.
- No asset files or audio registry currently exist; generated recipes can make
  this first audio slice inspectable without introducing download/licensing
  infrastructure.

## Assumptions

- A generated oscillator/noise recipe is an acceptable first technical asset;
  registry and credits will explicitly record project-generated ownership and
  no third-party asset.
- Existing visible fields are enough for the Phase 0 music classifier; no new
  Rust DTO or hidden source is needed.
- Browser support is optional. A fake/recording sink can verify classifications
  and cue requests even when no audio context or browser binary is available.
- Audio settings are local presentation state; persistence and cross-device
  preferences are deferred.

If any assumption requires simulation fields, downloaded assets, or a broader
settings system, stop and report the mismatch before expanding scope.

## Minimal implementation plan

1. Add a pure `audio-catalog-v1` module with four music entries, sixteen cue
   entries, visible sources/equivalents, generated recipes, cooldowns, and
   channel metadata; add registry and credits records.
2. Add pure functions that classify music from explicit visible presentation or
   resolution envelopes and map explicit UI/visible event IDs to cue entries.
   Keep the classifier free of formulas beyond the approved visible pressure
   categories and include a recording-sink event shape.
3. Add a browser audio client that lazily creates `AudioContext` after a user
   gesture, starts/stops generated loops, plays short cues, throttles repeats,
   supports master/music/interface/event/ambience controls, mute, focus loss,
   reduced notifications, and unsupported fallback.
4. Integrate controls/status and visual equivalents into `gui/index.html`; wire
   existing action/resolution statuses to explicit cue IDs without changing
   command submission or resolution loading.
5. Add static/Python tests for catalog coverage, visible-only sources, registry
   completeness, mapping determinism, controls, mute/focus/reduced-notification
   behavior, cooldown markers, no-network/no-asset behavior, and JS syntax.
6. Update Phase 5 contract, SPEC/architecture/README/changelog/lessons,
   version metadata to `0.12.21`, evidence/domain QA/handoff records.
7. Run focused and full checks, perform exactly one code-review pass, push the
   branch, open a PR, wait for CI, merge into `main`, and record Phase 6 as the
   next gate.

## Files and functions likely to change

- `gui/audio.mjs`: catalog, visible-only classifiers, recording sink, generated
  recipes, and audio client.
- `gui/audio-catalog.json`, `gui/ASSET_CREDITS.md`: machine-readable registry
  and generated credits; no third-party audio files.
- `gui/app.mjs`: explicit cue/music calls from existing visible UI outcomes and
  resolution envelope; no simulation logic.
- `gui/index.html`, `gui/README.md`: semantic audio controls, status, visual
  equivalents, and adapter guidance.
- `tests/test_gui_audio.py`: static contract/source-boundary tests.
- Phase 5 docs, project records, metadata, lessons, QA, and handoff.

Avoid editing Rust transition, resolver, randomness, scenario, replay, or MCP
files. Do not add a network, bundler, audio package, downloaded asset, or
general settings framework. If a source gap appears, stop and document it.

## Tests and checks

Run:

- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest tests/test_gui_audio.py tests/test_gui_resolution.py tests/test_gui_contextual_actions.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `node --check gui/app.mjs`
- `node --check gui/audio.mjs`
- `python3 scripts/check_release_metadata.py`
- `git diff --check`

Expected result: classification and recording-sink tests pass, muted/unsupported
paths preserve complete visual/text behavior, and all existing Rust/replay/hash
tests remain green.

## Acceptance criteria

- The catalog contains all four music states and sixteen approved cues, each
  with visible source, equivalent, generated recipe, channel, and provenance.
- Music maps only visible presentation state; event/interface cues map only
  explicit visible outcomes, and repeated IDs are throttled.
- Controls independently affect master/music/interface/event/ambience channels;
  mute, focus loss, reduced notifications, and unsupported audio are explicit
  and non-fatal.
- Audio never gates text, resolution controls, command submission, or replay;
  no audio call mutates session/history/hash state.
- Registry and credits contain no untracked third-party asset and identify the
  generated source and license/ownership status.
- No hidden state, network, audio file, Rust simulation, or other campaign is
  introduced; no human comprehension/accessibility claim is made.

## Non-goals

- No audio files, remote asset service, downloaded assets, dynamic composition,
  spatial audio, pitch-only information, or professional sound-design claim.
- No Rust audio DTO, core playback, simulation cue history, or state/hash field.
- No broad settings persistence, campaign-general audio semantics, Phase 6 map,
  human evaluation, or AI-agent testplay campaign.

## Stop conditions

Stop and request direction if audio classification needs hidden/private fields,
the visual equivalent is incomplete, generated recipes are not acceptable as a
first asset boundary, browser controls require a framework/network, or playback
changes transition/replay behavior.

## Review checklist

- Catalog IDs and visible equivalents match Phase 0 exactly.
- Classifier inputs are visible-only and deterministic; no client outcome
  formula or private rival source appears.
- Audio starts only after gesture, all channels/mute/focus/reduced-notification
  controls are reachable by keyboard, and missing audio is recoverable.
- Recording sink proves cue IDs/source/equivalent without loading assets.
- Repeated cues are throttled; replay and muted play remain complete.
- Registry/credits are complete and no network/assets enter the diff.
- Exactly one code-review pass occurs and handoff records residual browser/human
  evidence limits.

## Risk label

Risk: medium-high. Audio is presentation-only, but hidden-state leakage,
fatigue, focus behavior, accessibility equivalence, and provenance require
domain and interface QA.
