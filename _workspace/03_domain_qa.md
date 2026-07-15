# Domain QA — Visual and Audio Phase 4 Resolution and Causal Feedback v0.12.20

## Status

pass

## Reviewed Inputs

- User request and `_workspace/00_input/request-summary.md`.
- `_workspace/23_implementation_plan_visual_audio_phase4.md`.
- `_workspace/01_evidence_map.md`, `_workspace/02_mechanism_design.md`, and
  `docs/visual-audio-phase4-resolution-causal-v0.12.20.md`.
- The accepted Phase 0 alignment/ADR-0011 and merged Phase 1/2/3 documents.
- `SPEC.md`, `ARCHITECTURE.md`, `docs/visual_audio_upgrade_proposal.md`,
  canonical product docs, and the harness team spec.
- `src/mcp/resolution.rs`, `src/mcp/presentation.rs`, `src/mcp/session.rs`,
  `src/mcp/server.rs`, `gui/app.mjs`, `gui/index.html`, and Phase 4 tests.

## Findings

- `competitive-resolution-v1` is a read-only host envelope over committed
  `CompetitiveTransition` history. It supports latest and selected historical
  competitive turns and returns explicit errors for unsupported campaigns,
  missing history, and unavailable turns.
- Before/after resources, operations, and pending processes are derived through
  the existing actor-visible `observe_for_human`/presentation projection. The
  browser receives no true world state, resolved stochastic inputs, private
  rival actions, or effect queue.
- The eight resolution steps reuse the accepted `TransitionSummary` command,
  event, and effect surfaces plus actor-visible information. Source labels keep
  committed effects distinct from presentation-level before/after comparison;
  no inferred causal graph or new causal engine was added.
- Historical reads preserve the session observation and state hash. Browser
  play/pause/skip/review and reduced-motion behavior are local presentation
  state; all result text remains available immediately in the DOM.
- A successful `submit_turn` is reported separately from optional resolution or
  presentation refresh errors. Existing parser, validator, action catalog, and
  transition boundaries remain authoritative.

## Required Fixes

None.

## Residual Risks

- Browser rendering and viewport checks could not be exercised because no
  Chromium/Chrome binary is installed; browser-native QA remains a follow-up.
- The resolution step strings reuse existing committed summaries and are not a
  richer structured causal model; future clarity work must preserve the same
  source and observation boundary.
- Static/AI checks do not establish human comprehension, usability, lived
  accessibility, learning, engagement, domain-expert validity, calibration,
  balance, or policy validity.
- Phase 5 must keep audio optional, visible-only, provenance-backed, and
  independent of simulation state, hashes, and replay semantics.

## Verification Evidence

- Focused resolution/contextual/read-only GUI tests: 15 passed.
- Node syntax check, Rust formatting, and Clippy with warnings denied: passed.
- Full Python discovery: 257 tests passed.
- Serial Rust tests: 317 unit tests plus 13 integration/golden/scenario tests
  passed; doc-tests passed with zero tests.
- Node syntax, Rust formatting, Clippy with warnings denied, release metadata,
  and whitespace checks: passed at `0.12.20`.
