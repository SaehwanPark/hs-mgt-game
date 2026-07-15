# Request Summary — Visual and Audio Phase 8 AI-Agent Testplay Readiness v0.12.24

## User request

Continue the visual/audio upgrade sequence after merged Phase 7 campaign
coverage. For each bounded SPEC item, design, implement, perform exactly one
code-review pass, open a PR, wait for CI, merge to `main`, and continue to the
next phase without stopping.

## Bounded target

Promote Phase 8 as a dependency-free readiness slice for reproducible AI-agent
testplay across the existing competitive, stabilization, and affiliation
presentation surfaces. Add first-run guidance, local settings/accessibility
review, recoverable retry/error states, a sanitized `gui-playtest-v1` interaction
capture contract, a role/task protocol, and deterministic diagnostic output.

## Explicit non-goals

- No browser automation dependency, network service, deployment, screenshot
  generator, or external agent/model orchestration.
- No simulation state, command, transition, formula, resolved input, effect
  queue, history/hash/replay semantics, or campaign observation change.
- No private state, true-state view, raw adapter payload dump, hidden future
  outcome, or client-side legality/causal inference.
- No human usability, lived accessibility, learning, engagement, calibration,
  policy-validity, or domain-expert claim.

## Sources reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 8 objective, work,
  deliverables, and exit criteria.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `SPEC.md`, `ARCHITECTURE.md`, and the harness
  team spec.
- Existing `gui/app.mjs`, `gui/audio.mjs`, `gui/index.html`, `gui/README.md`,
  Phase 5–7 contracts, audio recording sink, MCP playtest wrapper, and
  diagnostics scripts.

## Expected files

- `_workspace/01_evidence_map.md`, `_workspace/02_mechanism_design.md`,
  `_workspace/27_implementation_plan_visual_audio_phase8.md`, and final handoff.
- `gui/playtest.mjs`, `gui/app.mjs`, `gui/index.html`, `gui/README.md`, and
  `gui/PLAYTEST_GUIDE.md`.
- `scripts/diagnose_gui_playtests.py`, a fixture capture, and focused tests.
- Phase 8 contract doc, SPEC/architecture/README/changelog/lessons, QA, and
  v0.12.24 metadata.

## Validation target

- A first-run user sees a concise next action and can open settings without
  leaving the current presentation.
- Reduced motion, text-equivalent, mute, and audio-channel preferences are
  explicit local presentation state with stable defaults.
- Adapter and submission failures expose retry/recovery actions and do not
  fabricate transitions.
- The recorder emits only allowlisted UI, command, validation, audio,
  history/hash, semantic-snapshot, and failure fields with deterministic
  ordering and no raw hidden payload.
- The diagnostic script validates captures, classifies failure classes, and
  reports evidence lanes separately.
- `cargo fmt`, `cargo test`, Clippy, full Python tests, Node syntax, metadata,
  and diff checks pass before the one review/PR/merge cycle.

## Generic skills

Use simple-code-writing, spec-driven records, end-user-XP, and preferred
workflow. Project-local orchestration, evidence mapping, mechanism design, and
domain QA are required. The user instruction overrides the generic workflow's
default three-review loop: Phase 8 uses exactly one code-review pass.
