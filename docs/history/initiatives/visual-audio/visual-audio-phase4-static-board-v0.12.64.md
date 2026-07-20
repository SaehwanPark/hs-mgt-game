# Visual/audio Phase 4.1 static regional board — v0.12.64

## Decision

Promote the existing typed actor-visible regional-world projection into the
first production-shaped board surface through a pure local scene adapter and
deterministic SVG mount.

## Scope

`gui/regional-board.mjs` maps `competitive-regional-world-v1` entities,
facilities, overlays, source labels, statuses, layout slots, and missingness to
the established `scene.mjs` vocabulary. `gui/app.mjs` mounts that scene beside
the existing semantic map/detail list and keeps report, institution, and
facility focus local and synchronized. `gui/regional-board-proof.html` and the
static SVG hash fixture provide a host-free demonstration.

## Authority boundary

The adapter accepts actor-visible DTO/fixture values only. It does not call a
host, submit commands, mutate simulation state, resolve stochastic inputs,
write history, alter hashes/replay, or create audio/debrief facts. Unknown
identities and facility kinds use generic tokens; missingness is written rather
than inferred.

## Verification

Focused adapter/SVG tests, existing GUI tests, asset registry and credits
checks, metadata, syntax, documentation links, full Python, full Rust,
formatting, presentation-contract, and diff checks passed for the merged
v0.12.64 slice. Evidence remains technical and does not establish human
usability, lived accessibility, learning, calibration, contrast, or policy
validity.

## Follow-up

Phase 4.2 owns report/entity consequence linkage beyond local focus,
project-state transitions, rival observability timing, historical/replay visual
sequencing, and first-month integration coverage.
