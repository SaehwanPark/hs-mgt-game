# Request Summary — Per-session durable GUI checkpoints v0.13.102

## Authorized outcome

Advance the Phase 11.1 durable save/load boundary from one latest GUI
checkpoint slot to a host-owned per-session checkpoint archive. Keep the
browser's opaque session-ID recovery path and the Rust host as the only
authority.

## Target slice

- Store each GUI campaign checkpoint in a separate sibling archive file keyed
  by its validated opaque session ID.
- Hydrate competitive, stabilization, and regional-affiliation checkpoints
  from the archive after a host restart.
- Preserve compatibility with the existing single-file checkpoint as a
  read/remove fallback during migration.
- Delete only the matching session's archive and legacy checkpoint on terminal
  end.
- Record source-bound tests and documentation for concurrent cross-campaign
  durable recovery.

## Non-goals

- No browser serialization of save artifacts or checkpoint discovery UI.
- No replay regeneration, new simulation rules, new routes, or client-side
  transition authority.
- No human accessibility, educational, audio, provenance, legal, clinical,
  browser-engine, device, or public-release decision.
- No fabricated completion of the remaining human/runtime gates.

## Validation target

Focused persistence/session and browser-boundary tests, full Python and Rust
verification, release/documentation/asset checks, exactly one medium-effort
code review, merge, temporary-branch cleanup, and post-merge persistence
re-audit.

## Evidence limits

This slice proves host-owned per-session durable checkpoint storage and legacy
read compatibility only. It does not establish real-device certification,
browser serialization, human usability, educational value, audio quality,
legal clearance, or release readiness.
