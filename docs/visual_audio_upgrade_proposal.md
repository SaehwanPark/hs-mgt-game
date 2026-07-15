---
title: "Visual and Audio Experience Upgrade Proposal"
author: "Sae-Hwan Park"
date: 2026-07-14
note: "The proposal was develooped based on the status of checkpoint commit `43e14a606279410f60ce0138eae0b0e524e0d4f7`"
---

**Status:** Proposed canonical product and implementation direction  
**Audience:** Project owner, developers, designers, contributors, and playtest coordinators  
**Scope:** Rich graphical user interface, visual communication, music, sound effects, and presentation-layer tooling  
**Primary target:** `competitive-regional-v1`, followed by reusable support for other campaigns  
**Architecture constraint:** Preserve the existing deterministic simulation, observation, replay, CLI, and MCP boundaries

---

## 1. Executive Summary

The Health Policy Strategy Game has established a strong deterministic simulation core, actor-specific observations, replayable histories, inspectable causal effects, multiple playable campaigns, and a bounded MCP interface. The next major product challenge is no longer primarily simulation breadth. It is making the existing depth immediately understandable, attractive, and engaging to human players.

This proposal recommends a substantial visual and audio upgrade inspired by the strengths of management games such as *Capitalism*: a persistent operating world, inspectable institutions, visible resource and consequence flows, contextual decision-making, and recognizable feedback. The goal is not to copy the exact visual style, city simulation, or micromanagement of those games. The goal is to make an abstract institutional simulation feel tangible and alive.

The upgraded experience should:

- present the regional health market as a persistent, navigable world;
- let players inspect health systems, facilities, competitors, markets, policies, and pending commitments;
- translate typed commands into contextual graphical actions without changing their semantics;
- visualize delayed and second-order consequences over time;
- use music, ambience, and sound effects to direct attention and establish pacing;
- preserve player-visible information boundaries and avoid leaking hidden state;
- support accessibility, muting, and non-audio alternatives;
- remain a thin client over the existing engine and MCP-shaped interface;
- and be developed through narrow, testable vertical slices before broad visual expansion.

The first implementation target should be one polished competitive month that demonstrates the complete visual and audio loop:

```text
observe regional conditions
  -> inspect a bottleneck
  -> choose contextual actions
  -> submit a command batch
  -> resolve the month
  -> see and hear consequences
  -> inspect causal attribution
  -> continue from the changed world
```

The project should prioritize information clarity and consequence visibility before decorative fidelity.

---

## 2. Motivation

### 2.1 Current Product Constraint

The command-line interface is well suited to:

- deterministic testing;
- reproducible commands;
- scripted and MCP agent play;
- rapid mechanics validation;
- complete textual histories;
- and technical inspection.

However, new human players must currently perform substantial mental translation. They must:

- understand abstract metrics before developing intuition;
- remember or discover command syntax;
- infer relationships among workforce, capacity, demand, finance, access, and policy;
- reconstruct a persistent regional world from sequential reports;
- and recognize which changes are immediate, delayed, uncertain, or rival-driven.

These demands are appropriate for expert inspection but create unnecessary friction for broad human playtesting.

### 2.2 Product Opportunity

A richer interface can reduce this translation burden without simplifying the model. A well-designed GUI can make the game more accessible by externalizing relationships that players currently hold in working memory.

Music and sound effects can further improve the experience by:

- distinguishing routine actions from major consequences;
- making turn resolution feel consequential;
- establishing emotional pacing;
- reinforcing event categories;
- signaling that a process has started, advanced, completed, or failed;
- and making the prototype feel like a game rather than a technical dashboard.

The intended result is not a cosmetic wrapper. It is a presentation system that makes institutional dynamics easier to perceive and reason about.

---

## 3. Proposal Thesis

> Preserve the simulation's fidelity of consequence while giving each consequence a visible and audible home in the world.

The graphical and audio layers should make the following relationships legible:

```text
executive decision
  -> institutional process
  -> delayed implementation
  -> operating consequence
  -> stakeholder response
  -> strategic adaptation
```

A player should be able to see not only that a metric changed, but also:

- where the change occurred;
- which institution or facility was affected;
- which prior decision contributed;
- what process remains in motion;
- what information was available at decision time;
- and which consequences remain uncertain or unresolved.

---

## 4. Goals

### 4.1 Primary Goals

The visual and audio upgrade should:

1. Increase the number and diversity of human playtesters willing to try the game.
2. Reduce onboarding and command-entry friction.
3. Improve players' ability to form a mental model of the regional health system.
4. Make operational and institutional bottlenecks visible.
5. Make delayed consequences and pending commitments easy to track.
6. Preserve actor-specific observation boundaries.
7. Turn causal attribution and debriefing into interactive product features.
8. Improve perceived polish and emotional engagement.
9. Reuse the same simulation and command semantics across CLI, MCP, and GUI.
10. Produce reusable presentation primitives for multiple campaigns.

