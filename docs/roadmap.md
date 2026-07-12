# Health Policy Strategy Game
## Phase-Based Development Roadmap

**Status:** Canonical companion to the initial game development proposal  
**Audience:** Project owner and contributors  
**Planning horizon:** From concept validation through an initial educational release  
**Approach:** Research-informed, design-led, vertical-slice development

---

## 1. Roadmap Purpose

This roadmap defines the sequence of work needed to turn the project proposal into a credible first release. It is intentionally phase-based rather than date-based. Progression should depend on evidence and exit criteria, not elapsed time.

The roadmap follows several principles:

- research before formalization;
- narrow vertical slices before broad frameworks;
- deterministic and testable core mechanics;
- explicit separation of true state, observed state, and stochastic inputs;
- strategic non-player actors introduced incrementally;
- educational usefulness evaluated alongside gameplay;
- and documented assumptions before numerical sophistication.

Detailed subsystem specifications will be created separately as each phase begins.

---

## 2. Phase Overview

| Phase | Primary Objective | Main Output |
|---|---|---|
| 0 | Establish project foundations | Governance, repository, decision process |
| 1 | Build the research foundation | Literature map and design implications |
| 2 | Define the conceptual model | Scope, ontology, and causal framework |
| 3 | Design the game and educational experience | Core loop, scenario concept, assessment model |
| 4 | Prove the technical architecture | Deterministic engine prototype |
| 5 | Build the first vertical slice | Small end-to-end playable simulation |
| 6 | Expand into an MVP | Complete first campaign and contributor-ready tooling |
| 7 | Validate and calibrate | Technical, domain, gameplay, and educational evidence |
| 8 | Prepare the initial release | Documented, teachable, reproducible release |
| 9 | Extend after release | Broader US policy and comparative-system capabilities |

---

# Phase 0: Project Foundations

## Objective

Create the minimum organizational and technical foundation needed for disciplined collaboration.

## 0.1 Canonical Project Setup

- Establish the proposal and this roadmap as initial canonical documents.
- Create the source repository and contribution workflow.
- Define issue, proposal, and decision-record conventions.
- Adopt a lightweight versioning strategy for code, rulesets, scenarios, and data.
- Define licenses for code, content, and external data.
- Record terminology in an initial glossary.

## 0.2 Engineering Baseline

- Create a Rust workspace with placeholder crates or modules.
- Configure formatting, linting, testing, and continuous integration.
- Establish rules for deterministic tests and seeded stochastic processes.
- Add architecture decision records for consequential technical choices.
- Define minimum documentation expectations for public types and mechanisms.

## Deliverables

- Repository and contributor guide
- Initial glossary
- Architecture decision record template
- Automated quality checks
- Versioning and licensing policy

## Exit Criteria

- A new contributor can understand the project purpose, build the repository, run tests, and propose a change.
- Canonical documents and technical decisions have clear ownership and revision procedures.

---

# Phase 1: Literature and Precedent Research

## Objective

Develop a defensible intellectual foundation and identify lessons from prior simulations, games, and social-science models.

Research should produce actionable design implications rather than an exhaustive bibliography.

## 1.1 Prior Games and Simulations

Study relevant precedents across:

- health-policy simulations;
- healthcare management games;
- business and market simulations;
- political strategy games;
- negotiation and role-playing exercises;
- grand-strategy and faction-based games;
- agent-based social simulations;
- and serious games used in graduate education.

For each precedent, document:

- player role and agency;
- world and actor model;
- treatment of uncertainty;
- non-player decision logic;
- transparency of assumptions;
- educational method;
- strengths, limitations, and transferable ideas.

## 1.2 Health Policy and Institutional Research

Review literature necessary to define the initial US setting:

- health-system finance and strategy;
- Medicare and Medicaid institutional structure;
- commercial payer-provider contracting;
- hospital market power and consolidation;
- nonprofit and safety-net obligations;
- healthcare labor markets;
- quality measurement and reporting;
- state and federal regulatory authority;
- and health-policy implementation.

The goal is to identify stable mechanisms and institutional constraints, not reproduce every current regulation.

## 1.3 Theoretical Foundations

Review candidate modeling approaches from:

- microeconomics;
- industrial organization;
- cooperative and non-cooperative game theory;
- bargaining theory;
- political economy;
- public choice;
- public administration;
- organizational behavior;
- behavioral economics;
- social psychology;
- system dynamics;
- agent-based modeling;
- and decision-making under uncertainty.

For each approach, determine whether it should inform:

- world-state transitions;
- actor preferences;
- actor decision procedures;
- observation and belief models;
- policy formation;
- or educational explanation.

## 1.4 Educational Design Research

Study:

- simulation-based learning;
- graduate management education;
- experiential learning;
- structured debriefing;
- decision-quality assessment;
- team-based role simulation;
- and evaluation of serious games.

Clarify how the game should distinguish:

- knowledge acquisition;
- strategic reasoning;
- decision quality;
- outcome quality;
- and reflective learning.

## Deliverables

- Annotated literature map
- Precedent comparison matrix
- Research-to-design implications memo
- Initial bibliography and evidence registry
- List of unresolved empirical and normative questions

## Exit Criteria

- The team can explain which prior approaches are being adopted, modified, or rejected.
- Every major proposed mechanism has at least a conceptual grounding or is clearly identified as a game abstraction.
- Important disagreements in the literature are documented rather than silently resolved.

---

# Phase 2: Conceptual and Domain Design

## Objective

Define what the first version represents before committing to detailed mechanics or data structures.

## 2.1 Scope and System Boundary

Specify:

- geographic and institutional setting;
- player role and authority;
- campaign duration and turn length;
- included and excluded actor classes;
- included policy domains;
- modeled population segments;
- and the boundary between endogenous and exogenous processes.

The initial scope should remain a fictional regional US market centered on a nonprofit health system.

## 2.2 Domain Ontology

Define the initial vocabulary and relationships for:

- actors;
- institutions;
- markets;
- policies and policy instruments;
- authority and jurisdiction;
- resources and constraints;
- preferences and utility;
- beliefs and observations;
- commands, events, and effects;
- true state and reported state;
- coalitions and agreements;
- and outcomes and welfare measures.

The ontology should remain implementation-neutral during this sub-phase.

## 2.3 Causal Framework

Create a high-level causal map linking:

- policy;
- financing;
- capacity;
- workforce;
- utilization;
- quality;
- access;
- population outcomes;
- organizational behavior;
- political response;
- and macroeconomic conditions.

Each link should identify:

- direction of influence;
- delay;
- uncertainty;
- likely heterogeneity;
- and whether it is a modeled mechanism or an external input.

## 2.4 Actor Framework

For each initial actor class, specify:

- objectives;
- legal and institutional authority;
- resources;
- constraints;
- available information;
- private information;
- time horizon;
- risk posture;
- outside options;
- and plausible decision procedures.

Separate actor utility from social-welfare evaluation.

## 2.5 Policy Lifecycle Framework

Define a general lifecycle covering:

- problem recognition;
- agenda formation;
- coalition building;
- design;
- enactment or rulemaking;
- implementation;
- enforcement;
- strategic adaptation;
- observed outcomes;
- and political feedback.

The first version may model only a subset, but the conceptual framework should avoid treating policy as an instantaneous external modifier.

## Deliverables

- Initial system-boundary specification
- Domain glossary and ontology
- High-level causal map
- Actor cards
- Policy lifecycle model
- Assumption and abstraction register

## Exit Criteria

- Contributors can describe the same simulated world using a shared vocabulary.
- The initial scope is small enough for a vertical slice.
- Important causal pathways and exclusions are explicit.
- No detailed implementation is required to resolve basic conceptual ambiguity.

---

# Phase 3: Game and Educational Design

## Objective

Translate the conceptual model into a coherent player experience and instructional structure.

## 3.1 Core Game Loop

Define the high-level turn cycle, including:

1. world and policy environment update;
2. actor-specific observation generation;
3. player review and decision-making;
4. non-player strategic choice;
5. interaction resolution;
6. deterministic state transition;
7. reporting and explanation;
8. board, stakeholder, and educational feedback.

Determine the limited resources that create strategy, such as:

- capital;
- management attention;
- political capital;
- trust;
- time;
- and implementation capacity.

## 3.2 Player Decisions and Feedback

Define a small initial action vocabulary covering:

- operations and capacity;
- workforce;
- payer strategy;
- capital allocation;
- public and government relations;
- partnerships;
- and policy response.

Specify how the game communicates:

- current conditions;
- uncertainty;
- forecasts;
- tradeoffs;
- delayed consequences;
- and reasons for outcomes.

## 3.3 Strategic Interaction Design

Select a small initial set of game forms, likely:

- bilateral payer-provider bargaining;
- one cooperative or political coalition problem;
- and one competitive capacity or market-entry interaction.

For each, define at a high level:

