# Implementation Plan — Phase 10.2 audio preference/listening review packet v0.13.86

## Target slice

Prepare a source-bound, participant-ready technical review packet for the open
Phase 10.2 audio gates. The packet will make authorized listening and audio
preference evaluation actionable without recording participant results,
claiming audio usefulness or fatigue outcomes, or converting human evidence
into a release decision.

This slice is documentation/evaluation infrastructure only. It does not change
the Rust simulation, browser authority, audio runtime, generated audio
recipes, asset registry, or release assets.

## Source and authority boundary

Use the existing contracts and preparation records as the only technical
authority:

- `docs/evaluation/phase10.2-evaluation-protocol.json` for the canonical audio
  task, rating dimensions, privacy limits, and pending decision record.
- `docs/evaluation/phase13.2-pilot-feedback-instrument.json` for the bounded
  anonymized pilot response shape and audio-choice task.
- `docs/guides/phase10.2-structured-evaluation.md` for facilitator setup,
  consent, accommodation, and recording boundaries.
- `docs/guides/gui-how-to-play.md` for player-visible audio settings and
  written-equivalent guidance.
- `gui/audio-cue-contract.mjs`, `gui/music-stem-contract.mjs`,
  `gui/ambience-contract.mjs`, `gui/audio-priority-contract.mjs`, and
  `gui/audio.mjs` for cue/music/ambience semantics, preference modes,
  priority/queue limits, fallback behavior, and visible-only triggers.
- `gui/index.html` and `gui/app.mjs` for the audio controls, status region,
  written-equivalent copy, keyboard/focus behavior, and low-distraction
  integration.
- Existing audio tests and registry/credits for executable contract evidence.

The packet must state that the Rust host remains authoritative for all game
state and visible event inputs; audio is optional presentation; browser-local
preferences do not mutate simulation state; and unavailable, muted, or
reduced audio must retain visible and written meaning.

## Deliverables

1. Add `docs/evaluation/phase10.2-audio-preference-review-packet.json` with:
   - exact source paths and source markers;
   - the full audio task path: full audio, cues-only, mute/audio-off, reduced
     notifications, unavailable audio, focus loss, and written equivalents;
   - contract-level coverage for music, ambience, interface/event cues,
     priority/queue bounds, and visible-only trigger sources;
   - technical observations and acceptance checks separated from human
     listening/comprehension questions;
   - anonymized response fields matching the existing pilot instrument;
   - explicit pending fields for participant results, ratings, interviews,
     revision decisions, go/no-go, and release approval.
2. Add a fail-closed Python validator covering exact protocol/instrument
   parity, source-marker presence, audio catalog and contract coverage,
   fallback/written-equivalent boundaries, privacy limits, and non-release
   status.
3. Update the roadmap, `SPEC.md`, request/presentation/domain-QA records,
   final handoff, `LESSONS.md`, `CHANGELOG.md`, README/Cargo version metadata,
   and generated asset-credit metadata to v0.13.86.

## Explicit non-goals

- Do not collect or invent participant audio ratings, comments, interviews, or
  go/no-go results.
- Do not claim loudness, fatigue, intelligibility, accessibility, educational
  value, or cross-device/browser quality from static/source checks.
- Do not add audio files, change generated synthesis, or promote any asset to
  release status.
- Do not expose hidden simulation state, private actor data, resolved inputs,
  or browser-owned transitions.

## Verification

- Focused packet validator, existing audio fallback/priority/contract tests,
  and Node syntax checks.
- Full Python test discovery, `cargo fmt --check`, `cargo clippy --all-targets
  -- -D warnings`, and serialized `cargo test`.
- Release metadata, documentation-link, asset-credit, provenance/security,
  offline/browser/device, and visual/audio contract gates.
- Exactly one medium-effort code review; fix actionable findings and obtain a
  clean recheck before PR handoff.

## Acceptance criteria

- The packet is technically complete and source-bound.
- Every claimed audio behavior has an executable or exact source marker.
- Human evidence fields remain pending/null and no release approval is
  inferred.
- The roadmap marks the technical packet prepared while leaving the Phase 10.2
  human audio gates open.
- Version metadata is consistently `0.13.86`.
