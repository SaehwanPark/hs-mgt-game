# Request Summary — Visual/audio Phase 4.2 consequence linkage v0.12.65

## Authorized outcome

Complete the Phase 4.2 visible consequence linkage checklist using existing
actor-visible regional-world and resolution envelopes.

## Slice boundary

- Project public regional signals and visible processes into deterministic links
  with explicit observed month, source, target entity, and information boundary.
- Project host-committed resolution effects into deterministic links while
  preserving targetless effects when the host provides no target.
- Connect reports to entities and entities back to related reports/consequences
  through local focus controls beside the existing board/detail surface.
- Preserve rival observation delay, missingness, historical state, replay
  turn/hash sequence, and non-animated focus behavior.
- Do not change Rust DTOs, simulation state, commands, transitions, stochastic
  inputs, history, hashes, replay authority, audio, or debrief behavior.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 4.2.
- `src/mcp/regional_world.rs` — observed regional signals/processes and lag.
- `src/mcp/resolution.rs` — host-committed effects and replay metadata.
- `gui/app.mjs`/`gui/index.html` — existing board, report, detail, resolution,
  and first-month surfaces.
- `docs/design_principles.md` — actor-visible boundaries and accessibility.

## Validation target

Focused consequence-link, GUI, resolution, first-month, registry, credits,
metadata, documentation-link, full Python, full Rust, formatting,
presentation-contract, and diff checks.

## Evidence limits

Static deterministic projections and GUI source checks establish technical
linkage and authority boundaries only. They do not establish human usability,
lived accessibility, contrast, learning, calibration, replay browser behavior,
or policy validity.
