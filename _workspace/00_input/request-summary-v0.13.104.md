# Request summary — v0.13.104 browser-safe checkpoint reference transfer

## User request

Continue the visual/audio enhancement roadmap loop after the merged v0.13.103
checkpoint discovery picker. Select the next unmet compatible item, design a
bounded plan, implement it, use exactly one medium-effort code reviewer, merge
to `main`, delete temporary branches locally and remotely, and re-audit before
selecting the next slice.

## Selected target

Add browser-safe export/import for a durable checkpoint reference. The browser
may serialize and transfer only the validated discovery metadata needed to
identify a host checkpoint: schema version, opaque session ID, campaign, seed,
committed-transition count, and archive/legacy source. Import fills the existing
session-ID control and leaves load/restore to the user and host.

## Why this slice

The v0.13.103 picker closes host/browser metadata discovery but leaves browser
checkpoint-reference transfer open. A reference file reduces recovery friction
between browser sessions while preserving the repository’s presentation-only
browser boundary. The actual host save artifact, true state, history,
resolved stochastic inputs, replay regeneration, and transition authority stay
outside the browser.

## Invariants to preserve

- The host remains authoritative for checkpoint existence, validation,
  hydration, replay verification, and all transitions.
- Browser serialization contains only the exact reference fields above; extra
  fields, save wrappers, history, hashes, or true-state-shaped data fail closed.
- Import validates the schema and fields, fills the existing opaque session-ID
  input, and never auto-loads, writes browser storage, or creates a new route.
- Export is deterministic and uses a safe filename derived only from the
  validated opaque ID.
- Existing picker, manual load, restore, refresh recovery, autosave, and
  host-only save artifacts remain compatible.

## Explicit non-goals

- Do not serialize or expose a host save artifact or true state.
- Do not add automatic loading, new persistence routes, replay regeneration,
  simulation rules, or browser-authored hashes.
- Do not claim browser/device certification, human accessibility, educational
  effectiveness, provenance/legal approval, or public-release readiness.

## Stop conditions

Stop and report if the reference requires a host route, contains more than
the discovery metadata contract, changes the existing load/restore path, or
requires browser storage beyond the existing opaque active-session ID.
