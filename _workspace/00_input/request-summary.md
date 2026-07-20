# Request Summary — Visual/audio Phase 3.2 event markers v0.12.62

## Authorized outcome

Complete the remaining deterministic, fixture-only Phase 3.2 regional map-kit
lane with event-marker vocabulary and an inspectable interaction proof.

## Slice boundary

- Add symbolic event markers with stable IDs, written equivalents, explicit
  visible-source boundaries, no severity or outcome inference, and a generic
  fallback.
- Add a fixture proof for the shared map vocabulary at compact, standard, and
  wide target resolutions.
- Define and test keyboard order, bounded zoom, and bounded pan behavior.
- Record the symbolic-geography disclaimer and register the new catalog with
  provenance and a deterministic source hash.
- Keep live GUI promotion, host/session behavior, simulation state, commands,
  transitions, stochastic inputs, history, hashes, replay, and audio out of
  scope.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 3.2.
- `docs/design_principles.md` — presentation authority and accessibility.
- `gui/map-environment.mjs`, `gui/map-tiles.mjs`, `gui/map-districts.mjs`,
  `gui/map-parcels.mjs`, `gui/map-relationships.mjs`,
  `gui/map-service-areas.mjs`, and `gui/map-uncertainty.mjs`.
- Existing Phase 3.2 focused tests and asset-registry validators.

## Validation target

Focused event-marker, map-proof, registry, credits, and JavaScript syntax tests;
then the repository Rust, Python, asset, metadata, documentation-link, and
diff checks required by the handoff.

## Evidence limits

Static fixture checks establish deterministic contracts and fallback coverage.
They do not establish human design quality, contrast, lived accessibility,
learning, calibration, policy validity, or live-board usability.
