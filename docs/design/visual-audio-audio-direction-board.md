# Audio-direction prototype board — Phase 1.3

**Status:** Complete in v0.12.38
**Prototype:** `gui/audio-proof.html`
**Recipe source:** `gui/audio-direction.mjs`

## Decision

The next audio direction uses short tonal cues, restrained low-level generated
beds, and explicit visible-source mappings. The prototype remains dependency-
free and generates previews through the Web Audio API after a user gesture. It
does not replace the existing runtime catalog yet.

## Standards

| Standard | Prototype target | Reason |
| --- | ---: | --- |
| Integrated loudness | -24 LUFS ±2 LU | Keeps optional audio below the visual reading task. |
| Peak ceiling | -6 dBFS | Leaves headroom for browser/device gain differences. |
| UI/event cue duration | 80–500 ms | Short enough to avoid interrupting reading. |
| Loop duration | 4,000–8,000 ms | Long enough to avoid obvious repetition. |
| Loop crossfade | 120 ms | Boundary treatment for later rendered loop assets. |
| Speech/text ducking | -8 dB | Written content remains primary when narration is added. |
| Preview gain floor | 0.25 relative | Directional distinctions survive low-volume inspection. |

The numbers are engineering targets for the prototype, not calibrated loudness
or hardware-listening evidence. A later rendered-asset slice must measure the
actual output and record release hashes.

## Prototype matrix

| Prototype | Visible source | Text equivalent | Pattern |
| --- | --- | --- | --- |
| Confirmation | Local confirmation or host validation | Confirmation status and affected control | Ascending major second |
| Rejection | Host rejection or visible validation failure | Error text and unchanged-session marker | Descending minor second |
| Report arrival | New visible report or briefing | Report heading, source, and timing | Soft open triad |
| Riverside motif | Visible Riverside identity | Riverside name, marker, and header | Open-fifth pulse |
| Neutral bed | Optional active-month ambience | Current month and operating summary | Filtered neutral noise |
| Pressure layer | Visible pressure category only | Pressure banner and affected metric | Slow low pulse |
| Environmental loop | Optional non-semantic environment | Regional board and written context | Filtered environmental noise |

All seven entries expose `visible_source` and `equivalent` fields. The pressure
layer may only be selected from actor-visible margin, unmet demand, runway, or
pressure language; it must never be selected from true deterioration, private
rival state, resolved inputs, or a future outcome.

## Loop and masking rules

- Loopable prototypes are bounded to the 4–8 second window and use the shared
  120 ms crossfade target.
- The environmental loop has no speech, institution names, sirens, or semantic
  event pattern. Its -32 dBFS target stays below the -8 dB speech/text ducking
  rule.
- The neutral bed is non-semantic. It must not communicate stability, pressure,
  success, failure, or urgency.
- Cue patterns differ by interval and contour, not by loudness alone. Written
  labels remain present at every preview card.

## Accessibility and evidence limits

The proof page uses native keyboard buttons, visible source/equivalent text, and
an explicit unavailable-audio status. Muting or browser audio failure leaves
the visible result complete. The static/recipe tests verify declared boundaries
and deterministic metadata only; they do not establish human perception,
contrast, accessibility experience, learning, calibration, balance, or policy
validity.

## Deferred next slice

Broader production assets, calibrated measurement, and human listening remain
separate gates. The policy prototype now covers deterministic priority order,
music ducking metadata, cooldown, full/cues-only/muted modes, and reduced-audio
preference behavior.

## Policy prototype — v0.12.38

The same fixture now exposes a deterministic policy layer. Event cues outrank
interface cues, which outrank music, which outranks ambience. A higher-priority
cue carries the -8 dB music-ducking decision. Repeated cues are suppressed by
their per-entry cooldown. Full-audio, cues-only, and muted modes are explicit;
the reduced-audio preference suppresses music and ambience while retaining
interface/event text and cue decisions.