- participants;
- feasible strategies;
- information structure;
- payoff categories;
- outside options;
- repeated-game effects;
- and the intended decision procedure.

Avoid solving a single global game containing all actors.

## 3.4 Scenario and Campaign Design

Design the first campaign around a focused executive challenge, such as organizational stabilization under policy and market pressure.

Specify:

- initial conditions;
- major tensions;
- learning objectives;
- scenario duration;
- possible strategic approaches;
- event cadence;
- and end-of-run evaluation.

The scenario should allow multiple defensible strategies rather than a hidden optimal path.

## 3.5 Educational and Debrief Design

Define:

- target learner;
- learning objectives;
- expected prerequisite knowledge;
- instructor-facing information;
- decision and outcome reports;
- counterfactual exercises;
- and post-game discussion prompts.

The design should explicitly distinguish a good decision made under uncertainty from a favorable realized outcome.

## Deliverables

- Core loop specification — see [`core-loop-spec.md`](core-loop-spec.md)
- Initial action catalog
- Strategic interaction briefs
- First campaign brief
- CLI interaction mockups
- Educational objectives and debrief outline

## Exit Criteria

- The proposed loop can be played manually as a paper or spreadsheet prototype.
- Each player action has a clear purpose and expected feedback.
- The first campaign tests the project thesis rather than merely demonstrating accounting.
- Educational objectives map to observable decisions or debrief evidence.

---

# Phase 4: Technical Architecture Proof

## Objective

Prove that the proposed architecture can support determinism, immutable history, stochastic observations, and strategic actors before building substantial content.

## 4.1 Deterministic Transition Kernel

Implement a minimal pure transition pipeline:

```text
prior state + validated commands + resolved inputs + ruleset
  -> next state + events + attributed effects
```

Demonstrate:

- no hidden randomness;
- no dependence on wall-clock or external mutable state;
- stable serialization;
- and reproducible state hashes.

## 4.2 Snapshot and History Model

Implement:

- immutable true-state snapshots;
- actor-specific observation snapshots;
- append-only committed transitions;
- replay from genesis;
- and periodic checkpoint support if needed.

Ensure later measurement revisions do not rewrite prior observations.

## 4.3 Stochastic Input Boundary

Implement external generation of:

- exogenous events;
- measurement noise;
- behavioral realizations;
- and deterministic tie-breaking inputs.

Use named or derived random streams so one subsystem's changes do not unnecessarily alter all others.

## 4.4 Minimal Strategic Actor Framework

Implement one localized game instance with:

- feasible-action generation;
- actor preferences;
- incomplete observations or beliefs;
- deterministic evaluation;
- and an explicit decision result with rationale.

The first implementation should favor clarity over theoretical completeness.

## 4.5 Analysis and Testing Harness

Add:

- state and event inspection;
- replay verification;
- invariant tests;
- property-based tests;
- golden trajectories;
- and export of run history for external analysis.

## Deliverables

- Architecture prototype
- Minimal executable simulation
- Replay and state-hash demonstration
- Strategic actor proof of concept
- Test and analysis harness
- Architecture review memo

## Exit Criteria

- Identical state, commands, resolved inputs, and ruleset always produce identical results.
- True and observed state are represented separately.
- A complete run can be replayed and verified.
- At least one non-player action is selected through an inspectable strategic procedure.
- No critical architectural assumption remains untested.

---

# Phase 5: First Vertical Slice

## Objective

Build the smallest end-to-end game that demonstrates the distinctive value of the project.

## 5.1 World Slice

Include only the minimum viable set:

- one player-controlled health system;
- one competitor;
- one commercial insurer;
- Medicare;
- Medicaid;
- a small labor market;
- a few patient cohorts;
- selected financial, capacity, access, quality, and trust measures;
- and one state-policy process.

## 5.2 Interaction Slice

Include:

- one payer negotiation;
- one workforce or capacity pressure;
- one policy proposal with stakeholder response;
- one cooperative or coalition opportunity;
- and delayed consequences across several turns.

## 5.3 Observation Slice

Demonstrate:

- true versus reported measures;
- actor-specific information;
- measurement delay or uncertainty;
- and later revisions.

## 5.4 Playable CLI Slice

Provide:

- a concise executive dashboard;
- event and policy briefings;
- command selection;
- forecasts and uncertainty;
- turn-resolution summaries;
- and an end-of-run causal explanation.

## 5.5 Internal Playtesting

Test for:

