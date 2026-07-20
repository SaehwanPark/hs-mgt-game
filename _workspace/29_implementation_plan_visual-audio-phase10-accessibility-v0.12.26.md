# Operational Plan — Phase 10 accessibility and visual-language hardening v0.12.26

**Status:** Implemented and verified; one code-review pass complete; PR/CI/merge pending

## Task restatement

Add a bounded presentation-only accessibility contract to the existing GUI:
keyboard skip/landmark navigation, explicit status language, persistent standard
or large text scale, and a working optional cue-explanation preference. Preserve
the host adapter and all existing simulation-facing behavior.

## Current understanding

- `gui/index.html` owns the semantic desktop markup, styles, controls, and
  responsive/reduced-motion rules.
- `gui/app.mjs` owns local presentation settings, status rendering, onboarding,
  and host-bound clients.
- Status text exists but the status symbol is one generic CSS diamond and there
  is no legend, skip link, or text-scale control.
- `text_equivalents` is persisted but currently has no observable rendering
  effect.
- Existing Python tests are static contract tests and Node syntax is available;
  browser automation and external dependencies are out of scope.

## Assumptions

- Native HTML/CSS and `localStorage` are sufficient for this slice.
- The existing status category is already host/fixture supplied and must not be
  recomputed from metrics.
- The optional cue explanation is the only text that may be hidden by the
  `text_equivalents` preference; decision and debrief text stays visible.
- If implementation requires a new host field, API, dependency, or local
  simulation state, stop and report the mismatch before editing further.

## Minimal implementation plan

1. Add a skip link, presentation navigation landmark, stable panel anchors, a
   status-language legend, and targeted live/status semantics in `gui/index.html`.
2. Add CSS focus-visible treatment, non-color status symbol/pattern rules, and a
   root large-scale mode while preserving existing
   responsive and reduced-motion rules.
3. Extend `createPresentationSettings` in `gui/app.mjs` with `text_scale` and
   functional `text_equivalents` application; expose `data-status`/accessible
   status labels from `createStatus`.
4. Add focused static contract tests for landmarks, legend vocabulary, settings
   behavior, status metadata, scaling, and no host/simulation boundary change.
5. Update the Phase 10 protocol/design document and aligned SPEC, architecture,
   README, GUI guide, changelog, lessons, metadata, QA, and handoff files.
6. Run focused/full checks, perform exactly one code-review pass, fix any
   actionable findings once, and complete the PR/CI/merge workflow.

## Files and functions likely to change

- `gui/index.html`: semantic navigation, legend, settings control, anchors, and
  CSS presentation/accessibility rules.
- `gui/app.mjs`: `createPresentationSettings`, `createStatus`, and exports only.
- `tests/test_gui_accessibility.py`: focused static contract tests.
- `docs/history/initiatives/visual-audio/visual-audio-phase10-accessibility-v0.12.26.md`: scope, contract,
  verification, and evidence limits.
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `gui/README.md`, `CHANGELOG.md`,
  `LESSONS.md`, release metadata, and `_workspace` handoffs.

Avoid changing `src/`, MCP schemas, `gui/audio.mjs`, `gui/playtest.mjs`, or
host adapter behavior unless discovery proves the bounded contract impossible;
then stop and report why.

## Tests and checks

- `python3 -m unittest tests.test_gui_accessibility tests.test_gui_playtest tests.test_release_metadata`
- `node --check gui/app.mjs`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt -- --check`
- `cargo test --all -- --test-threads=1`
- `cargo clippy --all-targets -- -D warnings`
- `python3 scripts/check_release_metadata.py`
- `git diff --check`

Expected result: focused and full tests pass; Rust behavior and package tests
remain unchanged; the local settings are deterministic and no host request is
introduced by presentation controls.

## Acceptance criteria

- A keyboard user can skip directly to briefing, action, resolution/result, and
  debrief regions through semantic navigation and stable IDs.
- Every supported status category has visible text plus a non-color symbol or
  pattern cue; `createStatus` exposes the category without inventing one.
- Standard/large text scale persists when storage is available and falls back
  to session-local behavior when it is not; reduced motion remains independent.
- The cue-equivalent preference actually toggles only optional audio explanation
  copy; written result, observation, history, resolution, and debrief remain.
- Focus styling and targeted live regions are present without making the whole
  desktop a live region.
- Existing host authority, command strings, validation, transitions, hashes,
  replay, audio mapping, capture schema, and campaign semantics are unchanged.

## Non-goals

- Do not add browser automation, a dependency, new host/MCP schema, asset files,
  network/deployment support, or a local simulation.
- Do not claim human accessibility, usability, learning, engagement, or expert
  validity from static tests.
- Do not redesign the map, add launch/session creation, or perform opportunistic
  visual refactoring outside the named controls and status primitives.
- Do not run a second general code-review pass for this item; the user requires
  exactly one.

## Stop conditions

Stop and report if the change needs a new public API, a browser-only behavior
that cannot be contract-tested, more than the named production files, a new
dependency, or a broader first-slice redesign.

## Review checklist

- The diff is limited to the named presentation behavior and documentation.
- Status categories are host/fixture supplied and remain text-readable.
- Text scale and cue-equivalent settings cannot reach host commands or state.
- Essential written results remain visible under every setting.
- Landmark/skip targets, focus rules, responsive layout, and reduced-motion
  behavior coexist without destructive CSS changes.
- Tests cover the contract rather than only fixture-specific implementation text.

## Risk label

Risk: medium

Reason: The change affects several user-facing browser semantics and persisted
local settings, but it remains outside host state, public APIs, and simulation.
