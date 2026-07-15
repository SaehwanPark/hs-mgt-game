# Mechanism Design — Visual and Audio Phase 9 AI-Agent Evaluation and Revision v0.12.25

## Goal and Roadmap Phase

Close the visual/audio Phase 9 gate with a narrow deterministic comparison
surface for repeated `gui-playtest-v1` artifacts and an explicit product
decision log. The output is triage evidence and bounded revision routing, not a
new simulation mechanism or an agent evaluator.

## Slice Boundary

The analyzer accepts one or more JSON capture paths or a directory, validates
each capture with the Phase 8 contract, and emits a JSON report containing:
coverage dimensions; per-capture event/failure/evidence counts; valid/invalid
status; stable comparisons; and prioritized revision candidates. A Phase 9
document records the matrix, decisions, hypotheses, limits, and next gate.

## Actors and Authority

The capture producer is an external test participant with declared role/task
metadata, not a simulated institution. The Phase 8 validator owns capture
schema/allowlist authority. The Phase 9 analyzer owns only aggregation and
priority labels. Product/contributor reviewers own any decision to revise the
browser. The host/core remains authoritative for campaign state, legality,
stochastic inputs, transitions, history, replay, hashes, and debriefs.

## State, Beliefs, and Observations

Analyzer input is immutable artifact data: session metadata, ordered event
types, failure classes, and Phase 8 evidence lanes. It does not read adapter
payloads, true state, resolved inputs, effect queues, private actions, or model
hidden reasoning. It records declared coverage as metadata, not as proof that
an agent had a particular belief or that a person understood a mechanism.

## Commands, Events, and Effects

No command is submitted and no transition occurs. The analyzer counts existing
`command_submitted`, `validation_result`, `audio_cue`, `history_observed`,
`semantic_snapshot`, `failure`, and `task_completed` events. It emits fixed
revision categories such as `capture_contract`, `task_recovery`,
`control_coverage`, and `evidence_completeness`; these are recommendations,
not game effects.

## Strategic Interaction

There is no new strategic interaction. Existing command text and history/hash
presence may be summarized as a strategic-trace evidence lane, but the analyzer
does not compare utilities, infer optimal actions, rank strategies, or pool
campaign-specific institutional outcomes.

## Assumptions and Parameters

- Input schema: `gui-playtest-v1` validated by
  `scripts/diagnose_gui_playtests.py`.
- Priority order is fixed: capture-contract errors, task/recovery gaps,
  control/semantic gaps, then evidence-completeness gaps.
- Findings are deduplicated by category, task, and observable issue code and
  sorted by priority/category/source key.
- No timestamps, random sampling, network, model, browser, or simulation calls
  are used.

## Educational Debrief Hooks

The product decision log preserves the difference between a trace showing a
command/history and a claim about decision quality or learning. Each candidate
revision includes the observable evidence, a bounded hypothesis, an owner/
status decision, and the human/domain question that remains unresolved.
Existing campaign debriefs are not rewritten by this analyzer.

## Determinism and Replay Notes

Input paths are normalized to stable relative/display names, captures are
processed in sorted order, and JSON keys/lists are emitted with stable sorting.
The analyzer never replays a session and cannot alter state hashes or replay
artifacts. Running it twice on unchanged captures must produce byte-identical
JSON.

## Open Questions

- Whether future authorized agent runs need a separate model/version field in
  the capture schema or can remain an external harness concern.
- Whether a repeated task failure warrants a UI revision after real browser or
  human evidence is available.
- Which Phase 10/post-release work, if any, should follow this completed gate.