- comprehensibility;
- strategic tension;
- causal transparency;
- pacing;
- action overload;
- and obvious exploits.

## Deliverables

- Playable vertical slice
- One short scenario
- Deterministic replay file
- End-of-run analysis report
- Internal playtest findings
- Revised scope and risk register

## Exit Criteria

- A player can complete the slice without developer intervention.
- The slice produces at least one meaningful conflict among finance, access, workforce, and policy.
- Non-player behavior is understandable without being entirely predictable.
- Players can explain why major outcomes occurred.
- The experience is recognizably a strategy game rather than a static model demonstration.

---

# Phase 6: Minimum Viable Product

## Objective

Expand the validated slice into a coherent first campaign suitable for
AI-agent validation and early educational review.

Future Phase 6 work should prioritize the first release as an educational
strategy simulation first, engaging gameplay second, reusable modeling platform
third, and research-grade policy model fourth. Broader abstractions should wait
for playtest, scenario-authoring, debrief, or domain-review evidence that the
current compact structures are blocking validated gameplay or learning.

## 6.0 Competitive Campaign Design Track

**Status:** Design artifacts delivered at v0.1.28; I1-I8 runtime delivered
through v0.1.37; 24-month campaign loop and hardening slices implemented.

Parallel to the stabilization demo (`stabilization-v1`), the competitive
regional market campaign (`competitive-regional-v1`) adds:

- monthly turn calendar with annual policy tick;
- 1 human + K AI health-system players on a shared market model;
- simultaneous monthly action resolution (ADR-0003);
- action-point, cash, and political capital economy (ADR-0005);
- executive one-page report with four deterministic consultant recommendations
  generated from the actor-visible observation and retained for debrief;
- reproducible MCP validation captures for consultant-option visibility and
  debrief traceability across policies, seeds, and Normal/Hard fixtures;
- partial observability of rival public actions;
- bounded game-theory AI with inspectable rationales;
- random monthly events and delayed effect queues;
- Stata-like command CLI for human entry (ADR-0006);
- difficulty profiles scaling K and CPU budgets (Capitalism-style).

**Deliverables (design):**

- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md)
- [`core-loop-spec.md`](core-loop-spec.md)
- [`competitive-scenario-brief.md`](competitive-scenario-brief.md)
- [`executive-report-format.md`](executive-report-format.md)
- [`action-catalog-draft.md`](action-catalog-draft.md)
- [`cli-command-grammar-draft.md`](cli-command-grammar-draft.md)
- ADRs 0003–0006

**Runtime slices delivered:** campaign router (I1), monthly executive report
(I2), action economy (I3), multi-system state (I4), simultaneous resolver (I5),
AI players (I6), events/delays/annual tick (I7), and Stata CLI (I8). The full
24-month competitive campaign length, prompt help, verb autocomplete, competitive
autosave/resume, competitive replay export, and competitive scenario loading are
implemented.

**Note:** Phase 9 role-based classroom multiplayer assigns human participants to
organizational roles (CEO, CFO, etc.). That is distinct from K AI health-system
competitors in this track.

## 6.1 Simulation Breadth

Add enough depth to support a complete campaign:

- several payer and provider actors;
- a richer workforce model;
- multiple service lines;
- capital allocation;
- selected quality and access mechanisms;
- state and federal policy pressures;
- macroeconomic inputs;
- and several strategic interaction types.

Expansion should follow demonstrated gameplay needs, not a desire for completeness.
Do not add a mechanism solely because the ontology can represent it; require a
scenario, playtest, or debrief need.

## 6.2 Scenario System

Create a versioned, validated scenario format for:

- initial state;
- actor definitions;
- ruleset selection;
- parameterization;
- event schedules;
- learning objectives;
- and scoring or evaluation profiles.

Support composition of known mechanisms without permitting arbitrary executable logic.
Before broadening runtime tooling, develop one exemplary scenario that
demonstrates financial pressure, a workforce conflict, a payer interaction, a
competitive response, a policy or regulatory process, delayed consequences, and
at least two defensible strategic directions.

## 6.3 Strategic Actor Expansion

Add bounded, interpretable decision models as required, such as:

- bargaining;
- approximate best response;
- coalition search;
- satisficing;
- level-k reasoning;
- and repeated-game reputation effects.

Every decision model should expose a rationale suitable for debugging and teaching.
Prefer explicit institutional heuristics, constrained optimization, aspiration
levels, organizational routines, and actor-specific attention limits over
increasingly formal global optimization.

## 6.4 Educational and Instructor Features

Implement:

