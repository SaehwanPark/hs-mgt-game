# Presentation Contract — Phase 7.3 adaptive music stems

## Authorized outcome

Provide seven optional generated music states that clarify visible strategic
context and pacing without adding moral valence, hidden information, or a
second authority. Existing state IDs remain stable; new states are selected only
from actor-visible context.

## Source and output ledger

| State | Authorized source | Output | Safe fallback |
| --- | --- | --- | --- |
| Menu/planning | Explicit page stage | Five generated stems with short planning cadence | Menu heading and controls |
| Stable operations | Actor-visible operating summary | Base pulse plus low-intensity institutional/policy layers | Operations summary and status |
| Pressure | Visible margin, unmet demand, runway, or pressure text | Bounded pressure layer and transition cadence | Pressure banner and affected metric |
| Regulatory scrutiny | Visible regulatory/policy report or stage | Bounded policy layer | Regulatory report and status |
| Competitive escalation | Visible public rival/market escalation | Bounded competitive layer | Public market signal and source |
| Affiliation/negotiation | Visible affiliation or negotiation stage | Bounded institutional motif and cadence | Partner/negotiation text |
| Debrief | Explicit debrief stage or completed session | Closing cadence | Debrief heading and timeline |

Every state has base pulse, institutional motif, visible pressure layer, policy
layer, and transition cadence recipes. Music is generated at playback time with
no speech, no real institution names, and no hidden-state or victory/defeat
encoding. Crossfades are bounded metadata and runtime fades, not a promise of
measured musical quality.

## Audio behavior

- Music is optional and independently suppressible through music-only mute, full
  mute, cues-only, focus loss, reduced notifications, or unavailable audio.
- Music does not mask visible text, event cues, or reading controls.
- Only explicit actor-visible stage, report, observation, or process text may
  select a state. No private rival state, true state, resolved input, inferred
  severity, or hidden outcome may select it.
- Missing or unknown state inputs use stable operations with a written generic
  fallback; unsupported audio is silent.

## Provenance and authority

All seven states and their stems are project-generated in the repository. The
catalog records the module source hash and no release audio file is distributed.
State selection, stem recipes, crossfade metadata, timers, and playback remain
local presentation state and never enter commands, transitions, history,
hashes, replay, or debrief.

## Evidence limits

The proof/tests establish metadata completeness, deterministic recipe shape,
visible-only classification, replay sequence determinism, safe fallback, and
mute behavior. They do not establish acoustic quality, audibility, fatigue,
lived accessibility, musical preference, human comprehension, learning,
calibration, or policy validity.
