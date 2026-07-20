# Implementation Plan — Visual/audio Phase 6.1 motion specification v0.12.68

## Objective

Complete Milestone 6.1 of `docs/visual_audio_enhancement_roadmap.md` as one
bounded motion-policy slice. Motion must remain supplementary to text and
actor-visible state and must not become a client transition authority.

## Work units

1. Define `gui/motion-catalog.mjs` for nine categories with semantic purpose,
   duration/easing, reduced-motion replacement, interruption, replay order,
   input, simultaneous-load, and declared frame-budget rules.
2. Add deterministic replay/interruption/load planning functions without
   timers, DOM mutation, host calls, or simulation data.
3. Add fixture-only `gui/motion-proof.html` with reduced-motion, interruption,
   replay-order, responsive, print, and local budget smoke inspection.
4. Add focused tests and registry/credits provenance.
5. Update roadmap, SPEC, ARCHITECTURE, CHANGELOG, README, GUI reference,
   lessons, and SDD handoff artifacts.
6. Run focused and full verification, perform one light code review, and merge
   the feature branch to `main` before selecting the next slice.

## Completion gate

- All nine checklist dimensions are evidenced.
- Reduced-motion and interruption preserve written information.
- Replay planning is deterministic and host-independent.
- Registry, credits, metadata, documentation, tests, formatting, performance
  smoke, and diff checks pass.
