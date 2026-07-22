# Request Summary — Visual/audio Phase 9.2 graceful asset fallback v0.12.82

## Authorized outcome

Add a deterministic presentation-only asset-availability/fallback contract so
missing or failed optional visual assets preserve visible meaning without
breaking the GUI or introducing a second source of simulation state.

## Target slice

- Add `gui/asset-availability.mjs` with pure loaded/fallback/unavailable
  projections for caller-supplied local asset-load results.
- Add facility and identity presentation adapters plus a keyboard-visible
  proof showing loaded and fallback states, preserving labels, written
  equivalents, generic markers, and release-path status.
- Add no-network/no-host/no-hidden-state tests for missing, failed, malformed,
  and successful availability results; keep all current assets unchanged.
- Keep pending portraits outside runtime and release authority.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 9.2.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `assets/source/`, `assets/release/`, and preserved generation previews.
- `scripts/validate_assets.py` and current release guidance.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Fallback contract/proof/tests, existing asset security/manifest/registry/
generation/credits/release/documentation checks, full Python/Rust tests,
formatting, Clippy, JavaScript, and diff checks.

## Evidence limits

The fallback contract establishes presentation recovery behavior only; it does
not load assets, prove legal clearance, establish human accessibility, validate
asset quality, or replace human review. Portrait human decisions, approved
local model/seed provenance, release derivatives, and registry bridges remain
explicit external gates.
