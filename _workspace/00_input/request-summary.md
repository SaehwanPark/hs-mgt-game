# Request Summary — Visual and Audio Phase 4 Resolution/Causal Feedback v0.12.20

## Scope

- Continue the merged visual/audio track after Phase 3 contextual action
  submission.
- Make one committed `competitive-regional-v1` month understandable through a
  host-supplied resolution sequence, operating/resource breakdown, and direct
  committed-effect presentation.
- Let the browser play, pause, skip, and review the presentation locally while
  replay lookup remains a non-mutating host read.
- Preserve actor-visible information boundaries, explicit uncertainty, replay
  hashes, and version `0.12.20` for the implementation PR.

## Sources

- `docs/visual_audio_upgrade_proposal.md` Phase 4 requirements and exit gate.
- Merged Phase 0–3 alignment, architecture, GUI, MCP, and action contracts.
- Existing `CompetitiveTransition`, `TransitionSummary`, `PlayerObservation`,
  `AttributedEffect`, `ReadOnlyPresentationEnvelope`, and replay/history code.
- Canonical proposal, roadmap, design principles, harness team spec, SPEC,
  architecture, changelog, lessons, and versioning policy.

## Expected files

- Typed read-only resolution DTO and `get_resolution` MCP/session tool.
- Browser resolution renderer integrated after a successful graphical submit,
  with local step, pause, skip, review, and reduced-motion behavior.
- Phase 4 contract document, SPEC/architecture/version records, tests, evidence,
  domain QA, lessons, and final handoff.

## Validation target

- Resolution steps are sourced from committed transition/history data and
  actor-visible before/after observations.
- Operating and resource changes are explicit before/after values; causal
  presentation uses direct host effects or documented display comparison only.
- Replay lookup does not advance, rewrite, or alter state, history, or hashes.
- Textual results are available immediately and remain complete when paused,
  skipped, reduced-motion, or refreshed.
- Full Python and Rust verification plus exactly one code-review pass and CI.

## Explicit non-goals

No new transition formula, stochastic input, causal inference engine, hidden
true-state field, private rival reveal, audio playback, asset pipeline, broad
replay UI, other campaign support, mobile redesign, deployment, or human-
usability claim. No browser-owned outcome calculation or second simulation.

## Global workflow

Use the repo orchestrator, evidence mapper, mechanism designer, domain QA, and
end-user experience workflow for the bounded resolution surface; use global
simple-code/spec-driven/plan-design skills and the preferred workflow with
exactly one code reviewer. Implement on a feature branch, verify, open a PR,
review once, merge into `main`, and then design Phase 5 audio only after the
Phase 4 gate closes.
