# Executive Report Format

**Status:** Phase 6.0 design artifact  
**Audience:** CLI implementers, instructors, playtest designers  
**Renders in:** `src/cli/display/executive_report.rs` (competitive campaign)

## Purpose

Define the one-page executive report shown to the human player before each
monthly decision. The report should read like a condensed management consulting
brief: bullet points, headline metrics, short analyst notes — not a raw debug dump.

## Section schema

| # | Section id | Title | Content |
| --- | --- | --- | --- |
| 1 | `header` | Executive summary header | `Year Y, Month M`; org name; remaining AP; cash runway signal |
| 2 | `market` | Market situation | Regional demand signal; observed rival moves (lagged); payer landscape bullets |
| 3 | `policy` | Policy and regulatory | State/federal signals; annual year-in-review block on month 12, 24, … |
| 4 | `own_status` | Health system status | Reported access, quality, workforce, trust, in-flight projects |
| 5 | `consultant` | Strategy consultant notes | 2–4 advisory options with tradeoff bullets; "Advisory — not binding" label |
| 6 | `intel_gaps` | Intelligence gaps | What rival activity is unobserved; hint that `monitor` may help |

## Field rules

- All metric values come from `PlayerObservation`, not true state.
- Indices (access, quality) use abstract 0–100 design scales, not empirical measures.
- Example percentages are illustrative reported deltas, not forecasts.
- Rival moves cite `public_action_log` entries from month t-1.
- Consultant options are deterministic template variants; never label one "optimal."
- Cash runway signal: `comfortable` / `watch` / `strained` from ruleset thresholds.
- On annual months, `policy` section leads with **Year in review** subsection.

## Current implementation note

The first interactive CLI report uses fixture consultant options. Later live
reports and the MCP observation path currently provide an empty consultant
option list. The 2-4-option section remains a design requirement, not a claim
that every current observation delivers advice. Restoring deterministic,
state-conditioned monthly advice is separate from the future advisor-market
proposal in [`expansion-proposal-review.md`](expansion-proposal-review.md).

## Example report (Month 4, Year 1)

```text
══════════════════════════════════════════════════════════════
  EXECUTIVE REPORT — Riverside Community Health
  Year 1, Month 4 (April)          Action points remaining: 3/3
  Cash runway: WATCH
══════════════════════════════════════════════════════════════

MARKET SITUATION
  • Regional inpatient demand: stable-to-rising (+1.2% vs prior month, reported)
  • Rival Northlake Health (observed, March): announced 12-bed med-surg expansion
  • Rival Summit Care (observed, March): held capacity; increased outpatient marketing
  • Commercial payer mix: two major carriers; renewal discussions expected Q4

POLICY AND REGULATORY
  • State Medicaid director signal: access reporting scrutiny increasing
  • Hospital association lobbying: workforce retention tax credit under committee review
  • No federal rule change this month

OWN HEALTH SYSTEM STATUS
  • Reported access index: 71 (prior revision: 69 in Month 2)
  • Reported quality index: 74
  • Workforce trust: moderate; vacancy rate elevated in nursing
  • Community trust: stable
  • In-flight: none

STRATEGY CONSULTANT NOTES — Advisory, not binding
  • Option A — Defensive capacity: invest in staffed beds to match Northlake
      expansion; protects share but strains cash if payer rate unchanged.
  • Option B — Workforce-first: recruit nurses and offer schedule relief;
      slower share defense but reduces escalation risk.
  • Option C — Monitor Summit: spend AP on competitor intelligence before
      committing capital; delays response one month.
  • Option D — Public access pledge: commit to ED wait-time target;
      may pre-empt state scrutiny; rivals will observe.

INTELLIGENCE GAPS
  • Northlake private payer negotiations (not publicly disclosed)
  • Summit capital budget allocation beyond marketing (unobserved)
  • Consider: monitor northlake depth=2 (cost: 1 AP)
══════════════════════════════════════════════════════════════
```

## CLI presentation notes

- Use existing `cli/display/style.rs` tokens for section headers and bullets.
- Respect `NO_COLOR` environment variable.
- Keep total output roughly one terminal screen at 80 columns (soft target).
- Consultant section uses indented bullets; options labeled A–D.

## Related documents

- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md) §2, §3
- [`core-loop-spec.md`](core-loop-spec.md)
- [`action-catalog-draft.md`](action-catalog-draft.md) (`monitor`, `commit`)
