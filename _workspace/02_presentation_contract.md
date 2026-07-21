# Presentation Contract — Phase 7.1 UI and event cue refinement

## Authorized outcome

Refine the existing generated Web Audio cue vocabulary so each visible cue has
an inspectable semantic contract, consistent synthesis envelope, explicit
cooldown, and a complete text equivalent. Audio remains optional and cannot
create information unavailable in the actor-visible host projection.

## Cue source and output ledger

| Cue family | Authorized trigger | Output | Fallback |
| --- | --- | --- | --- |
| Interface | Local visible control result or host validation result | Short normalized interface tone | Visible control/status text |
| Event | Host-committed visible event/effect or actor-visible result | Short normalized event tone | Written event/effect and source |

Every cue contract names its visible source, text equivalent, priority class,
duration, target loudness, peak ceiling, cooldown, and a distinction label. The
distinction label prevents two cue IDs from sharing an unexplained meaning; it
does not claim a real-world acoustic or clinical distinction.

## Audio behavior

- `full` mode permits the existing optional music, ambience, interface, and
  event channels.
- `cues-only` mode suppresses music and ambience while retaining interface/event
  cues and their text equivalents.
- Mute, unavailable browser audio, reduced notifications, and focus loss leave
  written status, source, and result information complete.
- The synthesis path uses one bounded normalization gain and the contract’s
  duration/peak metadata; this is a recipe invariant, not a measured hardware
  loudness claim.

## Authority and replay boundary

The cue contract accepts only explicit cue IDs and visible trigger metadata.
`visibleEventCues` may classify committed visible text and observations but may
not read true state, private rival intent, resolved inputs, effect queues, or
client-side formulas. Audio playback and cooldown timestamps remain local
presentation state and never enter commands, transitions, history, hashes,
replay artifacts, or debrief output.

## Accessibility and provenance

- Every cue has an adjacent text equivalent and visible source.
- Cues-only, muted, and unavailable-audio paths are complete without sound.
- No new recorded or third-party asset is introduced; the generated recipe
  module is registered with source hash, project-generated license basis,
  accessible equivalent, visible source, and approval state.

## Evidence limits

The proof and tests establish contract coverage, trigger mapping, and local
fallback behavior. They do not establish audibility, fatigue, musical quality,
lived accessibility, human comprehension, learning, calibration, or policy
validity.
