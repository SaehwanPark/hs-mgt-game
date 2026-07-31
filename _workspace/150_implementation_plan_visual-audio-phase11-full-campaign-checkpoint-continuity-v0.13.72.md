# Implementation Plan — Full-campaign checkpoint/replay continuity v0.13.72

## Task restatement

Continue the visual/audio roadmap with a bounded host-persistence evidence slice:
prove that a competitive checkpoint taken mid-campaign can be loaded by a fresh
host and continued through month 24 with the same immutable replay/history and
actor-visible presentation results.

## Current understanding

- The host already writes and verifies a `gui-competitive-save-v1` wrapper around
  `CompetitiveSessionSave`, and the browser retains only an opaque session ID.
- Existing durable recovery tests save after one month and compare only the next
  continuation hash; the roadmap still leaves full-campaign save/load/replay
  continuity open.
- Regional-world and campaign-coverage reads already expose terminal visible
  surfaces; they can provide a deterministic end-of-campaign comparison without
  adding a new presentation route.

## Target slice

1. Save a competitive session after a deterministic mid-campaign checkpoint at
   month 12, load it into a fresh host store, and continue both original and
   restored sessions through month 24.
2. Require equal terminal transition hashes/counts, replay rows, regional-world
   presentation, and campaign-coverage terminal envelope, plus cleanup of the
   durable file after the recovered session ends.
3. Record the bounded host continuity evidence in the Phase 11.1 ledger and
   Phase 13.1 competitive boundary; keep browser serialization, cross-campaign
   completion, screenshots, and human/release gates open.
4. Synchronize request/contract/QA/handoff records, roadmap, SPEC, lessons,
   changelog, and package metadata to `0.13.72`.

## Assumptions and stop conditions

- Existing host save/load routes, schema, deterministic replay verifier, and
  actor-visible read projections are sufficient; no new format or route is
  needed.
- “Full-campaign continuity” means a host checkpoint at month 12 followed by
  deterministic continuation through the existing 24-month limit. It does not
  claim browser-side persistence or human usability.
- The test must fail closed if restored history, state hashes, replay metadata,
  regional-world data, or campaign coverage diverge.

## Minimal implementation plan

1. Add a Rust session regression for mid-campaign durable save/load and terminal
   continuation comparison.
2. Extend the Phase 11.1 and Phase 13.1 evidence contracts and tests to anchor
   the new regression and explicitly retain the browser-only limits.
3. Update roadmap/SPEC and durable handoff records, bump to `0.13.72`, run full
   validation, and use exactly one medium-effort reviewer before PR handoff.
   The sole review is approved with no actionable findings; PR handoff is the
   next gate.

## Likely files

- `src/mcp/session.rs`
- `tests/test_phase11_browser_refresh_recovery.py`
- `tests/test_phase13_1_competitive_campaign_boundary.py`
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `docs/evaluation/phase13.1-competitive-campaign-boundary.json`
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, `_workspace/final/handoff.md`
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `LESSONS.md`,
  `CHANGELOG.md`, and release metadata

## Acceptance criteria

- A month-12 checkpoint loads into a fresh host and both sessions reach the
  same terminal state through 24 transitions.
- Replay/history hashes, terminal regional-world data, and terminal
  campaign-coverage data are equal; recovered checkpoint cleanup succeeds.
- Focused and full validation, exactly one medium-effort review, PR merge,
  temporary-branch deletion, and clean-main verification pass.
- Evidence explicitly excludes browser serialization, cross-campaign durable
  completion, pixel-level quality, human review, and public release.

## Non-goals

- No new route/schema, simulation mechanic, asset, audio file, browser save
  artifact, replay format, screenshot suite, or human approval.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally and remotely, verify clean `main`, then design the
next unmet roadmap slice.
