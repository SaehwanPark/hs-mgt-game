# Mechanism Design — Visual and Audio Phase 5 Foundational Audio v0.12.21

## Goal and Roadmap Phase

Add optional, source-traceable audio to the one-month competitive presentation
without changing simulation semantics, replay artifacts, or the completeness of
visual/text communication. This is roadmap Phase 5 after the merged Phase 4
resolution slice.

## Slice Boundary

The browser owns a small audio catalog, a visible-only classifier, synthesized
music/cue playback, local settings, and a recording-sink interface. The catalog
contains four music states and the eight Phase 0 interface/event cues. There are
no audio files, fetches, asset URLs, or audio DTOs in Rust in this slice.

## Actors and Authority

Rust/MCP remains authoritative for actions, transitions, observations, committed
events/effects, history, hashes, and debriefs. The browser audio client owns only
playback and settings. A catalog entry's `visible_source` and `equivalent` are
documentation metadata, not new simulation authority.

## State, Beliefs, and Observations

Music state classification consumes explicit page stage or actor-visible
`ReadOnlyPresentationEnvelope`/`ResolutionEnvelope` fields. Pressure may use
visible margin, unmet demand, runway signal, staffing labels, or a visible alert;
stable operations is the fallback. Debrief is selected only from explicit page
debrief state. No private rival, true-state, resolved-input, or effect-queue
field is read.

## Commands, Events, and Effects

Catalog IDs:

- music: `menu`, `stable_operations`, `pressure`, `debrief`;
- interface: `ui.action-confirm`, `ui.action-reject`, `ui.action-add`,
  `ui.action-remove`, `ui.submit`, `ui.advance-month`, `ui.report-received`,
  `ui.save-complete`;
- events: `event.project-complete`, `event.staffing-constraint`,
  `event.operating-loss`, `event.operating-recovery`, `event.payer-decision`,
  `event.regulatory-decision`, `event.rival-expansion`,
  `event.affiliation-milestone`.

Each entry has a visible equivalent, source, generated-audio recipe, cooldown,
and accessibility classification. The audio client reports missing support as a
non-fatal status and never calls `submitTurn`.

## Strategic Interaction

Audio should draw attention to institutional responses and operating pressure,
not reward a single score or imply optimal strategy. Repeated holds, rival
signals, and negative months remain understandable through the visible result;
audio only adds restrained category/timing emphasis.

## Assumptions and Parameters

- Schema: `audio-catalog-v1`.
- First supported campaign: `competitive-regional-v1`.
- Four generated music recipes, one optional ambience recipe, and sixteen
  total interface/event cues are sufficient for the first technical slice.
- Master, music, interface, event, and ambience channels are independent;
  default event cooldown is 1,500 ms and repeated event IDs are coalesced.
- Browser audio starts only after a user gesture; muted and unsupported paths
  are complete and visible.

## Educational Debrief Hooks

The page keeps source text and visual equivalents adjacent to audio controls.
Cue logs used by tests identify the source ID and visible equivalent, allowing a
later AI-agent trace to compare visible event text with audio classification.
This phase makes no claim about learning, engagement, or human accessibility.

## Determinism and Replay Notes

Classification is a pure mapping over visible input snapshots and explicit UI
actions. Playback timing, oscillator phase, focus, and volume are presentation
state only. Replay may regenerate the same cue IDs from the same visible
resolution envelope, but audio playback is never stored in history or hashes.

## Open Questions

- What evidence would justify replacing generated recipes with licensed files?
- Which visible pressure combinations should be grouped before a richer typed
  audio-event contract is needed?
- What repeated-session capture threshold should reopen cue throttling or mix
  decisions?