- seeded comparable scenarios;
- run export;
- decision logs;
- instructor-visible true state;
- counterfactual replay;
- and configurable debrief reports.

## 6.5 Contributor Tooling

Provide:

- schema documentation;
- scenario validation;
- debugging reports;
- model assumption documentation;
- and test fixtures for new mechanisms.

## Deliverables

- Complete MVP campaign
- Scenario authoring format
- Multiple strategic interactions
- Instructor and analysis outputs
- Contributor documentation
- Candidate balancing parameters

## Exit Criteria

- The campaign supports multiple viable strategies.
- A full run is reproducible and explainable.
- Contributors can add or modify scenario content without changing core engine code.
- The game can support structured AI-agent playtesting through reproducible
  observations, commands, histories, and debrief outputs.
- No major feature depends on hidden or undocumented model behavior.

---

# Phase 7: Validation, Calibration, and Evaluation

## Objective

Evaluate whether the game is technically correct, behaviorally credible,
strategically engaging, and educationally inspectable through reproducible
AI-agent playtests.

Phase 7 should answer whether repeated play produces difficult, legible, and
interesting decisions before the project expands its architecture or actor
ontology.

## 7.1 Technical Validation

Verify:

- accounting and population-flow invariants;
- deterministic replay;
- serialization compatibility;
- state migration;
- random-stream isolation;
- numerical stability;
- and performance for expected campaign sizes.

## 7.2 Domain Review

Engage health-policy, health-system, payer, labor, and public-sector experts to review:

- institutional plausibility;
- actor authority;
- causal mechanisms;
- strategic options;
- outcome explanations;
- and major omissions.

The goal is credible abstraction, not perfect predictive accuracy.

## 7.3 Behavioral and Strategic Validation

Test whether non-player actors:

- respond coherently to incentives;
- respect institutional constraints;
- use information available to them;
- change behavior when beliefs or outside options change;
- and avoid obvious dominated or nonsensical actions.

Use controlled test scenarios rather than relying only on full-game observation.

## 7.4 Calibration and Sensitivity Analysis

For important parameters:

- identify plausible ranges;
- document evidence and uncertainty;
- test local and global sensitivity;
- identify phase changes and unstable regions;
- and avoid tuning solely for preferred outcomes.

Separate empirical calibration from gameplay balancing.

## 7.5 AI-Agent Gameplay Evaluation

Conduct structured AI-agent and sub-agent playtests with:

- scripted strategy policies;
- LLM or sub-agent personas;
- naive first-time simulated players;
- adversarial exploit-seeking agents;
- and domain-informed reviewer agents.

Assess:

- command comprehension;
- pacing and action-overload proxies;
- strategic diversity;
- exploitability;
- and quality of explanations.

Default findings should test whether at least three strategies can succeed, no
single first-month command dominates, outcomes are explainable from the debrief,
rivals are recognizable but not perfectly predictable, and a month can be
completed without implementation documentation. When enough runs exist, include
action frequencies, outcome distributions, strategy clusters, stochastic
sensitivity, and dominance or near-dominance findings.

Agent playtests replace planned external human recruitment for this roadmap.
This is a budget and recruitment constraint as well as a reproducibility choice:
Phase 7 reserves no funding for participant recruitment, incentives, or study
administration. Any later human educational evaluation requires a separate
funded and approved plan and must remain distinct from AI gameplay validation.

The next AI validation cycle should emphasize gameplay maturity over content
count. Run access-first, commercially focused, workforce-resilience,
capital-modernization, and coalition-oriented policy hypotheses across named
seeds and rival configurations. Report strategy divergence, treated and unmet
demand, operating margins, bottlenecks, ignored or dominated commands,
threshold-cliff frequency, causal explanation quality, and whether the agent
selects a materially different approach on replay. These are simulated-player
diagnostics, not human enjoyment or learning measures.
They should capture campaign, seed, difficulty, agent profile or prompt,
actor-visible observations, submitted commands, validation failures, histories,
and debriefs.

