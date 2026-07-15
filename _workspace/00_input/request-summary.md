# Request Summary — Visual and Audio Phase 3 Contextual Action Submission v0.12.19

## Scope

- Promote the next SPEC item after the merged Phase 2 read-only viewer.
- Let an executive build, revise, validate, and submit one competitive month
  graphically without learning CLI syntax.
- Use host-supplied action catalog/validation data and the existing canonical
  `submit_turn` transition boundary.
- Preserve explicit costs, delays, constraints, uncertainty, rejection
  atomicity, observation boundaries, and version `0.12.19`.

## Sources

- `docs/visual_audio_upgrade_proposal.md` Phase 3 requirements.
- Phase 0 alignment, Phase 1 static desktop, Phase 2 read-only projection,
  ADR-0011, and merged GUI/MCP surfaces.
- Existing competitive command parser/specs, command costs, validator,
  transition boundary, MCP tests, CLI tests, and replay/golden tests.
- Canonical proposal, roadmap, design principles, harness team spec, SPEC,
  architecture, changelog, lessons, and versioning policy.

## Expected files

- Typed Rust action catalog/validation DTOs and non-mutating MCP reads.
- Browser contextual action builder, draft batch/revision/removal, validation,
  retry, and host-owned submit flow.
- Phase 3 contract document, SPEC/architecture/version records, tests, evidence,
  domain QA, lessons, and final handoff.

## Validation target

- Canonical command equivalence and host-derived costs/constraints.
- Non-mutating valid/invalid validation and rejected-submit atomicity.
- Graphical draft workflow, no-submit-before-validation, error recovery,
  explicit uncertainty, syntax, metadata, and no-network/no-asset checks.
- Full Python and Rust verification plus one code-review pass and CI.

## Explicit non-goals

No browser formulas, second parser, new command family, hidden outcome forecast,
resolution animation, causal overlay, audio, assets, replay playback, campaign
expansion, mobile support, deployment, or human-usability claim. No transition
path other than the existing host/MCP `submit_turn` boundary.

## Global workflow

Use the repo orchestrator and end-user experience workflow for the action
builder, the global simple-code/spec-driven/plan-design skills, and the
preferred workflow with exactly one code reviewer. Implement on a feature
branch, verify, open a PR, review once, merge into `main`, and then design
Phase 4.
