# Implementation Plan — Visual/audio Phase 7.1 UI and event cue refinement v0.12.70

## 1. Task restatement

Add a machine-checkable standards contract for all existing interface/event
audio cues, use the contract in the generated Web Audio client, and expose an
explicit cues-only mode while preserving visible-only sources and complete text
fallbacks.

## 2. Current understanding

- `gui/audio.mjs` already contains 16 cue IDs, cooldowns, visible sources,
  equivalents, generated recipes, mute, reduced notifications, and unsupported
  audio handling.
- It has no shared per-cue standards catalog and no explicit cues-only mode.
- The asset boundary already permits project-generated Web Audio recipes.

## 3. Assumptions

- Existing cue IDs and channels are public within the browser contract and must
  remain stable.
- A generated recipe metadata contract is sufficient for this technical slice;
  no recorded asset production is authorized.
- If a cue trigger would require hidden or true-state data, stop and retain the
  safe visible/text fallback instead of broadening the scope.

## 4. Minimal implementation plan

1. Add `gui/audio-cue-contract.mjs` with 16 cue definitions, shared standards,
   visible-source rules, safe equivalents, distinction labels, and contract
   lookup/validation helpers.
2. Update `gui/audio.mjs` to decorate existing cues from the contract, use the
   bounded normalization metadata, and add local `full`/`cues-only` mode state.
3. Add `gui/audio-cue-proof.html`, the `#audio-mode` control, focused tests, and
   registry/credits provenance for the generated contract.
4. Update roadmap, SPEC, architecture, README/GUI guidance, CHANGELOG, lessons,
   release metadata, and presentation QA artifacts.

## 5. Files and functions likely to change

- `gui/audio-cue-contract.mjs`: new pure cue standards catalog.
- `gui/audio.mjs`: cue decoration, normalization, mode state, and DOM control.
- `gui/index.html`: cues-only selector.
- `gui/audio-cue-proof.html`: fixture inspection page.
- `tests/test_audio_cue_contract.py`: new focused contract tests.
- `tests/test_release_metadata.py`: expected patch version.
- `assets/registry/audio-assets.json`, `assets/ASSET_CREDITS.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `README.md`, `gui/README.md`, `CHANGELOG.md`, `LESSONS.md`, and handoffs.
- `Cargo.toml`, `Cargo.lock`: patch version `0.12.70`.

## 6. Tests and checks

- `python3 -m unittest tests/test_audio_cue_contract.py tests/test_gui_audio.py tests/test_asset_registry.py`
- `node --check gui/audio-cue-contract.mjs`
- `node --check gui/audio.mjs`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/generate_asset_credits.py --check`
- `cargo fmt --check`
- `cargo test`
- `git diff --check`

## 7. Acceptance criteria

- All 16 existing cue IDs have semantic, timing, loudness, peak, cooldown,
  equivalent, distinction, source, and trigger-test metadata.
- Runtime cue entries expose the contract and use the shared bounded synthesis
  normalization without changing cue IDs or visible trigger rules.
- Cues-only suppresses only music/ambience; interface/event cues and written
  equivalents remain available. Mute and unavailable-audio fallbacks remain
  recoverable.
- Proof/tests cover each cue, visible-only forbidden markers, mode behavior,
  syntax, registry, and documentation.

## 8. Non-goals

- Do not add recorded audio, external models, third-party assets, spatial audio,
  dynamic music, or Phase 7.2–7.4 behavior.
- Do not alter host/simulation/replay APIs, state, formulas, or history.
- Do not claim measured loudness, fatigue, human usability, or musical quality.

## 9. Stop conditions

- Stop if a stable cue ID must be renamed or if any trigger requires hidden data.
- Stop if the implementation requires a new dependency or unrelated GUI rewrite.
- Stop on unrelated test failures rather than expanding the slice.

## 10. Review checklist

- Every cue maps to a visible source and written equivalent.
- Standards are metadata plus one shared playback rule, not duplicated formulas.
- Cues-only/mute/unavailable behavior keeps decision-relevant text complete.
- No audio metadata enters host payloads or deterministic state.
- Registry hash and generated credits match the new module.

## 11. Risk label

Risk: medium

Reason: The slice changes optional browser audio behavior and 16 cue contracts,
but does not change simulation or host authority.
