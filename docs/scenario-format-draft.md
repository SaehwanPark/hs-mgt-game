# Scenario Format Draft

**Status:** Phase 6.2 design draft (not approved for runtime)  
**Audience:** Contributors designing scenario loading and campaign content  
**Version:** draft-0.1.24

This document proposes a typed, versioned scenario description for the first
regional stabilization campaign. It is a **design artifact only**. No runtime
loader, parser, or schema validation ships until this draft is reviewed and an
ADR approves a format version.

## Design Goals

- Compose known mechanisms without arbitrary executable logic.
- Version scenarios, rulesets, and replay artifacts together per
  [`versioning-policy.md`](versioning-policy.md).
- Support instructor learning objectives and evaluation profiles.
- Keep initial state, actor stubs, and turn schedule inspectable in plain text.

## Proposed Top-Level Fields

| Field | Purpose | Example |
| --- | --- | --- |
| `scenario_id` | Stable identifier | `regional-stabilization-v1` |
| `scenario_version` | Content version string | `1.0.0` |
| `ruleset_id` | Validation and transition bounds | `demo-ruleset-0.1.9` |
| `title` | Human-readable name | Regional Market Stabilization |
| `learning_objectives` | Instructor-facing goals | List of strings |
| `initial_state` | Genesis `WorldState` fields | Typed integers matching `model/state.rs` |
| `default_seed` | Suggested run seed | `42` |
| `turn_schedule` | Ordered executive decision points | Five entries mapping turn index to expected command kind |
| `actor_stubs` | Non-player actor metadata | References to actor-card ids, not decision code |
| `evaluation_profile` | Debrief and assessment hooks | Optional scoring or discussion prompts |

## Turn Schedule Entry (draft)

Each entry describes one executive decision point:

```text
turn: 1
command_kind: StabilizeAccess
briefing_context: commercial_payer_negotiation
actor_stub: commercial_insurer
```

The runtime would validate that interactive or preset play follows the schedule
for campaign mode. The current five-turn demo hard-codes this schedule in CLI
strategy paths.

## Actor Stubs

Actor stubs link scenario content to [`actor-cards.md`](actor-cards.md) without
embedding decision logic:

```text
id: commercial_insurer
card_ref: actor-cards.md#commercial-insurer
turn: 1
```

Stubs must not include hidden payoff tables or undisclosed random draws. All
stochastic inputs remain in `ResolvedInputs` at runtime.

## Relationship to Replay Artifacts

| Artifact | Direction | Notes |
| --- | --- | --- |
| Scenario file | Input to a run | Defines genesis, ruleset, schedule, objectives |
| Replay artifact | Output of a completed run | Records actual commands, resolved inputs, hashes |
| Ruleset | Shared reference | Validation bounds; versioned separately |

A scenario file must not rewrite committed history. Replay artifacts remain the
source of truth for what actually happened in a session.

## Non-Goals (this draft)

- No executable scripts, WASM, or general-purpose expression language.
- No mid-run save format.
- No Medicare/Medicaid actor stubs until first-scenario scope expands.
- No empirical parameter files; use [`evidence-registry.md`](evidence-registry.md)
  ledger when calibrating rulesets.

## Open Questions

1. Should scenarios be TOML, JSON, or a custom line-oriented format?
2. How much of `Ruleset` is inlined versus referenced by id?
3. Should preset strategy paths be scenario data or CLI convenience presets?
4. How do instructors override seed and evaluation profile per session?

## Approval Gate Before Runtime Loader

Before implementing `feat/scenario-loader`:

- [ ] Domain QA on scenario scope and learning objectives
- [ ] ADR accepting format version and file extension
- [ ] Schema validation tests with one fixture matching current five-turn demo
- [ ] CHANGELOG and versioning-policy cross-links updated

## Related Documents

- [`first-scenario-brief.md`](first-scenario-brief.md)
- [`system-boundary.md`](system-boundary.md)
- [`decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`](decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md)
- [`phase5-scope-register.md`](phase5-scope-register.md)
