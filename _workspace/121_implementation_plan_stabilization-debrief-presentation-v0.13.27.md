# Implementation Plan — Phase 12 stabilization debrief presentation v0.13.27

## Task restatement

Continue Phase 12 with a bounded record of the current stabilization debrief
presentation. Bind the existing CLI educational debrief, host-authored
campaign/end-session envelopes, shared browser renderers, and written/audio
fallbacks while keeping the live GUI and instructor boundaries explicit.

## Current understanding

- `src/debrief/report.rs` already produces a deterministic stabilization
  debrief with run-level tradeoffs, actor rationales, attributed effects,
  observation-revision notes, and a decision-quality/outcome-quality
  distinction, followed by an existing instructor run summary appendix.
- `src/mcp/campaign_coverage.rs` and `src/mcp/session.rs` supply host-authored
  debrief lines only after a completed stabilization session.
- `gui/app.mjs` renders supplied campaign/end-session history and debrief text,
  but the live launcher currently supports `competitive-regional-v1` only.

## Target slice

Add `docs/evaluation/phase12-stabilization-debrief-presentation.json` and a
parity test that records:

- current CLI debrief sections and source markers;
- host/core ownership, completion gating, immutable history/replay alignment,
  shared campaign/end-session browser renderers, and written equivalents;
- optional debrief music/fallback treatment and the current competitive-only
  live GUI boundary; and
- open work for browser-native stabilization presentation, visual/audio
  quality, instructor-surface decisions, and human educational review.

## Assumptions

- This is current debrief evidence, not a new debrief implementation.
- The existing CLI instructor/run-summary appendix is recorded as an existing
  boundary; no new true-state view or instructor authority is introduced.
- Debrief text remains host-authored and complete when optional audio is muted
  or unavailable.

## Minimal implementation plan

1. Add the debrief presentation ledger and source-parity test.
2. Check only current stabilization debrief presentation in Phase 12.1 and
   synchronize canonical docs, lessons, version metadata, generated credits,
   and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add new debrief lines, browser routes, stabilization GUI launchers,
  runtime fields, persistence, replay regeneration, assets, audio files,
  screenshots, instructor exports, or human evaluation.
- Do not call existing CLI/shared renderers a complete visual stabilization
  debrief or an educational-effectiveness result.

## Stop conditions

Stop if debrief evidence cannot be source-linked to committed history/replay,
host-authored lines, and existing renderers without adding a runtime authority
path, new content, an asset, direct audio integration, or a human judgment.

## Risk label

Risk: low

Reason: The slice records current deterministic CLI/host/browser debrief
contracts and boundaries without changing simulation or presentation runtime.
