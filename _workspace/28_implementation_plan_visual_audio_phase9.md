# Implementation Plan — Visual and Audio Phase 9 AI-Agent Evaluation and Revision v0.12.25

Status: Implemented and verified; exactly one code-review pass completed with
targeted fixes applied. Ready for PR handoff and merge.

## Task restatement

Add a dependency-free deterministic analyzer for repeated `gui-playtest-v1`
captures and document the resulting revision decisions while preserving the
Phase 8 capture contract, all simulation behavior, and the distinction between
technical proxies and human/domain evidence.

## Current understanding

- `scripts/diagnose_gui_playtests.py` is the authoritative single-capture
  validator and already emits failure classes/evidence lanes.
- `gui-playtest-v1` captures contain declared session metadata, ordered events,
  and derived evidence arrays; no browser driver is available.
- Phase 9 requires reproducible multi-role/seed/mode findings, prioritized
  revisions, and a product decision log, not automatic UI or simulation edits.

## Assumptions

- The analyzer can consume existing valid captures and synthetic protocol
  fixtures without adding a new schema or dependency.
- A missing or repeated event is reported as an observable artifact hypothesis,
  never as a human comprehension finding.
- If the Phase 8 validator cannot be imported or a new host field is required,
  stop and report the mismatch rather than duplicating validation logic.

## Minimal implementation plan

1. Move Phase 9 into `SPEC.md` Present and write the request/evidence/design
   handoffs and a protocol/decision-log document.
2. Add `scripts/analyze_gui_playtests.py` that discovers JSON files from paths,
   validates each through the existing diagnostics module, aggregates stable
   role/task/campaign/seed/mode coverage, and emits fixed-priority findings.
3. Add a small matrix fixture with repeated declared roles/modes and one
   observable recovery/semantic failure, plus focused tests for deterministic
   output, invalid capture propagation, coverage grouping, and no strategy or
   human scoring fields.
4. Update README/GUI guidance, architecture/spec/changelog/lessons, metadata,
   QA, and handoff with the actual evidence limits and next gate.
5. Run focused/full checks, perform exactly one code-review pass, fix review
   findings once, and stop after PR merge because Phase 9 closes the current
   visual/audio sequence.

## Files and functions likely to change

- `scripts/analyze_gui_playtests.py`: path discovery, capture loading,
  aggregation, deterministic finding prioritization, and CLI output.
- `tests/test_gui_playtest_analysis.py` and
  `tests/fixtures/gui_playtest_matrix/`: focused matrix contract tests/fixtures.
- `docs/history/initiatives/visual-audio/visual-audio-phase9-ai-agent-evaluation-v0.12.25.md`: protocol,
  findings, decision log, revision status, and evidence limits.
- `README.md`, `gui/README.md`, `ARCHITECTURE.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`, metadata, `_workspace/03_domain_qa.md`, and final handoff.

Avoid changing `src/`, `gui/app.mjs`, `gui/audio.mjs`, `gui/playtest.mjs`, or
the Phase 8 validator unless discovery proves the analyzer cannot consume the
existing contract; if so, stop and report why.

## Tests and checks

- `python3 -m unittest tests.test_gui_playtest_analysis tests.test_release_metadata`
- `python3 scripts/analyze_gui_playtests.py tests/fixtures/gui_playtest_matrix`
- Run the analyzer twice and compare output byte-for-byte.
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt -- --check`
- `cargo test --all -- --test-threads=1`
- `cargo clippy --all-targets -- -D warnings`
- Node syntax checks, release metadata, and `git diff --check`.

Expected result: stable matrix output with no hidden-state or strategy-score
fields, existing Phase 8 tests remain green, and the Rust suite is unchanged.

## Acceptance criteria

- The analyzer accepts a file or directory of Phase 8 captures and processes
  input paths in deterministic order.
- Each capture is validated through the Phase 8 validator; invalid captures
  remain visible as `capture_contract` findings and cannot be treated as valid
  task evidence.
- The report preserves campaign/role/task/seed/interface/accessibility
  dimensions and counts observable events/evidence without exposing payloads.
- Revision candidates have fixed priorities, source capture IDs, observable
  evidence, hypothesis text, and explicit evidence limits; no strategy or
  human score is emitted.
- The decision log records what is accepted, deferred, or unresolved and does
  not auto-mutate product or simulation behavior.
- Repeated runs over unchanged inputs produce identical JSON.

## Non-goals

- Do not add browser automation, external agents/models, network calls,
  screenshots, deployment, a new capture schema, or a new dependency.
- Do not change simulation/MCP behavior, GUI transitions, audio mappings,
  history/hash/replay, campaign semantics, or debrief outputs.
- Do not infer causality, optimal strategy, balance, calibration, policy
  validity, human usability, lived accessibility, learning, or engagement.
- Do not automatically edit the interface based on a fixture-only finding.

## Stop conditions

Stop and report if the analyzer requires a new public schema, duplicated
validator logic, simulation access, browser/network/model execution, more than
one production script plus the named docs/tests, or an interpretation that
cannot be stated as an observable artifact hypothesis.

## Review checklist

- The analyzer consumes only the Phase 8 validated allowlist and propagates
  invalid captures without leaking forbidden fields.
- Coverage grouping retains campaign and declared role/task/mode distinctions.
- Priorities are fixed, deduplicated, sorted, and not strategy scores.
- Output is stable across repeated runs and contains no timestamps/randomness.
- Decision-log claims match the evidence lane and explicitly preserve unresolved
  human/domain questions.
- Existing Phase 8 and Rust contracts remain untouched and green.

## Risk label

Risk: medium

Reason: The analyzer is outside runtime state but introduces a new evidence
aggregation contract whose sorting, invalid-input, and interpretation limits
must remain reproducible and explicit.
