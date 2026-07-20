# Request Summary — Visual/audio Phase 3.3 operational overlays v0.12.63

## Authorized outcome

Complete the Phase 3.3 operational overlay library as a deterministic,
fixture-only, data-driven catalog for the twelve required visible overlay
categories.

## Slice boundary

- Add staffing, capacity, demand, project, payer/network, regulatory,
  community-trust, financial, operational-recovery, and uncertain/stale
  intelligence overlay contracts.
- Document the actor-visible triggering field, semantic role, non-color pattern,
  text equivalent, reduced-motion behavior, collision behavior, deterministic
  display priority, and generic fallback for every overlay.
- Add deterministic sorting, bounded collision/overflow layout, simultaneous
  overlay proof, registry/hash/credits coverage, and focused tests.
- Keep live board promotion, host/session DTO changes, simulation transitions,
  stochastic inputs, commands, history, hashes, replay, audio, and debriefs out
  of scope.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 3.3.
- `docs/design_principles.md` — actor-visible presentation and accessibility.
- `src/mcp/presentation.rs` and `src/mcp/regional_world.rs` — existing visible
  field names and observation boundaries.
- `gui/visual.mjs` and existing Phase 3.2 catalogs — local token conventions.

## Validation target

Focused operational-overlay, collision, registry, credits, and syntax tests;
then full Rust/Python, asset, metadata, documentation-link, and diff checks.

## Evidence limits

Static fixture checks establish deterministic vocabulary, fallback, and layout
contracts. They do not establish human design quality, contrast, lived
accessibility, learning, calibration, policy validity, or live-board usability.
