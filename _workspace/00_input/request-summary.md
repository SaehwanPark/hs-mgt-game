# Request Summary — Visual/audio Phase 10.1 first-month slice v0.12.86

## Authorized outcome

Add a machine-checkable acceptance contract for the integrated first-month
`competitive-regional-v1` visual/audio path while preserving host authority,
deterministic replay, actor-visible information boundaries, and explicit Phase
10.2 human-evaluation limits.

## Target slice

- Add `tests/test_phase10_first_month.py` with exact Phase 10.1 checklist
  coverage, live GUI/source markers, no-authority checks, and deterministic
  first-month/music/skip probes.
- Reconcile the Phase 10.1 technical checklist and record the integration
  evidence without adding a duplicate runtime path or new asset.
- Keep Phase 10.2 first-time-user, accessibility-quality, audio-fatigue, and
  educational-usability evaluation as explicit human gates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 10.1 and the v0.12.86
  first-month technical-evidence target slice.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `gui/app.mjs`, `gui/index.html`, `gui/first-month.mjs`,
  `gui/resolution-sequence.mjs`, `gui/music-stem-contract.mjs`, current GUI
  tests, and the Rust host/replay contracts.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not claim first-time-user comprehension, accessibility quality, audio
  usefulness/fatigue, educational usability, legal clearance, or portrait
  approval.
- Do not add assets, dependencies, host fields, simulation rules, hidden-state
  projections, registry/release changes, or a duplicate runtime path.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Phase 10.1 integration tests, existing GUI/host/replay/audio tests, full
Python/Rust tests, asset/security/release/credits/version/documentation checks,
formatting, Clippy, JavaScript, and diff checks.

## Evidence limits

The slice establishes technical integration and deterministic boundary checks
only; it does not establish first-time-user comprehension, accessibility
quality, audio usefulness/fatigue, educational usability, legal clearance,
ownership, or human review. Phase 10.2 remains an explicit external gate.