The v0.11.1 validation artifact completes this matrix across 60 runs and 1,440
committed months. Its bottleneck, loss, trajectory, and threshold findings are
descriptive routing evidence only; runtime promotion remains deferred pending a
concrete unexplained player-facing, instructor-facing, or domain-review gap.
The v0.11.2 read-only audit confirms complete decision and transition linkage but
no month-specific operating-outcome debrief linkage; this remains a debrief
review candidate, not a runtime tuning basis. The v0.11.3 debrief follow-up
closes that reporting-surface gap using committed player outcomes without
changing transition semantics or promoting balance, causal, or learning claims.
The v0.11.4 post-fix matrix re-runs the same 60-run baseline and confirms
1,440/1,440 monthly result lines and 469/469 categorized outcome links; this is
structural traceability evidence and does not promote runtime expansion. The
v0.11.5 operating-outcome use audit confirms 1,380 prior-month observation
matches, 1,440 exact debrief outcome matches, 441 non-terminal
signal-to-next-command opportunities, and 28 expected terminal signals; these
remain descriptive traceability evidence rather than causal or learning
evidence.
The v0.11.6 strategy-comparison use audit groups the same frozen capture by
profile, seed, and difficulty, confirms complete traceability across all 60
runs, and identifies no structural strategy-comparison or debrief-use gap;
runtime promotion remains deferred.
The v0.11.11 post-change all-tier validation reruns the five-profile matrix on
current code after the difficulty risk-posture and rival-resource changes,
confirming 60/60 complete runs, 1,440 committed months, varied trajectories,
and no candidate common or near-dominant first-month action. These remain
descriptive routing evidence; runtime promotion remains deferred.
The v0.11.12 current-code teachability capture reruns three observation-driven
profiles across seeds 42–44 at Hard difficulty, confirming 9/9 complete runs,
216 committed months, complete trace/debrief coverage, and no structural gap.
These remain descriptive pacing and traceability evidence; runtime promotion
remains deferred.

The v0.11.13 regional affiliation design gate promoted an affiliation-first
conceptual slice for one fictional nonprofit partner. The v0.11.14 proposal was
implemented in v0.12.0 as an opt-in six-stage `regional-affiliation-v1` scenario
with minimum state and observation boundaries, explicit resolved inputs,
scenario loading, replay verification, CLI/MCP commands, and debrief output.
The v0.12.1 Phase 7 capture covers independent, deferred, and pursuit policies
across seeds 42–44 with complete six-stage trace/debrief linkage. It identifies
one bounded MCP observation-context gap—the typed alternatives, assumptions,
and commitments are not rendered at decision time—while keeping transition,
ruleset, balance, legal, and educational-effect changes deferred.
The v0.12.2 follow-up renders those existing typed fields at the MCP boundary
and reruns the same 9-run matrix with 54/54 observations carrying the context;
no transition, ruleset, balance, or learning claim is promoted.
The v0.12.3 Phase 7 review audits that post-fix affiliation artifact against the
approved competitive teachability capture: 18 complete runs and 270 committed
transitions retain decision-context, action/response, transition/hash, outcome,
debrief, and source-specific context coverage with no structural gap. Runtime
promotion remains deferred.
Broader deal-market mechanics and legal forecasting remain deferred.

The v0.12.4 Phase 7/9 difficulty-depth review reads the existing v0.11.11
all-tier and v0.11.9 Expert artifacts. It validates 75 complete runs and 1,800
committed transitions, and identifies a candidate workforce-capacity pressure
signal rising from 0 Easy operating months to 160 Expert operating months.
Normal, Hard, and Expert scripted action counts remain identical in the source
matrix, so the result is descriptive routing evidence rather than a causal
difficulty, balance, or winnability claim.

The v0.12.5 workforce-capacity design gate confirms that the candidate signal
has a bounded MCP observation-context gap: typed Riverside staffing and
physical-capacity fields exist but are omitted from the decision-time formatter.
It routes an observation-only projection follow-up with focused boundary tests
and unchanged history/hash evidence; difficulty and balance tuning remain
deferred.

The v0.12.8 teachability queue closure confirms the existing cross-campaign
evidence chain across 18 complete runs and 270 transitions with no structural
gap. The teachability track is closed until a new concrete comprehension,
pacing, traceability, strategy-comparison, or debrief-use finding appears.

The v0.12.9 difficulty-depth closure confirms that the candidate
workforce-capacity signal is visible and the tested Expert paths are clearable,
but identifies no unexplained gap that would justify tuning. Difficulty and
balance remain evidence-gated.

The v0.12.10 affiliation queue closure confirms that the existing
`regional-affiliation-v1` runtime already satisfies its bounded proposal. No
broader acquisition or consolidation work is authorized without new concrete
evidence.

The v0.12.6 follow-up renders the safe staffing and physical-capacity fields
from `PlayerObservation` and validates 75 complete runs with 1,800 transitions.
All source histories and state-hash sequences match exactly, closing the
bounded interface gap without promoting a difficulty, balance, winnability, or
human-learning claim.

