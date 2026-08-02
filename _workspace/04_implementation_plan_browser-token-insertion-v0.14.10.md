# Implementation Plan — Browser-safe response token insertion v0.14.10

## Target slice

Harden the registered response-token heading insertion with a standards-based
`insertBefore` fallback when `Element.prepend` is absent. Preserve the current
Chromium path and all actor-visible content; the fallback is presentation-only.

## Boundaries

- In scope: a tiny DOM insertion helper, focused source/visual tests, current
  docs, and synchronized device evidence.
- Out of scope: new browser-engine support or certification, host routes/DTOs,
  simulation, persistence/replay, action legality, assets/audio, and campaign
  changes.

## Acceptance criteria

1. In a normal DOM, the registered token remains before the response title.
2. If `heading.prepend` is unavailable, `insertBefore(token, firstChild)`
   produces the same order without throwing.
3. Written label, symbol, tooltip, focus, mute/reduced-motion, source/replay,
   and information-boundary behavior remain unchanged.
4. Browser compatibility/offline/loading/device checks and focused/full suites
   pass; the sole medium-effort reviewer reports no actionable issue.
