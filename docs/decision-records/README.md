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

## Status Values

- **Proposed** — under discussion, not yet implemented
- **Accepted** — reflects current project direction
- **Superseded** — replaced by a later ADR (link the successor)
