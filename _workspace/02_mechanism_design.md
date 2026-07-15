# Mechanism Design — Visual and Audio Phase 8 AI-Agent Testplay Readiness v0.12.24

## Goal and Roadmap Phase

Implement roadmap Phase 8 as a readiness boundary for reproducible AI-agent
interface tasks across the existing presentation clients. The deliverable is
capture/recovery infrastructure and a diagnostic protocol, not a new game
mechanism.

## Slice Boundary

The browser adds first-run guidance, local settings/accessibility controls,
recoverable read/submission errors, and an optional `gui-playtest-v1` recorder.
The recorder captures a declared session role/task/mode plus allowlisted UI,
command, validation, audio, history/hash, semantic-snapshot, and failure
events. A dependency-free Python diagnostic consumes capture JSON and emits
machine-readable evidence lanes and issue classes.

## Actors and Authority

The host/MCP server remains authoritative for campaign state, observation,
command legality, stochastic inputs, transitions, history, hashes, replay, and
debrief. The agent is a test participant whose role/task metadata is declared in
the capture; it is not a simulated institution. The browser owns local settings,
onboarding visibility, recovery buttons, semantic snapshot selection, and the
recorder buffer only.

## State, Beliefs, and Observations

Recorder fields are presentation evidence, not simulation state. Visible
observations may be summarized by stable labels, campaign/stage identifiers,
source labels, and committed history/hash metadata. Raw envelopes, true state,
resolved inputs, effect queues, private outcomes, DOM secrets, and model hidden
reasoning remain unavailable. A screenshot field, when supplied by an external
agent harness, is a reference string rather than browser-generated content.

## Commands, Events, and Effects

Onboarding and settings events are local and non-mutating. Retry invokes the
existing host read path. A submitted command is recorded only after the existing
client calls the canonical adapter submission path; rejected commands record the
error class and leave the current view/session unchanged. Audio events reuse the
existing recording sink shape and carry cue source/equivalent metadata.

The diagnostic script classifies `adapter_error`, `submit_rejected`,
`unsupported_schema`, `missing_control`, `semantic_gap`, `capture_invalid`, and
`task_incomplete` without recommending strategies or inferring causality.

## Strategic Interaction

Phase 8 does not add strategic actions or change actor responses. Role/task
profiles deliberately cover first-time onboarding, strategy-oriented decision
review, keyboard/reduced-motion access, mute/audio fallback, and invalid-action
recovery so that the same existing campaign semantics are exercised through
different interface paths.

## Assumptions and Parameters

- Schema: `gui-playtest-v1`.
- Capture ordering is append-only within one client session.
- Event payloads are JSON-safe, allowlisted, and bounded to visible metadata.
- Settings defaults are written-text complete: reduced motion off unless the
  browser preference says on, text equivalents on, audio muted/off until a
  user gesture, and all audio channels independently adjustable.
- Diagnostic output is deterministic for the same capture JSON and does not use
  wall-clock time, randomness, network, or model calls.

## Educational Debrief Hooks

The capture retains committed commands, validation outcomes, visible history,
state hashes, and debrief availability so an agent trace can be compared with
the host record. Diagnostics label the result as technical correctness,
interface-task proxy, strategic trace, document-grounded domain consistency, or
unresolved human question. They do not score learning or decision quality.

## Determinism and Replay Notes

Settings and recorder events are outside transitions and replay hashes. A
repeated host session with the same seed and commands must retain the existing
hash/replay result even when settings or recording are changed. Diagnostic JSON
sorts output lists by declared input order and uses fixed class labels.

## Open Questions

- Which future browser driver should supply real screenshots and accessibility
  tree snapshots without making the game bundle network-dependent?
- Which repeated semantic gaps should become Phase 9 product hypotheses?
- How should future captures link multiple browser sessions to one replay while
  preserving campaign-specific semantics?
