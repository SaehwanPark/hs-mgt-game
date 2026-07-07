# Competitive Gameplay Sketch — Canonical Specification

**Status:** Phase 6.0 design artifact; 24-month runtime implemented
**Audience:** Contributors, domain reviewers, playtest designers  
**Campaign:** `competitive-regional-v1` (parallel to stabilization demo)

This document expands the user gameplay sketch into requirements with acceptance
criteria. Initial runtime slices I1-I8 and the full 24-month campaign loop are
complete; future work should be driven by playtest, authoring, debrief, or
domain-review evidence.

## Overview

The competitive campaign models a regional US health market where one human player
and K AI-controlled health systems compete for access, margin, workforce, and
community trust over a multi-month horizon. All players share one market model;
they differ only in command choices (human input vs programmed logic plus bounded
stochastic tie-breaks).

## Sketch Requirements

### 1. Monthly strategy turns

**Requirement:** One strategy turn equals one calendar month.

**Mechanics:**

- `turn_unit: month` in scenario format
- Display `Year Y, Month M` in executive report
- Campaign length parameterized (default 24 months)

**Acceptance criteria:**

- [x] Scenario format documents `turn_unit` and `campaign_length_months`
- [x] Core loop spec describes month advance and year boundary
- [x] Stabilization demo remains on abstract turns until separately migrated

---

### 2. Executive one-page report briefing

**Requirement:** Briefing resembles a one-page executive report with bullet
points covering market situation, policy movements, own health system status, and
related context.

**Mechanics:**

- Six-section report schema in `docs/executive-report-format.md`
- Realistic tone: headline metrics, bullet lists, short analyst notes
- Rendered in CLI before human decision phase

**Acceptance criteria:**

- [x] Report schema has all six sections with field definitions
- [x] Example month report included in executive-report-format doc
- [x] Report uses observation data only (no future outcome leakage)

---

### 3. Consultant recommendations

**Requirement:** Several recommendable actions with strategy-consultant thoughts;
players may or may not follow advice.

**Mechanics:**

- 2–4 options per month with tradeoff rationale
- Generated deterministically from scenario templates + state conditions
- Labeled "Advisory — not binding" in report
- Multiple defensible paths remain viable

**Acceptance criteria:**

- [x] Mechanism design documents generation rules
- [x] Debrief compares advisory vs actual player choices
- [x] No single option marked as "correct"

---

### 4. One player per health system

**Requirement:** Each health system is controlled by one player (human or computer).

**Mechanics:**

- `HealthSystemPlayer` entity with `system_id` and `controller: Human | Ai`
- Exactly one human-controlled system per run
- K AI-controlled systems per difficulty profile

**Acceptance criteria:**

- [x] ADR-0004 defines multi-system player state
- [x] Actor cards include AI player card template distinct from NPC cards
- [x] Scenario format includes `k_competitors` and `difficulty`

---

### 5. One human + K competing AI players

**Requirement:** One human plus multiple computer competitors; K varies by
difficulty (Capitalism-style).

**Mechanics:**

- Difficulty table: Easy K=1 through Expert K=4
- AI ability tier and style weights vary by profile
- Asymmetric starting conditions allowed per scenario

**Acceptance criteria:**

- [x] Difficulty profiles documented in mechanism design and scenario brief
- [x] Evidence map cites Capitalism-style precedent
- [x] Competitive scenario brief lists default K per tier

---

### 6. Shared market model

**Requirement:** All players share the model; only action choice differs
(human vs programmed logic + stochastics).

**Mechanics:**

- Single `CompetitiveWorldState` with `systems[]` vector
- Same action catalog and validation rules for all players
- AI stochasticity only in tie-break and forecast noise streams

**Acceptance criteria:**

- [x] ADR-0004 specifies shared `CompetitiveWorldState`
- [x] No per-player duplicate market simulation
- [x] Replay stores all player action batches in one history (runtime)

---

### 7. Simultaneous monthly actions

**Requirement:** Players take actions in sequence during UX, but all actions for
the same month are treated as simultaneous choices.

**Mechanics:**

- Human enters commands during decision phase
- AI batches computed before resolution from pre-resolution observations
- `SimultaneousActionResolver` aggregates then calls `transition()`
- Deterministic sub-step order by `system_id`

**Acceptance criteria:**

- [x] ADR-0003 documents resolution contract
- [x] Core loop spec shows simultaneous resolve step
- [x] AI choices not revealed to human before human submits (same-month)

---

### 8. Partial observability of rival decisions

**Requirement:** Each player can partly observe prior decisions other players made.

**Mechanics:**

- Public action log with 1-month lag for announcements and pledges
- `monitor` verb reduces intel lag for AP cost
- Private negotiations hidden until disclosed

