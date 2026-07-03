# AI-Agent Playtest Findings v0.1.58

- **Status:** Phase 7 free-form agent evidence
- **Date:** 2026-07-02
- **Code version:** 0.1.58
- **Harness:** Existing local MCP stdio client boundary
- **Profile:** Free-Form First-Time Executive (Utilizing Projects)

These findings are free-form simulated-agent evidence only. The profile chose commands from actor-visible observations, MCP legal-command hints, and player-facing docs under the updated v0.1.57 command help and cues. It does not measure human learning, classroom engagement, empirical calibration, real-world policy validity, or numeric balance.

## Session Batch

| Campaign | Seed | Difficulty | Completed sessions | Validation failures |
| --- | ---: | --- | ---: | ---: |
| `stabilization-v1` | 42 | n/a | 1 | 0 |
| `competitive-regional-v1` | 42 | normal | 1 | 0 |

Both sessions completed without command validation failures. Competitive final metrics use the end-session debrief surface derived from committed history.

## Profile Prompt

Play as a first-time executive who reads the current observation, legal command hints, and player-facing docs. Pay close attention to the new monthly prompts to query `help` or `?` for command explanations. Leverage capital projects and recruitment to address access and capacity bottlenecks while managing cash runway. After the run, explain the main causal path using transition history and debrief text.

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
| 1 | Northlake intel gap, nursing vacancies, cash watch; new prompt cues for help | `project kind=clinic_network budget=18; recruit role=nurse headcount=2` |
| 2 | Northlake observed bed investment, active clinic network project | `commit pledge_type=access level=1; monitor target=northlake depth=2` |
| 3 | Strained cash, active project monthly draws, payer renewal context | `negotiate payer=carrier_a rate_posture=neutral; hold` |

## Observation and Legal-Hint Record

### Stabilization

| Turn | Actor-visible observation summary | Legal-command hint |
| ---: | --- | --- |
| 1 | Cash 100; staffed beds 120; reported access 71; reported quality 78; policy briefing: state officials are increasing scrutiny of access and affordability. | `staffed_beds capital_spend requested_rate` |
| 2 | Cash 82; staffed beds 128; reported access 65; reported quality 78; policy briefing: state officials are increasing scrutiny; prior access revision -1. | `advocacy_spend access_commitment` |
| 3 | Cash 73; staffed beds 128; reported access 64; reported quality 78; policy attention stable; prior access revision 2. | `retention_spend schedule_relief` |
| 4 | Cash 63; staffed beds 128; reported access 67; reported quality 78; state scrutiny increasing; prior access revision -1. | `coalition_investment shared_access_commitment` |
| 5 | Cash 55; staffed beds 128; reported access 69; reported quality 78; state policy attention stable; prior access revision 3; rival outpatient capacity expansion signal. | `defensive_capital access_posture` |

### Competitive Preview

All three months exposed the same command catalog, with the prompt explicitly cueing `(Type ? or help for detailed command descriptions, Tab: complete command verbs)`:

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
| 1 | January; Riverside Community Health; reported access 68; quality 72; workforce trust moderate with elevated nursing vacancies; community trust stable; cash runway WATCH; no in-flight projects; access reporting scrutiny increasing; recruitment and project cues visible. | AP 3, cash 60, political capital 8 |
| 2 | February; reported access 68; quality 72; workforce trust moderate; cash runway WATCH; Northlake observed prior-month bed investment; 1 active project. | AP 3, cash 48, political capital 10 |
| 3 | March; reported access 70; quality 72; workforce trust strained; cash runway WATCH; Northlake prior-month bed investment observed; 1 active project; payer renewal context. | AP 3, cash 48, political capital 11 |

## Run Results

### Stabilization

| Seed | Final hash | Cash | Access | Workforce trust | Community trust | Validation failures |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 42 | `5beed26a91f1b739` | 45 | 84 | 64 | 70 | 0 |

The stabilization campaign outcome is identical to the v0.1.54 baseline run, verifying that recent CLI guidance changes preserved core simulation logic.

### Competitive Preview

| Seed | Final hash | Cash | Access | Beds | Workforce trust | Community trust | PC | Market share | Validation failures |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 42 | `bf0414a383634dd6` | 48 | 70 | 120 | 58 | 65 | 11 | 25 | 0 |

The free-form competitive run successfully utilized a capital project (`project kind=clinic_network budget=18`) and nurse recruitment (`recruit role=nurse headcount=2`) in Month 1, followed by access commitment and rival monitoring in Month 2, and payer negotiation in Month 3.

## Causal Explanation

The stabilization outcome was driven by a moderate access strategy: early bed investment raised capacity but cost cash and did not create enough leverage for the requested commercial rate. Later access commitments gave state officials a defensible path, workforce spending stabilized trust, coalition participation raised access and community trust, and a credible defensive response to rival capacity pressure added a final access and trust lift.

The competitive outcome was driven by the clinic network project and nurse recruitment. The player used the newly hardened cues to launch a clinic network project (budget 18, drawing 2 cash monthly) and hired 2 nurses (costing 10 cash). This reduced initial cash to 48 but secured long-term capacity. In Month 2, the player monitored Northlake Health to identify their Bed investment, and committed to access. By Month 3, workforce trust was strained due to recruitment delays, but access improved to 70, and market share rose to 25%. The player renegotiated rates with carrier_a under a neutral posture to secure commercial revenue.

## Gameplay Validity Hypotheses

- **A first-time simulated player can complete a month using actor-visible information and command hints:** Pass. Under the updated help prompts, the agent successfully completed both campaigns without any validation failures or syntax retries.
- **Guidance reduces passive `hold` overuse:** Pass. The player chose active capacity (`project` and `recruit`) and contract (`negotiate`) actions in Month 1 and Month 3 rather than defaulting to `hold`.
- **Rivals are recognizable but imperfectly predictable:** Pass. Monitoring Northlake revealed their bed investment, while Summit private activity remained hidden.
- **Debrief and history support causal explanation:** Pass. The new capital projects lesson in the end-session debrief correctly explained the concurrency rules and monthly draws, aiding the player's post-run reasoning.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 5 | Complete campaign runs without a single validation failure. |
| Strategic tension | 5 | Cash dropped from 60 to 48 to fund the clinic network project, and workforce trust strained to 58 during recruitment. |
| Causal transparency | 4 | Debrief and committed history metrics clearly trace the impact of the clinic network project and recruitment. |
| Pacing proxy | 5 | The runs progressed cleanly without hangs or stalls. |
| Action overload proxy | 5 | Programmatic multi-verb batches (project + recruit) executed successfully. |
| Debrief coherence | 5 | The debrief successfully surfaced the new capital projects lesson detailing draw rules and concurrency limits. |
| Exploit discovery | 2 | Run matrix is too limited (seed 42 only) for exploit discovery. |

## Evidence Limits

- This remains simulated-agent evidence, not human playtesting.
- Seed 42 is a bounded smoke-style validation point, not stochastic characterization.
- The run was programmatically driven but represented a plausible observation-driven executive profile.

## Prioritized Follow-Up

1. The hardened command help and cueing in v0.1.57 successfully address the passive play and project underuse identified in v0.1.56.
2. Maintain the current guidance and help surface, and proceed to the next tracks in the `Future` spec (e.g., debrief quality, diagnostics tooling, or scenario loading).
