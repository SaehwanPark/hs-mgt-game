# Evidence Map — Simulation Breadth and Strategic Actors Queue Closure v0.12.12

| Requirement | Authority | Result | Limit |
| --- | --- | --- | --- |
| Service-line and capacity breadth | `src/model/competitive_command.rs`, `src/model/competitive_world.rs`, `src/sim/observe_competitive.rs` | Emergency, ICU, obstetrics, psychiatric, cardiology, oncology, infusion, neurology, ASC, staffed-bed, and outpatient capacity are typed and observed | These are bounded game capacities, not clinical service data |
| Operating and distributional proxies | `HealthSystemState`, `PlayerObservation`, competitive debrief | Demand, treated volume, unmet demand, access, community trust, market share, quality, and operating margin are connected to player tradeoffs | No individual patients or validated distributional-equity outcome is modeled |
| Capital tradeoffs | `CompetitiveCommand::Project`, `PendingEffectKind`, competitive debrief lessons | Cash, Action Points, project duration, capacity, quality, and access tradeoffs are debriefable | No portfolio optimizer or calibrated capital model |
| Market and strategic interaction | `observe_competitive.rs`, `actors/ai_player.rs`, committed v0.11.11 evidence | Rival styles, public lag, monitoring, private actions, and response rationales are visible at the permitted boundary | No equilibrium or general actor framework is claimed |
| Public-payer interaction | `PayerId`, payer validation/resolution, SPEC Past entries | Medicare and Medicaid negotiation commands and bounded compliance effects exist | Public payers are not promoted as strategic actor models or social-welfare estimators |
| Repeated-play strategy evidence | v0.11.11 all-tier artifact and findings | 60/60 runs complete; 1,440 transitions; 10 distinct command trajectories; no common first-month action; varied tradeoffs | Descriptive simulated-policy evidence, not human strategy or causal balance evidence |
| Traceability and debrief continuity | v0.11.12 capture and v0.12.3 review | Current-code runs remain complete and the cross-campaign review reports zero structural gaps | No comprehension, classroom, or learning-effect claim |

## Conclusion

The current compact campaign already supports several bounded strategic
tradeoffs. The evidence does not identify a concrete unexplained breadth or
strategic-actor gap that authorizes new runtime behavior. Close the Future item
as an evidence-gated queue decision, preserve the deferred scope, and reopen
only after a new concrete finding.