### 4.2 Secondary Goals

The upgrade should also support:

- screenshots and short demonstrations suitable for recruitment and portfolio presentation;
- easier remote playtesting;
- instructor or analyst views in later phases;
- replay visualization;
- campaign-specific visual identity;
- and future localization or accessibility improvements.

---

## 5. Non-Goals

The initial visual and audio upgrade should not attempt to:

- replace or rewrite the deterministic simulation engine;
- duplicate simulation state in the browser;
- create a second set of GUI-only game rules;
- build a real-time simulation;
- reproduce an entire city or individual-patient simulation;
- create detailed hospital interior management;
- require manual placement of individual workers;
- introduce a general-purpose visual scenario editor;
- implement network multiplayer;
- create production-grade deployment infrastructure before the interface is validated;
- or claim educational effectiveness based on interface completion alone.

The design should remain executive-level. The player leads a health system and responds to a regional institutional environment; the player does not directly manage every clinical workflow.

---

## 6. Product Design Principles

### 6.1 Visualize Relationships, Not Merely Metrics

A richer GUI should not become a collection of dashboard cards. It should show how facilities, actors, markets, projects, policies, and outcomes relate.

Whenever possible, a metric should have:

- a visible owner;
- a location or institutional context;
- a recent direction;
- a causal explanation;
- and a connection to available decisions.

### 6.2 Preserve the Executive Perspective

The interface should emphasize:

- allocation of attention;
- capital and workforce strategy;
- payer and regulatory relationships;
- regional competition and cooperation;
- public commitments;
- uncertainty;
- and long-term consequences.

Operational detail should be included only when it creates a meaningful executive decision.

### 6.3 Use Progressive Disclosure

The initial screen should remain comprehensible. Detailed information should be available through inspection rather than displayed simultaneously.

A useful hierarchy is:

```text
regional overview
  -> institution or facility
  -> subsystem or issue
  -> causal details and history
```

### 6.4 Keep Commands Canonical

Graphical actions should produce the same validated typed commands used by the CLI and MCP interfaces.

For example:

```text
GUI selection:
  Riverside Hospital
  -> Recruit
  -> Nurse
  -> Headcount 4

Canonical command:
  recruit role=nurse headcount=4
```

The GUI may optionally display the generated command before submission.

### 6.5 Show Process, Not Only Results

The interface should visualize:

- recruitment pipelines;
- capital-project progress;
- negotiations;
- regulatory review;
- affiliation stages;
- public commitments;
- pending effects;
- delayed observations;
- and unresolved risks.

The world should feel active even though resolution remains turn-based.

### 6.6 Communicate Uncertainty Honestly

Visuals should distinguish:

- observed values;
- estimates;
- uncertain signals;
- delayed reports;
- revised information;
- hidden or unavailable information;
- and realized outcomes.

Uncertainty should not be represented as false numerical precision.

### 6.7 Avoid Moralizing Feedback

The project distinguishes organizational performance, actor utility, social welfare, and decision quality. The interface and audio system should not collapse these into generic success and failure signals.

A profitable closure may harm access. A regulatory condition may protect the community while increasing cost. An affiliation approval may create difficult obligations.

Feedback should communicate:

- event category;
- significance;
- direction;
- and consequences;

not a universal judgment of good or bad.

### 6.8 Treat Audio as Information

Music and sound should:

- direct attention;
- distinguish process categories;
- communicate confirmation and rejection;
- support emotional pacing;
- and reinforce important consequences.

Audio should not be required to understand the game.

### 6.9 Preserve Thin-Client Architecture

The graphical client should consume:

- scenario metadata;
- actor-visible observations;
- legal commands and validation information;
- committed transition summaries;
- pending effects;
- history and state hashes;
- and debrief output.

It must not calculate hidden outcomes or mutate the simulation independently.

---

## 7. Target Player Experience

### 7.1 Persistent Regional World

The primary competitive screen should represent the regional healthcare environment as a persistent board or map.

Possible entities include:

- player-owned hospitals and ambulatory facilities;
- competitor systems;
- service areas;
- patient-demand zones;
- workforce markets;
- payer influence;
- community and political jurisdictions;
- active projects;
- affiliation candidates;
- and major policy processes.

The first version may use a stylized schematic map rather than realistic geography.

The map should help players answer:

- Where is demand emerging?
- Which facilities are constrained?
- Where are rivals expanding?
- Which areas are underserved?
- Where do workforce and payer pressures differ?
- Which institutions are currently engaged in a strategic process?

### 7.2 Inspectable Institutions and Facilities

Selecting a health system or facility should reveal a focused detail panel containing player-visible information such as:

