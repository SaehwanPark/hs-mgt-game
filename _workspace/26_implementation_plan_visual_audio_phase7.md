# Implementation Plan — Visual and Audio Phase 7 Campaign Coverage v0.12.23

Status: Complete; implementation, verification, and exactly one code-review
pass are complete.

## Task restatement

Add an additive, typed campaign-coverage read and a shared browser route for
the existing stabilization and affiliation campaigns. Preserve their distinct
stage, actor, obligation, command, observation, history, hash, and debrief
semantics. Keep competitive Phase 2–6 contracts unchanged.

## Minimal implementation plan

1. Add `campaign-coverage-v1` DTOs in `src/mcp/campaign_coverage.rs` for
   session/stage, briefing, visible metrics, actors, processes, decisions and
   host-shaped parameters, history, replay, and terminal debrief.
2. Add `GetCampaignCoverageRequest`, a non-mutating store method, and MCP tool
   for stabilization and affiliation. Derive only existing observation and
   debrief sources; exclude true state, resolved inputs, effect queues, and
   private future outcomes.
3. Add Rust tests for both campaigns, repeated-read non-mutation/hash stability,
   hidden-field exclusion, campaign-specific role/stage/actor semantics,
   terminal debrief, unsupported competitive response, and decision metadata.
4. Add browser campaign coverage renderer/client with shared stage/metric/history
   primitives, campaign-specific actor/process sections, host-shaped forms,
   recoverable submit errors, optional adapter behavior, and generated-audio
   stage/cue mapping. Keep competitive clients intact.
5. Add semantic HTML/CSS for campaign stage/actor/decision panels and static
   tests for no formulas/network/private-state exposure, keyboard operation,
   rejection recovery, and campaign distinction.
6. Update Phase 7 contract, SPEC/architecture/README/changelog/lessons, version
   metadata to `0.12.23`, and QA/handoff records.
7. Run focused/full checks, perform exactly one code-review pass, push, open a
   PR, wait for CI, merge into `main`, and record Phase 8 as the next gate.

## Expected files

- `src/mcp/campaign_coverage.rs`, `src/mcp/session.rs`, `src/mcp/server.rs`,
  `src/mcp/mod.rs`, and Rust session tests.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`, and
  `tests/test_gui_campaign_coverage.py`.
- Phase 7 contract/project records, metadata, lessons, QA, and handoff.

## Acceptance criteria

- Both non-competitive campaigns return `campaign-coverage-v1` with campaign
  role, stage, visible metrics/briefing, decisions, actors/processes, history,
  replay metadata, and terminal debrief when done.
- Stabilization keeps short executive onboarding semantics; affiliation keeps
  partner fit, commitments, review, stakeholder response, and integration
  semantics.
- Browser forms use host-provided parameter metadata and canonical templates;
  rejected submission is recoverable and does not replace the current read.
- Generated audio remains optional, visible-only, and complete when muted.
- Competitive regional world/action/resolution/audio paths remain compatible.

## Non-goals and stop conditions

No new simulation mechanics, campaign state, true-state view, resolved-input
exposure, global action framework, asset/network/deployment work, campaign
flattening, or human-evaluation claim. Stop if a campaign requires changing its
transition semantics solely to fit the shared browser shell.