The v0.12.7 affiliation runtime-boundary proposal confirms that the existing
opt-in `regional-affiliation-v1` implementation already satisfies the minimum
state, observation, resolved-input, deterministic-transition, history/replay,
and debrief contracts. No additional affiliation runtime is authorized without
a new concrete evidence gap; broader acquisition and consolidation remain
deferred.

## 7.6 Educational Artifact and Debrief Review

Evaluate whether the game artifacts make the intended reasoning inspectable:

- recognizing stakeholder incentives;
- identifying second-order effects;
- reasoning under uncertainty;
- distinguishing observed from true conditions;
- and explaining policy implementation and strategic response.

Use agent decision traces, rationale reviews, debrief quality, and scenario
counterfactuals rather than relying only on final scores. Do not present
AI-agent playtests as measured human learning, classroom effectiveness, or
formal learner assessment.
Treat the debrief as a primary product surface: it should explain what happened,
why it happened, what the player knew at the time, which assumptions mattered,
what alternatives were available, and whether a bad outcome reflected poor
decision quality or unfavorable realization.

## 7.7 Expansion Proposal Review Gate

Before broadening the game beyond the current competitive campaign, review
candidate expansions as proposals rather than immediate implementation tracks.
This gate exists to keep future work research-informed, playable, and
inspectable.

Review in this order:

1. assess the proposal and precedent evidence;
2. identify the smallest credible slice;
3. update this roadmap and SDD documents;
4. run domain QA; and
5. only then promote a bounded implementation item into `SPEC.md` Present.

Current proposal-review candidates:

- **Difficulty expansion:** extend the existing Capitalism-style tiers beyond K
  rivals and AP budgets by varying rival resource access, information access,
  and risk/aggression posture. Harder tiers must remain explainable, and Expert
  difficulty must be validated as severe but winnable rather than punitive or
  impossible.
- **Regional merger/acquisition:** model a realistic US regional affiliation or
  acquisition slice with regulatory review, community commitments, payer
  leverage, labor effects, integration drag, and access/quality consequences.
  Full deal-market simulation, private-equity rollups, and national
  consolidation strategy remain deferred.
  The v0.11.13 affiliation-first design gate, v0.11.14 runtime proposal, and
  v0.12.0 bounded runtime implementation and v0.12.2 observation-context
  follow-up are complete. The post-fix evidence closes the structural MCP gap;
  broader runtime breadth still requires separate implementation and
  domain/design review.
- **GUI thin client:** design a graphical layer that reuses the same core,
  scenario, observation, replay, and debrief data as the CLI/MCP interfaces.
  Publicly downloadable pixel assets require license review, with CC0 sources
  preferred.
- **Differentiated in-house advisors:** evaluate a shared, scarce advisor market
  against repaired state-conditioned monthly advice before adding a roster,
  payroll, candidate availability, or hire/fire mechanic. Any future slice must
  preserve observation boundaries, symmetric human/AI rules, deterministic
  arrivals and hiring contention, and debriefable advice provenance.

## Deliverables

- Technical validation report
- Expert review summary
- Parameter evidence registry
- Sensitivity analysis
- AI-agent gameplay findings
- Educational artifact review findings
- Expansion proposal review artifact when future-feature proposals are under
  consideration
- Prioritized revision plan

## Exit Criteria

- Critical mechanisms are technically reliable and institutionally defensible.
- Known limitations and uncertainties are documented.
- No dominant exploit trivializes the campaign.
- AI-agent playtest evidence shows major causal pathways are inspectable from
  actor-visible observations and debriefs.
- Game artifacts make the stated reasoning objectives inspectable. Evidence of
  learner attainment remains deferred to a separately funded human evaluation.
- Future expansion candidates have explicit review artifacts, evidence limits,
  non-goals, and promotion gates before runtime implementation.

---

# Phase 8: Initial Release Preparation

## Objective

Produce a stable, documented release that can be used, studied, and extended.

## 8.1 Product Stabilization

- Resolve high-priority defects and balance issues.
- Freeze the release ruleset and scenario versions.
- Confirm save, replay, and migration behavior.
- Improve terminal accessibility and error messages.
- Establish compatibility and support expectations.

## 8.2 Documentation

Publish:

- player guide;
- instructor guide;
- contributor guide;
- architecture overview;
- model and assumptions guide;
- scenario authoring guide;
- and limitations statement.

The limitations statement should clearly distinguish educational simulation from policy forecasting.

