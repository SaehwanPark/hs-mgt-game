# AI-Agent Playtest Findings v0.1.55

- **Status:** Phase 7 free-form profile synthesis
- **Date:** 2026-07-02
- **Code version:** 0.1.55
- **Harness:** Existing local MCP stdio client boundary
- **Profiles:** Free-Form Fiscal Steward; Free-Form Access Expansion Advocate

These findings are free-form simulated-agent evidence only. The profiles chose
commands from actor-visible observations, MCP legal-command hints, and
player-facing docs. They do not measure human learning, classroom engagement,
empirical calibration, real-world policy validity, or numeric balance.

## Session Batch

| Campaign | Seed | Difficulty | Profiles | Completed sessions | Validation failures |
| --- | ---: | --- | --- | ---: | ---: |
| `stabilization-v1` | 42 | n/a | Fiscal Steward; Access Expansion Advocate | 2 | 0 |
| `competitive-regional-v1` | 42 | normal | Fiscal Steward; Access Expansion Advocate | 2 | 0 |

All four sessions completed without command validation failures. Competitive
final metrics use the end-session debrief surface derived from committed
history.

## Profile Prompts

- **Free-Form Fiscal Steward:** Protect cash runway, favor low-risk moves,
  monitor rivals before committing, and use modest access commitments when
  legitimacy is at stake.
- **Free-Form Access Expansion Advocate:** Prioritize access, staffed capacity,
  and public legitimacy while preserving enough cash to finish the short
  campaign.

## Submitted Commands

### Stabilization

| Profile | Turn 1 | Turn 2 | Turn 3 | Turn 4 | Turn 5 |
| --- | --- | --- | --- | --- | --- |
| Fiscal Steward | `4 10 106` | `5 4` | `6 4` | `5 4` | `6 4` |
| Access Expansion Advocate | `10 22 110` | `12 8` | `12 7` | `12 9` | `12 8` |

### Competitive Preview

| Profile | Month 1 | Month 2 | Month 3 |
| --- | --- | --- | --- |
| Fiscal Steward | `monitor target=northlake depth=1; hold` | `commit pledge_type=access level=1; hold` | `negotiate payer=carrier_a rate_posture=conservative; hold` |
| Access Expansion Advocate | `invest domain=beds amount=20; recruit role=nurse headcount=4` | `commit pledge_type=access level=3; monitor target=northlake depth=1` | `negotiate payer=carrier_a rate_posture=neutral; invest domain=outpatient amount=10` |

## Observation and Legal-Hint Record

### Stabilization

| Profile | Turn | Actor-visible observation summary | Legal-command hint | Command |
| --- | ---: | --- | --- | --- |
| Fiscal Steward | 1 | Cash 100; staffed beds 120; reported access 71; reported quality 78; state officials increasing scrutiny of access and affordability. | `staffed_beds capital_spend requested_rate` | `4 10 106` |
| Fiscal Steward | 2 | Cash 90; staffed beds 124; reported access 63; reported quality 78; state scrutiny increasing; prior access revision -1. | `advocacy_spend access_commitment` | `5 4` |
| Fiscal Steward | 3 | Cash 85; staffed beds 124; reported access 61; reported quality 78; state policy attention stable; prior access revision 2. | `retention_spend schedule_relief` | `6 4` |
| Fiscal Steward | 4 | Cash 79; staffed beds 124; reported access 64; reported quality 78; state scrutiny increasing; prior access revision -1. | `coalition_investment shared_access_commitment` | `5 4` |
| Fiscal Steward | 5 | Cash 74; staffed beds 124; reported access 64; reported quality 78; state policy attention stable; prior access revision 3; rival outpatient expansion signal. | `defensive_capital access_posture` | `6 4` |
| Access Expansion Advocate | 1 | Cash 100; staffed beds 120; reported access 71; reported quality 78; state officials increasing scrutiny of access and affordability. | `staffed_beds capital_spend requested_rate` | `10 22 110` |
| Access Expansion Advocate | 2 | Cash 78; staffed beds 130; reported access 66; reported quality 78; state scrutiny increasing; prior access revision -1. | `advocacy_spend access_commitment` | `12 8` |
| Access Expansion Advocate | 3 | Cash 66; staffed beds 130; reported access 66; reported quality 78; state policy attention stable; prior access revision 2. | `retention_spend schedule_relief` | `12 7` |
| Access Expansion Advocate | 4 | Cash 54; staffed beds 130; reported access 70; reported quality 80; state scrutiny increasing; prior access revision -1. | `coalition_investment shared_access_commitment` | `12 9` |
| Access Expansion Advocate | 5 | Cash 42; staffed beds 130; reported access 74; reported quality 80; state policy attention stable; prior access revision 3; rival outpatient expansion signal. | `defensive_capital access_posture` | `12 8` |

