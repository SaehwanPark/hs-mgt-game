# Visual and Audio Phase 0 Alignment

Status: Accepted for Phase 0; implementation remains sequentially gated.

Date: 2026-07-14

Primary target: `competitive-regional-v1`, one competitive month.

This document closes the product and architecture alignment gate from
[`docs/visual_audio_upgrade_proposal.md`](visual_audio_upgrade_proposal.md). It
does not claim that the later graphical, animation, audio, or asset work exists.

## Approved interface boundary

The presentation client is a non-authoritative browser surface over the existing
host/MCP boundary:

```text
deterministic Rust simulation
  -> committed transition and immutable history
  -> actor-visible observation / debrief projection
  -> host or MCP adapter envelope
  -> browser client state
  -> semantic HTML/CSS, native SVG, animation, and optional audio
```

The host remains authoritative for campaign genesis, command parsing and
validation, resolved stochastic inputs, transitions, pending effects, history,
replay/state hashes, and debrief generation. The client may own navigation,
selection, draft command batches, viewport state, animation progress, and local
accessibility/audio preferences. It may not own true state, infer hidden state,
resolve randomness, duplicate formulas, or create GUI-only commands.

The initial technology choice is browser-native HTML, CSS, and JavaScript ES
modules, served as static files or embedded by a later host adapter. Native SVG
is the initial schematic-map and icon format because it supports labels and
semantic inspection without adding a rendering dependency. The first slice has
no framework, bundler, remote asset service, networked core, or deployment
requirement. Later audio playback may use the browser Web Audio API behind the
same boundary; Phase 0 adds no playback code.

## First-month experience contract

The first graphical month must preserve the executive, turn-based perspective:

1. Start or load `competitive-regional-v1` and show the actor-visible session
   date/stage, resources, Riverside identity, facilities, regional signals, and
   current briefing.
2. Inspect one workforce or capacity bottleneck and recent visible payer,
   policy, market, or rival information. Missing, delayed, uncertain, revised,
   and unavailable information must retain those labels.
3. Select at least two contextual actions. The client displays the existing
   canonical command, AP/cash/political-capital cost, known delay, visible
   validation constraints, and consequence categories. It labels stochastic
   results as uncertain and never promises a realized result.
4. Revise or remove draft actions, submit the batch through the host adapter,
   and keep a rejected submission non-mutating.
5. Watch or skip the committed monthly resolution, then inspect visible events,
   effects, operating volume, unmet demand, revenue, cost, margin, pending
   processes, newly visible information, and the resulting state hash.
6. Receive restrained optional cues with a visual/textual equivalent and move to
   the next actor-visible observation. Replay and debrief remain retrospective
   views over committed history.

The first-slice command families are existing `CompetitiveCommand` variants:
`hold`, `recruit`, `invest`, `monitor`, `negotiate`, `commit`, and `project`.
Contextual forms may filter these by selected entity, but may not invent another
command or alter parser semantics.

## Current presentation DTO inventory

This inventory distinguishes existing sources from Phase 2+ structured gaps. It
does not authorize new Rust types during Phase 0.

