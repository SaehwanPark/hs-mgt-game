# Request Summary — Visual and Audio Phase 9 AI-Agent Evaluation and Revision v0.12.25

## User request

Continue the visual/audio upgrade sequence after merged Phase 8 readiness. For
each bounded SPEC item, design, implement, perform exactly one code-review pass,
open a PR, wait for CI, merge to `main`, and continue until the visual/audio
upgrade sequence is complete.

## Bounded target

Implement Phase 9 as a dependency-free, deterministic analyzer for repeated
`gui-playtest-v1` captures. Compare declared roles, tasks, campaigns, seeds,
interface/accessibility modes, event coverage, failure classes, and evidence
lanes; emit prioritized observable revision candidates and a product decision
log without scoring strategy or claiming human experience.

## Explicit non-goals

- No browser automation, model/network service, deployment, screenshot capture,
  or external agent orchestration.
- No simulation, Rust/MCP schema, command legality, transition, stochastic
  input, effect queue, history/hash/replay, debrief, or campaign observation
  change.
- No inferred causal graph, optimal strategy, balance/calibration conclusion,
  human usability/accessibility/learning/engagement claim, or domain-policy
  validity claim.
- No automatic product mutation from a capture; revisions are prioritized
  recommendations and explicit decisions for human/contributor review.

## Sources reviewed

- Phase 9 row, success/stop rules, and AI-agent playtest requirements in
  `docs/visual_audio_upgrade_proposal.md` and `SPEC.md`.
- Phase 8 `gui-playtest-v1` protocol, recorder, diagnostic script, fixture,
  and evidence limits.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `ARCHITECTURE.md`, and the harness team spec.

## Expected files

- `_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`,
  `_workspace/02_mechanism_design.md`, Phase 9 implementation plan, QA, and
  final handoff.
- `scripts/analyze_gui_playtests.py`, a deterministic matrix fixture, and
  focused tests.
- Phase 9 decision-log/protocol documentation, SPEC/architecture/changelog/
  README/lessons updates, and v0.12.25 metadata.

## Validation target

- The analyzer accepts a bounded set of valid captures, validates each through
  the Phase 8 contract, and produces stable sorted summaries for the same input
  files.
- Coverage and revision candidates cite observable capture fields and retain
  campaign/role/task/mode distinctions.
- Failure priorities are deterministic and do not become strategy scores or
  human-evaluation claims.
- A product decision log records decisions, evidence, hypotheses, limits, and
  deferred work; no recommendation changes simulation behavior automatically.
- Existing Phase 2–8 contracts and the full Rust/Python/Node/metadata checks
  remain green before the one review/PR/merge cycle.

## Generic skills

Use simple-code-writing, plan-designer, spec-driven records, end-user-XP, and
preferred workflow. Project-local orchestration, evidence mapping, mechanism
design, and domain QA are required. The user instruction overrides the generic
workflow's default three-review loop: Phase 9 uses exactly one code-review pass.