- staffed capacity;
- physical capacity;
- utilization or treated volume;
- unmet demand;
- quality and access indicators;
- workforce condition;
- operating revenue and cost in game units;
- contribution to cash margin;
- payer pressure;
- active projects;
- commitments;
- recent events;
- and available actions.

The panel should identify major bottlenecks in plain language while preserving uncertainty.

Example:

> Demand exceeds staffed capacity. Physical beds are available, but nursing shortages limit treated volume. Recruiting may help after a delay; additional bed investment is unlikely to resolve the current bottleneck.

This may be presented as an advisory interpretation derived from the actor-visible observation, not hidden state.

### 7.3 Executive Header

A persistent header should summarize limited resources and major organizational conditions:

- date or campaign stage;
- cash;
- monthly operating margin;
- action points;
- political capital;
- workforce trust;
- community trust;
- current strategic alerts;
- and save or session status.

### 7.4 Executive Briefing Panel

The briefing panel should summarize:

- major risks;
- recent changes;
- pending decisions;
- delayed observations;
- rival intelligence;
- policy developments;
- and advisor recommendations.

Players should be able to move from a briefing item directly to the relevant facility, actor, policy, or timeline event.

### 7.5 Contextual Action Panel

Available actions should depend on the selected context.

Examples:

**Facility selected**

- recruit;
- invest;
- start project;
- adjust service priority;
- inspect operating drivers.

**Payer selected**

- negotiate;
- review contract pressure;
- inspect payer exposure.

**Competitor selected**

- monitor;
- inspect known public actions;
- compare market position.

**Policy process selected**

- commit;
- advocate;
- review authority and uncertainty.

**Affiliation partner selected**

- assess;
- choose posture;
- negotiate commitments;
- submit for review;
- integrate.

The GUI should show:

- action-point cost;
- cash cost;
- political-capital cost;
- implementation delay;
- known constraints;
- and visible uncertainty.

### 7.6 Pending-Effects Timeline

A timeline should display processes already in motion:

- recruitment completion;
- construction or technology rollout;
- annual policy events;
- contract milestones;
- regulatory review;
- affiliation stages;
- delayed reports;
- and prior commitments.

The timeline is important because it converts delayed effects from an invisible rule into an understandable strategic state.

### 7.7 Monthly Resolution

After submission, the interface should present a concise resolution sequence:

1. submitted player actions;
2. known rival or institutional responses;
3. process advancement;
4. operating results;
5. resource changes;
6. access, quality, workforce, and trust effects;
7. newly visible information;
8. updated pending processes.

The sequence may use restrained animation, highlighting, and audio cues. It should remain skippable and reviewable.

### 7.8 Causal Overlays

Interactive causal overlays should become the project's distinctive graphical feature.

Selecting an outcome such as operating margin should reveal visible contributors:

```text
treated volume
  + quality adjustment
  + payer-pressure realization
  - workforce cost
  - physical-footprint cost
  - project draws
  = operating margin
```

Selecting access deterioration might highlight:

- demand zones;
- constrained facilities;
- unmet demand;
- staffing shortages;
- delayed capacity projects;
- and recent strategic decisions.

The first implementation should show direct and documented attributed effects. More advanced inferred causal graphs should be deferred unless supported by the engine's committed history.

### 7.9 Replay and Debrief

The GUI should eventually support:

- month-by-month replay;
- action and observation review;
- state-hash visibility;
- consequence-chain inspection;
- advisor recommendation comparison;
- strategy summaries;
- and separation of decision-time information from realized outcomes.

An instructor or analytic mode may later expose true state, but the standard player mode must preserve historical information boundaries.

---

## 8. Proposed Screen Architecture

A representative competitive-campaign layout:

```text
+--------------------------------------------------------------------+
| Date | Cash | Margin | AP | Political Capital | Trust | Alerts     |
+--------------------------------------+-----------------------------+
|                                      | Executive Briefing          |
|                                      | - major risks               |
|         Regional Market View         | - opportunities             |
|                                      | - rival intelligence        |
| facilities, rivals, demand zones,    | - delayed information       |
| projects, policy and community areas | - advisor recommendations   |
|                                      |                             |
+--------------------------------------+-----------------------------+
| Selected Entity                      | Contextual Actions           |
| capacity, workforce, quality, access | recruit / invest / monitor  |
| finance, projects, history           | negotiate / commit / project|
+--------------------------------------+-----------------------------+
| Pending Processes and Event Timeline                               |
+--------------------------------------------------------------------+
```

The visual design should support both larger desktop displays and narrower laptop layouts. Mobile support is not a first-release requirement.

---

## 9. Visual Language

### 9.1 Overall Direction

The desired visual tone should be:

- serious but inviting;
- information-rich but not visually crowded;
- contemporary rather than retro imitation;
- institutional rather than clinical;
- and visually distinct from generic business dashboards.

The Capitalism inspiration should appear in:

- persistent world representation;
- inspectable operating entities;
- visible economic and organizational flows;
- and layered management information.

