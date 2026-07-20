# AI-Agent Playtest Findings v0.1.54

- **Status:** Phase 7 free-form agent evidence
- **Date:** 2026-07-02
- **Code version:** 0.1.54
- **Harness:** Existing local MCP stdio client boundary
- **Profile:** Free-Form First-Time Executive

These findings are free-form simulated-agent evidence only. The profile chose
commands from actor-visible observations, MCP legal-command hints, and
player-facing docs. It does not measure human learning, classroom engagement,
empirical calibration, real-world policy validity, or numeric balance.

## Session Batch

| Campaign | Seed | Difficulty | Completed sessions | Validation failures |
| --- | ---: | --- | ---: | ---: |
| `stabilization-v1` | 42 | n/a | 1 | 0 |
| `competitive-regional-v1` | 42 | normal | 1 | 0 |

Both sessions completed without command validation failures. Competitive final
metrics use the end-session debrief surface derived from committed history.

## Profile Prompt

Play as a first-time executive who reads only the current observation, legal
command hints, and player-facing docs. Preserve enough cash to stay flexible,
but act on visible access, workforce, policy, and market pressure. After the
run, explain the main causal path using transition history and debrief text
rather than hidden implementation details.

## Submitted Commands

### Stabilization

| Turn | Observation cue | Command |
| ---: | --- | --- |
| 1 | Access scrutiny, adequate starting cash, staffed-bed pressure | `8 18 112` |
| 2 | Lower reported access and state scrutiny | `9 7` |
| 3 | Workforce pressure after capacity investment | `10 6` |
| 4 | Coalition opportunity with community-trust stakes | `8 8` |
| 5 | Rival outpatient expansion signal | `10 6` |

### Competitive Preview

| Month | Observation cue | Command |
| ---: | --- | --- |
| 1 | Northlake intel gap, nursing vacancies, cash watch | `monitor target=northlake depth=1; recruit role=nurse headcount=3` |
| 2 | Northlake observed bed investment, access scrutiny | `invest domain=beds amount=15; commit pledge_type=access level=1` |
| 3 | Strained cash, improved access, payer renewal context | `negotiate payer=carrier_a rate_posture=neutral; hold` |

## Observation and Legal-Hint Record

### Stabilization

| Turn | Actor-visible observation summary | Legal-command hint |
| ---: | --- | --- |
| 1 | Cash 100; staffed beds 120; reported access 71; reported quality 78; policy briefing: state officials are increasing scrutiny of access and affordability. | `staffed_beds capital_spend requested_rate` |
| 2 | Cash 82; staffed beds 128; reported access 65; reported quality 78; policy briefing: state officials are increasing scrutiny; prior access revision -1. | `advocacy_spend access_commitment` |
| 3 | Cash 73; staffed beds 128; reported access 64; reported quality 78; policy attention stable; prior access revision 2. | `retention_spend schedule_relief` |
| 4 | Cash 63; staffed beds 128; reported access 67; reported quality 78; state scrutiny increasing; prior access revision -1. | `coalition_investment shared_access_commitment` |
| 5 | Cash 55; staffed beds 128; reported access 69; reported quality 78; policy attention stable; prior access revision 3; rival outpatient capacity expansion signal. | `defensive_capital access_posture` |

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

| Month | Actor-visible observation summary | Available resources |
| ---: | --- | --- |
| 1 | January; Riverside Community Health; reported access 68; quality 72; workforce trust moderate with elevated nursing vacancies; community trust stable; cash runway WATCH; no in-flight projects; stable-to-rising demand; access reporting scrutiny increasing; recruitment spends cash now and resolves after role-specific delays; Northlake/Summit intel gaps. | AP 3, cash 60, political capital 8 |
| 2 | February; reported access 68; quality 72; workforce trust moderate; cash runway WATCH; Northlake observed prior-month bed investment; Summit private activity unobserved; access reporting scrutiny and recruitment timing notes remain visible. | AP 3, cash 45, political capital 10 |
| 3 | March; reported access 71; quality 72; workforce trust strained; cash runway STRAINED; Northlake prior-month bed investment still visible; Summit private activity unobserved; payer renewal context and access scrutiny remain visible. | AP 3, cash 30, political capital 11 |

