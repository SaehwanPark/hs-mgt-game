# Domain QA — Visual and Audio Phase 2 Live Read-Only Integration v0.12.18

## Status

pass

## Reviewed Inputs

- User request and `_workspace/00_input/request-summary.md`.
- `_workspace/21_implementation_plan_visual_audio_phase2.md`.
- `docs/visual-audio-phase2-live-read-only-v0.12.18.md`, the accepted Phase 0
  alignment/ADR-0011, and the merged Phase 1 document.
- `SPEC.md`, `ARCHITECTURE.md`, `docs/visual_audio_upgrade_proposal.md`,
  canonical product docs, and the harness team spec.
- `src/mcp/presentation.rs`, `src/mcp/session.rs`, `src/mcp/server.rs`,
  `gui/app.mjs`, `gui/index.html`, and Phase 2 tests.

## Findings

- The new `competitive-read-only-v1` envelope selects typed session/resources,
  `PlayerObservation` facts, player-owned capacity/facility lines, visible
  pending text, and committed transition/history/hash summaries.
- `get_presentation` is a read-only MCP operation. Rust tests verify that it
  leaves the session unchanged, carries committed hashes, rejects unsupported
  campaigns explicitly, and omits legal commands, true world state, effect
  queues, event metadata, resolved inputs, private actions, and non-observation
  flags.
- The browser path accepts live or recorded envelopes through the same versioned
  adapter, renders state/hash history, and labels loading, empty, missing,
  adapter-error, and unsupported-schema states without calling `submitTurn`.
- The projection does not recalculate margin, capacity, trust, delays, rival
  behavior, outcomes, or causal claims. Facility detail is explicitly limited
  to observed player capacity lines until a structured facility source is
  justified.
- Legacy MCP tools and thin-client exports remain available, while the Phase 2
  page defaults to read-only behavior. No simulation, randomness, replay
  verification, scenario, audio, asset, or network core behavior changed.

## Required Fixes

None.

## Residual Risks

- Browser rendering and viewport checks could not be exercised because no
  Chromium/Chrome binary is installed; browser-native QA remains a follow-up.
- Typed projection parity can drift if future observation fields are added
  without source-map and serialization updates.
- Static/AI checks do not establish human usability, lived accessibility,
  learning, engagement, domain-expert validity, or policy validity.
- Phase 3 must establish any action DTO from canonical command/validation
  sources and must not turn this read-only projection into client authority.

## Verification Evidence

- Focused GUI/thin-client/read-only tests: 18 passed.
- Full Python test discovery: 248 tests passed.
- Node syntax check: passed.
- Focused projection tests: 3 passed.
- `cargo fmt --check`: passed.
- `cargo clippy --all-targets -- -D warnings`: passed.
- `cargo test --all -- --test-threads=1`: passed (311 unit tests plus
  integration/golden/doc-test targets).
- `python3 scripts/check_release_metadata.py`: passed at `0.12.18`.
- `git diff --check`: passed.
