# Visual and Audio Phase 1 — Static Executive Desktop

Status: Implemented and merged as a fixture-only information-architecture prototype in PR #168.

Date: 2026-07-15

Primary target: one actor-visible `competitive-regional-v1` month.

This document records the Phase 1 implementation promised by
[`docs/history/initiatives/visual-audio/visual-audio-upgrade-proposal.md`](visual-audio-upgrade-proposal.md) and
the Phase 0 boundary in
[`docs/history/initiatives/visual-audio/visual-audio-phase0-alignment-v0.12.16.md`](visual-audio-phase0-alignment-v0.12.16.md).
It validates information architecture, not live integration or polished artwork.

## User and use context

The target user is an executive or first-time reviewer who needs to decide what
to inspect next on a typical laptop or desktop. Their immediate job is to locate
financial pressure, workforce/capacity bottlenecks, access/quality context, and
public rival signals without learning CLI syntax or reading raw JSON or CLI output.

The common path is deliberately short: read the header and briefing, select a
system from the regional cards, inspect its facilities, review visible action
costs/delays/constraints, then compare pending processes with the committed
monthly result. Advanced command entry remains visibly labeled as an adapter
path rather than being disguised as a local form resolver.

## Implemented presentation surface

`gui/app.mjs` adds an optional `presentation_fixture` to the existing display
envelope. It is injected fixture data, not simulation state. `renderPresentation`
uses it to render:

| Surface | Fixture source | User-facing purpose |
| --- | --- | --- |
| Executive header | `header_metrics` | Find month, cash, margin, AP, political capital, trust, and session status. |
| Executive briefing | `briefing` | Find source-linked workforce, operations, and public rival signals. |
| Regional schematic | `entities` | Navigate among Riverside and public rival system cards. |
| System/facility cards | `entities[].facilities` | Inspect visible capacity, staffing, and facility summaries. |
| Selected detail | `entities[].metrics` and `facilities` | Compare access, quality, workforce, margin, and visible facility status. |
| Contextual action panel | `actions` | Preview existing command families, costs, delays, constraints, and uncertainty. |
| Pending timeline | `pending` | Track visible commitments without promising hidden future results. |
| Monthly result | `monthly_result` | Read direct visible volume, unmet demand, revenue/cost/margin, and effects. |
| Existing contracts | `observation`, `legal_commands`, `history`, `debrief` | Preserve the previous MCP-shaped proof and adapter-owned path. |

Entity-card selection updates `selectedEntityId` and re-renders the selected
detail only. It does not call an adapter, alter a command, advance a month, or
resolve an outcome.

## Design and accessibility decisions

- CSS custom properties define color, spacing, radius, surface, and status
  tokens; a status always includes text and a diamond marker.
- The desktop uses semantic sections, headings, lists, definition lists, and
  keyboard-focusable buttons for entity selection.
- Grid columns collapse at 1120px, 760px, and 500px to preserve reading order on
  narrower laptop widths; the first release remains desktop-oriented.
- `prefers-reduced-motion: reduce` disables transitions. No information depends
  on hover, color, pitch, or downloaded imagery.
- Public-rival cards explicitly label private actions as unavailable. The
  fixture contains no true-state, resolved-input, or private-actor fields.

## Static review checklist

The reviewer should be able to complete these tasks from the rendered page:

1. Locate cash, monthly margin, AP, political capital, and workforce trust.
2. Identify the nursing/capacity bottleneck and its source-linked briefing item.
3. Select Riverside, Northlake, and Summit cards and inspect each detail panel.
4. Find access/quality, workforce, capacity, and facility status information.
5. Find the public rival expansion signal and the explicit private-information gap.
6. Read an action's canonical command, cost, delay, constraint, and uncertainty.
7. Follow a delayed/uncertain process and a monthly result to their visible source.
8. Repeat at a narrow viewport and using keyboard focus on the system cards.

Automated checks cover source structure, syntax, token/responsive markers,
adapter preservation, and no external asset/network calls. These are technical
and interface-task proxies only; they do not establish human usability,
engagement, lived accessibility, learning, classroom effectiveness, or domain
validity.

## Explicit non-goals and next gate

This phase does not implement typed live DTOs, live read-only integration,
command validation forms, monthly resolution, animation, audio, assets, replay
visualization, instructor true-state views, mobile support, or other campaigns.
It does not change Rust, MCP, scenarios, commands, transitions, randomness,
history, replay artifacts, hashes, or debrief semantics.

Phase 2 is the next candidate: a typed live/recorded adapter that renders only
actor-visible observations, entity detail, pending/history/hash views, and
explicit missingness. Phase 2 must first prove that a structured projection is
needed; it may not expose `CompetitiveWorldState` directly or duplicate formulas.
