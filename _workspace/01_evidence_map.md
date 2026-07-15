# Evidence Map — Visual and Audio Phase 2 Live Read-Only Integration v0.12.18

## Scope

Phase 2 promotes only a typed read-only projection for one
`competitive-regional-v1` viewer. It connects live or recorded host data to the
Phase 1 presentation surfaces without enabling actions or claiming human
usability.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 2 requirements and exit gate.
- Phase 0 alignment, ADR-0011, Phase 1 static-desktop document, and merged GUI.
- `src/mcp/session.rs`, `src/mcp/server.rs`, `src/sim/observe_competitive.rs`,
  `PlayerObservation`, `CompetitiveTransition`, and existing MCP tests.
- README, SPEC, architecture, design principles, and project harness spec.

## Mechanisms and Institutions

The host computes the competitive observation and committed history. A typed
presentation projection selects the player's visible institution/capacity
metrics, public market signals, visible pending processes, and transition
summaries. The browser renders those values and can identify a selected player
facility, but does not model a regional world of its own.

## Actor Incentives and Information

The player receives the same actor-visible facts already supplied through the
MCP observation plus typed session resources, public signals, explicit gaps,
pending process text, and committed hashes. Legal commands are deliberately not
part of the Phase 2 read-only envelope. Private rival commands, true world
state, effect queues, event metadata, resolved stochastic inputs, and non-player
private utility remain excluded.

## Assumptions

- `PlayerObservation` and committed transition summaries are the authoritative
  source for the DTO; the projection does not recalculate outcomes.
- The first typed contract targets the competitive campaign only and can be
  returned by either a live MCP adapter or a recorded fixture provider.
- Facility detail means observed player capacity/staffing lines until a future
  structured facility source is justified.
- Loading, errors, empty arrays, missing fields, and unsupported campaigns are
  meaningful states, not reasons to guess or silently fall back to true state.

## Unresolved Questions

- Whether later phases need typed public rival identities beyond market bullets.
- Which structured action catalog fields should be promoted for Phase 3 without
  duplicating command costing/validation.
- How much replay navigation is useful after the first non-mutating history
  view; Phase 2 only establishes the view and metadata.

## Design Implications

- The MCP contract needs a separate read-only presentation request/tool rather
  than overloading `submit_turn` or exposing `CompetitiveWorldState`.
- The browser adapter needs a versioned envelope and must not depend on whether
  the host source is live or recorded.
- State hashes and transition summaries belong to immutable committed history;
  selection and loading state remain local presentation state.
- Unsupported campaigns and missing fields must be visible so a later campaign
  cannot silently inherit competitive semantics.

## Risks

Typed fields can create false confidence if they drift from CLI/MCP formatting,
or if DTO projection accidentally serializes true-world fields. Rust parity and
JSON exclusion tests are therefore promotion gates. Browser static checks are
technical interface proxies and cannot establish human usability, lived
accessibility, learning, or domain validity.
