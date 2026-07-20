# Visual/audio Phase 1.3 — Audio policy prototype

Status: Complete in v0.12.38.

## Outcome

Closed the remaining Phase 1.3 checklist items on top of the v0.12.37 recipe
board. The fixture policy now implements deterministic priority order,
high-priority music-ducking metadata, per-entry repeat-cue cooldowns,
full-audio/cues-only/muted modes, complete text-equivalent results, and a
reduced-audio preference that suppresses music and ambience only.

The proof page exposes these controls without loading the host or changing a
session. The live `gui/audio.mjs` client remains unchanged.

## Verification and limits

- Focused policy, fallback, loop, source, and syntax tests pass.
- Full Python, Rust, Clippy, formatting, asset/credits, metadata,
  documentation-link, Node, and diff checks pass.
- Deterministic policy tests are technical evidence only; they do not establish
  human listening, calibrated loudness, accessibility experience, learning,
  engagement, balance, or policy validity.
