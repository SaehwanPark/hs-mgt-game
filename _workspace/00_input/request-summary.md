# Request Summary — Visual/audio Phase 6.1 motion specification v0.12.68

## Authorized outcome

Complete the Phase 6.1 motion specification checklist as a bounded policy and
proof slice without adding runtime animation or changing host authority.

## Slice boundary

- Define nine restrained motion categories: focus transition, report arrival,
  month transition, project progress, project completion, new visible rival
  action, status change, metric delta reveal, and relationship-line change.
- Document semantic purpose, duration, easing, reduced-motion replacement,
  interruption behavior, replay behavior/order, input behavior, simultaneous
  load, and declared frame-budget rules.
- Add deterministic replay/interruption planning and a fixture-only proof page.
- Test the local catalog’s declared performance budget without claiming baseline
  hardware, human usability, or production animation performance.
- Do not change Rust DTOs, simulation state, commands, transitions, stochastic
  inputs, history, hashes, replay authority, audio, or debrief behavior.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 6.1.
- `gui/motion-catalog.mjs` — pure motion policy and planning functions.
- `gui/motion-proof.html` — fixture proof.
- `gui/index.html` — existing reduced-motion and transition surface context.
- `docs/design_principles.md` — actor-visible boundaries and accessibility.

## Validation target

Focused motion-catalog, GUI, registry, credits, metadata, documentation-link,
full Python, full Rust, formatting, presentation-contract, performance-smoke,
and diff checks.

## Evidence limits

Static catalog/planning checks and local smoke timing establish technical policy
coverage only. They do not establish browser animation behavior, baseline
hardware performance, lived accessibility, usability, learning, calibration,
or policy validity.
