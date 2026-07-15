# Implementation Plan — Visual/audio Phase 13 first-month continuity v0.12.29

## 1. Task restatement

Make the existing competitive first-month GUI path inspectable as one bounded
workflow by adding a local text-first stage rail and an adapter-driven contract
test. Preserve every existing host and simulation boundary.

## 2. Assumptions

- Existing launch, read-only, action, resolution, regional-world, campaign, and
  audio clients remain the source of behavior.
- A first-month review threshold of two local drafts matches the proposal's
  required experience; it does not replace host validation or impose a runtime
  action limit.
- The page can render one rail for the competitive action/read-only desktop;
  other campaigns remain outside this slice.
- If a required change needs a DTO, adapter method, dependency, or simulation
  field, stop and report rather than expanding scope.

## 3. Files and functions

- Add `gui/first-month.mjs` with the stage catalog, pure stage derivation, and
  local DOM renderer.
- Update `gui/app.mjs` to create the flow client for read-only/action clients,
  advance it only at confirmed existing handoffs, and expose it through
  `HsMgtGui`.
- Update `gui/index.html` with the semantic rail and responsive styling.
- Add `tests/test_gui_first_month.py` for pure stage transitions, semantic
  rendering markers, adapter-sequence coverage, failure non-advancement, and
  boundary exclusions.
- Update `gui/README.md`, `ARCHITECTURE.md`, `README.md`, `SPEC.md`,
  `CHANGELOG.md`, `LESSONS.md`, the Phase 13 protocol, domain QA, and handoff.
- Bump release metadata from `0.12.28` to `0.12.29`.

## 4. Test-first sequence

1. Add pure stage-function tests for start, inspect, draft, validation,
   submission, resolution, continue, and rejection recovery.
2. Add static contract checks for the rail, stage labels, text equivalence,
   semantic current state, and no simulation/network/hidden-field references.
3. Add a Node adapter-sequence test that runs start/load, adds two draft
   actions, validates, submits, reads resolution, and refreshes presentation;
   assert the host call order and final `continue` stage.
4. Implement the smallest module, app hooks, and markup needed by those tests.
5. Run focused GUI tests, full Python discovery, Node syntax, Rust tests,
   formatting, Clippy, release metadata, and diff checks.

## 5. Acceptance criteria

- The rail has seven stable stages with visible text for current, completed,
  and upcoming states.
- A loaded session cannot appear complete before the action catalog, valid
  unchanged batch, committed submit, resolution read, and refreshed
  presentation handoffs occur.
- At least two local drafts are visible before the rail advances to validation;
  existing add/revise/remove behavior remains intact.
- Failed or rejected host operations do not advance the flow or replace the
  current session.
- The read-only client never calls `submitTurn`.
- The flow contains no host payload, formula, hidden state, external asset,
  network call, or mutation outside existing adapter operations.
- Technical checks pass; no human or policy claim is made.

## 6. Non-goals and stop conditions

- No new MCP/Rust schema, command, transition, stochastic input, history/hash/
  replay/debrief behavior, browser transport, audio source, image, or
  campaign-generalized onboarding.
- Stop if the rail requires adapter payload inspection, a new host operation,
  client-side legality, or changes to an existing canonical action.
- Stop if existing failure/recovery behavior cannot preserve the last confirmed
  stage without inventing a fallback outcome.

## 7. Review checklist

- Confirm stage labels describe presentation handoffs, not outcomes.
- Confirm two-draft guidance does not constrain host action batches.
- Confirm load/validation/submit/resolution/refresh failures do not advance the
  flow.
- Confirm semantic text remains available under reduced motion and muted audio.
- Run exactly one general code-review pass for Phase 13 and fix its findings;
  do not run a second review pass.
