# Request Summary — Visual/audio Phase 9.2 asset security scanner v0.12.80

## Authorized outcome

Add a dependency-free asset security/integrity scanner for the visual/audio
asset paths in scope, with fail-closed SVG safety, file-size/dimension limits,
audio signature checks, and focused tests without adding external assets.

## Target slice

- Add `scripts/validate_asset_security.py` to scan registered source/release
  files plus preserved generation previews in a bounded asset root.
- Reject SVG scripts, event handlers, external references, embedded raster
  images, foreign objects, external fonts, entity declarations, and malformed
  or overlarge view boxes; enforce a per-file byte limit.
- Validate PNG/JPEG/GIF dimensions and WAV/OGG/MP3/FLAC signatures when those
  files are present; fail closed on unsupported audio extensions or signatures.
- Add focused malicious-fixture, dimension, size, codec, and repository-scan
  tests and wire the scanner into CI/release guidance.
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

Asset security scanner, registry/release hash checks, malicious fixtures,
dimension/size/audio signature checks, existing generation/credits/release/
documentation checks, full Python/Rust tests, formatting, Clippy, JavaScript,
and diff checks.

## Evidence limits

The scanner establishes bounded file-shape and signature safety only; it does
not sanitize or rewrite files, prove legal clearance, establish human
accessibility, validate audio quality, or replace human review. Portrait human
decisions, approved local model/seed provenance, release derivatives, and
registry bridges remain explicit external gates.