## 8.3 Reproducible Release Package

Include:

- source code;
- versioned ruleset;
- initial scenario;
- seeds or replay fixtures;
- test suite;
- example run;
- and machine-readable run exports.

## 8.4 Early Adoption

Prepare the release for educational or expert review after the agent-playtest
baseline is stable. Collect any future human feedback through a separate
approved evaluation plan while preserving a stable baseline for comparison.

## Deliverables

- Versioned initial release
- Canonical campaign
- Complete documentation set
- Reproducibility package
- Agent-playtest protocol
- Public issue and feedback process

## Exit Criteria

- A new player can install and complete the campaign using the documentation.
- An instructor can run a structured session and debrief.
- A contributor can inspect assumptions, reproduce a run, and propose a change.
- The released model is clearly versioned and its limitations are visible.

---

# Phase 9: Post-Release Expansion

## Objective

Expand only after the initial model has demonstrated technical, gameplay, and educational value.

## 9.1 Broader US Scenarios

Potential additions include:

- rural health-system crisis;
- academic medical center strategy;
- value-based care transition;
- insurer market instability;
- merger and antitrust review;
- labor action;
- Medicaid expansion or retrenchment;
- public-health emergency;
- and state-level regulatory variation.

Difficulty expansion is also a candidate post-release track. If Phase 7
evidence supports it, refine tiers so they differ by more than rival count:
rival capital and borrowing slack, monitoring depth, information delay, risk
posture, implementation-capacity pressure, and scenario-specific starting
asymmetries. The hardest tier should remain clearable by strong play across
more than one strategy family.

Merger and antitrust review should begin with one regional nonprofit/community
affiliation or acquisition scenario, not a national deal market. The first
slice should model partner fit, regulatory and community review,
community-benefit commitments, payer leverage, labor alignment, integration
cost, and post-deal access or quality consequences.

## 9.2 Deeper Strategic Models

Potential additions include:

- richer coalition formation;
- legislative bargaining;
- signaling and commitment;
- endogenous market entry and exit;
- network formation;
- repeated regulatory relationships;
- and strategic information acquisition.

## 9.3 Platform and Pedagogy

Potential additions include:

- role-based multiplayer;
- graphical or web interfaces that reuse the same deterministic core,
  observations, command validation, replay history, and debrief outputs as the
  CLI/MCP interfaces;
- richer instructor controls;
- assignment and learning-management integration;
- and comparative cohort analytics.

A GUI proof should start as a thin client. Rendering, input handling, layout,
asset loading, and packaging must remain outside the transition core. Pixel
assets must be publicly downloadable and license-audited before distribution;
CC0 assets should be preferred for the first proof.

## 9.4 Comparative Health Systems

International expansion should begin with a new institutional design phase.

Other countries should not be represented merely by changing US parameters. Comparative scenarios may reuse general mechanisms while redefining:

- financing;
- purchasing;
- ownership;
- authority;
- labor relations;
- capital allocation;
- benefit design;
- and patient choice.

## Exit Criteria

Each expansion should have:

- a clear educational or gameplay rationale;
- an explicit research basis;
- a bounded design specification;
- and evidence that the core architecture can support it without distorting the initial model.

---

# 3. Cross-Phase Workstreams

Some work should continue throughout the roadmap.

## Documentation and Decision Records

Keep canonical documents, assumptions, architecture decisions, and mechanism specifications synchronized with implementation.

## Evidence and Assumption Management

Maintain traceability from literature or expert judgment to model parameters and abstractions. Record uncertainty and competing interpretations.

## Testing and Reproducibility

Every new mechanism should include deterministic tests, invariants, and replay fixtures where applicable.

## Ethical and Normative Review

Continuously review:

- how populations are represented;
- which outcomes are valued;
- whether scoring hides normative choices;
- whether disparities are modeled responsibly;
- and whether results could be mistaken for validated forecasts.

## Scope Control

At each phase gate, explicitly decide what will not be built next.

---

# 4. Recommended Immediate Next Steps

1. Complete Phase 0 repository and governance setup.
2. Begin Phase 1 with a structured literature matrix rather than unorganized reading.
3. In parallel, draft the Phase 2 system-boundary specification.
4. Delay detailed Rust type design until the initial ontology and vertical-slice scope are stable.
5. Select one candidate first campaign and one strategic interaction to anchor subsequent design.

The next canonical design document should be the **research plan and literature matrix**, followed by the **initial system-boundary and ontology specification**.
