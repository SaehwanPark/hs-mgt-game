# Action Catalog Draft

**Status:** Phase 6.0 design artifact  
**Audience:** Simulation implementers, scenario authors  
**Campaign:** `competitive-regional-v1`

All costs, thresholds, and delays are **balancing abstractions** subject to
playtest iteration. They are not empirically calibrated health-finance parameters.

Commands are `verb` + typed arguments. Costs apply on submission. Validation
failures return explicit errors; unfavorable market outcomes are valid modeled
results.

## Cost legend

| Column | Meaning |
| --- | --- |
| AP | Action points consumed this month |
| Cash | Cash debited on submit (may spread for `project`) |
| PC | Political capital consumed |
| Delay | Months until primary effect resolves (0 = same month) |

## MVP verbs

| Verb | Arguments | AP | Cash | PC | Delay | Public? | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `hold` | none | 0 | 0 | 0 | 0 | no | Explicit pass; no state change |
| `recruit` | `role`, `headcount` | 1 | 5×headcount | 0 | 1–3 | yes | Hire clinical or admin staff; delay by role |
| `invest` | `domain`, `amount` | 1 | amount | 0 | 0–2 | yes if amount≥20 | Capacity, technology, or outpatient domain spend |
| `monitor` | `target`, `depth` | depth | 0 | 0 | 0 | no | Intel on rival system; reveals at next report |
| `negotiate` | `payer`, `rate_posture` | 1 | 0 | 2 | 1 | no until outcome | Commercial rate negotiation posture |
| `commit` | `pledge_type`, `level` | 1 | 0 | 1 | 0 | yes | Public access or quality pledge |
| `project` | `kind`, `budget` | 2 | budget/resolve_months per mo | 0 | 6–18 | yes at start | Multi-month pipeline (e.g., EHR migration) |

`hire advisor=<id>` and `fire advisor=<id>` are future proposal-only commands,
not part of the current catalog. A promoted advisor slice must define payroll
timing, roster-cap validation, candidate visibility, and simultaneous-hire
resolution before adding them.

### Argument enums (MVP)

- `role`: `nurse`, `physician`, `admin`
- `domain`: `beds`, `outpatient`, `technology`
- `target`: rival `system_id` (e.g., `northlake`, `summit`)
- `depth`: integer 1–3 (AP cost equals depth)
- `payer`: `carrier_a`, `carrier_b`
- `rate_posture`: `aggressive`, `neutral`, `conservative`
- `pledge_type`: `access`, `quality`
- `level`: integer 1–5
- `kind`: `ehr_epic`, `ehr_cerner`, `tower`, `clinic_network`

## Validation rules

1. Sum of AP costs in monthly batch ≤ monthly AP budget.
2. Cash on hand ≥ sum of cash costs (including scheduled project draws).
3. Political capital ≥ sum of PC costs.
4. At most 2 concurrent `project` commands per system.
5. `recruit` headcount 1–10 per command; ruleset max staffed beds enforced.
6. `invest` amount within ruleset `max_capital_spend` per command.
7. Unknown verb or enum → validation error (not modeled rejection).

## Public vs private actions

| Visibility | Verbs | Observability |
| --- | --- | --- |
| Public | `recruit`, `invest` (large), `commit`, `project` start | Appear in rival reports next month |
| Private | `monitor`, `negotiate`, `hold`, small `invest` | Hidden unless disclosed by event or monitor |

## Delayed effects

`project` and some `recruit` commands enqueue `PendingEffect`:

```text
project ehr_epic budget=60
  → enqueue_month: M
  → resolve_month: M+12
  → monthly_cash_draw: budget / 12  (5 per month)
  → on resolve: quality +Δ, workforce_trust -Δ short-term
```

## Mapping from stabilization commands

Stabilization turn-locked commands remain in `stabilization-v1` only. Competitive
verbs generalize similar ideas:

| Stabilization | Competitive analog |
| --- | --- |
| `StabilizeAccess` | `invest beds` + `negotiate` |
| `RespondToStateAccessMandate` | `commit access` + `negotiate` |
| `RespondToWorkforcePressure` | `recruit nurse` + `invest technology` |
| `JoinRegionalAccessCoalition` | `commit access` (coalition NPC responds) |
| `RespondToCompetitorCapacityMove` | `invest beds` + `monitor` |

## Related documents

- [`cli-command-grammar-draft.md`](cli-command-grammar-draft.md)
- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md) §10–11
- ADR-0005
