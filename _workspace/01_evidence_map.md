# Evidence Map — Visual and Audio Phase 8 AI-Agent Testplay Readiness v0.12.24

## Scope

Phase 8 prepares the existing browser presentation for reproducible AI-agent
task traces. It is a testability and recovery surface, not an evaluation of
people or a new simulation layer.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 8 and testing strategy.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `SPEC.md`, and the harness team spec.
- Existing GUI clients, audio recording sink/catalog, campaign coverage,
  resolution/replay surfaces, and `gui/README.md`.
- Existing MCP `scripts/play_game.py` and `scripts/diagnose_runs.py` patterns
  for declared sessions, validation failures, history, hashes, and debriefs.

## Mechanisms and Institutions

The relevant mechanism is the interface-to-authority boundary: an agent must
recognize the current campaign role, choose a canonical host-shaped action,
recover from a rejection, and inspect committed visible results. The health
policy institutions remain those already modeled by each campaign; Phase 8
does not introduce actors or new institutional behavior.

The readiness artifact therefore records interaction steps and source-linked
outcomes rather than scoring whether an agent understood policy or made a good
decision. Competitive, stabilization, and affiliation campaign identifiers are
retained so diagnostics cannot silently pool incompatible meanings.

## Actor Incentives and Information

- The player/agent sees only the current presentation and host responses.
- The recorder may capture submitted canonical command text, validation result
  metadata, committed history/hash values, visible audio cue IDs, and a bounded
  semantic snapshot.
- The recorder must not capture raw adapter envelopes, true state, resolved
  inputs, effect queues, private rival actions, hidden DOM payloads, or model
  chain-of-thought.
- Settings are local presentation preferences; they do not change commands,
  transitions, randomness, history, hashes, or replay.

## Assumptions

- A browser-side recorder can be injected as an optional adapter/client concern
  without changing the host contracts.
- Existing audio recording-sink events are sufficient for cue evidence when
  combined with visible source/equivalent labels.
- Existing MCP playtest wrapper and diagnostics conventions can inform role/task
  fields without merging GUI traces with simulation state.
- A deterministic event sequence is more useful for Phase 8 than an external
  screenshot or agent service that would add dependencies and operational risk.

## Unresolved Questions

- Which future browser runtime will provide real semantic DOM and screenshot
  capture for agent runs, if that is authorized after this readiness slice?
- Which task failures represent interface friction versus strategy disagreement?
- What evidence would justify changing onboarding copy rather than recording a
  bounded interface hypothesis?

## Design Implications

- Add explicit onboarding and recovery controls with stable IDs and text.
- Add a local settings panel for reduced motion, text equivalents, mute, and
  audio channels; default to complete written play.
- Define `gui-playtest-v1` with allowlisted events, declared role/task/mode,
  semantic snapshot, optional screenshot reference, and separate evidence lanes.
- Validate/classify capture files deterministically and fail closed on unknown
  schema or forbidden fields.
- Keep capture, settings, and diagnostics outside simulation transitions and
  preserve all Phase 2–7 contracts.

## Risks

The recorder could become a hidden state export, diagnostics could overinterpret
agent behavior as human evidence, or recovery controls could silently retry a
mutation. Prevent this with explicit allowlists, source/evidence labels,
non-mutating retry reads, canonical submit-only commands, schema tests, and
documentation that calls AI/static traces interface-task proxies only.
