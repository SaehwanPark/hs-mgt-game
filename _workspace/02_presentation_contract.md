# Presentation Contract — Phase 1.3 audio policy prototype v0.12.38

## Goal and Authorization

Add deterministic policy behavior to the fixture-only audio-direction proof.
The roadmap authorizes priority, cooldown, mode, and reduced-audio behavior in
the prototype; the live audio client remains outside this slice.

## Player Questions and Consequences

- Which visible cue takes precedence when several presentation signals occur?
- Why was a repeated cue suppressed?
- What remains audible in full, cues-only, muted, or reduced-audio modes?

Every answer remains visible through source-linked text and status messaging.

## Actor-Visible Source Ledger

| Policy | Allowed source | Prohibited source | Equivalent |
| --- | --- | --- | --- |
| Priority/ducking | Declared cue channel and visible event class | Hidden severity or outcome | Visible event/report text |
| Cooldown | Local preview request timing and declared cue ID | Simulation time or host state | Status text when throttled |
| Modes/preferences | Local user control | Host settings or hidden state | Mode label and written result |

## Visual, Motion, and Audio Semantics

- Event > interface > music > ambience is the deterministic priority order.
- Event/interface decisions carry the -8 dB music-ducking instruction.
- Cooldowns are per prototype entry and return a visible throttled result.
- Cues-only retains interface/event decisions; muted suppresses all playback;
  reduced audio suppresses music/ambience while retaining text.

## Accessibility and Fallbacks

- Native mode buttons and a reduced-audio checkbox are keyboard-operable.
- Filtered, throttled, unsupported, and muted results retain the entry's text
  equivalent and visible source.
- Audio policy never removes the page's written content.

## Authority, History, and Replay Boundaries

The policy consumes only local fixture IDs, declared channels, and local user
preference/request timing. It does not read host state, submit commands, create
session state, or alter transitions, history, hashes, replay, or debriefs.

## Asset Provenance and Release Requirements

The same registered project-generated `gui/audio-direction.mjs` source remains
the only audio-direction asset. Its hash is refreshed for v0.12.38; no release
file or third-party source is introduced.

## Verification and Evidence Limits

Focused tests cover priority, ducking, cooldown, modes, reduced audio, text
equivalents, and fallback. These are technical checks, not calibrated loudness,
human listening, accessibility, learning, engagement, balance, or policy
evidence.

## Non-Goals and Open Questions

Do not integrate the policy into `gui/audio.mjs`, add recorded assets, add
adaptive composition, or claim human perception or hardware behavior.