| Presentation responsibility | Existing actor-visible source | Phase 0 decision |
| --- | --- | --- |
| Campaign/session summary | `SessionEnvelope.campaign`, `seed`, `difficulty`, `turn`, `max_turns`, `done` | Treat as session metadata; preserve current envelope until a typed adapter is promoted. |
| Regional map | `PlayerObservation.market_bullets` and public organization names; current MCP formatting is textual | No map DTO yet; Phase 1 uses injected fixture fields and Phase 2 must add only justified actor-visible projections. |
| Institution/facility detail | `PlayerObservation.org_name`, staffing, service-line capacity, access/quality, trust, and operating fields | Keep field ownership in `PlayerObservation`; do not expose `CompetitiveWorldState` directly. |
| Executive briefing | `market_bullets`, `policy_bullets`, `intel_gaps`, and `consultant_options` | Preserve advisory/non-binding labels and missingness. |
| Action catalog | `legal_commands` plus visible AP/cash/political-capital line | Structured cost/constraint catalog is a Phase 3 adapter requirement; it must reuse command costing/validation. |
| Action preview | No current typed preview; command parser and validator are authoritative | Phase 0 defines required fields only: canonical command, costs, delays, constraints, uncertainty, and validation result. |
| Pending processes | `PlayerObservation.in_flight_projects`, committed effects, and transition events | No client-side countdown or inferred completion; Phase 2+ must use committed visible data. |
| Monthly resolution | `TransitionSummary.events`, `effects`, `state_hash`, and the next `SessionEnvelope` | Render committed summaries first; no presentation transition may change the history. |
| Causal attribution | `AttributedEffect` rendered through transition effects and existing debrief explanations | Show direct committed effects and labeled presentation formulas only; never infer a broad causal graph. |
| Replay/debrief | `HistoryEnvelope.transitions` and `EndSessionEnvelope.debrief` | Preserve observation-time history and hashes; instructor true-state views require a separate authorization. |
| Audio presentation event | No current audio event DTO | Derive future cues only from visible `TransitionSummary` events/effects or explicit client actions. |

### Hidden-state exclusions

The standard client must not receive or infer rival private commands, resolved
stochastic inputs before they become visible, true unreported values, private
actor utility, hidden future effects, server/session internals, or instructor
true-state comparisons. A displayed `seed` remains session metadata already
exposed by the current MCP envelope; it is not a license to derive outcomes.

Organizational outcomes, actor utility, social welfare, decision quality, and
educational evaluation remain separate labels. A visual state or sound may
describe pressure, change, or consequence, but may not declare a universal
ethical or strategic good/bad result.

## Preliminary wireframe

The layout is a responsive executive desktop for laptop and desktop widths. It
uses labels plus icons/patterns, not color alone.

```text
+--------------------------------------------------------------------------------+
| Campaign / month | cash | margin | AP | political capital | trust | save state |
+--------------------------------------------------------------------------------+
| Executive briefing / alerts       | Regional schematic map                    |
| - risk, change, report, rival     | [Riverside] [facilities] [demand zones]    |
| - advisor, source, missingness    | [public signals / legend / status text]   |
|                                   |                                              |
+-----------------------------------+----------------------------------------------+
| Selected institution/facility detail                                             |
| capacity | treated/unmet demand | workforce | access/quality | finance | source |
+--------------------------------------------------------------------------------+
| Contextual action builder                                                        |
| action catalog -> preview/cost/delay/constraint -> draft batch -> remove/revise  |
| [submit through host] [validation result; no stochastic promise]                 |
+--------------------------------------------------------------------------------+
| Pending-process timeline                                                         |
| committed process | visible stage | expected category | delayed/revised marker     |
+--------------------------------------------------------------------------------+
| Monthly resolution / skip / pause / review                                      |
| event -> direct effect -> operating result -> newly visible information         |
+--------------------------------------------------------------------------------+
| Replay / debrief: decisions | observations | hashes | consequences | tradeoffs   |
+--------------------------------------------------------------------------------+
```

Required status language is text plus icon, shape, or pattern for stable, watch,
constrained, critical, improving, uncertain, delayed, and revised states. The
map is schematic: every marker must support a decision or explanation.

## Audio catalog and visible mapping

Audio is optional, restrained, independently controllable, and never required
for comprehension. Every entry has an equivalent text/status/animation path.

### Music states

| State | Visible source | Visual equivalent |
| --- | --- | --- |
| `menu` | No active campaign or explicit menu stage | Menu heading and start/load controls |
| `stable_operations` | Active month, no visible pressure classification, and nonnegative visible margin | Stable status label and unchanged operating summary |
| `pressure` | Visible `WATCH`/`STRAINED` runway, negative margin, unmet demand, staffing constraint, or equivalent committed alert | Pressure banner, source-linked alert, and affected metric |
| `debrief` | End-session/debrief view | Debrief heading and retrospective timeline |

Precedence is `debrief` > `pressure` > `stable_operations` for an active
campaign. The client may crossfade between these states, but the classifier must
be deterministic from the visible summary and may not inspect hidden rival or
stochastic fields.

