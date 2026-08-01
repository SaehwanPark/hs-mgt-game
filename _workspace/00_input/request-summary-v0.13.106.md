# Request Summary — v0.13.106 Automatic Resume Policy

## User objective

Continue the visual/audio enhancement roadmap through the next unmet item,
using the required loop: bounded plan, implementation, one medium-effort code
review, merge to `main`, temporary-branch cleanup, and re-audit.

## Selected target slice

Make browser-refresh recovery an explicit, inspectable resume policy. The
browser may automatically request one host-owned restore only when it recovered
the opaque session ID from its best-effort session storage after a refresh. A
manually entered session ID remains explicit-load-only. The browser never reads,
parses, serializes, stores, or reconstructs a save artifact.

## Required behavior

- Add a versioned resume-policy contract and source-bound evidence.
- Scope automatic recovery to browser-refresh initialization only.
- Permit at most one host `loadSession` retry, then stop without a retry loop.
- Preserve the opaque ID after transient failures so the user can retry.
- Clear the stored ID after a confirmed unknown-session result.
- Keep manual Load, Restore, checkpoint discovery, reference import, and save
  artifact download explicit and host-authorized.
- Preserve all campaign-specific host authority and actor-visible boundaries.

## Explicit exclusions

- No browser save schema, save bytes, serialization, parsing, or replay
  regeneration.
- No new simulation transition, stochastic input, asset, audio file, or route.
- No automatic checkpoint discovery or automatic selection of a different ID.
- No claim of human usability, accessibility, educational, browser/device, or
  public-release approval.
