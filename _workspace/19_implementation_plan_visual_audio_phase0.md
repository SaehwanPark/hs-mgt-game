# Operational Coding Plan — Visual/Audio Phase 0 Alignment v0.12.16

## Task restatement

Complete Phase 0 of the visual/audio Future track by documenting and testing an
approved presentation boundary for one `competitive-regional-v1` month while
preserving the existing Rust simulation, MCP contract, CLI behavior, replay
history, and state hashes.

## Current understanding

- The current `gui/` proof renders injected MCP-shaped strings and delegates
  submission through `HsMgtGameAdapter`; it does not own simulation state.
- `SessionEnvelope`, `TransitionSummary`, and `EndSessionEnvelope` expose the
  current actor-visible session, committed transition, and debrief surfaces.
- Competitive observations already contain workforce, capacity, access,
  operating, market, policy, consultant, and information-gap signals, but the
  MCP boundary currently serializes them as lines rather than presentation DTOs.
- The proposal requires Phase 0 to deliver a boundary decision, first-slice
  experience contract, DTO inventory, wireframe, audio catalog, asset policy,
  and any needed ADR.

## Assumptions

- The first presentation client remains a browser-native static client using
  semantic HTML/CSS/ES modules and native SVG; no framework or bundler is
  required by the current proof.
- The host/MCP boundary remains authoritative for command legality, stochastic
  resolution, transitions, history, hashes, and debriefs.
- Existing MCP strings are valid inventory evidence, not a claim that typed
  presentation DTOs already exist.

If any assumption is false, stop and report the mismatch before editing runtime
code or selecting a new dependency.

## Minimal implementation plan

1. Record the Phase 0 evidence, mechanism boundary, and implementation plan in
   the `_workspace/` handoff files.
2. Add one alignment document containing the one-month experience contract,
   current-surface DTO inventory, wireframe, technology decision, audio catalog,
   asset policy, hidden-state exclusions, and exit evidence.
3. Add one ADR for the browser-native thin-client and adapter boundary, and link
   it from the ADR index and architecture notes.
4. Add a dependency-free documentation contract test covering the Phase 0
   deliverables and the absence of runtime/asset changes.
5. Promote only Phase 0 in `SPEC.md`, bump metadata to `0.12.16`, and record the
   next gate as Phase 1 static desktop work.
6. Run focused documentation tests, metadata checks, formatting, the full Rust
   test suite, and one independent code-review pass.

## Files and functions likely to change

- `docs/visual-audio-phase0-alignment-v0.12.16.md`: new Phase 0 decision and
  deliverables.
- `docs/decision-records/0011-browser-native-presentation-client.md`: accepted
  technology and authority-boundary decision.
- `docs/decision-records/README.md`: link ADR-0011.
- `ARCHITECTURE.md`: mark the Phase 0 boundary as accepted while retaining the
  implementation-gated status of later presentation phases.
- `SPEC.md`: close/promote Phase 0 and keep Phases 1–9 sequentially gated.
- `tests/test_visual_audio_phase0.py`: static contract checks for the document,
  ADR, and unchanged-runtime boundary.
- `CHANGELOG.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, `LESSONS.md`, and
  `_workspace/` handoffs: release metadata and durable project state.

No Rust production function should change in this slice.

## Tests and checks

Run:

```text
python3 -m unittest tests/test_visual_audio_phase0.py
python3 scripts/check_release_metadata.py
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
```

Expected result:

- The Phase 0 contract test and metadata checker pass.
- No Rust source, scenario, replay, or ruleset files are changed.
- Formatting, clippy, and the full serial test suite pass.

## Acceptance criteria

- The alignment document names the client technology, authoritative host
  boundary, one-month flow, actor-visible sources, hidden-state exclusions,
  wireframe, audio catalogs, asset policy, and explicit non-goals.
- Every first-slice action is one of the existing competitive command families;
  previews show cost, delay, visible constraints, and uncertainty without
  promising a realized outcome.
- Audio and music mappings use only visible or committed presentation events,
  have visual/text equivalents, and cannot affect simulation history or hashes.
- The ADR index and architecture record the decision, while later phases remain
  gated by evidence.
- Version metadata is consistently `0.12.16`.

## Non-goals

- Do not add Rust DTOs, transitions, commands, randomness, balance values, or
  scenario fields.
- Do not implement the static desktop, live adapter, action workflow, animation,
  audio playback, asset files, packaging, deployment, or human usability study.
- Do not claim AI testplay proves human usability, engagement, lived
  accessibility, learning, calibration, or policy validity.
- Do not rewrite the existing GUI proof or reformat unrelated files.

## Stop conditions

Stop and report if:

- Phase 0 requires a new runtime API or dependency rather than documentation of
  the existing host boundary.
- The current MCP/CLI surface cannot identify an actor-visible source for a
  required first-slice value.
- A proposed wireframe requires hidden state, GUI-only rules, or a second
  transition path.
- The change needs more than the named documentation/test files or exposes an
  unrelated test failure.

## Review checklist

- The diff closes only Phase 0 and does not imply later phases are implemented.
- Every document claim is traceable to current code, canonical docs, or a labeled
  game abstraction.
- Hidden state, actor utility, organizational outcomes, social welfare, and
  educational evaluation remain distinct.
- The audio catalog includes visual equivalents, deterministic visible sources,
  mute behavior, and restrained repetition.
- The test checks the contract rather than implementation-only formatting.

## Risk label

Risk: medium

Reason: The slice is documentation-only but establishes a project-wide
presentation boundary and technology decision that later GUI work must follow.

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.
