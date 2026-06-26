# ADR-0008: MCP Agent Interface

**Status:** Accepted  
**Date:** 2026-06-26  
**Deciders:** Project maintainer and implementation agent

## Context

AI agents need a structured way to play the current bounded campaigns
autonomously. The project already has CLI parsers, deterministic transition
functions, actor-visible observations, append-only histories, and replay state
hashes. The interface must preserve the deterministic core boundary from
ADR-0001 and avoid turning this slice into a general networked game server.

The latest MCP specification supports stdio and Streamable HTTP transports. The
official Rust SDK is available as `rmcp`.

## Decision

Add a local stdio MCP server binary, `hs-mgt-game-mcp`, using the official
`rmcp` Rust SDK.

The server exposes tools to:

- start a bounded `stabilization-v1` or `competitive-regional-v1` session;
- read the current actor-visible observation and command format;
- submit one command string for the current turn/month;
- inspect append-only transition summaries and state hashes;
- end a session with a debrief summary.

Session state is in-memory per server process. The MCP layer remains an
interface adapter over existing campaign primitives and does not alter core
transition, RNG, replay, artifact, or save/load semantics.

## Consequences

### Positive

- AI agents can play both current campaigns without scraping terminal prompts.
- The tool surface keeps observations, commands, validation errors, and history
  explicit and inspectable.
- Stdio avoids auth, network, and deployment concerns for the first slice.

### Negative / tradeoffs

- Adds async/MCP dependencies to the package.
- MCP sessions are not durable across process exit.
- The first interface supports only bounded current campaign lengths.

### Follow-ups

- Evaluate whether agent play produces evidence for full competitive campaign
  length, replay export, or durable MCP session persistence.
- Consider Streamable HTTP only when there is a concrete multi-client or remote
  workflow.

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Hand-written JSON-RPC server | Higher protocol-maintenance risk than using the official SDK |
| Streamable HTTP first | Adds auth/network/session complexity before local agent play is validated |
| CLI automation only | Requires agents to parse display text and terminal prompts |
| Expose hidden true state | Conflicts with the project observation boundary and educational design |

## Verification

- `cargo check --bin hs-mgt-game-mcp`
- `cargo test`
- MCP session tests must show invalid commands do not advance state.
- Existing stabilization and competitive golden hashes must remain unchanged.
