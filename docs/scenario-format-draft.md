# Scenario Format Draft

**Status:** Phase 6.2 design draft; stabilization and competitive runtime loading implemented  
**Audience:** Contributors designing scenario loading and campaign content  
**Version:** draft-0.1.28

This document proposes a typed, versioned scenario description for regional
market campaigns. ADR-0007 accepted the first narrow `scenario-toml-0.1.40`
runtime format for the bundled `stabilization-v1` scenario; later slices added
validated custom scenario loading for both `stabilization-v1` and
`competitive-regional-v1`. Broader authoring workflows and scenario migration
tooling remain deferred.

## Campaign kinds

| `campaign_id` | Turn unit | Schedule model |
| --- | --- | --- |
| `stabilization-v1` | abstract | `turn_schedule` maps turn index to command kind |
| `competitive-regional-v1` | month | `campaign_length_months`; open verb catalog per month |

## Design Goals

- Compose known mechanisms without arbitrary executable logic.
- Version scenarios, rulesets, and replay artifacts together per
  [`versioning-policy.md`](versioning-policy.md).
- Support instructor learning objectives and evaluation profiles.
- Keep initial state, actor stubs, and turn schedule inspectable in plain text.

## Proposed Top-Level Fields

| Field | Purpose | Example |
| --- | --- | --- |
| `campaign_id` | Campaign kind | `stabilization-v1` or `competitive-regional-v1` |
| `scenario_id` | Stable identifier | `regional-stabilization-v1` |
| `scenario_version` | Content version string | `1.0.0` |
| `turn_unit` | Calendar mapping | `abstract` or `month` |
| `ruleset_id` | Validation and transition bounds | `demo-ruleset-0.1.9` |
| `title` | Human-readable name | Regional Market Stabilization |
| `learning_objectives` | Instructor-facing goals | List of strings |
| `initial_state` | Genesis state fields | Typed integers matching campaign world state |
| `default_seed` | Suggested run seed | `42` |
| `turn_schedule` | Stabilization only: ordered decision points | Five entries mapping turn index to command kind |
| `campaign_length_months` | Competitive only | `24` |
| `k_competitors` | Competitive only: AI health systems | `2` |
| `difficulty` | Competitive only: profile tier | `normal` |
| `action_catalog_ref` | Competitive only | `action-catalog-draft.md` |
| `event_schedule` | Competitive only: monthly/annual event deck ref | `events-competitive-v1` (placeholder; deck TBD) |
| `systems` | Competitive only: per-system genesis | List of `{system_id, controller, initial_state}` |
| `actor_stubs` | Non-player actor metadata | References to actor-card ids, not decision code |
| `evaluation_profile` | Debrief and assessment hooks | Optional scoring or discussion prompts |

Future expansion fields should be added only after proposal review and domain
QA. Candidate additions include explicit difficulty-pressure profiles
(resource access, information delay, monitoring depth, risk posture), regional
consolidation scenario events or actor stubs, and GUI presentation metadata.
These fields should compose known mechanisms; they must not become executable
logic or a second rules language.

## Turn Schedule Entry (draft)

Each entry describes one executive decision point:

```text
turn: 1
command_kind: StabilizeAccess
briefing_context: commercial_payer_negotiation
actor_stub: commercial_insurer
```

The runtime would validate that interactive or preset play follows the schedule
for **stabilization-v1** campaign mode. Competitive campaigns use open monthly
verbs per `action_catalog_ref`, not `turn_schedule`.

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
- No competitive mid-run save format (stabilization session save: ADR-0002).
- No Medicare/Medicaid actor stubs until first-scenario scope expands.
- No empirical parameter files; use [`evidence-registry.md`](evidence-registry.md)
  ledger when calibrating rulesets.
- No merger/acquisition deal-market schema until one regional consolidation
  slice proves the needed fields.
- No GUI-only scenario behavior; graphical clients should consume existing
  scenario content and observation/debrief outputs.

## Open Questions

1. Should scenarios be TOML, JSON, or a custom line-oriented format?
2. How much of `Ruleset` is inlined versus referenced by id?
3. Should preset strategy paths be scenario data or CLI convenience presets?
4. How do instructors override seed and evaluation profile per session?

## Runtime Loader Gate

For the first runtime slice:

- [x] Domain QA through existing first-scenario scope and learning objectives
- [x] ADR accepting format version and file extension: ADR-0007
- [x] Schema validation tests with one fixture matching current five-turn demo
- [x] CHANGELOG and versioning-policy cross-links updated

Still deferred:

- Scenario migration tooling or schema generation.
- Broader scenario-authoring workflow beyond validated TOML files.

## Related Documents

- [`first-scenario-brief.md`](first-scenario-brief.md)
- [`competitive-scenario-brief.md`](competitive-scenario-brief.md)
- [`system-boundary.md`](system-boundary.md)
- [`decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`](decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md)
- [`phase5-scope-register.md`](phase5-scope-register.md)
