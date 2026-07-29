# Implementation Plan — Campaign decision-time observation recovery v0.13.61

## Task restatement

Expose the actor-visible observation paired with each committed stabilization
and regional-affiliation decision in the existing campaign-coverage history,
then render it as an optional written detail in the browser campaign history.
Preserve the competitive history/replay paths, host authority, and all hidden-
state exclusions.

## Current understanding

- Core `Transition` and `AffiliationTransition` records already retain the
  observation that preceded each command.
- `TransitionSummary` currently exposes turn, command, events, effects, hash,
  and consultant options, but not the paired actor-visible observation.
- The campaign-coverage panel already renders committed history but has no
  decision-time observation detail.
- `docs/evaluation/phase12-decision-time-recovery-boundary.json` explicitly
  leaves browser-native per-decision observation recovery open.

## Assumptions

- Existing formatter functions produce actor-visible written observations and
  do not include resolved inputs, private rationale, or true state.
- An additive optional `observation` field on `TransitionSummary` preserves
  older history/replay consumers and older browser fixtures.
- The campaign-coverage history renderer can show the detail with native
  `<details>`/`<summary>` and no new asset, route, or authority path.

If any assumption is false, stop and report the mismatch before broadening the
slice.

## Minimal implementation plan

1. Inspect the existing stabilization/affiliation observation formatters,
   transition summarizers, campaign history renderer, and recovery ledger.
2. Add optional actor-visible observation lines to `TransitionSummary` for
   stabilization and affiliation summaries; competitive summaries remain
   omitted/unchanged.
3. Render an accessible optional “Decision-time observation” disclosure for
   each campaign history entry when the host supplies observation lines.
4. Add Rust, Node, and Python evidence for source parity, observation-before-
   command semantics, omitted-field compatibility, hidden-state exclusions,
   and written fallback.
5. Update the decision-time recovery ledger, roadmap, guides/GUI README,
   SPEC/changelog/lessons, package version to `0.13.61`, generated metadata,
   device measurement, and current request/contract/QA/handoff records.
6. Run full validation, perform exactly one medium-effort code review, fix only
   relevant findings, and prepare the PR handoff.

## Files and functions likely to change

- `src/mcp/session.rs`: optional `TransitionSummary.observation`,
  stabilization/affiliation summarizer bindings, compatibility assertions.
- `gui/app.mjs`: campaign history observation disclosure renderer.
- `gui/index.html` or existing CSS only if the disclosure needs a minimal
  style rule; no new visual asset is expected.
- `tests/test_phase12_decision_time_recovery_boundary.py`,
  `tests/test_phase12_live_campaign_coverage.py`, and focused Rust/Node probes.
- `docs/evaluation/phase12-decision-time-recovery-boundary.json` and test:
  close only the current technical browser recovery boundary.
- Roadmap, `SPEC.md`, `CHANGELOG.md`, `LESSONS.md`, `README.md`,
  `Cargo.toml`, `Cargo.lock`, generated credits, device policy, and current
  `_workspace` records.

Avoid editing competitive simulation, competitive GUI rendering, persistence,
assets, audio catalogs, or new routes. If an observation line requires hidden
state or a schema-version change, stop and report before broadening scope.

## Tests and checks

- `cargo fmt --check`
- focused Rust campaign coverage/history tests
- focused decision-time recovery, live campaign, and GUI coverage tests
- Node browser-renderer observation disclosure probe
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- release metadata, documentation links, asset/security/generation,
  device-performance, offline, browser-compatibility, visual/audio contract,
  and `git diff --check` checks

Expected results:

- Stabilization and affiliation campaign history entries expose the
  actor-visible observation that preceded each command.
- Competitive summaries omit the optional field, preserving existing output.
- Browser fixtures without observation remain valid and render no empty
  disclosure; audio-off and written equivalents remain complete.
- No resolved inputs, private rationale, true state, local transition
  authority, or simulation behavior changes.

## Acceptance criteria

- The optional summary field is sourced from existing actor-visible host
  observation formatters and is serialized only when present.
- The browser campaign history presents the observation in an accessible,
  written-only disclosure tied to its committed turn/command.
- Legacy summaries without the field remain valid; competitive paths are
  unchanged.
- The decision-time recovery ledger no longer marks browser-native campaign
  observation recovery as open, while causal visualization, human quality,
  accessibility, and educational review remain open.
- Full checks pass at v0.13.61.

## Non-goals

- No new route, schema version, asset, audio file, simulation rule, persistence,
  replay regeneration, true-state view, resolved-input field, private actor
  rationale, causal graph, counterfactual, or instructor-only authority.
- Do not claim human comprehension, accessibility, educational value, or
  visual quality from the technical disclosure.

## Stop conditions

Stop and report if:

- the paired observation cannot be rendered from existing visible formatters;
- any field would expose resolved inputs, private rationale, true state, or
  future outcome;
- competitive summaries or browser paths require unrelated behavior changes;
- a schema-version bump, new route, persistence mechanism, or new asset is
  required; or
- unrelated test failures cannot be isolated from this slice.

## Review checklist

- Verify the observation is recorded before the corresponding command.
- Verify competitive summaries remain unchanged/omitted.
- Verify old summaries without `observation` deserialize/render safely.
- Verify disclosure text has no hidden-state or private-rationale markers.
- Verify command/history/hash alignment remains host-owned and immutable.
- Verify written/audio-off and reduced-motion behavior remains complete.
- Verify the diff matches this plan and records deviations and unresolved risks.

## Risk label

Risk: medium

Reason: the slice adds a typed optional host projection and a new browser
history disclosure across two campaign paths, while preserving compatibility,
authority, and information-boundary constraints.

## Execution record

- Implemented the optional `TransitionSummary.observation` projection from the
  existing stabilization and regional-affiliation actor-visible formatters;
  competitive summaries remain omitted.
- Added native browser disclosure rendering and written fallback coverage for
  campaign history entries, plus Rust coverage for observation/history pairing
  and legacy/competitive compatibility.
- Updated the decision-time recovery ledger, roadmap, guides, SPEC, changelog,
  lessons, generated release metadata, device measurement, and handoff records.
- Validation passed before review: 344 Rust tests, 764 Python tests, format,
  Clippy, release metadata, documentation links, asset registry/security/
  budget, audio packaging, generation, device, offline, browser, raster, and
  visual/audio contract checks; `git diff --check` also passed.
- The sole medium-effort review found no Critical, High, or Medium findings.
  Two Low findings were fixed: nested observation-list CSS is no longer styled
  as a history card, and explicit legacy-summary deserialization plus
  competitive JSON-omission assertions were added.
- Final validation after the review fixes passed: 344 Rust tests, 764 Python
  tests, format, Clippy, release metadata, documentation links, asset
  registry/security/budget, audio packaging, generation, device, offline,
  browser, raster, visual/audio contract, asset-credit, and `git diff --check`.
- PR/merge handoff remains pending; no plan deviation or new risk has been
  identified.
