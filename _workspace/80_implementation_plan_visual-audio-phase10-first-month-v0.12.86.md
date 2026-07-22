# Implementation Plan — Visual/audio Phase 10.1 first-month slice v0.12.86

## Task restatement

Add a machine-checkable acceptance contract for the integrated first-month
`competitive-regional-v1` visual/audio slice and reconcile the Phase 10.1
technical checklist with the existing live GUI, host contracts, deterministic
resolution, replay, accessibility, audio, and provenance evidence.

## Current understanding

- The live GUI already mounts the regional board, actor/facility surfaces,
  semantic containers, first-month flow, resolution sequence, consequence links,
  optional audio, and campaign coverage.
- Host/Rust contracts already expose actor-visible regional-world and resolution
  DTOs, committed history, replay hashes, and observation timing.
- Existing focused tests cover the individual surfaces, but the roadmap has no
  single acceptance test that binds every Phase 10.1 feature bullet to evidence.
- Phase 10.2 first-time-user evaluation, accessibility quality review, audio
  fatigue feedback, and educational usability remain human gates.

## Assumptions

- “Feature complete” means the technical first-month path is present and
  contract-tested; it does not claim a new-player evaluation or polished human
  comprehension result.
- Existing modules are the production surfaces; no duplicate proof-only runtime
  path or new asset is needed.
- The integrated contract remains thin-client and host-authority preserving.

## Minimal implementation plan

1. Inspect the Phase 10.1 checklist and existing GUI/host/audio tests to define
   exact labels and source evidence.
2. Add `tests/test_phase10_first_month.py` with exact checklist assertions,
   source/authority boundary checks, and deterministic first-month module
   probes.
3. Update the roadmap, request, presentation contract, QA, specification,
   architecture, README, changelog, lessons, version projections, and CI.
4. Run focused/full Python and Rust tests, asset/release/documentation checks,
   JavaScript syntax, formatting, Clippy, and diff checks.
5. Use exactly the existing sole reviewer before PR merge; keep Phase 10.2
   human evaluation explicitly open.

## Files and functions likely to change

- `tests/test_phase10_first_month.py`: integrated Phase 10.1 evidence.
- `.github/workflows/ci.yml`: focused first-month acceptance test.
- `docs/visual_audio_enhancement_roadmap.md`: Phase 10.1 technical checklist
  and v0.12.86 evidence.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`:
  target contract and QA.
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `CHANGELOG.md`, `LESSONS.md`,
  `Cargo.toml`, `Cargo.lock`, `tests/test_release_metadata.py`, and generated
  credits/notices/version projections.

No runtime, host, simulation, asset, registry, release hash, or manifest
implementation change is authorized unless the acceptance test exposes a
concrete existing defect.

## Tests and checks

- `python3 -m unittest tests.test_phase10_first_month`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets -- -D warnings`
- `cargo fmt --check`
- asset/security/release/credits/version checks
- documentation links, JavaScript syntax, and `git diff --check`

## Acceptance criteria

- Every Phase 10.1 technical checklist label is explicitly checked only when
  the live source/tests provide evidence.
- A deterministic first-month probe covers start/inspect/draft/validate/
  submit/resolution/continue, visible music classification, and skip/replay
  contracts without reading hidden state or changing host authority.
- The regression test fails if a Phase 10.1 technical label or evidence marker
  disappears, or if browser code gains forbidden simulation/network authority.
- Documentation distinguishes technical completeness from Phase 10.2 human
  evaluation, accessibility quality, audio fatigue, and educational usability.

## Non-goals and stop conditions

- Do not add new assets, external dependencies, host fields, simulation rules,
  hidden-state projections, screenshot claims, or human-evaluation conclusions.
- Stop if any feature bullet is not supported by current code/tests, or if a
  real runtime defect requires a separate implementation slice.

## Review checklist

- Exact checklist labels and source evidence are asserted.
- First-month probe is deterministic and read-only.
- Phase 10.2 human gates remain explicit.
- Exactly one existing code reviewer inspects the final diff.

## Risk label

Risk: low to medium

Reason: the slice strengthens an existing integration boundary and roadmap
evidence without changing runtime behavior or authority.
