# Request Summary — Visual/audio Phase 9.2 release reproducibility v0.12.81

## Authorized outcome

Add a dependency-free metadata audit and deterministic release-manifest check
for the visual/audio asset paths in scope, without adding external assets or
mutating contributor files.

## Target slice

- Add `scripts/verify_asset_release.py` to derive a sorted release manifest
  from approved registry release paths, including byte size, SHA-256, and a
  canonical manifest digest.
- Add metadata checks to the dependency-free asset security gate for raster
  text/EXIF/comment chunks and audio metadata markers, with explicit source
  versus release scope and no asset rewriting.
- Add a committed manifest projection and stale-output/reproducibility tests;
  wire the check into CI and contributor/release guidance.
- Keep all current assets unchanged and keep pending portraits outside runtime
  and release authority.

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

Metadata audit, deterministic release-manifest generation/check, registry and
release hash checks, focused malformed-metadata fixtures, existing security/
generation/credits/release/documentation checks, full Python/Rust tests,
formatting, Clippy, JavaScript, and diff checks.

## Evidence limits

The audit and manifest establish bounded metadata and reproducibility evidence
only; they do not sanitize or rewrite files, prove legal clearance, establish
human accessibility, validate audio quality, or replace human review. Portrait
human decisions, approved local model/seed provenance, release derivatives,
and registry bridges remain explicit external gates.
