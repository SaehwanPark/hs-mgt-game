# Request Summary — Visual and Audio Phase 7 Campaign Coverage v0.12.23

## User request

Continue the visual/audio upgrade sequence after the merged Phase 6 regional
world slice. Follow the repository workflow: bounded design, implementation,
exactly one code-review pass, PR handoff, CI, merge to `main`, then repeat for
the next phase.

## Bounded target

Promote Phase 7 for a shared campaign-coverage presentation contract and browser
router covering the existing `stabilization-v1` and
`regional-affiliation-v1` campaigns. Keep campaign-specific observations,
stages, decisions, commitments, actor responses, pending obligations, hashes,
and debrief meanings intact.

The host supplies an additive, non-mutating `campaign-coverage-v1` envelope.
The browser renders shared stage/briefing/metric/history/debrief primitives,
campaign-specific actors and processes, and host-shaped decision forms. Submit
still uses the existing canonical `submit_turn` boundary; rejected commands
remain recoverable and non-mutating.

## Explicit non-goals

- No competitive campaign regression or replacement of the Phase 6 regional
  world projection.
- No new simulation actors, commands, state variables, transition formulas,
  stochastic-input exposure, true state, or replay semantics.
- No flattening stabilization into competitive monthly operations or affiliation
  into a generic market/relationship dashboard.
- No human usability, accessibility, learning, policy-validity, or domain-expert
  claim; no external assets, network calls, deployment, or mobile redesign.

## Sources reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 7 campaign-coverage objective,
  stabilization/affiliation work, deliverables, and exit criteria.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `SPEC.md`, and the harness team spec.
- Existing `SessionEnvelope`, stabilization `Observation`/commands/history,
  `AffiliationObservation`/stage/commands/history, debrief functions, and the
  merged Phase 1–6 presentation contracts.

## Expected files

- `_workspace/01_evidence_map.md`, `_workspace/02_mechanism_design.md`,
  `_workspace/26_implementation_plan_visual_audio_phase7.md`, and final handoff.
- `src/mcp/campaign_coverage.rs`, MCP session/server/module wiring, and tests.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`, and campaign-coverage tests.
- Phase 7 contract, SPEC/architecture/README/changelog/lessons, and v0.12.23
  metadata.

## Validation target

- Host coverage reads are typed, actor-visible, non-mutating, schema-versioned,
  and exclude true state/resolved inputs.
- Stabilization and affiliation retain distinct stage, briefing, decision,
  actor, obligation, and debrief semantics.
- Browser forms are host-shaped, keyboard reachable, recoverable on rejection,
  and keep visual/text results complete when audio is muted or unavailable.
- `cargo fmt`, `cargo test`, Clippy, full Python tests, JavaScript syntax,
  metadata, and diff checks pass before the one review/PR/merge cycle.

## Generic skills

Use simple-code-writing for the implementation, code-reviewer exactly once,
spec-driven records, and end-user-XP review. Project-local orchestration,
evidence mapping, mechanism design, and domain QA are required.
