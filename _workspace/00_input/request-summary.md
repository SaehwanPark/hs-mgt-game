# Request Summary — GUI Thin-Client Proof v0.12.11

## Decision

Implement one small browser surface over existing MCP-shaped outputs and close
the GUI Future item without changing simulation ownership.

## Target slice

- Render observations, legal command hints, history/state hashes, and debrief.
- Delegate submission and legality to an injected MCP adapter.
- Audit assets and verify the static surface locally.

## Explicit non-goals

No duplicated simulation state, parser, transition logic, network service,
hosting, authentication, GUI-only scenario behavior, or CLI/MCP replacement.
