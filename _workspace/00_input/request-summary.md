# Request Summary — Visual/audio Phase 9.2 SVG metadata sanitizer v0.12.84

## Authorized outcome

Add a deterministic release-boundary SVG metadata sanitizer that can produce an
explicit derivative while leaving canonical registry-controlled assets and
runtime presentation unchanged.

## Target slice

- Add `scripts/sanitize_svg_metadata.py` with a deterministic bytes transform
  that removes SVG `<metadata>` elements while preserving title/description
  accessibility content and all other markup.
- Add an explicit output mode for contributor-created derivatives plus a
  read-only `--check-release` mode that verifies approved release SVGs are
  already sanitized without rewriting registry-controlled files.
- Add fixture tests for metadata removal, title/description preservation,
  malformed/unbalanced input, and release-root/path boundaries.
- Keep audio metadata audit behavior, pending portraits, and runtime assets
  unchanged.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 9.2 and the v0.12.84
  SVG-sanitization target slice.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `scripts/verify_asset_release.py`, `scripts/validate_asset_security.py`,
  release guidance, and current asset tests.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not rewrite canonical release/source assets, registry hashes, or manifests
  in the check path.
- Do not sanitize raster/audio metadata or redesign asset validation.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Sanitizer/fixture tests, release-root check, existing asset security/manifest/
registry/generation/credits/release/documentation checks, full Python/Rust
tests, formatting, Clippy, JavaScript, and diff checks.

## Evidence limits

The sanitizer establishes bounded SVG metadata transformation and release-check
behavior only; it does not establish decoder safety, legal clearance, asset
quality, accessibility, ownership, or human review. Existing portrait human
decisions, approved model/seed provenance, release derivatives, and registry
bridges remain explicit external gates.
