# Architecture Decision Records

This directory holds lightweight architecture decision records (ADRs) for
consequential technical and design choices in the Health Policy Strategy Game.
Accepted ADR bodies are point-in-time decisions: do not rewrite them to make
them agree with later implementation. Current operational details belong in
`ARCHITECTURE.md` and the active roadmaps.

## When to Write an ADR

- Changing deterministic core boundaries or replay semantics
- Adding a new strategic actor class or command vocabulary entry
- Introducing a scenario, ruleset, or artifact format version
- Adopting a dependency or CI policy with project-wide impact

## Process

1. Copy [`0000-template.md`](0000-template.md) to the next sequential number.
2. Fill in context, decision, and consequences.
3. Link the ADR from `CHANGELOG.md` or relevant design docs when merged.
4. Do not rewrite accepted ADRs; supersede with a new record if the decision changes.

## Accepted Records

- [ADR-0001: Deterministic transition and stochastic input boundary](0001-deterministic-transition-and-stochastic-input-boundary.md)
- [ADR-0002: Mid-run session save](0002-mid-run-session-save.md)
- [ADR-0003: Simultaneous monthly player actions](0003-simultaneous-monthly-player-actions.md)
- [ADR-0004: Multi-system player state](0004-multi-system-player-state.md)
- [ADR-0005: Action economy and monthly budget](0005-action-economy-and-monthly-budget.md)
- [ADR-0006: Stata-like CLI layer](0006-stata-like-cli-layer.md)
- [ADR-0007: Minimal stabilization scenario TOML](0007-minimal-stabilization-scenario-toml.md)
- [ADR-0008: MCP agent interface](0008-mcp-agent-interface.md)
- [ADR-0009: AI-agent playtest validation path](0009-ai-agent-playtest-validation-path.md)
- [ADR-0010: Regional affiliation runtime slice](0010-regional-affiliation-runtime-slice.md)
- [ADR-0011: Browser-native presentation client and host authority](0011-browser-native-presentation-client.md)
- [ADR-0012A: Loopback GUI host](0012-loopback-gui-host.md)
- [ADR-0012B: Institutional flat visual direction](0012-visual-audio-art-direction.md)
- [ADR-0013: Fixture-only audio direction prototype](0013-audio-direction-prototype.md)
- [ADR-0014: AI-native GUI progression and default-browser boundary](0014-ai-native-gui-and-browser-boundary.md)

## Historical numbering note

The repository accepted two records using the `ADR-0012` identifier. The `A` and
`B` labels above are index-only disambiguators; filenames and decision headers are
preserved. Do not renumber accepted records. ADR-0010 is implemented, not
proposed.

## Status Values

- **Proposed** — under discussion, not yet implemented
- **Accepted** — reflects current project direction
- **Superseded** — replaced by a later ADR (link the successor)
