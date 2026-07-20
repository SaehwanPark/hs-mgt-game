# Visual/audio Phase 6.1 — Motion specification v0.12.68

## Outcome

The project now has a deterministic motion policy for focus transition, report
arrival, month transition, project progress/completion, new visible rival
action, status change, metric delta reveal, and relationship-line change. Each
category documents timing, reduced-motion replacement, interruption, replay,
input, simultaneous-load, and a declared frame budget. The fixture proof
demonstrates planning without starting animation or timers.

## Boundary

Motion remains local presentation guidance. The catalog does not load a host,
submit commands, consume hidden state, change DTOs, resolve simulation or
stochastic inputs, rewrite history or hashes, own replay authority, or create
audio/debrief facts. Reduced motion and interruption retain the written
information.

## Evidence

- `gui/motion-catalog.mjs`
- `gui/motion-proof.html`
- `tests/test_motion_catalog.py`
- `assets/registry/visual-assets.json`
- `docs/visual_audio_enhancement_roadmap.md`

Static verification records technical policy coverage and a local budget smoke
test only; it does not establish browser animation behavior, baseline hardware
performance, lived accessibility, usability, learning, calibration, or policy
validity.
