# Visual and Audio Phase 8 — AI-Agent Testplay Readiness

Status: Implemented, verified, and reviewed once on the Phase 8 branch.

Phase 8 prepares the dependency-free browser presentation for reproducible
AI-agent interface tasks. It adds onboarding, local settings/accessibility
review, recovery controls, an allowlisted interaction capture contract, role and
task guidance, and deterministic diagnostics. It does not evaluate people or
change the simulation.

## Readiness contract

`gui-playtest-v1` is an optional browser-side artifact with:

- declared campaign, seed/viewport when supplied, agent role, task, interface
  mode, accessibility mode, and capture method;
- ordered visible interaction events such as onboarding, settings, retry,
  semantic snapshot, command submission, validation, and recovery;
- sanitized command text, validation outcomes, audio cue source/equivalent,
  committed history/hash metadata, and failure classes;
- optional externally supplied screenshot references, never screenshots generated
  by or uploaded from the game itself; and
- an evidence-lane summary separating technical correctness, interface-task
  proxy, strategic trace, document-grounded domain consistency, and unresolved
  human questions.

The recorder rejects or omits raw adapter payloads, true state, resolved inputs,
effect queues, private rival actions, hidden DOM payloads, and model hidden
reasoning.

## Browser behavior

The first-run panel states the current campaign role and suggests one next
action. The settings panel exposes reduced motion, written equivalents, mute,
and independent audio channel preferences. Preferences are local and do not
alter the host session. Adapter and submission errors show an actionable
recovery status; retry invokes the existing read path and cannot submit a
command.

All written result/debrief content remains available when audio is muted,
reduced notifications are enabled, reduced motion is active, or browser audio
is unsupported. Keyboard operation and semantic labels remain the primary
interaction path.

## Roles and tasks

The protocol defines bounded roles rather than claiming cognitive profiles:

| Role | Task | Required paths |
| --- | --- | --- |
| first-time | identify role, briefing, and first valid decision | onboarding, campaign coverage, canonical submit |
| strategy-review | inspect visible tradeoffs and committed result | history/hash, briefing, decision, debrief |
| access-check | complete a task with presentation constraints | keyboard, reduced motion, written equivalents, mute |
| recovery-check | recover from a rejected or unavailable read | invalid command, error text, retry, unchanged session |

Each capture declares the role/task and records completion or failure without
turning the outcome into a score or strategy recommendation.

## Diagnostics and failure classes

`diagnose_gui_playtests.py` validates the schema, rejects forbidden fields, and
classifies only observable artifact conditions:

- `adapter_error`
- `submit_rejected`
- `unsupported_schema`
- `missing_control`
- `semantic_gap`
- `capture_invalid`
- `task_incomplete`

The diagnostic output is deterministic for the same JSON input and never calls
the network, a model, or the game transition engine.

## Source and authority map

| Evidence | Source | Authority |
| --- | --- | --- |
| campaign/stage/briefing | existing host presentation or campaign coverage | host read |
| command/validation/rejection | existing client adapter and canonical submit path | host/core |
| history/hash/debrief availability | existing committed presentation/history | host/core |
| audio cue/source/equivalent | existing generated audio recording sink/catalog | browser presentation |
| settings/onboarding/retry clicks | local browser event recorder | browser presentation |
| screenshot reference | external test harness input when available | external harness, not game |

## Static review checklist

1. Launch with no adapter and confirm onboarding/recovery text remains useful.
2. Load each existing campaign surface and confirm campaign identity is retained
   in the capture metadata.
3. Toggle reduced motion, written equivalents, mute, and independent channels;
   verify settings remain local and text remains complete.
4. Submit a valid and rejected host-shaped command; confirm only the canonical
   adapter path is invoked and rejected state remains unchanged.
5. Validate a capture with a forbidden field and confirm diagnostics fail closed.
6. Run the same fixture twice and compare deterministic diagnostic JSON and
   confirm audio trace selection is not dependent on cue-throttle timing.
7. Confirm no raw adapter payload, true state, resolved input, effect queue,
   private action, network call, or model hidden reasoning appears.

These checks are technical/interface-task proxies. They do not establish human usability,
lived accessibility, learning, engagement, calibration, balance,
policy validity, legal validity, or domain-expert validity.

## Explicit non-goals and next gate

This phase does not add browser automation, screenshot generation, external
agent orchestration, deployment, a new simulation mechanic, a new host DTO,
human evaluation, or Phase 9 product revisions.

Phase 9 is the next candidate: AI-agent evaluation and revision using repeated
declared traces and a product decision log. It remains gated until this capture,
recovery, and evidence-classification boundary is verified.
