# Request Summary — Visual/audio Phase 9.1 provenance and notices v0.12.78

## Authorized outcome

Make the canonical visual/audio asset registries provenance-auditable and
generate reproducible asset credits and third-party notices without inventing
external sources or promoting the pending portrait previews.

## Target slice

- Add per-entry provenance metadata to the canonical visual/audio registries.
- Enforce provenance kind, source/license reference shape, retrieval-date
  requirements, license compatibility, and denylisted provenance text.
- Extend deterministic credits output and add a generated third-party notices
  file, with stale-output checks in tests and CI.
- Keep all current entries repository-authored with a local policy reference;
  do not add third-party or portrait-release assets.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 9.1.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `scripts/validate_assets.py` and `generate_asset_credits.py`.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Registry provenance, hash/path, allowlist/denylist, generated credits/notices,
malformed metadata, stale-output, existing generation/release/documentation
checks, full Python/Rust tests, formatting, Clippy, JavaScript, and diff
checks.

## Evidence limits

The registry makes provenance fields and release projections auditable but does
not perform a legal review. Portrait human decisions, approved local
model/seed provenance, release derivatives, and registry bridges remain
explicit external gates.
