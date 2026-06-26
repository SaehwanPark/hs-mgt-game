# Architecture Decision Records

This directory holds lightweight architecture decision records (ADRs) for
consequential technical and design choices in the Health Policy Strategy Game.

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

## Status Values

- **Proposed** — under discussion, not yet implemented
- **Accepted** — reflects current project direction
- **Superseded** — replaced by a later ADR (link the successor)