It need not copy:

- isometric city construction;
- window-heavy interface conventions;
- low-resolution retro graphics;
- or product-level retail micromanagement.

### 9.2 Entity Identity

Each health system should have:

- a consistent emblem or icon;
- a restrained color identity;
- recognizable facility markers;
- and consistent appearance across map, reports, timelines, and charts.

Color must not be the only means of distinction.

### 9.3 Status and Severity

Status indicators should distinguish:

- stable;
- watch;
- constrained;
- critical;
- improving;
- uncertain;
- delayed;
- and revised.

Icons, labels, patterns, and shape should accompany color.

### 9.4 Animation

Animation should explain changes rather than decorate them.

Appropriate uses include:

- project progress;
- recruitment pipelines;
- demand movement;
- capacity activation;
- regulatory-stage advancement;
- affiliation progress;
- month transition;
- and highlighting changed causal contributors.

Animations should be:

- brief;
- skippable;
- compatible with reduced-motion preferences;
- and based on committed visible outcomes.

---

## 10. Audio Direction

### 10.1 Audio Layers

The audio system should contain three independently controllable layers:

1. **Music**
2. **Interface and notification effects**
3. **Ambient and event-specific effects**

### 10.2 Music

Music should establish pace and institutional atmosphere without overpowering analytical play.

Recommended musical states:

| Music state | Intended character |
|---|---|
| Main menu | distinctive, restrained theme |
| Stable operations | measured, calm, lightly optimistic |
| Financial pressure | lower pulse, reduced harmonic stability |
| Workforce strain | restrained tension and irregular rhythm |
| Regulatory scrutiny | sparse and deliberative |
| Competitive escalation | stronger forward movement |
| Affiliation negotiation | ambiguous and reflective |
| Debrief | slower and contemplative |

The initial implementation should use a small number of loopable tracks with crossfades. Dynamic composition is unnecessary.

Music state must derive from player-visible conditions or explicit campaign stage. It must not reveal hidden state.

### 10.3 Interface Sounds

Initial interface sounds should include:

- selection or button confirmation;
- command added;
- command removed;
- action rejected;
- batch submitted;
- month advanced;
- report received;
- save completed;
- and panel or timeline focus where useful.

Effects should be short, restrained, and consistent.

### 10.4 Event and Consequence Sounds

Priority event cues include:

- project started;
- project completed;
- staffing constraint;
- operating loss;
- operating recovery;
- payer agreement;
- payer rejection;
- regulatory approval;
- regulatory conditions;
- rival expansion;
- community response;
- affiliation milestone;
- and revised information.

The sounds should communicate category and significance rather than moral approval.

### 10.5 Ambient Sound

Optional ambience may support selected contexts:

- quiet hospital or office ambience;
- meeting-room or administrative atmosphere;
- distant facility activity;
- construction;
- regional market or city ambience;
- and restrained policy or news cues.

The game should avoid sensational or ethically inappropriate clinical audio, including repeated patient distress, emergency alarms, resuscitation sounds, or sirens used as entertainment.

### 10.6 Audio Controls

The GUI must include:

- master volume;
- music volume;
- effects volume;
- ambience volume;
- mute;
- mute when unfocused;
- reduced notification sounds;
- and persistent settings.

The game must remain fully understandable when muted.

---

## 11. Technical Architecture

### 11.1 Boundary

The intended architecture is:

```text
deterministic simulation
  -> committed transition and history
  -> actor-visible presentation model
  -> GUI state
  -> visual rendering and audio cues
```

The GUI must not:

- resolve randomness;
- read hidden state;
- independently apply game formulas;
- create GUI-only commands;
- or calculate authoritative outcomes.

### 11.2 Presentation DTOs

The GUI should consume stable, serializable presentation objects, potentially through the existing MCP boundary or a closely related adapter.

Candidate objects include:

- `CampaignSummary`
- `RegionalMapView`
- `InstitutionView`
- `FacilityView`
- `ExecutiveBriefing`
- `ActionCatalogView`
- `ActionPreview`
- `PendingProcessView`
- `MonthlyResolutionView`
- `CausalAttributionView`
- `DebriefView`
- `AudioPresentationEvent`

These objects should contain actor-visible information only.

### 11.3 Action Submission

The graphical client should construct canonical typed commands or command strings and submit them through the same validation path used elsewhere.

A GUI action preview should include:

- canonical command;
- costs;
- delays;
- visible constraints;
- validation result;
- and known consequence categories.

It must not promise realized outcomes.

### 11.4 Audio Cue Mapping

Audio cues should be presentation-layer outputs derived from committed visible events.

A conceptual type:

