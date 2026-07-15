# Request Summary — Phase 10 accessibility and visual-language hardening v0.12.26

## Scope

Implement the next bounded item left explicitly `Not Yet Done` in `SPEC.md`:
make the existing dependency-free GUI's first-run surface more usable through
keyboard landmarks and skip navigation, persistent text scaling, explicit
non-color status language, and a functional cue-equivalent preference. This
slice is derived from the accessibility, cognitive-accessibility, visual and
motion, and first-slice requirements in `docs/visual_audio_upgrade_proposal.md`.
The branch is `feat/visual-audio-phase10-accessibility-v0.12.26` and targets
version `0.12.26`.

## User and use context

The immediate users are a first-time executive player using a laptop browser,
an AI-agent test profile exercising semantic controls, and a contributor
reviewing the presentation boundary without a browser driver. Their job is to
find the current briefing, understand status language, reach a decision or
result panel, and keep written information available when audio or motion is
not useful.

## Non-goals

- No new host/MCP endpoint, browser automation, network call, dependency,
  screenshot, asset download, or deployment convention.
- No simulation, command legality, transition, stochastic input, history/hash,
  replay, debrief, campaign, or audio-source semantics change.
- No claim of human usability, lived accessibility, learning, engagement,
  calibration, balance, or policy validity; static and Node checks remain
  technical proxies.
- No local GUI simulation or fake campaign-start flow.
- Exactly one general code-review pass is required for this PR-equivalent
  change, overriding the generic workflow's three-pass default.

## Sources

- `SPEC.md`: visual-language, presentation-boundary, assets/accessibility,
  first-vertical-slice, and verification requirements still marked incomplete.
- `docs/visual_audio_upgrade_proposal.md`: Sections 6, 7, 9, 13, 14, 15, and
  16.
- `gui/index.html`, `gui/app.mjs`, `gui/audio.mjs`, `gui/playtest.mjs`.
- Existing GUI contract tests and `docs/visual-audio-phase8-ai-agent-testplay-v0.12.24.md`.
- `docs/harness/health-policy-strategy-game/team-spec.md` and canonical project
  docs.

## Expected files

- `_workspace/01_evidence_map.md`
- `_workspace/02_mechanism_design.md`
- `_workspace/03_domain_qa.md`
- `_workspace/29_implementation_plan_visual-audio-phase10-accessibility-v0.12.26.md`
- `_workspace/final/handoff.md`
- `gui/index.html`, `gui/app.mjs`, and focused GUI tests
- `docs/visual-audio-phase10-accessibility-v0.12.26.md`
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `gui/README.md`, `CHANGELOG.md`,
  `LESSONS.md`, and release metadata.

## Validation target

Verify the new semantic landmarks, skip link, focus treatment, status legend,
text-scale persistence, and cue-equivalent behavior with focused static tests
and Node syntax checks. Then run the full Python and Rust suites, clippy,
formatting, metadata, and whitespace checks. Domain QA must pass, followed by
exactly one general code-review pass and the PR/CI/merge workflow.
