# Operational Plan — Visual/audio first-month contract audit v0.12.30

**Status:** Implemented; verification and one-review handoff in progress

## Task restatement

Implement a deterministic, dependency-free repository audit that proves the
bounded technical `competitive-regional-v1` first-month visual/audio contract
from current GUI source and focused tests, then align the active spec and
release records while preserving all runtime behavior.

## Current understanding

- Phase 0–13 presentation surfaces are present on merged `main` and PR #180
  closed the latest first-month continuity rail.
- `SPEC.md` still marks the first competitive vertical slice and several track
  summaries as incomplete even though the source and focused tests cover the
  bounded technical contract.
- The repository uses dependency-free Python/Node contract tests and a release
  metadata checker.
- The audit must not claim browser transport, human usability, lived access,
  learning, engagement, calibration, balance, policy validity, or domain
  expertise.

## Assumptions

- `gui/app.mjs`, `gui/audio.mjs`, `gui/first-month.mjs`, and `gui/visual.mjs`
  are the authoritative browser source surfaces for the audit.
- Existing focused GUI test modules are the authoritative technical evidence
  lanes; no new dependency or browser driver is required.
- Version `0.12.30` is the next patch release under the repository policy.

If any assumption is false, stop and report the mismatch before editing runtime
code.

## Minimal implementation plan

1. Add `scripts/audit_visual_audio_contract.py` with a frozen contract manifest,
   source/test marker checks, required phase-document checks, boundary exclusions,
   stable sorting, and JSON output.
2. Add focused tests for a complete audit and for fail-closed missing-marker,
   missing-test, and forbidden-boundary cases.
3. Run the audit, record its JSON evidence in a versioned document, and update
   `SPEC.md`, `README.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, Cargo metadata,
   lessons, and the workspace handoffs.
4. Run Python, Node, Rust, release-metadata, formatting, Clippy, and diff checks.
5. Stop if the audit cannot prove every required surface without broadening into
   browser automation, new host APIs, assets, or simulation changes.

## Files and functions likely to change

- `scripts/audit_visual_audio_contract.py`: audit manifest and JSON projection.
- `tests/test_visual_audio_contract_audit.py`: complete/fail-closed audit tests.
- `docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md`: evidence and limits.
- `SPEC.md`, `README.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`:
  closure and release alignment.
- `Cargo.toml`, `Cargo.lock`, `tests/test_release_metadata.py`: patch version.
- `_workspace/00_input/`, `_workspace/01_evidence_map.md`,
  `_workspace/02_mechanism_design.md`, `_workspace/03_domain_qa.md`,
  `_workspace/final/handoff.md`: durable handoff state.

Do not edit GUI runtime files unless the audit exposes a concrete missing
contract. If it does, stop and report before widening the plan.

## Tests and checks

- `python3 -m unittest tests/test_visual_audio_contract_audit.py`
- `python3 -m unittest discover -s tests -p 'test_gui*.py' -q`
- `python3 -m unittest discover -s tests -q`
- `node --check gui/app.mjs` and changed modules
- `python3 scripts/check_release_metadata.py`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `git diff --check`

Expected result: all focused and full checks pass, and the audit JSON reports
`status: complete` with no missing evidence or boundary violations.

## Acceptance criteria

- The audit schema and JSON output are deterministic and dependency-free.
- Every required first-month surface has existing source and focused-test
  evidence; missing evidence and forbidden markers fail closed.
- The audit distinguishes technical/interface-task evidence from unresolved
  human and policy questions.
- SPEC and release records no longer describe the bounded technical sequence as
  unimplemented, while deferred work remains explicit.
- No Rust/MCP, simulation, stochastic, history/hash/replay, debrief, network,
  asset, audio-source, or browser-transport behavior changes.

## Non-goals

- Do not add browser automation, network calls, dependencies, screenshots, or
  real audio assets.
- Do not change command legality, host DTOs, transition behavior, or GUI runtime
  flow.
- Do not make human usability, accessibility lived experience, learning,
  engagement, calibration, balance, policy, or domain-expert claims.
- Do not remove the deferred proposal queue or broaden into mobile, geography,
  city-building, or production deployment.

## Stop conditions

Stop and report if:

- a required surface lacks concrete current source/test evidence;
- the audit requires importing or executing the simulation or network;
- more than the named audit/docs/test/version files need runtime edits; or
- any unrelated test or metadata failure appears.

## Review checklist

- The manifest maps each obligation to a real source and focused test.
- Fail-closed behavior is tested with missing files/markers and forbidden
  boundary markers.
- The JSON output contains no hidden state, model reasoning, timestamps, or
  network-dependent values.
- SPEC closure language matches the audit and preserves evidence limits.
- The diff contains no runtime or dependency changes beyond the plan.

## Risk label

Risk: medium

Reason: The change is documentation/tooling-only but changes the project's
completion claim and release metadata, so evidence scope and overclaiming need
careful review.
