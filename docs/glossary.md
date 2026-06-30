# Glossary

**Status:** Phase 0 governance artifact  
**Audience:** Contributors, domain reviewers, and playtest designers

Core terms for the Health Policy Strategy Game, aligned with
[`system-boundary.md`](system-boundary.md) and [`design_principles.md`](design_principles.md).

## Simulation Core

| Term | Definition |
| --- | --- |
| True state | The full modeled world state used by the transition core. |
| Observation | Actor-specific reported measures derived from true state and resolved inputs. |
| Resolved inputs | Seeded stochastic values computed before `transition()` runs. |
| Transition | One deterministic step: prior state + command + resolved inputs + ruleset → next state. |
| History | Genesis state plus append-only committed transitions. |
| State hash | Stable 64-bit FNV-1a fingerprint over canonical state for replay checks. |
| Replay | Re-execution of committed transitions from genesis to verify hashes and final state. |
| Replay artifact | Versioned text export of seed, play mode, ruleset, and committed history. |

## Actors and Commands

| Term | Definition |
| --- | --- |
| Player command | CEO action validated against the ruleset before transition. |
| Action points (AP) | Monthly management-attention budget limiting competitive campaign commands. |
| Political capital | Advocacy and negotiation resource consumed by some competitive verbs. |
| Simultaneous resolution | Aggregating all player monthly batches before transition (ADR-0003). |
| AI player | Computer-controlled health-system peer using the same command catalog as the human. |
| AI-agent playtester | External AI or sub-agent client that plays a campaign through MCP to generate validation evidence; distinct from an in-game AI player. |
| Human player | Person playing the CEO role through the CLI; not required for the active Phase 7 playtest path. |
| NPC actor | Institution (insurer, state, labor, coalition) that responds to market state; not a peer player. |
| Actor decision | Non-player strategic outcome with inspectable rationale text. |
| Attributed effect | Labeled delta linking a source, metric, and value change. |
| Actor card | Design artifact defining authority, objectives, and decision procedure before runtime implementation. |

## Educational

| Term | Definition |
| --- | --- |
| Debrief | End-of-run causal explanation from committed history, not omniscient state. |
| Decision quality | Whether a choice was reasonable given observations at decision time. |
| Outcome quality | Realized state after actor responses and stochastic inputs. |
| Agent-playtest evidence | Simulated-player observations, commands, histories, and debriefs used to inspect gameplay and explanation quality; not measured human learning evidence. |

## Scope

| Term | Definition |
| --- | --- |
| Vertical slice | Bounded end-to-end demo proving architecture and gameplay thesis. |
| Ruleset | Versioned validation bounds and transition parameters for a demo or scenario. |
| Scenario | Packaged initial conditions, actor set, and learning objectives; format draft only. |
| Campaign | Playable run configuration (`stabilization-v1` or `competitive-regional-v1`). |
| Abstraction | Prototype mechanism labeled as design simplification, not calibrated fact. |

## Related Documents

- [`system-boundary.md`](system-boundary.md)
- [`actor-cards.md`](actor-cards.md)
- [`competitive-scenario-brief.md`](competitive-scenario-brief.md)
- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md)
- [`versioning-policy.md`](versioning-policy.md)
