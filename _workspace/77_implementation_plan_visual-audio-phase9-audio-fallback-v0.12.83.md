# Implementation Plan — Visual/audio Phase 9.2 audio playback fallback v0.12.83

## Task restatement

Implement a local, deterministic audio-fallback projection and runtime failure
boundary while preserving existing audio catalog, priority, mute, cues-only,
and visible/text behavior.

## Current understanding

- `gui/audio.mjs` owns generated Web Audio setup, cue scheduling, music,
  ambience, local status text, and the recording sink.
- `gui/asset-availability.mjs` already provides fail-closed normalization and
  release-path-clearing presentation descriptors.
- Existing audio entries already expose `visible_source` and `equivalent`;
  no recorded audio files are loaded.
- The main risk is an exception during context setup or `playTone` that can
  leave optional audio failure less explicit than the visual/text surface.

## Assumptions

- Existing audio catalog IDs and `createAudioClient` are the only runtime audio
  paths for this slice.
- `#audio-state` is the existing visible status region and can carry a concise
  fallback message.
- Local browser state is sufficient; no host response is needed to classify a
  playback failure.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Inspect the existing catalog lookup and `createAudioClient` failure paths;
   preserve the current queue, priority, and preference semantics.
2. Add a pure `audioPresentationFor` projection that uses the shared
   availability contract, preserves known cue/music/ambience source and
   written equivalent, and uses an explicit generic fallback for unknown IDs.
3. Route unsupported context creation and thrown cue/background playback
   through one bounded local fallback announcer that updates `#audio-state`,
   clears optional pending work where necessary, and records the fallback in
   the existing local recording sink without changing host data.
4. Add focused Python/Node tests with a fake context that fails setup, throws
   during oscillator creation, and records a successful cue; assert fallback
   descriptors, status text, queue recovery, and authority-boundary markers.
5. Update versioned documentation, CI focused tests, roadmap evidence, and
   lessons; run the complete validation matrix.

## Files and functions likely to change

- `gui/audio.mjs`: catalog-specific fallback projection, local failure
  announcer, and guarded setup/playback paths.
- `tests/test_audio_fallback.py`: pure projection and fake-context failure
  tests.
- `.github/workflows/ci.yml`: focused audio fallback test invocation.
- `_workspace/00_input/request-summary.md`: current slice framing.
- `_workspace/02_presentation_contract.md`: actor-visible audio contract.
- `_workspace/03_presentation_qa.md`: QA evidence and limits.
- `docs/visual_audio_enhancement_roadmap.md`: v0.12.83 target/evidence.
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `CHANGELOG.md`, `LESSONS.md`:
  version and boundary records.

Avoid editing files outside this list unless the plan is incomplete; if that
happens, stop and explain why.

## Tests and checks

- `python3 -m unittest tests.test_audio_fallback tests.test_gui_audio`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate_assets.py`
- `python3 scripts/validate_asset_security.py`
- `python3 scripts/verify_asset_release.py --check`
- `python3 scripts/generate_asset_credits.py --check`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `node --check gui/audio.mjs`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`
- `git diff --check`

Expected result: all focused and existing checks pass with no asset or
simulation-authority change.

## Acceptance criteria

- `audioPresentationFor` maps loaded, missing, failed, malformed,
  contradictory, and unknown availability results to explicit output; known
  entries preserve their source and written equivalent and unavailable output
  clears any release path.
- Unsupported audio setup and thrown playback return recoverable results,
  expose visible fallback status text, and leave visual/text operation intact.
- A successful fake context retains existing queue/recording behavior.
- No new asset, network call, host field, command, transition, observation,
  history, hash, replay, or debrief data is introduced.
- Versioned docs and QA accurately state technical evidence and human-review
  limits.

## Non-goals

- Do not add recorded audio, decode files, fetch assets, or add dependencies.
- Do not redesign audio priority, music classification, ambience selection,
  host APIs, or simulation mechanics.
- Do not alter pending portrait approval, registries, release manifests, or
  legal/provenance status.
- Do not perform opportunistic cleanup or unrelated formatting.

## Stop conditions

Stop and report if the change requires a host/API schema change, more than two
production runtime files, a new dependency, a catalog redesign, or changes to
simulation/history/replay/debrief authority. Report unrelated test failures
separately rather than broadening the slice.

## Review checklist

- The diff implements only local audio failure recovery.
- Known catalog entries retain visible source and written equivalents.
- Failure handling is fail-closed and does not overstate playback or browser
  compatibility.
- Fake-context tests cover both setup and playback failure without fixture-only
  assumptions.
- Existing mute, cues-only, queue, priority, and recorder behavior remains.
- Exactly one read-only code reviewer will inspect the final worktree before
  PR merge.

## Risk label

Risk: medium

Reason: the change touches the shared audio runtime and asynchronous playback
queue, but remains local, presentation-only, and preserves the existing public
catalog and host boundary.

## Review disposition

The one designated code reviewer approved the final worktree with no actionable
findings after unknown catalog IDs were made fail-closed, successful cue retry
cleared stale fallback status, and the roadmap/QA evidence was updated.
