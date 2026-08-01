# ADR-0014: AI-native GUI progression and default-browser boundary

**Status:** Accepted
**Date:** 2026-08-01
**Deciders:** Project maintainer and repository agents

## Context

The loopback GUI now covers all three campaigns through a host-authoritative
action surface, durable checkpoints, history/replay, and task workspaces. Earlier
roadmap and evaluation prose treated human pilots, approvals, and cross-browser
certification as promotion gates even though the repository can already verify
many technical properties automatically. The project also has two accepted files
named ADR-0012; their point-in-time decision bodies must remain unchanged.

## Decision

1. Make GUI development the active presentation focus while retaining the CLI as
   a supported, reproducible reference interface and MCP as an agent boundary.
2. Define agent-executable entry and exit criteria for workspace quality,
   consequence legibility, registered assets/audio, default-browser hardening,
   and documentation/evidence maintenance. Technical failures may pause a slice;
   human participation, approval, or review is optional external feedback and is
   never a routine stop gate.
3. Treat automated evidence as bounded: it may establish implementation,
   traceability, replay safety, accessibility-equivalent presence, provenance
   metadata, and browser-default compatibility, but not human learning, lived
   accessibility, legal clearance, calibration, balance, policy validity, or
   resemblance.
4. Support Chromium evergreen desktop as the default end-user browser target.
   Use the Codex in-app browser for development inspection. Defer Firefox,
   WebKit/Safari, mobile, legacy browsers, and real-device certification; existing
   artifacts are historical technical evidence, not active support gates.
5. Fail closed on uncertain asset identity, resemblance, provenance, license, or
   generation metadata by excluding the asset and using a registered generic
   fallback.

## Consequences

- Roadmaps can move from one bounded technical slice to the next without waiting
  for a participant study or sign-off.
- Handoffs must name changed-file groups, checks, evidence limits, and deferred
  browser scope.
- Human and legal questions remain visible as claim limits rather than being
  silently converted into technical completion claims.
- A future browser target or runtime authority change requires a separate ADR and
  implementation slice.
- ADR numbering remains historically imperfect: both
  `0012-loopback-gui-host.md` and `0012-visual-audio-art-direction.md` are
  accepted records. They are preserved and referenced by filename; no renumbering
  is performed.

## Verification

The current implementation is checked against `ARCHITECTURE.md`,
`docs/visual_audio_enhancement_roadmap.md`, the documentation currentness
checker, browser compatibility policy, asset checks, and the Rust/GUI test
suite. This ADR does not change a runtime API, schema, persistence format,
simulation rule, or browser implementation.