```rust
pub enum AudioCue {
  ActionAccepted,
  ActionRejected,
  MonthAdvanced,
  ReportReceived,
  ProjectStarted,
  ProjectCompleted,
  StaffingConstraint,
  OperatingLoss,
  OperatingRecovery,
  PayerAgreement,
  PayerRejection,
  RegulatoryApproval,
  RegulatoryCondition,
  RivalExpansion,
  AffiliationMilestone,
  InformationRevised,
}
```

The mapping should be testable without playing sound.

The simulation core should not contain audio asset paths, volumes, or playback logic.

### 11.5 Music-State Mapping

Music state should be derived from a visible presentation summary:

```text
visible campaign conditions
  -> presentation mood classification
  -> music state
  -> crossfade in client
```

The classifier should be deterministic for a given visible presentation state.

### 11.6 Replay Compatibility

Audio and animation should not alter:

- replay artifacts;
- state hashes;
- command histories;
- or deterministic outcomes.

During replay, the client may regenerate presentation cues from committed visible history. Audio playback itself need not be recorded as simulation history.

---

## 12. Asset Strategy and Licensing

### 12.1 Asset Sources

The project may use publicly downloadable visual and audio assets from reputable libraries and individual creators, provided each asset's license is reviewed.

Preferred licenses:

1. CC0 or equivalent public-domain dedication
2. CC BY with manageable attribution
3. clearly documented permissive game-asset licenses
4. custom licenses reviewed individually

Avoid by default:

- noncommercial-only assets;
- personal-use-only assets;
- unclear redistribution rights;
- assets requiring the original file to remain separately downloadable;
- licenses incompatible with later paid or institutional distribution;
- and music likely to trigger automated copyright claims.

A free download is not evidence of permission to redistribute.

### 12.2 Asset Registry

All third-party assets should be recorded in a machine-readable registry.

Example:

```toml
[[asset]]
id = "audio.ui.action-confirm"
path = "assets/audio/ui/action-confirm.ogg"
kind = "sound_effect"
title = "Soft Confirmation"
creator = "Creator Name"
source_page = "https://example.org/asset"
downloaded_on = "YYYY-MM-DD"
license = "CC0-1.0"
license_url = "https://creativecommons.org/publicdomain/zero/1.0/"
modified = true
modifications = "Trimmed, normalized, and converted to Ogg Vorbis"
original_sha256 = "..."
release_sha256 = "..."
```

The registry should generate or support:

- `ASSET_CREDITS.md`;
- in-game credits;
- source and license auditing;
- and replacement of assets when terms are uncertain.

### 12.3 Asset Storage

Recommended approach:

```text
original source assets
  -> retained outside the release tree or in Git LFS

processed release assets
  -> compressed and optimized under assets/

licenses and provenance
  -> ordinary version-controlled text
```

Audio release assets may use Ogg Vorbis, with additional formats only where browser compatibility requires them.

### 12.4 Original Art Direction

Public assets should be treated as raw material. Visual coherence may require:

- recoloring;
- cropping;
- icon simplification;
- consistent line weight;
- consistent perspective;
- and standardized resolution.

All modifications must remain compatible with the source license and be documented.

---

## 13. Accessibility Requirements

The visual and audio upgrade should include accessibility from the start.

### 13.1 Visual Accessibility

- Do not rely only on color.
- Support readable type sizes and zoom.
- Maintain sufficient contrast.
- Use text labels and icons together.
- Support reduced motion.
- Provide keyboard navigation for primary actions.
- Ensure major interface elements have semantic labels.
- Avoid dense hover-only information.

### 13.2 Audio Accessibility

- All audio-signaled events must have visual equivalents.
- Support complete mute.
- Support independent volume channels.
- Avoid using stereo position as the only event distinction.
- Avoid using pitch alone to encode severity.
- Provide subtitles or textual labels for any spoken or broadcast audio.
- Respect browser autoplay restrictions.
- Begin music only after user interaction.

### 13.3 Cognitive Accessibility

- Use progressive disclosure.
- Keep terminology consistent with canonical project documents.
- Explain game-unit metrics.
- Make action costs and delays visible.
- Keep current decisions separate from retrospective explanations.
- Allow resolution animations to be skipped and reviewed.

---

## 14. Development Sequence

The visual and audio upgrade should proceed through evidence-gated phases.

# Phase 0: Product and Architecture Alignment

## Objective

Agree on the role of the GUI and audio system before implementation.

## Work

- Confirm the GUI as a thin client.
- Select `competitive-regional-v1` as the primary first target.
- Define the first-month vertical slice.
- Identify canonical observation, action, transition, and debrief surfaces.
- Define hidden-state exclusions.
- Select the initial technology stack.
- Establish visual and audio asset policies.
- Create architecture decision records where needed.

## Deliverables

- approved interface boundary;
- first-slice experience specification;
- presentation DTO inventory;
- preliminary wireframes;
- audio cue catalog;
- asset license policy.

## Exit Criteria

