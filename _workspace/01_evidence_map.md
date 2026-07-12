# Evidence Map - Workforce Capacity Difficulty Design Gate v0.12.5

## Scope

Decide whether the v0.12.4 workforce-capacity signal is interpretable from the
current decision-time MCP observation, and define the smallest safe projection
follow-up if it is not.

## Sources Reviewed

- `_workspace/experiments/v0.12.4-difficulty-depth-evidence/results.json` and
  `diagnostics.md`.
- `src/model/campaign.rs` (`PlayerObservation`).
- `src/sim/observe_competitive.rs` observation construction and consultant
  options.
- `src/mcp/session.rs` competitive observation formatter and session tests.
- `src/sim/transition_competitive.rs` staffing constraints and operating events.
- `src/debrief/report.rs` attribution and decision/outcome framing.
- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/playtest-findings-v0.11.11.md` / `v0.11.12.md`.

## Evidence chain

| Stage | Existing surface | Design finding |
| --- | --- | --- |
| prior evidence | v0.12.4 reports workforce-capacity counts 0/15/30/160 by tier | candidate pressure signal only |
| decision context | workforce trust summary, nursing vacancy note, prior operations, labor-market note, consultant option B | visible but not numerically specific |
| typed observation | nurses, physicians, admins, staffed beds, outpatient and service-line capacities | safe fields exist in `PlayerObservation` |
| MCP projection | `format_competitive_observation` omits those staffing/capacity fields | bounded observation-context gap |
| transition/debrief | staffing deficit/capacity events, operating effects, attributed mechanisms, decision/outcome separation | follow-through exists; decision context is incomplete |

## Actor and information boundaries

- Safe to render: Riverside's own staffing counts and physical capacities
  already present in `PlayerObservation`.
- Already visible: workforce trust category, prior operating results, generic
  labor-market delay/cost note, and state-conditioned consultant tradeoffs.
- Not safe to render: hidden staffing targets, effective allocation by service
  line, future pending hires, rival private workforce state, or realized future
  actor responses.

## Concrete gap

The MCP player view says workforce trust is strained and that nursing vacancy is
elevated, but it does not show the current Riverside staffing counts or the
physical capacity that the staffing constraint is limiting. A player or
instructor cannot inspect the numeric decision context for the v0.12.4 signal
from the MCP observation alone, even though the typed observation already owns
safe current values and the debrief later explains the realized constraint.

This supports an interface projection follow-up, not difficulty or balance
tuning.

## Design assumptions and limits

- `PlayerObservation` remains the authoritative safe source for any new lines.
- A field's presence does not establish that humans understand it or that a
  difficulty tier is balanced.
- The v0.12.4 source version and simulated-policy limits remain explicit.
- The next implementation gate must rerun the same v0.12.4 evidence matrix and
  compare history/state hashes exactly.

## Routing decision

`observation_context_follow_up_required`: yes.

The follow-up should render a compact staffing line and a compact physical
capacity line from existing typed fields, add MCP boundary tests, and preserve
all transition, replay, hash, command, and competitive golden contracts.
