# Mechanism Design — Phase 10 accessibility and visual-language hardening v0.12.26

## Goal and Roadmap Phase

Close a narrow part of the `SPEC.md` product contract and first competitive
vertical-slice requirements: a keyboard-reachable, text-scalable, non-color-only
presentation surface. This is a Phase 10 follow-up derived from the proposal's
accessibility and visual-language exit criteria after the numbered Phase 0–9
slices.

## Slice Boundary

Included:

- semantic skip link and presentation navigation landmark;
- stable anchors for briefing, regional/action, resolution/result, and debrief;
- visible status legend and shape/pattern cues;
- standard/large text scale persisted locally;
- functional optional cue-explanation visibility preference;
- targeted live/status semantics and visible focus styling;
- static contract tests and documentation.

Excluded:

- browser launch/session creation, real assets, visual map redesign, screen-reader
  certification, contrast measurement by people, or human evaluation;
- any host, MCP, Rust, simulation, transition, or command change.

## Actors and Authority

- Player: selects navigation targets and local presentation preferences.
- AI-agent test profile: exercises stable controls and records visible settings.
- Host/core: sole authority for observations, commands, validation, stochastic
  resolution, history, hashes, replay, and debrief.

## State, Beliefs, and Observations

No true game state changes. Local GUI state consists only of `reduced_motion`,
`text_scale`, and `text_equivalents`. These values are not sent to the host,
included in command text, or used to classify visible audio sources. Host data
continues to be rendered as actor-visible facts, labels, uncertainty, delays,
revisions, or explicit missingness.

## Commands, Events, and Effects

No new game commands or transition events exist. The client adds only local
navigation and settings events to the existing allowlisted playtest recorder:

- `settings_changed(setting=text_scale|text_equivalents, value=...)`;
- `onboarding_next(target=<stable panel>)`.

Skip navigation, legend expansion, and text scaling produce no host request or
simulation effect. The cue-equivalent preference may hide the optional audio
explanation paragraph only; it never hides the written result, observation,
history, resolution, or debrief.

## Strategic Interaction

There is no new strategic interaction. Existing player decisions remain
host-shaped and host-validated. The presentation must not imply that a status
label, cue, or visual emphasis is an objective score or a universal good/bad
judgment across organizational performance, actor utility, social welfare, and
decision quality.

## Assumptions and Parameters

- `standard` text scale is the current root size; `large` is a modest CSS scale
  using the platform's normal layout flow rather than a second layout engine.
- Status symbols are decorative but paired with visible status text and a
  machine-readable `data-status` value.
- Browser `localStorage` may fail or be absent; settings remain session-local.
- Existing `prefers-reduced-motion` behavior remains an independent fallback.

## Educational Debrief Hooks

Navigation and status language should make it easier to reach the existing
briefing, pending-process, resolution, causal, history, and debrief surfaces.
The slice makes no claim that this improves learning. Existing debrief content
and decision/outcome distinction remain host-provided and unchanged.

## Determinism and Replay Notes

Local settings and CSS transitions are presentation-only. They do not affect
commands, validation, resolved inputs, state transitions, history, hashes,
replay artifacts, or committed debriefs. Replaying the same host envelope with
different local text scale must render the same host facts.

## Open Questions

- A real browser accessibility audit still requires an appropriately designed
  human or assistive-technology evaluation.
- The visual asset registry and first competitive session-launch experience
  remain separate future slices after this local presentation contract.
