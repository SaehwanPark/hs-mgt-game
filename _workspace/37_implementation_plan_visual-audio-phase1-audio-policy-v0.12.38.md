# Implementation Plan — Phase 1.3 audio policy prototype v0.12.38

## Objective

Close the remaining Phase 1.3 policy behavior with a deterministic fixture
policy attached to the audio-direction preview.

## Scope

- Add explicit event/interface/music/ambience priority ordering.
- Add high-priority music-ducking metadata.
- Add per-entry repeat-cue cooldown decisions.
- Add full-audio, cues-only, and muted modes.
- Add reduced-audio preference filtering while retaining text equivalents.
- Keep the live audio client and host/simulation contracts unchanged.

## Acceptance criteria

- A report event outranks interface, music, and ambience entries.
- Repeated cues are throttled until their declared cooldown expires.
- Modes return visual-only decisions for filtered channels.
- Reduced audio suppresses music/ambience without removing visible meaning.
- Every policy result retains the entry's visible source/equivalent.
- Phase 1.3 roadmap checklist, SPEC, architecture, changelog, registry, and
  workspace handoffs align to v0.12.38.

## Verification

- `python3 -m unittest tests.test_audio_direction`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
