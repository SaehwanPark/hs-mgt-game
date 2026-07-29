# Implementation Plan — Campaign-aware first-month rail v0.13.59

## Task restatement

Add a campaign-aware first-session rail for the existing
`stabilization-v1` and `regional-affiliation-v1` campaign-coverage GUI path
while preserving the existing seven-stage competitive rail and host authority.

## Current understanding

- `gui/first-month.mjs` currently derives and renders only the
  `competitive-first-month-v1` seven-stage draft/validate/submit flow.
- `gui/app.mjs` already loads campaign coverage and renders its host-shaped
  decisions, but `loadCampaignCoverage` resets the first-month rail to state
  fields that imply the competitive action catalog.
- Campaign coverage submits through `adapter.submitTurn(command)` and refreshes
  its typed envelope inside `createCampaignCoverageClient`; the rail needs a
  small callback to observe that successful host refresh.
- `gui/index.html`, `gui/README.md`, the guides, evaluation ledger, roadmap,
  release metadata, and tests are the relevant documentation and evidence
  surfaces.
- Main uncertainty: whether any alternate first-month rail call site exists.
  Search must confirm the named module is the only rail implementation; if a
  second incompatible implementation is found, stop before editing.

## Assumptions

- The competitive rail’s schema, stage IDs, renderer behavior, and tests remain
  public compatibility surfaces and must not change.
- A campaign-coverage decision is a single host-shaped command; no local draft
  or client-side validation stage should be invented for it.
- A successful campaign-coverage `load` after submission is the host-owned
  evidence for the review/continue handoff; rejected commands must leave the
  rail at the decision stage.
- No new host route, simulation field, asset, audio file, persistence behavior,
  or true-state field is required.

If any assumption is false, stop and report the mismatch before broadening the
implementation.

## Minimal implementation plan

1. Inspect all `createFirstMonthFlow`, `firstMonthStageFor`, and campaign
   coverage submit/load call sites; confirm the rail is local presentation state.
2. Add a separate `campaign-coverage-first-session-v1` stage vocabulary and
   derive its five bounded stages: start/load, inspect, choose a host decision,
   review the committed stage, and continue. Keep competitive derivation and
   schema unchanged.
3. Add the smallest campaign-client commit callback needed for the action
   client to advance the campaign rail only after a successful host refresh;
   keep rejected decisions recoverable at the decision stage.
4. Update launcher/rail wording and user-facing guides so stabilization and
   regional affiliation no longer inherit competitive draft instructions.
5. Add focused Node/Python contract tests, update the Phase 13.1 evidence
   ledger and roadmap, bump the patch version to `0.13.59`, regenerate any
   derived release metadata, and run the full validation suite.
6. Perform exactly one medium-effort code review, fix any Critical/High issue
   and directly relevant findings, then prepare the PR handoff.

## Files and functions likely to change

- `gui/first-month.mjs`: separate campaign-coverage stage schema, stages, and
  state derivation/render selection.
- `gui/app.mjs`: campaign coverage commit callback, rail state updates, and
  global schema export if needed.
- `gui/index.html`: campaign-neutral first-month heading/detail wording.
- `gui/README.md`, `docs/guides/gui-how-to-play.md`,
  `docs/guides/how-to-play.md`: describe both rail variants and their host
  boundaries.
- `tests/test_gui_first_month.py`,
  `tests/test_phase12_live_campaign_coverage.py`: pure derivation, renderer,
  accepted/rejected campaign handoff, and source-boundary tests.
- `docs/evaluation/phase13.1-first-session-boundary.json` and a focused
  Phase 13.1 test: record the campaign-aware rail without claiming human
  first-time-user completion.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, generated credits,
  device policy, and release metadata tests: current-cycle bookkeeping.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, and `_workspace/final/handoff.md`:
  current request, contract, QA, and handoff records.

Avoid editing files outside this list unless a generated check identifies a
required derived file. If that happens, stop and explain why before proceeding.

## Tests and checks

- `python3 -m unittest tests.test_gui_first_month tests.test_phase12_live_campaign_coverage tests.test_phase13_1_first_session_boundary`
- `node --check gui/first-month.mjs && node --check gui/app.mjs`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- release metadata, documentation links, asset registry/credits/release,
  security/generation, device-performance, offline, browser-compatibility,
  visual/audio contract, and `git diff --check` checks.

Expected results:

- Competitive tests retain the seven-stage schema and continue to reach
  `continue` only after the existing host reads.
- Campaign coverage renders a five-stage rail, reaches `continue` only after
  a successful canonical submit/refresh, and remains at `choose` after a
  rejected command.
- No hidden-state, local transition, or new campaign rule marker appears.

## Acceptance criteria

- `firstMonthStageFor` returns the unchanged competitive stages for existing
  competitive state and the new campaign-coverage stages for the two supported
  campaign IDs.
- The live campaign-coverage rail distinguishes inspection, host-shaped
  decision selection, committed-stage review, and continuation in visible text.
- Accepted campaign decisions advance the rail only after the existing
  `campaign-coverage-v1` refresh succeeds; rejected decisions do not advance it.
- Guides and the GUI README explain both rail variants and retain the
  host-authority/written-fallback boundary.
- Full tests and release checks pass at v0.13.59, with human accessibility,
  educational usability, and public-release gates still explicit.

## Non-goals

- Do not change the competitive seven-stage schema, IDs, or action semantics.
- Do not add local drafts, client validation, campaign rules, routes, fields,
  persistence, true-state content, or simulation authority.
- Do not add assets, audio files, screenshots, browser automation, or human
  evaluation claims.
- Do not refactor unrelated onboarding, resolution, or campaign renderers.
- Do not perform opportunistic formatting or cleanup.

## Stop conditions

Stop and report before continuing if:

- more than three production files beyond the named GUI modules require edits;
- the campaign rail requires a new host schema or mutation path;
- an existing incompatible first-month rail implementation is found;
- accepted/rejected behavior cannot be observed without inventing client state;
- unrelated tests fail and cannot be isolated from this slice.

## Review checklist

- Confirm the competitive rail is byte/schema-compatible in behavior and tests.
- Confirm campaign state is selected from the existing host campaign identity,
  not guessed from UI labels or commands.
- Confirm accepted/rejected transitions are driven by host responses only.
- Confirm the diff contains no true-state, resolved-input, effect-queue, or
  local transition authority.
- Confirm focused tests cover initial load, accepted submit, rejected submit,
  malformed/failing refresh, and written fallback.
- Confirm the diff matches this plan, remains minimal, and records deviations,
  unresolved risks, files changed, and tests run.

## Risk label

Risk: medium

Reason: the change touches a shared presentation state machine and two live
campaign handoff call sites, but it preserves existing host APIs and simulation
authority.

## Execution record

- Files changed: `gui/first-month.mjs`, `gui/app.mjs`, `gui/index.html`, current
  guides/README, focused tests, Phase 13.1 evidence, roadmap/spec/release
  records, generated credits, and device-performance measurement.
- Verification: focused rail/coverage tests (17), Rust tests (344), Python
  discovery (761), release/documentation/assets/security/generation/device/
  offline/browser/contract checks, and `git diff --check` passed.
- Review: one medium-effort reviewer found no Critical/High issue. The final
  captured source-size correction and explicit malformed/failed-refresh tests
  were applied; no unresolved deviations remain.
