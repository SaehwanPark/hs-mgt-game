# Operational Coding Plan — Visual/Audio Phase 1 Static Desktop v0.12.17

## Task restatement

Extend the dependency-free `gui/` proof into a static, injected-data executive
desktop prototype for one `competitive-regional-v1` observation while preserving
the existing adapter submission path and keeping all simulation authority outside
the browser.

## Current understanding

- `gui/index.html` currently presents observation lines, legal command hints,
  committed history, and debrief in a two-column console.
- `gui/app.mjs` renders an injected `demoEnvelope`, performs only empty-input
  checking, and delegates non-empty submissions to `HsMgtGameAdapter.submitTurn`.
- The Phase 0 decision accepts browser-native HTML/CSS/ES modules and native SVG,
  with no new framework, bundler, network call, or asset pipeline.
- Phase 1 requires an executive header, regional schematic, system/facility cards,
  selected-entity detail, contextual action panel, executive briefing,
  pending-effects timeline, monthly result view, responsive layout, design tokens,
  entity/status language, and a usability review checklist.

## Assumptions

- The prototype may add a clearly labeled `presentation_fixture` to the injected
  demo envelope; it is display data and not a second simulation state.
- Existing live envelopes remain renderable through the current observation,
  legal-command, history, and debrief fallback paths.
- Phase 1 is static/injected-data work. Buttons may navigate/select fixture data,
  but action resolution and typed live submission remain later-phase work.
- The primary user is an executive or first-time reviewer trying to locate the
  next institutional pressure quickly on a laptop or desktop, without reading
  raw JSON or CLI output.

If any assumption is false, stop and report the mismatch before adding a live
adapter, dependency, or simulation-facing API.

## Minimal implementation plan

1. Add a Phase 1 experience document and update the workspace request framing
   with the target user, information architecture, fixture boundary, and review
   checklist.
2. Replace the console-only layout with semantic, responsive desktop regions:
   header metrics, briefing, regional map, system/facility cards, selected detail,
   action previews, pending processes, monthly result, history, and debrief.
3. Add a structured display-only `presentation_fixture` beside the existing
   MCP-shaped fallback data. Render it with text plus icons/status labels and
   preserve the existing adapter-owned command form.
4. Add entity selection/navigation within fixture data only; do not submit a
   GUI-only command or calculate a simulation result.
5. Add static contract tests for required regions, visible information,
   responsive tokens, selection hooks, hidden-state exclusions, no external
   assets/network calls, and JavaScript syntax.
6. Bump metadata to `0.12.17`, promote Phase 1 in `SPEC.md`, and keep Phase 2–9
   work explicitly gated.

## Files and functions likely to change

- `gui/index.html`: semantic desktop regions, design tokens, responsive layout,
  icons/status language, and accessible navigation hooks.
- `gui/app.mjs`: `presentation_fixture`, fixture rendering helpers,
  `renderPresentation`, and selection-only client state; preserve
  `renderEnvelope`, `validateCommand`, and `createThinClient` behavior.
- `gui/README.md`: describe the static desktop fixture and Phase 1 review scope.
- `docs/visual-audio-phase1-static-desktop-v0.12.17.md`: experience contract,
  fixture mapping, checklist, limitations, and exit evidence.
- `tests/test_gui_static_desktop.py`: Phase 1 source contract tests.
- `SPEC.md`, `README.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`,
  `tests/test_release_metadata.py`, `LESSONS.md`, and `_workspace/` handoffs:
  state and version alignment.

Avoid editing Rust, MCP, scenario, replay, ruleset, asset, or audio files.

## Tests and checks

Run:

```text
python3 -m unittest tests/test_gui_thin_client.py tests/test_gui_static_desktop.py
python3 -m unittest discover -s tests -p 'test_*.py'
node --check gui/app.mjs
python3 scripts/check_release_metadata.py
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
```

Expected result:

- Static and existing GUI contracts pass, including the adapter boundary.
- The new desktop is syntactically valid and has no external assets/network.
- Full repository checks remain green; no Rust behavior changes.

## Acceptance criteria

- A fixture-only desktop visibly contains executive metrics, briefing, regional
  schematic, system/facility cards, selected detail, action preview, pending
  timeline, monthly result, committed history, and debrief.
- A reviewer can locate cash/margin, workforce, capacity, access/quality, and
  public rival information from labeled panels without raw JSON/CLI output.
- Status meaning uses text plus icon/shape/pattern; the layout has design tokens
  and a responsive single-column fallback for laptop widths.
- Selecting a fixture entity changes only presentation detail and cannot advance
  simulation or create a GUI-only command.
- Existing live envelope fallback and adapter submission semantics remain intact.
- The Phase 1 document records the user context, fixture source mapping,
  usability checklist, hidden-state exclusions, and explicit non-goals.
- Version metadata is consistently `0.12.17`.

## Non-goals

- Do not implement live read-only integration, typed DTOs, action forms, command
  previews backed by validation, monthly resolution animation, audio playback,
  assets, replay visualization, or campaign expansion.
- Do not add a frontend dependency, build step, server, network request, or
  browser-owned simulation state.
- Do not claim human usability, engagement, lived accessibility, learning, or
  domain validity from static source checks.
- Do not remove the existing command form or change adapter validation behavior.

## Stop conditions

Stop and report if:

- Rendering the required panels needs hidden `CompetitiveWorldState` fields or a
  new MCP/Rust projection.
- The fixture needs formulas, stochastic outcomes, live networking, or a new
  dependency.
- The desktop requires changing command semantics or the existing adapter path.
- More than the named GUI/docs/test/metadata files need production edits.
- A failing check is unrelated to the Phase 1 surface.

## Review checklist

- Every required Phase 1 region has a visible heading and fixture source.
- Finance/workforce/capacity/access/rival information is findable without raw
  output and does not expose hidden/private fields.
- Responsive rules, semantic labels, keyboard selection, and status text are
  present; color is not the sole status channel.
- Selection is non-authoritative and the current live envelope path is preserved.
- The diff does not accidentally implement Phase 2+ behavior or add assets.

## Risk label

Risk: medium

Reason: The slice is browser-only but changes the primary information hierarchy
and user-facing interpretation of the existing actor-visible session surface.

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.
