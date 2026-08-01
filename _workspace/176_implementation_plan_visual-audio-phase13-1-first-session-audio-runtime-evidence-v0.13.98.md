# Implementation Plan — First-session/audio runtime-boundary evidence v0.13.98

## Task restatement

Record and validate a bounded live-GUI observation of the competitive
first-session rail and presentation/audio fallback states. Preserve the
existing host authority, settings behavior, written equivalents, audio policy,
and all pending human/listening/release gates.

## Current understanding

- The live loopback GUI can start a fresh competitive session and expose the
  seven-stage first-session rail, actor-visible briefing, current observation,
  and written history/debrief placeholders.
- The settings surface exposes low-distraction mode, reduced motion, optional
  cue explanations, and Large text. Low-distraction mode intentionally forces
  reduced motion, Large text, written cue explanations, muted audio, and
  reduced notifications.
- The audio surface exposes Full/Cues-only mode, mute, reduced notifications,
  channel controls, and a written equivalent. The audio explanation is an
  optional cue explanation and is hidden only when optional cue explanations
  are intentionally disabled; the settings summary and written results remain.
- Existing packets prepare first-session/audio human evaluation but do not
  record a current host-backed browser observation of these states.

## Assumptions

- The observation is technical runtime evidence, not participant evidence,
  listening feedback, accessibility review, educational evidence, or release
  approval.
- Only an opaque host session ID and actor-visible text/state are recorded; no
  private state, browser history, identity, or raw media is captured.
- No browser permission, audio device, external service, or new dependency is
  needed. If playback permission or an unavailable decoder is encountered,
  record the fallback rather than claiming playback.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Add a source-bound evidence packet for the observed Chrome 150 loopback
   first-session start, seven visible rail stages, actor-visible observation,
   low-distraction/reduced-motion/Large-text state, cues-only/muted states, and
   written-equivalent presence.
2. Add a dependency-free validator with strict schema, loopback, engine/version,
   host/session, rail-stage, settings, audio-state, source-marker, and pending
   human/listening/release-boundary checks.
3. Add focused tests for valid evidence, missing rail stages, hidden written
   equivalents, false audio-playback claims, browser/URL drift, type coercion,
   source-marker drift, and support/release promotion.
4. Update the roadmap, SPEC, changelog, README/package metadata, lessons,
   request summary, presentation contract, domain/presentation QA, and final
   handoff; bump the package from `0.13.97` to `0.13.98` and regenerate only
   version-derived credit artifacts.
5. Run focused, full Python, serial Rust, formatting, Clippy, metadata,
   asset/release, browser/device, remaining-gate, and diff checks.

## Files and functions likely to change

- `docs/evaluation/phase13.1-first-session-audio-runtime-evidence.json`: new
  current technical observation.
- `scripts/validate_first_session_audio_runtime_evidence.py`: new strict,
  dependency-free validator.
- `tests/test_phase13_1_first_session_audio_runtime_evidence.py`: packet,
  validator, privacy, fallback, and promotion regressions.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`,
  `tests/test_release_metadata.py`, and generated credits/notices: version
  metadata only.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `LESSONS.md`, and
  `_workspace` request/contract/QA/handoff files: evidence-state updates.

Avoid editing GUI/runtime source unless a validator or test proves an actual
presentation defect. If the source behavior differs from this plan, stop and
report the mismatch instead of improvising.

## Public contract and compatibility effects

- Additive evidence schema only; no GUI, Rust, simulation, host, audio,
  persistence, asset, browser-policy, device-policy, or public API change.
- The packet must retain explicit false/pending fields for first-time-user,
  accessibility, educational, audio-listening, browser/device, provenance,
  expansion, and public-release decisions.
- Audio controls and written-equivalent behavior remain existing contracts;
  this slice records them and does not promote audio support or quality.

## Tests and checks

```text
python3 -m unittest tests.test_phase13_1_first_session_audio_runtime_evidence
python3 scripts/validate_first_session_audio_runtime_evidence.py
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/check_release_metadata.py
python3 scripts/validate_assets.py
python3 scripts/verify_asset_release.py --check
python3 scripts/check_browser_compatibility.py
python3 scripts/check_device_performance.py
python3 scripts/validate_remaining_gate_technical_audit.py
git diff --check
```

Expected result: all checks pass while first-session human evaluation, audio
listening feedback, and public-release decisions remain pending.

## Acceptance criteria

- The packet records a current Chrome 150 host-backed first-session start and
  all seven visible rail stages without hidden state or participant data.
- The packet distinguishes low-distraction forced settings from independent
  reduced-motion/Large-text/cue-explanation settings.
- The packet records cues-only and muted status language plus a visible written
  equivalent, without claiming audio playback or quality.
- The validator rejects missing stages, hidden equivalents, false playback or
  human claims, browser/URL drift, source drift, type coercion, and promotion.
- Version/docs/release metadata consistently identify v0.13.98.

## Non-goals

- Do not enable browser audio, collect listening ratings, run participant
  interviews, or infer accessibility, educational, fatigue, or comprehension
  results.
- Do not change the GUI, audio engine, host commands, simulation mechanics,
  asset registry, support policy, or release manifest semantics.
- Do not claim Firefox/WebKit, real-device, decoder, battery, or hardware
  certification.

## Stop conditions

Stop and ask for review if the slice requires a browser permission change,
external upload, new dependency, public API change, runtime-source edit, or
any evidence not directly observed in the local GUI.

## Handoff requirements

Implement exactly this plan. Do not broaden scope. Report changed files, tests,
deviations, unresolved risks, and the remaining human/listening gates. Before
merge, obtain exactly one medium-effort code review and resolve every finding.

## Risk label

Risk: medium

Reason: the slice is additive and fail-closed, but it records accessibility and
audio presentation boundaries where technical smoke must not be mistaken for
lived human or playback-quality evidence.
