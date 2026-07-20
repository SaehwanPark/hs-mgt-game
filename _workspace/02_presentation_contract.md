# Presentation Contract — Phase 1.3 audio-direction prototype v0.12.37

## Goal and Authorization

Define and preview a bounded sound vocabulary without changing the live audio
client or host contract. The roadmap authorizes standards, recipes, and a
fixture-only proof page; runtime priority and preference behavior remain out of
scope.

## Player Questions and Consequences

- What kind of visible interface result just occurred?
- Has a visible report arrived?
- Which visible institution or pressure category is being emphasized?
- Is this sound optional context rather than a hidden result?

The answer must remain available in the visible status, report, identity, or
metric text when audio is muted or unavailable.

## Actor-Visible Source Ledger

| Prototype | Allowed source | Prohibited source | Equivalent |
| --- | --- | --- | --- |
| Confirmation/rejection | Local result or host validation response | Hidden legality or future outcome | Visible status/error text |
| Report arrival | New visible report/briefing item | Private report timing | Heading, source, timing |
| Riverside motif | Visible Riverside identity | Hidden player state | Name, marker, header |
| Neutral/environmental bed | Optional presentation context | Status or outcome inference | Month, board, operating text |
| Pressure layer | Visible margin, unmet demand, runway, or pressure language | True deterioration/private rival state | Banner and metric text |

## Visual, Motion, and Audio Semantics

- Cues use distinct contour/pattern metadata and conservative peak targets.
- Loopable beds use the shared 4–8 second window and 120 ms crossfade target.
- Environmental audio is generated filtered noise with no speech, names, sirens,
  or decision signal.
- Audio is a reinforcement channel, never the only semantic channel.

## Accessibility and Fallbacks

- Preview controls are native keyboard buttons.
- Each card displays source and text equivalent.
- Unsupported audio returns an explicit visual-only result.
- Mute, reduced-audio preferences, priority ordering, and production assets are
  deferred to later slices with their own tests.

## Authority, History, and Replay Boundaries

`audio-direction.mjs` consumes only declarative fixtures and returns local audio
preview actions. It does not import host state, submit commands, create session
state, read private fields, alter transitions, or write history, hashes, replay,
or debrief output.

## Asset Provenance and Release Requirements

The recipe source is registered as project-generated with a current SHA-256,
accessible equivalent, visible source, modifications, approval, and no release
path. No third-party audio file or network source is introduced.

## Verification and Evidence Limits

Focused tests cover seven prototypes, standards, distinct cue patterns, loop
bounds, source/equivalent presence, unsupported fallback, and authority markers.
Static evidence does not establish calibrated LUFS, hardware response, human
perception, accessibility experience, learning, engagement, balance, or policy
validity.

## Non-Goals and Open Questions

Do not implement live catalog replacement, priority/ducking scheduler,
repeat-cue cooldown, mute/cues-only/full-audio modes, reduced-audio preference,
recorded assets, release derivatives, adaptive composition, or human listening
evaluation in this slice.
