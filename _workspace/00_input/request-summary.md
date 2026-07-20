# Request Summary — Visual/audio roadmap execution v0.12.34

## Classification and scope

- Track: presentation; Phase 0 foundation.
- Slice: product brief plus asset repository architecture and provenance gate.
- Target scenario: one month of `competitive-regional-v1`.
- Workflow: preferred branch/verification/PR handoff, one light independent code
  review, autonomous merge to `main`, then select the next bounded slice.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `SPEC.md`, and `ARCHITECTURE.md`.
- `docs/visual_audio_enhancement_roadmap.md` Phase 0 milestones 0.1 and 0.2.
- `docs/harness/health-policy-strategy-game/team-spec.md` and the existing
  visual/audio history through v0.12.33.

## Expected files

- Product brief/history, asset repository README, registry schemas/manifests,
  validation and credits scripts, generated credits, contributor checklist,
  focused tests, CI invocation, roadmap/SPEC/architecture/changelog/lesson
  bookkeeping, and required `_workspace` handoffs.

## Non-goals

- No new host DTO, command, transition, stochastic input, history/hash/replay,
  debrief, browser simulation state, third-party asset, recorded audio, or
  broad visual production.
- No human usability, lived accessibility, legal, calibration, balance, policy,
  or educational-effectiveness claim.
- No implementation of Phase 1+ runtime behavior in this slice.

## Acceptance and validation

- Product/style/audio/accessibility/licensing/authority decisions are explicit.
- Source/release directories and machine-readable registries exist.
- Validator fails closed for metadata, roles, IDs, hashes, licenses, approvals,
  and unregistered release files.
- Credits are deterministic and CI-checkable.
- Phase 0.1 and 0.2 checklists are checked only for demonstrated deliverables.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`,
  Python tests, metadata, docs links, Node syntax, and diff checks pass.