- No proposed GUI component requires direct simulation-state ownership.
- Every first-slice action maps to an existing canonical command.
- Every displayed value has an identified actor-visible source.
- Audio cues can be derived from visible or committed presentation events.

---

# Phase 1: Static Executive Desktop Prototype

## Objective

Validate information architecture without full interaction or polished artwork.

## Work

Create a static or injected-data prototype containing:

- executive header;
- regional schematic;
- system and facility cards;
- selected-entity detail panel;
- contextual action panel;
- executive briefing;
- pending-effects timeline;
- and monthly result view.

Use representative injected MCP-shaped data.

## Deliverables

- navigable desktop prototype;
- responsive layout for typical laptop and desktop widths;
- initial design tokens;
- initial entity icons and status language;
- usability review checklist.

## Exit Criteria

- A new reviewer can locate financial, workforce, capacity, access, and rival information.
- Major bottlenecks are visible without reading raw JSON or CLI output.
- The screen does not expose hidden state.
- The layout remains comprehensible at common desktop resolutions.

---

# Phase 2: Live Read-Only Integration

## Objective

Render real campaign observations and committed history without enabling actions.

## Work

- Connect the GUI adapter to live or recorded session data.
- Render current observations.
- Display institutional and facility detail.
- Render pending effects and history.
- Display state hashes and replay metadata where appropriate.
- Add loading, error, and empty states.

## Deliverables

- live read-only campaign viewer;
- typed adapter contract;
- fixture-based rendering tests;
- hidden-field exclusion tests;
- first replay-view prototype.

## Exit Criteria

- The GUI renders the same player-visible facts as CLI or MCP output.
- No simulation formulas are duplicated.
- Golden or replay fixtures render consistently.
- Missing information is represented explicitly rather than guessed.

---

# Phase 3: Contextual Action Submission

## Objective

Allow a player to complete one competitive month graphically.

## Work

- Implement contextual action forms.
- Show canonical command previews.
- Validate action batches through the existing engine boundary.
- Display action costs, delays, and constraints.
- Support action removal and revision.
- Submit the month.
- Handle rejected actions without advancing the turn.
- Preserve CLI/MCP command compatibility.

## Deliverables

- graphical action workflow;
- action-batch builder;
- validation and retry experience;
- command-preview component;
- integration tests against existing command validation.

## Exit Criteria

- A player can complete a month without typing commands.
- The generated commands are equivalent to supported CLI commands.
- Rejected actions leave simulation state unchanged.
- The GUI does not imply certainty about stochastic outcomes.

---

# Phase 4: Resolution, Animation, and Causal Feedback

## Objective

Make one full decision-to-consequence cycle understandable and satisfying.

## Work

- Build monthly resolution sequencing.
- Highlight changed facilities, resources, and processes.
- Animate project and recruitment progress.
- Add operating-result breakdown.
- Add direct causal-attribution overlays.
- Support skip, pause, and review.
- Distinguish observation-time information from realized outcomes.

## Deliverables

- polished one-month visual loop;
- consequence animation framework;
- causal overlay components;
- reduced-motion behavior;
- replayable monthly resolution.

## Exit Criteria

- Players can identify the principal bottleneck and outcome drivers.
- Animation does not conceal or delay access to textual results.
- All displayed causal claims originate from committed effects or documented presentation logic.
- Resolution can be replayed without changing simulation state.

---

# Phase 5: Foundational Audio Integration

## Objective

Add a coherent but bounded audio layer to the polished visual slice.

## Work

Implement:

**Music**
- menu theme;
- stable-operations loop;
- pressure loop;
- debrief track.

**Interface sounds**
- confirm;
- reject;
- add action;
- remove action;
- submit;
- advance month;
- report received;
- save complete.

**Event sounds**
- project completion;
- staffing constraint;
- operating loss;
- operating recovery;
- payer decision;
- regulatory decision;
- rival expansion;
- affiliation milestone.

Also implement:

- audio cue mapping;
- music-state mapping;
- volume controls;
- mute and focus behavior;
- asset registry;
- credits generation;
- and audio tests using a recording sink or equivalent.

## Deliverables

- integrated audio vertical slice;
- initial licensed asset set;
- asset registry and credits;
- audio settings;
- cue-mapping tests.

## Exit Criteria

- Audio changes no simulation outcome, hash, or replay.
- The game remains fully understandable when muted.
- Music does not leak hidden state.
- Every asset has recorded provenance and license.
- Effects remain restrained during repeated monthly play.

---

# Phase 6: Regional Map and Persistent World Expansion

## Objective

Make the campaign feel like an evolving regional system rather than a sequence of reports.

## Work

- Expand the regional map.
- Add demand and access overlays.
- Show facility and competitor identity.
- Visualize active projects and public rival actions.
- Add navigation between briefing, map, details, and timeline.
- Add institutional relationship indicators where justified.
- Improve visual identity and coherence.