**Acceptance criteria:**

- [x] Mechanism design defines public vs private action classes
- [x] Executive report includes observed rival moves section
- [x] Intelligence gaps section lists unobserved rival activity

---

### 9. Game-theory AI for computer players

**Requirement:** Apply competitive game theory to model computer decisions.

**Mechanics:**

- Bounded level-1 best response to observed rival moves ([`design_principles.md`](design_principles.md) §5)
- Style-weighted utility; satisficing threshold
- No global equilibrium solver ([`phase1-implications-memo.md`](phase1-implications-memo.md))
- Inspectable rationale per AI decision

**Acceptance criteria:**

- [x] AI player card template in actor-cards.md
- [x] Design principles §5 cited; phase1 memo rejection of global equilibrium
- [x] Named RNG stream per AI for tie-break only (runtime)

---

### 10. Command + arguments action model

**Requirement:** Player action is command plus arguments (recruit, invest, monitor, …).

**Mechanics:**

- Verb + typed arguments per `docs/action-catalog-draft.md`
- Stata-like surface syntax maps to typed commands

**Acceptance criteria:**

- [x] Action catalog draft lists MVP verbs with args and validation
- [x] CLI grammar draft documents parse mapping
- [x] Invalid commands fail validation separately from unfavorable outcomes (design)

---

### 11. Action costs and monthly limits

**Requirement:** Each action has its own cost; monthly limit on player capacity;
CPU limits may vary by difficulty.

**Mechanics:**

- Costs: cash, action points, optional political capital
- Monthly AP budget per player; difficulty scales CPU AP
- Cash feasibility enforced at validation

**Acceptance criteria:**

- [x] ADR-0005 documents action economy
- [x] Action catalog includes cost columns per verb
- [x] Difficulty table links CPU AP to tier

---

### 12. Stata-like human CLI

**Requirement:** Human actions entered like Stata commands with color syntax and
autocomplete; in-game help for commands.

**Mechanics:**

- `verb arg1=value arg2=value` grammar
- Syntax highlighting when TTY and color enabled
- Tab autocomplete for verbs and enum args
- `help <verb>` and `help` global

**Acceptance criteria:**

- [x] `docs/cli-command-grammar-draft.md` complete
- [x] ADR-0006 limits parser to I/O layer
- [x] LESSONS.md documents competitive-track parser exception

---

### 13. Random events

**Requirement:** Random events reduce excessive determinism in play experience.

**Mechanics:**

- `monthly_events` stream at month start
- Narrative + bounded numeric shock
- Logged in committed history

**Acceptance criteria:**

- [x] Scenario format includes `event_schedule` or deck reference (placeholder)
- [x] Events resolved in `inputs/resolve.rs` per ADR-0001 (runtime)
- [x] Debrief can cite event impacts

---

### 14. Delayed action effects

**Requirement:** Some actions take longer than others (e.g., Epic EHR migration).

**Mechanics:**

- `PendingEffect` queue with enqueue and resolve months
- `project` verb for multi-month pipelines
- In-flight status in own-system report section

**Acceptance criteria:**

- [x] Action catalog documents delay column per verb
- [x] Architecture documents `EffectScheduler`
- [x] Mechanism design includes EHR example

---

### 15. Yearly policy and insurance changes

**Requirement:** Policy and insurance changes may operate on longer periods
(e.g., yearly).

**Mechanics:**

- Annual tick at month 12, 24, …
- `annual_policy` stream resolves insurance renewal and major policy shifts
- Monthly `policy_signal` for shorter movements

**Acceptance criteria:**

- [x] Core loop spec documents annual tick
- [x] Executive report policy section flags year-in-review on annual months
- [x] Evidence map documents annual cadence rationale

## Non-goals

- Replacing or refactoring the stabilization demo
- Medicare/Medicaid actors in competitive v1
- Classroom hot-seat multiplayer (Phase 9)
- Empirical forecasting claims
- LLM-generated consultant advice

## Implementation sequence

See `SPEC.md` Future for gated next work. The initial I1-I8 runtime sequence and
24-month campaign loop are complete; likely next work should come from playtest
synthesis, competitive hardening, or scenario-authoring evidence.

## Related documents

- [`core-loop-spec.md`](core-loop-spec.md)
- [`competitive-scenario-brief.md`](competitive-scenario-brief.md)
- [`executive-report-format.md`](executive-report-format.md)
- [`action-catalog-draft.md`](action-catalog-draft.md)
- [`cli-command-grammar-draft.md`](cli-command-grammar-draft.md)
- [`../_workspace/02_mechanism_design.md`](../_workspace/02_mechanism_design.md)
