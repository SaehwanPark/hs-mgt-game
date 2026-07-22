# Request Summary — Visual/audio Phase 9.1 in-game credits v0.12.79

## Authorized outcome

Expose a read-only, keyboard-accessible in-game credits surface backed by the
canonical generated asset provenance projection, without inventing external
sources or promoting the pending portrait previews.

## Target slice

- Generate `gui/asset-credits.mjs` from the canonical registry and keep it
  stale-checkable alongside the existing credits/notices outputs.
- Add a visible Asset credits and provenance panel in the static executive
  desktop with source, license, approval, provenance, accessibility, and
  release-status text for each registry entry.
- Preserve text-first, keyboard, large-text, reduced-motion, and no-network
  behavior; the panel must remain available when host/session data is absent.
- Keep all current entries repository-authored with no third-party or
  portrait-release assets.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 9.1.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `scripts/generate_asset_credits.py`, `assets/ASSET_CREDITS.md`, and
  `assets/THIRD_PARTY_NOTICES.md`.
- `gui/index.html`, `gui/app.mjs`, and current static GUI tests.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Generated runtime credits, registry/projection parity, HTML/DOM accessibility,
no-network/static-boundary checks, existing generation/release/documentation
checks, full Python/Rust tests, formatting, Clippy, JavaScript, and diff
checks.

## Evidence limits

The in-game panel makes the current registry projection visible but does not
perform a legal review or establish human accessibility. Portrait human
decisions, approved local model/seed provenance, release derivatives, and
registry bridges remain explicit external gates.