### Competitive Preview

All three months exposed the same command catalog:

```text
hold
invest domain=beds|outpatient|technology amount=<int>
recruit role=nurse|physician|admin headcount=<int>
monitor target=northlake|summit|valley|metro depth=<1-3>
negotiate payer=carrier_a|carrier_b rate_posture=aggressive|neutral|conservative
commit pledge_type=access|quality level=<1-5>
project kind=ehr_epic|ehr_cerner|tower|clinic_network budget=<int>
Separate multiple commands with ';' on one line.
```

| Profile | Month | Actor-visible observation summary | Available resources | Command |
| --- | ---: | --- | --- | --- |
| Fiscal Steward | 1 | January; reported access 68; quality 72; workforce trust moderate with elevated nursing vacancies; community trust stable; cash runway WATCH; no in-flight projects; stable-to-rising demand; access reporting scrutiny increasing; recruitment timing note visible; Northlake/Summit intel gaps. | AP 3, cash 60, political capital 8 | `monitor target=northlake depth=1; hold` |
| Fiscal Steward | 2 | February; reported access 68; quality 72; workforce trust moderate; cash runway WATCH; Northlake prior-month bed investment observed; Summit private activity unobserved; access scrutiny and recruitment timing notes visible. | AP 3, cash 60, political capital 10 | `commit pledge_type=access level=1; hold` |
| Fiscal Steward | 3 | March; reported access 70; quality 72; workforce trust moderate; cash runway WATCH; Northlake prior-month bed investment observed; payer renewal context and access scrutiny visible. | AP 3, cash 60, political capital 11 | `negotiate payer=carrier_a rate_posture=conservative; hold` |
| Access Expansion Advocate | 1 | January; reported access 68; quality 72; workforce trust moderate with elevated nursing vacancies; community trust stable; cash runway WATCH; no in-flight projects; stable-to-rising demand; access reporting scrutiny increasing; recruitment timing note visible; Northlake/Summit intel gaps. | AP 3, cash 60, political capital 8 | `invest domain=beds amount=20; recruit role=nurse headcount=4` |
| Access Expansion Advocate | 2 | February; reported access 70; quality 72; workforce trust moderate; cash runway STRAINED; Northlake prior-month bed investment observed; Summit private activity unobserved; access scrutiny and recruitment timing notes visible. | AP 3, cash 20, political capital 10 | `commit pledge_type=access level=3; monitor target=northlake depth=1` |
| Access Expansion Advocate | 3 | March; reported access 76; quality 72; workforce trust strained; cash runway STRAINED; Northlake prior-month bed investment observed; payer renewal context and access scrutiny visible. | AP 3, cash 20, political capital 11 | `negotiate payer=carrier_a rate_posture=neutral; invest domain=outpatient amount=10` |

## Run Results

### Stabilization

| Profile | Seed | Final hash | Cash | Access | Workforce trust | Community trust | Policy pressure | Validation failures |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fiscal Steward | 42 | `b5ba1b2a51d998f9` | 68 | 75 | 64 | 66 | 52 | 0 |
| Access Expansion Advocate | 42 | `20ad2f9a97dd9e00` | 30 | 90 | 67 | 73 | 35 | 0 |

The fiscal profile protected cash and accepted weaker access gains, while the
access profile spent heavily to produce a much stronger access and legitimacy
path. Both completed without parser or command-surface friction.

### Competitive Preview