## Run Results

### Stabilization

| Seed | Final hash | Cash | Access | Workforce trust | Community trust | Validation failures |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 42 | `5beed26a91f1b739` | 45 | 84 | 64 | 70 | 0 |

The free-form stabilization run spent more than the naive profile but improved
access and community trust. The insurer rejected the high initial rate request,
but later policy, workforce, coalition, and competitor responses produced a
legible access-focused path.

### Competitive Preview

| Seed | Final hash | Cash | Access | Beds | Workforce trust | Community trust | PC | Validation failures |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 42 | `10c3060949fa8aa1` | 30 | 71 | 124 | 57 | 65 | 11 | 0 |

The free-form competitive run was more active than the scripted naive profile:
it monitored a rival, recruited nurses, added beds, made an access pledge, and
used a neutral payer negotiation. It improved access modestly while preserving
more cash than the scripted growth profile, but workforce trust declined during
the recruitment and capacity sequence.

## Causal Explanation

The stabilization outcome was driven by a moderate access strategy: early bed
investment raised capacity but cost cash and did not create enough leverage for
the requested commercial rate. Later access commitments gave state officials a
defensible path, workforce spending stabilized trust, coalition participation
raised access and community trust, and a credible defensive response to rival
capacity pressure added a final access and trust lift.

The competitive outcome was driven by visible capacity and workforce tradeoffs.
Monitoring converted the Northlake intel gap into a prior-month signal, nurse
recruitment and bed investment raised staffed beds and access, and the access
pledge improved reported access. The same path reduced cash and strained
workforce trust, which the debrief correctly frames as a timing and decision
quality issue rather than a hidden scoring result.

## Gameplay Validity Hypotheses

- **A first-time simulated player can complete a month using actor-visible
  information and command hints:** Pass for this bounded profile. Both current
  campaigns completed with zero validation failures.
- **Agents can explain the main cause of an outcome from debrief and history:**
  Partial pass. The transition histories and debriefs supported a concise
  causal explanation for both runs.
- **Multiple strategies can complete the current slice:** Still supported when
  considered alongside v0.1.52 scripted profiles.
- **No single first-month command dominates:** Not tested by this one-profile
  run.
- **Rival behavior is recognizable but imperfectly predictable:** Partial pass.
  Monitoring made Northlake's prior bed investment visible, while Summit private
  activity remained outside the player observation.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 5 | Both campaigns completed without validation failures or retries. |
| Strategic tension | 4 | The run traded cash and workforce trust for access, beds, and legitimacy. |
| Causal transparency | 4 | Histories and debriefs supported post-run explanation without relying on hidden runtime details. |
| Pacing proxy | 4 | The bounded MCP flow completed both sessions without stalls. |
| Action overload proxy | 4 | The profile used legal multi-command batches without exhausting the action space. |
| Debrief coherence | 4 | Debriefs separated decisions, outcomes, and committed-history metrics. |
| Exploit discovery | 2 | One free-form profile is too small for exploit or dominance claims. |

## Evidence Limits

- This is one free-form simulated-agent profile, not a human playtest.
- Seed 42 is a bounded smoke-style validation point, not stochastic
  characterization.
- The profile was operator-run; it tests whether the current MCP surface and
  docs can support one observation-driven run, not whether all agents will make
  useful choices.
- No numeric balance, formula, scenario, actor-behavior, command-surface, MCP
  DTO, or replay-format change should be made from this run alone.

## Prioritized Follow-Up

1. Run at least two additional free-form profiles with different strategic
   priorities before drawing stronger conclusions about command comprehension or
   passive competitive play.
2. If repeated free-form competitive runs underuse commitments or negotiations,
   review monthly report guidance and command help before considering balance
   changes.
3. Keep broader strategy-space diagnostics as analysis artifacts until repeated
   scripted or free-form findings show a concrete tooling need.