## Deliverables

- persistent regional-world interface;
- map overlays;
- institution identity system;
- expanded timeline;
- visual asset library.

## Exit Criteria

- A player can explain the broad regional situation from the map and linked panels.
- Map elements represent actionable or explanatory information.
- Decorative complexity does not obscure decision-relevant state.
- Player-visible rival information respects observation lag.

---

# Phase 7: Campaign Coverage

## Objective

Extend the validated presentation system to the other campaigns.

## Work

### Stabilization

- create an onboarding-oriented visual flow;
- simplify the action surface;
- emphasize briefing, uncertainty, and causal debrief;
- use it as a potential tutorial.

### Affiliation

- create partner-condition and fit views;
- visualize commitments;
- show institutional review stages;
- show stakeholder responses;
- visualize integration progress and obligations;
- add campaign-specific music and event cues where justified.

## Deliverables

- visual stabilization campaign;
- visual affiliation campaign;
- shared and campaign-specific components;
- campaign-specific audio mapping.

## Exit Criteria

- Shared primitives are reused without forcing incompatible campaign semantics.
- Each campaign has a clear product role.
- Campaign-specific information structures remain intact.
- No campaign requires simulation changes solely to fit the GUI.

---

# Phase 8: Human Playtest Readiness

## Objective

Prepare the upgraded experience for external human testing.

## Work

- improve onboarding;
- add guided first-run flow;
- add settings and accessibility review;
- improve error recovery;
- instrument non-sensitive interaction events where appropriate;
- prepare a playtest build;
- create a facilitator protocol;
- define observation and interview questions;
- establish bug-report and feedback channels.

## Deliverables

- playtest-ready build;
- onboarding flow;
- accessibility checklist;
- tester guide;
- facilitator protocol;
- structured feedback form.

## Exit Criteria

- A new player can install or launch the game and complete a session without developer intervention.
- Testers can mute audio and reduce motion.
- Major errors provide actionable recovery.
- The test protocol distinguishes usability, engagement, institutional plausibility, and educational claims.

---

# Phase 9: External Evaluation and Revision

## Objective

Use real player evidence to determine subsequent development.

## Work

Conduct separate evidence tracks:

1. **Usability observation**
   - navigation;
   - action entry;
   - error recovery;
   - information overload;
   - onboarding.

2. **Game-experience observation**
   - strategy formation;
   - perceived agency;
   - surprise;
   - desire to replay;
   - pacing;
   - emotional engagement.

3. **Domain review**
   - institutional plausibility;
   - terminology;
   - authority;
   - consequence interpretation.

4. **Educational evaluation**
   - deferred to an appropriately designed and resourced study.

## Deliverables

- playtest findings;
- prioritized interface revisions;
- product decision log;
- evidence-based reopening or closure of feature areas.

## Exit Criteria

- The next major development decision is grounded in observed human use.
- Automated traces are not substituted for human experience claims.
- Major misunderstandings between player mental models and simulation behavior are documented.
- The project can decide whether to prioritize polish, mechanics revision, onboarding, or broader release.

---

## 15. Suggested First Vertical Slice

The first polished slice should include exactly one month of `competitive-regional-v1`.

### Required Experience

1. Start or load a campaign.
2. View the regional market.
3. Inspect Riverside and its facilities.
4. Identify a workforce or capacity bottleneck.
5. Inspect recent rival and payer information.
6. Choose at least two contextual actions.
7. Review canonical commands, costs, and delays.
8. Submit the action batch.
9. Watch or skip monthly resolution.
10. See updated volume, unmet demand, revenue, cost, and margin.
11. Inspect the direct causal breakdown.
12. Hear restrained music and event cues.
13. Continue to the next observation.

### Initial Asset Scope

**Visual**
- three system identities;
- facility markers;
- demand and capacity icons;
- project and staffing indicators;
- policy, payer, and timeline icons;
- map background;
- status and severity language.

**Audio**
- four music tracks;
- eight interface sounds;
- eight event sounds;
- optional one or two ambient loops.

This is enough to test the experience without committing to a full asset production pipeline.

---

## 16. Testing Strategy

### 16.1 Architecture Tests

Verify that:

- the GUI uses presentation DTOs rather than core state;
- hidden fields are excluded;
- all actions map to canonical commands;
- validation failures do not advance state;
- and presentation changes do not alter golden hashes.

### 16.2 Rendering Tests

Test:

- representative normal states;
- empty and missing data;
- extreme values;
- uncertain and delayed observations;
- long names and text;
- different difficulty tiers;
- and multiple viewport sizes.

### 16.3 Audio Tests

Test:

- event-to-cue mapping;
- visible-state-to-music-state mapping;
- mute behavior;
- independent channel volumes;
- reduced notification mode;
- focus loss;
- repeated-event throttling;
- and missing-asset fallback.

### 16.4 Accessibility Tests

