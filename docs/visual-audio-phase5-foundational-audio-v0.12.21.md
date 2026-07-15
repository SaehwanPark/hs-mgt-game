# Visual and Audio Phase 5 — Foundational Audio

Status: Implemented, reviewed once, and merged in PR #172.

Phase 5 adds optional browser audio to the existing Phase 3/4 competitive
action and monthly-resolution surface. The first implementation uses generated
Web Audio recipes rather than downloaded files, so the registry and credits can
be complete without adding a network or third-party licensing dependency.

## Typed/pure presentation contract

The planned `audio-catalog-v1` catalog contains:

- music states `menu`, `stable_operations`, `pressure`, and `debrief`;
- interface cues `ui.action-confirm`, `ui.action-reject`, `ui.action-add`,
  `ui.action-remove`, `ui.submit`, `ui.advance-month`, `ui.report-received`,
  and `ui.save-complete`; and
- event cues `event.project-complete`, `event.staffing-constraint`,
  `event.operating-loss`, `event.operating-recovery`, `event.payer-decision`,
  `event.regulatory-decision`, `event.rival-expansion`, and
  `event.affiliation-milestone`.

Each entry records its visible source, visual/text equivalent, channel,
cooldown, generated recipe, and provenance/ownership. Pure mapping functions
can write a recording-sink event without creating an audio context. One optional
`regional_ambience` recipe uses the same generated/provenance boundary.

## Source and authority map

| Audio output | Visible source | Equivalent |
| --- | --- | --- |
| Music state | explicit page stage or actor-visible summary | stage/status label and current briefing/result |
| Interface cue | local draft/validation/control outcome | status text and changed control/row |
| Monthly event cue | committed visible resolution/event/effect text | resolution step and direct effect/result text |
| Report cue | newly rendered visible report/history item | report heading and source label |
| Missing/fallback | browser capability or user setting | audio status and unchanged visual content |

The browser never reads true state, hidden rival behavior, resolved stochastic
inputs, or effect queues. Audio playback, volume, focus, and registry metadata
remain outside the deterministic simulation and history.

## Browser behavior

Audio controls are semantic buttons/sliders with visible labels and status:
master, music, interface, event, ambience, mute, and reduced notifications.
Audio context creation is lazy and requires a user gesture. Focus loss pauses or
attenuates configured channels without changing the page result. Unsupported
audio, denied autoplay, missing recipes, and muted play are non-fatal states.

Music changes only when the visible classifier changes state. Explicit UI and
resolution calls can request cues, but repeated IDs are throttled. Textual
resolution, visual statuses, and controls remain complete when audio is muted,
disabled, reduced, skipped, or unavailable.

## Registry and credits

The registry is machine-readable and records generated source, release path,
ownership/license status, modifications, and approval. `ASSET_CREDITS.md`
states that Phase 5 ships no third-party audio files; all recipes are generated
by the repository's browser module. A later asset-backed audio slice must add
retrieval, hash, license, attribution, and approval evidence before replacing
these recipes.

## Static review checklist

1. Verify all four music states and sixteen cues have sources/equivalents.
2. Exercise confirm/reject/add/remove/submit/advance/report/save cue requests.
3. Resolve visible stable, pressure, and debrief states; confirm no private or
   hidden source affects music.
4. Test channel sliders, master mute, focus loss, reduced notifications,
   repeated-event throttling, denied/unsupported audio, and keyboard operation.
5. Mute audio and confirm the complete Phase 4 resolution and action workflow
   remains available.
6. Inspect registry/credits and confirm no network or downloaded asset appears.
7. Confirm the recording sink is deterministic and audio reads do not change
   session turn, history, hash, or replay output.

These are technical/interface-task checks only. They do not establish human
usability, lived accessibility, engagement, learning, calibration, balance,
domain validity, or policy validity.

## Explicit non-goals and next gate

This phase does not add audio to Rust, audio history, downloaded/licensed audio
files, dynamic composition, spatial or pitch-only signals, a broad settings
framework, other campaigns, map/world expansion, or human evaluation.

Phase 6 is the next candidate: persistent regional map/world expansion only
after optional audio, provenance, visual equivalents, and unchanged replay/hash
behavior are verified.
