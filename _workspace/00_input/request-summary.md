# Request Summary — Visual/audio Phase 8.2 review-ready portrait approval worksheet v0.12.77

## Authorized outcome

Prepare a review-ready, per-role approval worksheet for the seven fictional
actor portrait previews. Make every human-review gate explicit and hash-bound
without claiming that an AI inspection is human approval or promoting any
preview into runtime/release.

## Target slice

- Add `assets/generation/portrait-review-queue.json` with exactly one review
  packet for each canonical portrait role.
- Bind every packet to the matching preview asset ID, role-derived source path,
  source hash, accessible equivalent, generic fallback, and pending metadata.
- Record separate identity-only, role-consistency, resemblance/marks,
  artifact, small-size, grayscale, accessibility, provenance, derivative, and
  registry gates with reviewer identity/date/notes left null until a human
  reviewer completes them.
- Add a static proof and focused tests that expose per-role review state,
  disabled/fallback behavior, and fail-closed approval rules without network,
  host, or runtime access.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 8.2.
- `assets/generation/portrait-set.json` and `portrait-previews.json`.
- `scripts/validate_generation_metadata.py` and Phase 8.1 review checklist.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add registry/release entries, or populate
  the generation manifest.
- Do not infer human resemblance, accessibility, legal clearance, quality,
  learning, clinical plausibility, or policy validity from automated checks.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Review-queue schema and hash/path checks, malformed queue and attempted
promotion tests, static proof checks, existing generation/asset/credits/release/
documentation checks, full Python/Rust tests, formatting, Clippy, JavaScript,
and diff checks.

## Evidence limits

The worksheet makes human review actionable and auditable but does not perform
that review. Approved local model/seed provenance, human decisions, release
derivatives, and registry bridges remain explicit external gates.