| Profile | Seed | Final hash | Cash | Access | Beds | Workforce trust | Community trust | PC | Market share | Validation failures |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fiscal Steward | 42 | `4479e68d2a4516e3` | 60 | 70 | 118 | 60 | 65 | 11 | 25 | 0 |
| Access Expansion Advocate | 42 | `34a4653b135f1e63` | 10 | 76 | 126 | 56 | 67 | 11 | 26 | 0 |

The fiscal profile remained legal and legible but was passive in a way that
preserved cash while ceding capacity momentum to Northlake. The access profile
used the command surface more fully, converting cash into beds, access, and a
slightly higher market-share position, while lowering workforce trust.

## Causal Explanation

The fiscal stabilization path shows a low-risk strategy that kept cash high but
left policy pressure elevated. A modest initial capacity investment and accepted
commercial rate improved financial flexibility, but low advocacy, coalition,
and defensive commitments produced limited access gains and did not create a
strong state-policy or regional response.

The access stabilization path shows the opposite tradeoff. High capital
spending, state engagement, workforce retention, coalition participation, and a
strong defensive response created a visible access and trust improvement. The
insurer rejected the higher requested rate, so the path achieved legitimacy and
access gains through spending rather than payment leverage.

The fiscal competitive path used monitoring, a small access pledge, and a
conservative payer negotiation. The committed history and debrief show a
plausible cautious strategy: cash stayed at 60, workforce trust stayed at 60,
and access rose only from 68 to 70 while Northlake repeatedly invested in beds.

The access competitive path spent aggressively in month 1, then paired a higher
access pledge with monitoring and a neutral payer negotiation. Access rose from
68 to 76 and staffed beds from 118 to 126, but cash fell to 10 and workforce
trust fell to 56, confirming that capacity expansion carries an immediate
financial and labor-timing cost.

## Gameplay Validity Hypotheses

- **A first-time simulated player can complete a month using actor-visible
  information and command hints:** Pass for these bounded profiles. All four
  sessions completed with zero validation failures.
- **At least three materially different strategies can complete the current
  slice:** Supported when combined with v0.1.54. Fiscal stewardship,
  access-expansion, and first-time balanced play all complete both current
  campaigns with different resource and outcome profiles.
- **Agents can explain the main cause of an outcome from debrief and history:**
  Pass for this synthesis. The committed histories and debriefs identify the
  tradeoffs behind cash preservation, access gains, workforce strain, and
  policy response.
- **No single first-month command dominates:** Still not proven. The profiles
  show distinct successful first moves, but seed 42 and two additional profiles
  are not enough for dominance claims.
- **Rival behavior is recognizable but imperfectly predictable:** Partial pass.
  Monitoring made Northlake's bed investment visible, while Summit private
  activity remained hidden and rival actions continued to shape outcomes.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 5 | Four sessions completed without validation failures or retries. |
| Strategic tension | 4 | Fiscal and access profiles produced sharply different cash, access, and workforce-trust outcomes. |
| Causal transparency | 4 | Histories and debriefs supported causal explanation without implementation details. |
| Pacing proxy | 4 | Both profiles completed both current campaigns without stalls. |
| Action overload proxy | 4 | Competitive profiles used multi-command batches, but the fiscal profile stayed conservative and partially passive. |
| Debrief coherence | 4 | Debriefs separated decisions, outcomes, resources, and committed-history metrics. |
| Exploit discovery | 2 | The batch is still too small and seed-limited for exploit or dominance claims. |

## Evidence Limits

- These are two additional free-form simulated-agent profiles, not human
  playtests.
- Seed 42 remains a bounded validation point, not stochastic characterization.
- The profiles were operator-run through the existing MCP client; they do not
  add reusable LLM orchestration.
- No numeric balance, formula, scenario, actor-behavior, command-surface, MCP
  DTO, or replay-format change should be made from this batch alone.

## Prioritized Follow-Up

1. Treat command comprehension as provisionally supported for the current MCP
   surface, while continuing to label the evidence as simulated-agent evidence.
2. Review competitive monthly report guidance before formula tuning if future
   free-form profiles continue to preserve cash while underusing commitments,
   negotiations, or projects.
3. Promote strategy-space diagnostics only as a lightweight analysis artifact
   once a larger profile/seed matrix is available.
