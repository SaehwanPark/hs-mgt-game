# Request Summary — Visual and Audio Phase 2 Live Read-Only Integration v0.12.18

## Scope

- Promote the next SPEC item after the merged Phase 1 static executive desktop.
- Add a typed, actor-visible `competitive-regional-v1` presentation projection
  for live or recorded read-only viewing.
- Render current observations, player institution/facility detail, public
  signals, pending processes, committed history/state hashes, replay metadata,
  and explicit loading/error/empty/missing states.
- Preserve the Phase 0 browser-native/host-authoritative boundary and promote
  only Phase 2 at version `0.12.18`.

## Sources

- `docs/visual_audio_upgrade_proposal.md`, Phase 0 alignment, ADR-0011, and the
  merged Phase 1 static-desktop document.
- Current `src/mcp/session.rs`, MCP server tools, player observation projection,
  competitive history/transition summaries, and GUI proof.
- Canonical proposal, roadmap, design principles, harness team spec, SPEC,
  architecture, changelog, lessons, and versioning policy.

## Expected files

- Typed Rust read-only presentation DTO/projection and `get_presentation` MCP
  tool.
- Browser read-only adapter/client, typed-envelope rendering, replay/hash view,
  and loading/error/empty contracts.
- Phase 2 contract document, SPEC/architecture/version records, tests, evidence,
  domain QA, lessons, and final handoff.

## Validation target

- Projection serialization and hidden-field exclusion.
- Read-only no-transition/no-submission behavior and committed history/hash
  parity.
- Live/recorded browser mapping, missingness, loading/error/empty states,
  syntax, metadata, and no-network/no-asset checks.
- Full Python and Rust verification plus one code-review pass and CI.

## Explicit non-goals

No graphical actions, command validation/submission, batch editing, resolution
animation, causal overlays, audio playback, asset acquisition, campaign
expansion, mobile support, replay playback, deployment, or human-usability
claims. No browser formulas, true-world state, resolved stochastic inputs,
private rival actions, or client-owned history.

## Global workflow

Use the repo orchestrator and end-user experience workflow for the live viewer,
the global simple-code/spec-driven/plan-design skills, and the preferred
workflow with exactly one code reviewer. Implement on a feature branch, verify,
open a PR, review once, merge into `main`, and then design Phase 3.
