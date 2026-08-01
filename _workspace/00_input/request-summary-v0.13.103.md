# Request summary — v0.13.103 checkpoint discovery

## User request

Continue the visual/audio enhancement roadmap loop after the merged v0.13.102
per-session durable GUI checkpoint archive slice. Select the next unmet item,
design a bounded plan, implement it, use exactly one medium-effort code
reviewer, merge to `main`, delete temporary branches locally and remotely, and
re-audit before selecting the next slice.

## Selected target

Implement host-owned durable checkpoint discovery for the existing GUI archive.
The loopback host will expose a typed read at `GET /api/v1/checkpoints` that
lists only validated checkpoint metadata for competitive, stabilization, and
regional-affiliation sessions. The browser will render an accessible list with
campaign, opaque session ID, storage source, and committed-transition count;
selecting an entry fills the existing session-ID load flow and does not load it
automatically.

## Current repository understanding

- v0.13.102 stores one validated checkpoint file per opaque session ID in the
  host-owned sibling `.checkpoints` directory and retains a legacy single-file
  fallback.
- The browser currently accepts a manually entered opaque session ID but has no
  way to discover durable checkpoints.
- The GUI already has a loopback-only Axum host, a local fetch adapter, a
  session launcher, and actor-visible save/load envelopes.
- The consolidated technical audit and Phase 11.1 ledger explicitly leave
  checkpoint discovery UI open.

## Invariants to preserve

- The host remains authoritative for persistence, replay validation, and all
  simulation transitions.
- Browser storage contains only the opaque active session ID and presentation
  preferences; it never receives or stores a save artifact or true state.
- Discovery exposes metadata only: session ID, campaign, seed, transition
  count, and whether the entry came from the archive or legacy fallback.
- Invalid, unsupported, mismatched, or unreadable files are not exposed as
  checkpoint entries; valid entries remain discoverable when another file is
  invalid.
- Selecting a discovered entry reuses the existing manual load/restore path;
  the picker does not auto-load or create a second authority path.

## Explicit non-goals

- Browser save serialization or local checkpoint artifacts.
- Automatic loading, session resume policy changes, autosave changes, replay
  regeneration, or simulation rules.
- New dependencies, screenshots, browser certification, human usability,
  accessibility, audio, educational, provenance, or release approval claims.

## Assumptions and stop conditions

- The configured GUI persistence path remains the single host archive root for
  all three launchable campaigns.
- The existing checkpoint wrapper schemas remain the source of truth for
  metadata extraction.
- Stop and report if discovery requires exposing save contents, changing the
  current load route, or adding more than the listed production surfaces.
