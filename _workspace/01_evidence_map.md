# Evidence Map — Visual and Audio Phase 5 Foundational Audio v0.12.21

## Scope

Phase 5 adds optional browser audio to the existing one-month competitive
surface. Audio is a presentation consequence of visible page state or an
explicit local UI action; it is not a simulation input or history record.

## Sources Reviewed

- Phase 5 and first-vertical-slice requirements in
  `docs/visual_audio_upgrade_proposal.md`.
- Phase 0 audio-state/cue catalog and asset/license policy.
- ADR-0011 and the Phase 1–4 GUI/MCP contracts.
- `ReadOnlyPresentationEnvelope`, `ResolutionEnvelope`, visible action status,
  and current DOM controls in `gui/`.
- README, SPEC, architecture, design principles, lessons, and harness spec.

## Mechanisms and Institutions

The player remains a health-system executive deciding among institutional
tradeoffs. Music communicates the current visible presentation mode; cues mark
local interaction or already committed visible events. No audio cue represents a
private rival decision, hidden stochastic input, or an inferred causal edge.

## Actor Incentives and Information

Audio can reinforce category, timing, and attention without saying whether an
organizational outcome is universally good or bad. The visual/text equivalent
remains authoritative and complete when muted, unfocused, reduced-notification,
or unsupported by the browser.

## Assumptions

- Web Audio API synthesis is sufficient for a first technical vertical slice;
  no external file or license download is required.
- Phase 0's four music modes and eight cue IDs are the approved catalog; no new
  semantic event taxonomy is needed.
- Visible observation fields and explicit UI outcomes are sufficient for a
  deterministic classifier; no true-state or hidden transition access is
  justified.
- Local settings can be held in the audio client without a persisted settings
  schema or simulation mutation.

## Unresolved Questions

- Which synthesized timbres remain restrained across repeated monthly play?
- Should asset-backed music replace generated loops after an evidence gap is
  identified, and what provenance gate would authorize that change?
- Which focus behavior best fits later AI-agent capture without claiming human
  accessibility?

## Design Implications

- Add one pure catalog/classifier boundary that maps visible envelopes and
  explicit UI actions to stable cue/music IDs.
- Add one browser audio client with independent channel volumes, master mute,
  focus/reduced-notification policy, event throttling, and no-op fallback.
- Record generated source, ownership, license status, and credits in a registry;
  keep the simulation core free of audio paths, volumes, and playback rules.
- Test classification through a recording sink and test playback behavior with
  injected fake contexts where possible; browser visual/audio hardware checks
  remain residual limits.

## Risks

Audio can become a hidden score, reveal unobserved state, fatigue repeated play,
or make muted play incomplete. Keep every mapping source-labeled, restrained,
throttled, independently controllable, and paired with existing visual/text
content.
