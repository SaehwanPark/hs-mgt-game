# Implementation Plan — Visual/audio Phase 11.2 audio packaging review v0.13.1

## Task restatement

Add a deterministic, dependency-free audio packaging-scope report that proves
the current release contains no file-backed audio and records compression as
not applicable to runtime-generated Web Audio recipes, while preserving all
existing playback and authority boundaries.

## Current understanding

- `assets/release` contains 15 SVG files and no audio directory/files.
- `assets/registry/audio-assets.json`, `gui/audio-catalog.json`, and the live
  audio modules describe generated recipes with no release paths.
- Phase 11.2 leaves `Audio compression reviewed` unchecked while prior slices
  explicitly keep audio packaging open.
- The target is a release-governance check, not a runtime audio change.

## Assumptions

- The current release scope intentionally contains zero file-backed audio.
- Known audio suffixes are sufficient to detect an accidental file-backed
  release asset for this bounded scope.
- The release root remains `assets/release` and paths are repository-relative.

If any assumption is false, stop and report the mismatch before implementing
the checker or closing the roadmap item.

## Minimal implementation plan

1. Add `assets/audio-packaging-scope.json` with the schema, release-root,
   known audio suffixes, zero-file/zero-byte limits, runtime-generated source
   modules, and explicit compression decision.
2. Add `scripts/check_audio_packaging.py` to validate safe paths and schema,
   scan the release tree, verify the current audio registries have null release
   paths, and emit a deterministic `audio-packaging-report-v1` JSON report.
3. Add focused tests for the green report/CLI, unexpected release audio,
   malformed definitions, path escapes, and non-null registry/catalog release
   paths.
4. Update the roadmap, `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `LESSONS.md`,
   `CHANGELOG.md`, generated metadata/version projections, and the durable
   handoff/QA records.
5. Run focused Python tests, Rust formatting/tests, asset/release checks, and
   the visual/audio contract audit; stop if the change reaches browser
   playback, simulation authority, or actual codec work.

## Files and functions likely to change

- `assets/audio-packaging-scope.json`: current package boundary and limits.
- `scripts/check_audio_packaging.py`: definition validation, release scan,
  registry checks, and report generation.
- `tests/test_audio_packaging.py`: focused contract and failure coverage.
- `assets/README.md`: usage and evidence boundary.
- `docs/visual_audio_enhancement_roadmap.md`: close only audio compression
  review with v0.13.1 evidence.
- `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `LESSONS.md`, `CHANGELOG.md`,
  `Cargo.toml`, `Cargo.lock`, `gui/asset-credits.mjs`, asset credits/notices,
  and release metadata: version and current-slice records.

Avoid editing live audio or simulation files unless a test proves the stated
registry boundary cannot be checked at the packaging boundary.

## Tests and checks

- `python3 -m unittest tests.test_audio_packaging`
- `python3 scripts/check_audio_packaging.py`
- `cargo fmt --check`
- `cargo test`
- `python3 scripts/check_asset_budget.py`
- `python3 scripts/check_raster_scope.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/audit_visual_audio_contract.py`

Expected result: all focused and repository checks pass; the audio report
contains zero release audio files and zero release audio bytes.

## Acceptance criteria

- The current report is deterministic, passes, and says compression is not
  applicable because all current audio is runtime-generated.
- Any known audio file under `assets/release` fails the checker.
- Registry and GUI catalog entries remain explicit about null release paths.
- The checker cannot read outside the repository through configured paths.
- No command, transition, stochastic input, history/hash/replay, debrief, or
  live playback behavior changes.
- Phase 11.2 marks only `Audio compression reviewed` complete; later packaging,
  device, compatibility, screenshot, and human gates stay open.

## Non-goals

- Do not add or compress audio.
- Do not add dependencies or a codec abstraction.
- Do not implement lazy loading, preloading, offline support, or device tests.
- Do not claim runtime performance or human-quality evidence.
- Do not perform unrelated formatting or cleanup.

## Stop conditions

Stop and report if a file-backed audio asset is already present, the registries
use incompatible release-path schemas, more than the planned packaging/docs
files need production edits, or the implementation requires changing browser
playback or host authority.

## Review checklist

- The diff closes only the selected roadmap item.
- Scope and registry checks are fail-closed and path-safe.
- Tests cover green and representative negative cases.
- Runtime-generated audio remains optional with written fallbacks.
- No release/preview or simulation claims are overstated.
- Version, docs, changelog, and handoff evidence agree.

## Risk label

Risk: low

Reason: This is a read-only package-governance check over an existing empty
release audio surface with no runtime or public simulation behavior change.
