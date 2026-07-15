# ADR-0012: Loopback GUI Host

**Status:** Accepted
**Date:** 2026-07-15
**Deciders:** Project maintainer and implementation agent

## Context

ADR-0011 established a non-authoritative browser client and deferred networking.
The completed first-month source contracts still could not start a shipped game:
the page required manual adapter injection, while the only Rust host used stdio
MCP. Mock-adapter tests did not exercise this browser transport gap.

## Decision

Add `hs-mgt-game-gui`, a loopback-only Axum host that embeds the existing GUI
files and exposes same-origin JSON routes over `GameSessionStore`. Inject the
local action adapter only into pages served by this binary. Keep sessions in
memory and support the competitive GUI path only. The HTTP start DTO accepts
only campaign, seed, and difficulty; it rejects custom scenario paths and
unknown fields.

The Rust store remains authoritative for session creation, observations, action
catalogs, validation, transitions, resolved inputs, history, hashes, replay, and
debriefs. The browser continues to own only presentation, navigation, drafts,
audio, and local settings.

## Consequences

### Positive

- A player can start and complete the competitive first month with one Cargo
  command and no MCP or adapter setup.
- Static fixture and externally injected-adapter workflows remain available.
- Same-origin loopback transport avoids CORS and remote exposure.

### Negative / tradeoffs

- Axum and its HTTP dependencies become part of the package.
- GUI session IDs disappear when the host stops.
- Stabilization and affiliation still require CLI play.

### Follow-ups

- Treat persistence, remote binding, authentication, packaging, and other GUI
  campaigns as separately authorized work.

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Keep manual adapter injection | Leaves the player-facing Start control unusable from a normal checkout. |
| Browser-owned simulation | Duplicates legality and transition rules and violates deterministic host authority. |
| Remote/production web service | Adds authentication, persistence, deployment, and security scope not required for local play. |
| Hand-written HTTP parsing | Creates avoidable protocol and security risk compared with a maintained router. |

## Verification

- Transport tests start a real competitive session, load typed reads, validate
  and submit a command, and read the committed resolution.
- Bind parsing rejects non-loopback addresses.
- Browser and documentation tests preserve demo/live distinctions and the exact
  player launch command.