### Interface cues

| Cue ID | Visible equivalent | Source |
| --- | --- | --- |
| `ui.action-confirm` | Confirmed draft/validation status | Local form result or host validation response |
| `ui.action-reject` | Error text and unchanged-session marker | Host rejection |
| `ui.action-add` | Draft-batch row added | Local draft state |
| `ui.action-remove` | Draft-batch row removed | Local draft state |
| `ui.submit` | Submitted/awaiting-resolution status | Host accepted command batch |
| `ui.advance-month` | Month-resolution control and date change | Committed transition |
| `ui.report-received` | New report/briefing item with source and timing | Committed visible history |
| `ui.save-complete` | Save/session status | Host save result when supported |

### Event cues

| Cue ID | Visible equivalent | Source |
| --- | --- | --- |
| `event.project-complete` | Project completion event and changed process marker | Committed visible event/effect |
| `event.staffing-constraint` | Staffing status and affected capacity explanation | Visible observation/effect |
| `event.operating-loss` | Margin/cost result with direct contributors | Visible monthly result |
| `event.operating-recovery` | Improved margin/result with direct contributors | Visible monthly result |
| `event.payer-decision` | Payer response text and commitment/result marker | Committed visible event |
| `event.regulatory-decision` | Regulatory response text and status marker | Committed visible event |
| `event.rival-expansion` | Public rival action/intelligence line | Public visible event only |
| `event.affiliation-milestone` | Affiliation stage/status marker when that campaign is later supported | Committed visible affiliation history |

No cue is assigned to private rival actions, hidden outcome resolution, or an
unlabeled inferred causal relationship. Repeated cues must be throttled in later
implementation phases, and a missing asset must fall back to the same visual or
textual event without blocking play.

## Asset and license policy

Phase 0 selects policy but adds no release assets. New assets must be CC0/public
domain, manageable CC BY, or a separately reviewed permissive license. Reject
unclear, personal-use-only, noncommercial-only, redistribution-hostile, or
copyright-claim-prone sources by default.

Each approved asset requires a machine-readable registry entry with:

```text
id, release_path, type, title, creator, source_url, retrieval_date,
license, license_url, modifications, original_hash, release_hash,
attribution_text, approval_status
```

Original downloads remain outside the release tree or in an explicitly adopted
large-file store. Optimized release assets and generated `ASSET_CREDITS.md`
belong under a documented presentation/distribution path once Phase 5 begins.
No asset path, license, volume, or playback rule may enter the simulation core.
Original art direction uses consistent line weight, perspective, scale,
recoloring, cropping, and simplification; decorative quantity is not a phase
success criterion.

From the first implemented slice, presentation work must support semantic labels,
keyboard navigation, readable scaling, contrast, color-independent status,
reduced motion, no essential hover-only information, complete mute, independent
audio channels, and non-spatial/non-pitch-only event distinctions. These are
technical design requirements, not lived human accessibility evidence. AI/static
checks are development proxies and do not establish human usability, engagement,
learning, or domain-expert validity.

## Verification and promotion gate

Phase 0 is complete when the following are true:

- The client/host authority flow and hidden-state exclusions are documented.
- Every first-slice action maps to an existing competitive command family.
- Every first-slice displayed value has an existing actor-visible source or is
  explicitly marked as a Phase 2+ structured adapter gap.
- Every audio cue has a visible source and equivalent.
- The contract test passes, metadata is aligned, and no runtime source changes.
- Domain QA records the residual DTO, browser rendering, asset, and audio
  implementation risks.

Phase 1 may be promoted next for a static injected-data executive desktop. It
must not add live transitions, audio playback, broad map production, or campaign
coverage before its own acceptance criteria are present in `SPEC.md`.

## Explicit non-goals

This alignment does not implement a GUI, typed DTOs, action forms, live adapter,
animation, Web Audio playback, asset acquisition, packaging, deployment,
localization, mobile layout, instructor true-state view, or human evaluation.
It does not change simulation rules, balance, stochastic inputs, scenarios,
commands, histories, replay artifacts, state hashes, or debrief semantics.