Test:

- keyboard navigation;
- screen-reader semantics where applicable;
- color-independent status interpretation;
- contrast;
- reduced motion;
- text scaling;
- and complete muted play.

### 16.5 Human Playtests

Observe:

- time to first valid action;
- ability to identify current bottlenecks;
- ability to predict directional consequences;
- use of map versus briefing;
- recovery from validation errors;
- comprehension of pending effects;
- interpretation of audio cues;
- and post-run causal explanations.

These observations should be treated as product evidence, not formal learning evidence unless collected under an appropriate study design.

---

## 17. Contributor Workstreams

The project may organize contributions into the following workstreams.

### Product and UX

- information architecture;
- wireframes;
- onboarding;
- action flows;
- resolution pacing;
- user research.

### Visual Design

- map;
- icons;
- institution identity;
- layout;
- animation;
- accessibility;
- asset adaptation.

### Front-End Engineering

- client state;
- rendering;
- adapter integration;
- action submission;
- settings;
- audio playback;
- testing.

### Rust and Interface Contracts

- presentation DTOs;
- MCP or adapter surfaces;
- actor-visible projections;
- action validation integration;
- replay and debrief access.

### Audio

- music selection;
- sound design;
- normalization;
- cue taxonomy;
- licensing;
- mixing and playback rules.

### Asset Governance

- license review;
- provenance registry;
- credits;
- source archiving;
- release-asset optimization.

### Playtesting

- recruitment;
- protocols;
- observation;
- interviews;
- issue triage;
- evidence classification.

Contributors should avoid changing simulation mechanics merely to solve presentation problems unless a documented model or information gap is identified.

---

## 18. Risks and Mitigations

### Risk: GUI Becomes a Parallel Game Engine

**Mitigation:** Require canonical commands, presentation DTOs, hidden-field exclusion tests, and unchanged golden hashes.

### Risk: Attractive Graphics Conceal Weak Mental Models

**Mitigation:** Prioritize causal overlays, process timelines, and directional explanations before decorative polish.

### Risk: Scope Expands Into a City Builder

**Mitigation:** Preserve the executive perspective and require every map element to support a decision or explanation.

### Risk: Audio Becomes Fatiguing

**Mitigation:** Use restrained cues, event throttling, independent volume controls, and repeated-session testing.

### Risk: Music Leaks Hidden State

**Mitigation:** Derive music only from player-visible conditions or explicit campaign stages.

### Risk: Licensing Problems

**Mitigation:** Prefer CC0/CC BY, maintain an asset registry, retain license evidence, and audit every release asset.

### Risk: Accessibility Is Deferred

**Mitigation:** Include keyboard, reduced-motion, color-independent, and mute requirements in the first vertical slice.

### Risk: Visual Polish Delays Human Testing

**Mitigation:** Test the static prototype and first live month before broad asset production.

### Risk: Automated Validation Is Mistaken for Human Evidence

**Mitigation:** Preserve separate claims for technical correctness, interface traceability, human usability, engagement, domain plausibility, and learning.

### Risk: Existing Campaigns Are Forced Into One Interface Metaphor

**Mitigation:** Share primitives while allowing campaign-specific information structures and visual flows.

---

## 19. Measures of Success

The visual and audio upgrade should be considered successful when:

- new players can begin a campaign without learning command syntax;
- players can identify major workforce, capacity, finance, access, and policy pressures;
- players can track pending and delayed effects;
- graphical actions remain equivalent to canonical engine commands;
- monthly consequences are understandable without reading raw logs;
- audio reinforces events without becoming required or exhausting;
- players can explain important outcomes using visible consequence chains;
- the GUI preserves replay and observation boundaries;
- external testers demonstrate willingness to complete and replay sessions;
- and subsequent development priorities are informed by observed human use.

The upgrade should not be considered validated solely because:

- the interface renders;
- all automated tests pass;
- agents can complete sessions;
- the game appears more polished;
- or players report that it “looks good.”

---

## 20. Immediate Next Steps

1. Approve this proposal as the working visual/audio direction.
2. Define the exact one-month competitive vertical slice.
3. Inventory current MCP and presentation data needed by the slice.
4. Create low-fidelity wireframes for the principal screen.
5. Define the initial presentation DTO contract.
6. Define the audio cue and music-state catalogs.
7. Adopt the asset licensing and provenance policy.
8. Build the static executive desktop using injected session data.
9. Review the prototype with developers and a small number of prospective testers.
10. Proceed to live read-only integration only after the information architecture is understandable.

---

## 21. Guiding Principle

> Build a visual and audio system that makes institutional relationships, delayed processes, and causal consequences easier to perceive without weakening the deterministic, inspectable, and actor-bounded simulation underneath.

The upgrade should make the game more attractive because it makes the modeled world more legible and alive—not because it hides complexity behind spectacle.
