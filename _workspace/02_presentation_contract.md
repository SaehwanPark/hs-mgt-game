# Presentation Contract — Phase 7.4 audio priority and fatigue manager

## Goal and Authorization

The player should be able to read a dense committed resolution without audio
stacking, repeated tones, or background layers masking an important visible
consequence. This slice authorizes a local priority/queue policy for the
existing generated cues, music stems, and ambience bed. It does not authorize
simulation, host, history, replay, or asset-source changes.

## Player Questions and Consequences

| Player question | Visible source | Audio treatment | Written fallback |
| --- | --- | --- | --- |
| What needs attention first? | Committed visible critical/major cue entry | Priority order and one active transient voice | Existing heading, status, event, and source text |
| Did several visible reports arrive together? | Same synchronous resolution batch | Routine/minor requests collapse to one representative cue with count metadata | All reports remain in the visible list |
| Is the signal repeated? | Cue ID plus local request time | Existing cue cooldown and in-batch duplicate suppression | Repeated visible text remains unchanged |
| Is background audio masking the consequence? | Local cue priority and active background layers | Bounded ambience/music ducking | Visible consequence and audio-equivalent text remain complete |
| What are my local preferences? | Local browser storage only | Restore mode, mute, reduced notifications, and volumes when available | Controls and written results work when storage is absent |

## Actor-Visible Source Ledger

| Semantic element | Authorized source and timing | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Cue priority | `audio-cue-contract.mjs` priority class attached to an already visible cue request | Unknown cue is rejected without sound | No local severity, intent, probability, or outcome classification |
| Batch membership | Synchronous local calls between queue flushes | A single request forms a one-item batch | No reconstruction of host transition boundaries |
| Duplicate/cooldown state | Local cue ID and browser clock | Suppress sound but retain visible result | No hidden state or true-state timing |
| Ducking target | Local channel and cue priority policy | No background gain change when audio is unavailable | No inferred urgency beyond the cue contract label |
| Preferences | Explicit user controls and local storage | Defaults/session-local state | No account, host, or cross-session identity data |

## Visual, Motion, and Audio Semantics

- Priority classes are ordering controls, not moral valence, clinical severity,
  actor intent, probability, or a forecast.
- Critical beats major, major beats routine, and routine/minor requests may be
  aggregated. At most one critical request is selected per local batch.
- One transient interface/event cue voice is active at a time. Music stems and
  one ambience bed remain separate optional background layers.
- Major and critical cues apply bounded local ducking: ambience ducks for both;
  music ducks for critical only. Ducking ramps must have explicit attack and
  release bounds and must not replace visible content.
- Queue overflow is bounded and reported as suppressed/aggregated metadata;
  it never creates an uncontrolled sound stack.
- Focus loss, reduced notifications, cues-only, music-only mute, full mute,
  unavailable audio, and storage failure leave written state complete.

## Accessibility and Fallbacks

- `#audio-state` remains a polite live status region; control labels and
  `#audio-equivalent` explain optional audio state in text.
- No meaning depends on pitch, loudness, timing, or background sound alone.
- Reduced notifications suppress eligible transient audio while preserving
  visible event text and source/status labels.
- Full mute, music-only mute, cues-only, unsupported Web Audio, reduced motion,
  and blocked local storage use complete visual/text fallbacks.
- Rapid queue draining must not reorder DOM updates or steal focus from the
  active form/control.

## Authority, History, and Replay Boundaries

The browser queue, cooldowns, timers, ducking gains, active voices, and stored
preferences are reversible local presentation state. They never enter command
payloads, host transitions, true state, observations, immutable history, state
hashes, replay artifacts, or debrief facts. The host remains authoritative for
all visible cue triggers and written consequences.

## Asset Provenance and Release Requirements

This slice reuses the existing project-generated Web Audio recipes and adds no
recorded files or third-party dependencies. The cue, music, and ambience source
hashes and approval records remain in `assets/registry/audio-assets.json`;
generated catalog/credits checks must pass. The priority manager is code and
policy metadata, not a releasable audio asset.

## Verification and Evidence Limits

Focused tests must cover pure batch planning, one-critical selection,
duplicate/cooldown/aggregation behavior, queue cap, ducking targets, fake
Web-Audio voice counts, preference persistence/failure, rapid input, dense
month-resolution requests, and text/live-region markers. Full repository
checks remain required. These checks do not establish measured loudness,
fatigue reduction, lived accessibility, screen-reader usability, human
comprehension, learning, calibration, or policy validity.

## Non-Goals and Open Questions

- No priority changes to the simulation or host contracts.
- No audio scoring, adaptive difficulty, hidden-state alerting, or automatic
  severity derivation.
- Human review remains needed for cue audibility, screen-reader coexistence,
  fatigue, and classroom suitability.
- Later work may revisit user-configurable priority preferences only with an
  explicit contract; this slice uses fixed policy order and local mute/volume
  controls.
