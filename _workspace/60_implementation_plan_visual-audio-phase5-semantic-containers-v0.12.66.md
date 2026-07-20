# Implementation Plan — Visual/audio Phase 5.1 semantic containers v0.12.66

## Objective

Complete Milestone 5.1 of `docs/visual_audio_enhancement_roadmap.md` as one
bounded presentation slice. The implementation must differentiate eight
information classes without changing host, simulation, stochastic, history,
replay, audio, or debrief authority.

## Work units

1. Define `gui/semantic-containers.mjs` as a deterministic catalog with one
   complete contract for each target container plus a generic fallback.
2. Apply the catalog’s restrained classes and non-color markers to the existing
   panels in `gui/index.html`, retaining their current text and source/status
   language.
3. Add `gui/semantic-container-proof.html` for compact/expanded, responsive,
   print, and reduced-motion inspection.
4. Add focused tests and registry/credits provenance.
5. Update roadmap, SPEC, ARCHITECTURE, CHANGELOG, README, GUI reference,
   lessons, and SDD handoff artifacts.
6. Run focused and full verification, perform one light code review, and merge
   the feature branch to `main` before selecting the next slice.

## Completion gate

- All ten checklist dimensions are evidenced for all eight containers.
- Existing actor-visible text and status/source boundaries remain available.
- No hidden state or new host authority is consumed.
- Registry, credits, metadata, documentation, tests, formatting, and diff checks
  pass.
