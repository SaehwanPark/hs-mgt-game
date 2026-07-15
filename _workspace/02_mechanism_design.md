# Mechanism Design — Loopback GUI host v0.12.31

## Authority and data flow

```text
browser forms/drafts
  -> same-origin host adapter
  -> loopback HTTP routes
  -> GameSessionStore
  -> actor-visible typed envelopes
  -> browser rendering and optional audio
```

- The browser owns setup fields, selection, drafts, playback, and settings.
- `GameSessionStore` owns session identity, validation, stochastic resolution,
  transitions, observations, history, hashes, replay, and debriefs.
- The HTTP edge performs only routing, JSON extraction/serialization, loopback
  enforcement, and error-status mapping.

## Failure behavior

- Invalid setup and host/domain errors return structured recoverable messages.
- A replacement session becomes active only after its presentation and action
  catalog both load successfully.
- Competitive paths do not request stabilization/affiliation campaign coverage.
- Static/direct serving retains fixture mode and cannot claim a live session.

## Scope boundaries

The live GUI supports competitive play only and stores sessions only for the
host process lifetime. Remote access, persistence, authentication, and other
campaigns require separate decisions.
