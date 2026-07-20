# Health Policy Strategy Game
## Visual and Audio Enhancement Roadmap

**Status:** Proposed implementation roadmap  
**Scope:** Graphical and sound asset development for the browser GUI  
**Preferred direction:** Flat-vector isometric executive simulation with hybrid synthesized and recorded audio  
**Primary reference point:** *Capitalism 2*–style functional visual density, spatial legibility, and visible consequences  
**Project constraints:** Open-source distribution, deterministic simulation, actor-visible information boundaries, accessibility, and explicit asset provenance

---

## 1. Purpose

This roadmap defines a comprehensive path for advancing the project's visual and audio presentation from its current token-, CSS-, and synthesis-based form into a coherent graphical management simulation.

The recommended direction is:

> A flat-vector isometric regional simulation board, modular health-facility assets, stable institutional visual identities, restrained consequence animation, and hybrid synthesized/recorded audio.

The roadmap deliberately preserves the project's existing architectural strengths:

- the simulation host remains authoritative;
- presentation consumes only actor-visible information;
- rendering does not infer hidden state;
- deterministic replay remains intact;
- accessibility is preserved;
- and every external or generated asset has documented provenance.

This is not a roadmap for replacing the CLI-first architecture or turning the browser client into an independent simulation frontend. It is a roadmap for making the existing simulation more legible, memorable, and game-like without weakening its conceptual or technical foundations.

---

## 2. Guiding Principles

### 2.1 Visualize consequences, not decoration

Every visual or audio addition should help the player understand one or more of:

- what institution or facility is involved;
- what changed;
- where pressure is accumulating;
- which consequence is immediate versus delayed;
- what information is known versus uncertain;
- and how prior decisions propagated through the system.

Decorative assets that do not improve strategic comprehension should be deferred.

### 2.2 Preserve actor-visible information boundaries

The GUI may only render facts, categories, statuses, and relationships available in the actor-visible state.

The presentation layer must not:

- infer hidden rival intent;
- reveal true-state deterioration before observation;
- derive severity not supplied by the host;
- expose future project outcomes;
- or use music and animation to leak hidden information.

### 2.3 Prefer modular asset systems

Reusable visual parts should be favored over individually illustrated screens or scenes.

Examples:

- modular hospital-campus components;
- layered project and pressure overlays;
- reusable report and notification frames;
- institutional palette and logo tokens;
- reusable audio motifs and stems.

### 2.4 Use a restrained visual language

The target is a serious management simulation rather than a mobile dashboard or cinematic hospital game.

Prefer:

- compact information density;
- stable panel geometry;
- muted institutional colors;
- isometric or oblique facility illustrations;
- small purposeful animations;
- and visual hierarchy based on strategic relevance.

Avoid:

- excessive gradients and glow;
- generic stock photography;
- photorealistic AI imagery as the dominant style;
- constant movement;
- and animations that delay access to information.

### 2.5 Treat accessibility as part of the asset specification

Color, animation, and sound must never be the only channels for information.

Every semantic asset should have:

- a visible text label or accessible name;
- non-color differentiation where applicable;
- a reduced-motion behavior;
- a text or visual equivalent for meaningful sound;
- and sufficient contrast at supported text scales.

### 2.6 Treat provenance as a release gate

No asset enters the release tree without:

- source or generation method;
- creator or model identification;
- license;
- retrieval or creation date;
- original and release hashes;
- modification history;
- attribution text where required;
- and explicit approval status.

---

## 3. Target Experience

The player should experience the GUI as an illustrated executive operating environment composed of:

1. **Regional strategy board**  
   A stylized isometric view of the market, systems, facilities, projects, and visible institutional relationships.

2. **Executive desktop**  
   Compact operational, financial, workforce, policy, and intelligence panels.

3. **Institutional identities**  
   Distinct visual and sonic identities for Riverside, Northlake, Summit, and other recurring actors.

4. **Visible consequence chain**  
   Decisions should visibly propagate across facilities, reports, metrics, rival actions, and the month-resolution sequence.

5. **Hybrid audio layer**  
   Synthesized UI cues, restrained adaptive music, and carefully selected or generated environmental sounds.

The presentation should evoke the functional qualities of classic business simulations while retaining modern readability, accessibility, and deterministic behavior.

---

# Phase 0: Program Foundation and Scope Lock

## Objective

Establish the governance, constraints, test surfaces, and asset pipeline required before creating substantial artwork or audio.

## Milestone 0.1: Visual/audio product brief approved

**Status:** Complete in v0.12.34
**Evidence:** `docs/history/initiatives/visual-audio/visual-audio-phase0-foundation-v0.12.34.md`

### Deliverables

- A concise visual/audio product brief.
- Formal statement of target style.
- Explicit list of presentation goals.
- Explicit list of non-goals.
- Definition of the first vertical slice.
- Definition of acceptable external licenses.
- Definition of acceptable AI-generation routes.
- Definition of supported browser and display targets.

### Required decisions

- Flat-vector isometric is the primary visual style.
- SVG is the initial map and facility rendering format.
- Existing HTML/CSS panel architecture remains.
- Recorded audio supplements rather than replaces synthesized UI cues.
- No photorealistic patient or clinical imagery in the initial release.
- No third-party asset is accepted without machine-readable provenance.
- No asset may encode hidden simulation information.

### Checklist

- [x] Product brief written.
- [x] Target visual style approved.
- [x] Target audio style approved.
- [x] First vertical-slice scenario selected.
- [x] Supported resolutions documented.
- [x] Reduced-motion behavior documented.
- [x] License allowlist documented.
- [x] License denylist documented.
- [x] AI-generation policy documented.
- [x] Asset review ownership assigned.
- [x] Simulation-authority boundary documented.
- [x] Accessibility requirements documented.

### Exit criteria

- Contributors can determine whether a proposed asset fits the project without subjective reinterpretation.
- The first visual/audio slice is bounded enough to complete without redesigning the entire GUI.
- Licensing and provenance rules are established before acquisition begins.

---

## Milestone 0.2: Asset repository architecture implemented

**Status:** Complete in v0.12.34
**Evidence:** `assets/README.md`, `scripts/validate_assets.py`, and
`scripts/generate_asset_credits.py`

### Recommended structure

```text
assets/
  README.md
  registry/
    visual-assets.json
    audio-assets.json
    schemas/
  source/
    visual/
      identity/
      facilities/
      regional-map/
      actors/
      reports/
      ui/
    audio/
      cues/
      ambience/
      music/
      source-recordings/
  generated/
    visual/
    audio/
  release/
    visual/
      svg/
      raster/
    audio/
      opus/
      wav/
  tools/
    validate_assets.py
    build_assets.py
    hash_assets.py
```

### Deliverables

- Asset directories.
- Registry schemas.
- Naming convention.
- Asset validation script.
- Hash-generation script.
- Release-build script.
- Attribution generator.
- Pull-request checklist for asset changes.

### Checklist

- [x] Source and release assets are separated.
- [x] Registry schema validates.
- [x] Every release asset requires a registry entry.
- [x] Original and release hashes are computed automatically.
- [x] Missing license fields fail validation.
- [x] Missing source or generation metadata fail validation.
- [x] Attribution output is generated automatically.
- [x] Duplicate asset IDs fail validation.
- [x] Unknown semantic roles fail validation.
- [x] CI runs asset validation.
- [x] Asset review checklist is added to contribution docs.

### Exit criteria

- A new asset cannot enter the release tree without provenance metadata.
- Asset processing is reproducible from committed source material.
- CI detects missing, altered, or unregistered assets.

---

# Phase 1: Art Direction and Technical Prototyping

## Objective

Validate the preferred visual style and rendering approach through a small number of concrete prototypes.

## Milestone 1.1: Art-direction reference board

**Status:** Complete in v0.12.35
**Evidence:** `docs/design/visual-audio-art-direction-board.md` and
`docs/decision-records/0012-visual-audio-art-direction.md`

### Deliverables

A committed reference board covering:

- color palette;
- system identity palette;
- facility architecture language;
- line weight;
- shadow and depth treatment;
- icon geometry;
- map density;
- panel density;
- typography hierarchy;
- texture policy;
- animation restraint;
- portrait style;
- report/document metaphors;
- and examples of unacceptable drift.

### Required variants

Create at least three tightly bounded alternatives:

1. Flat-vector isometric.
2. Pixel/isometric.
3. Low-poly rendered sprites.

Evaluate each against:

- readability;
- contributor accessibility;
- SVG compatibility;
- state-layering capability;
- animation feasibility;
- accessibility;
- asset-generation consistency;
- and maintenance burden.

### Decision rule

Flat-vector isometric should remain the default unless another prototype materially outperforms it on both strategic legibility and maintainability.

### Checklist

- [x] Three reference variants produced.
- [x] Evaluation criteria scored.
- [x] Preferred style selected.
- [x] Rejected styles documented with reasons.
- [x] Color-blind review completed.
- [x] Small-size rendering reviewed.
- [x] Large-text rendering reviewed.
- [x] Screenshot examples committed.
- [x] Art-direction ADR approved.

### Exit criteria

- The project has one enforceable visual direction.
- Contributors can identify visual inconsistency.
- The selected style works at realistic GUI sizes.

---

## Milestone 1.2: SVG rendering proof of concept

**Status:** Complete in v0.12.36
**Evidence:** `gui/scene.mjs`, `gui/svg-proof.html`, and
`tests/test_svg_scene.py`

### Scope

Create a non-authoritative prototype rendering:

- one regional board;
- three facilities;
- three institutional identities;
- one construction state;
- one staffing-pressure state;
- one uncertain observation;
- and one selected-facility interaction.

### Deliverables

- Semantic scene model.
- SVG renderer.
- Keyboard-selectable facility markers.
- Accessible labels.
- CSS-variable theming.
- Reduced-motion mode.
- Screenshot fixtures.
- Rendering performance benchmark.

### Recommended semantic model

```text
VisibleScene
  systems
  facilities
  relationships
  projects
  pressures
  observation overlays
  event markers
```

The scene model must consume only visible host data or static fixture data matching host DTOs.

### Checklist

- [x] Scene model defined.
- [x] SVG renderer implemented.
- [x] Facilities are selectable by keyboard.
- [x] Every meaningful graphic has a text equivalent.
- [x] System identity is not color-only.
- [x] Uncertainty has a distinct pattern or shape.
- [x] Unknown states render generic fallbacks.
- [x] No hidden-state field is consumed.
- [x] Static fixture produces deterministic SVG output.
- [x] Screenshot regression tests added.
- [x] Reduced-motion rendering tested.
- [x] Render time meets target.

### Exit criteria

- The SVG approach is technically viable.
- The scene is legible without animation.
- The renderer preserves simulation-authority boundaries.
- The selected-facility workflow is no less accessible than the current GUI.

---

## Milestone 1.3: Audio-direction prototype

**Status:** Complete in v0.12.38
**Evidence:** `gui/audio-direction.mjs`, `gui/audio-proof.html`,
`docs/design/visual-audio-audio-direction-board.md`, and
`tests/test_audio_direction.py` and the v0.12.38 policy extension

### Scope

Create a prototype containing:

- one refined UI confirmation cue;
- one rejection cue;
- one report-arrival cue;
- one institutional motif;
- one neutral ambient bed;
- one pressure layer;
- and one recorded or generated environmental loop.

### Deliverables

- Loudness and peak standards.
- Cue duration standards.
- Motif specification.
- Audio priority model.
- Ducking behavior.
- Looping standards.
- Text-equivalent policy.
- Prototype comparison with current oscillator cues.

### Checklist

- [x] Audio loudness target documented.
- [x] Peak ceiling documented.
- [x] Cue duration ranges documented.
- [x] Loop points are seamless.
- [x] UI cues remain distinguishable at low volume.
- [x] Environmental loop does not mask speech or reading.
- [x] Pressure music does not reveal hidden state.
- [x] Audio priority order implemented in prototype.
- [x] Repeat-cue cooldown tested.
- [x] Mute, cues-only, and full-audio modes tested.
- [x] Text equivalents remain available.
- [x] Reduced-audio preference tested.

### Exit criteria

- The hybrid audio approach is perceptibly better than oscillator-only ambience.
- Audio remains cognitively unobtrusive.
- Event meaning is not dependent on sound.
- No hidden information is communicated.

---

# Phase 2: Institutional Identity System

## Objective

Make recurring systems and actors immediately recognizable across the map, reports, panels, and soundscape.

## Milestone 2.1: Health-system identity kits

**Status:** Complete in v0.12.41
**Evidence:** `assets/source/visual/identity/riverside-kit.svg`,
`assets/release/visual/svg/riverside.svg`, `gui/identity-kits.mjs`,
`gui/identity-proof.html`, `tests/test_riverside_identity.py`,
`tests/test_northlake_identity.py`, `tests/test_summit_identity.py`, and
`tests/test_audio_direction.py`.

### Initial systems

- Riverside
- Northlake
- Summit

### Each identity kit should include

- logo mark;
- short text monogram;
- primary and secondary colors;
- monochrome variant;
- facility signage treatment;
- map marker;
- report-header treatment;
- compact badge;
- institutional motif;
- and generic fallback behavior.

### Design constraints

- Fictional.
- No resemblance to real health-system branding.
- Readable at 16–24 pixels.
- Distinguishable without color.
- Usable on light and dark backgrounds.
- Compatible with SVG and CSS variables.

### Checklist per system

#### Riverside

- [x] Logo mark completed.
- [x] Monochrome mark completed.
- [x] Compact marker completed.
- [x] Text monogram completed.
- [x] Palette passes contrast review.
- [x] Shape remains recognizable without color.
- [x] Facility signage variant completed.
- [x] Report-header variant completed.
- [x] Audio motif completed.
- [x] Registry entries completed.
- [x] Source files committed.
- [x] Release derivatives generated.
- [x] Cross-screen consistency tested.

#### Northlake

- [x] Logo mark completed.
- [x] Monochrome mark completed.
- [x] Compact marker completed.
- [x] Text monogram completed.
- [x] Palette passes contrast review.
- [x] Shape remains recognizable without color.
- [x] Facility signage variant completed.
- [x] Report-header variant completed.
- [x] Audio motif completed.
- [x] Registry entries completed.
- [x] Source files committed.
- [x] Release derivatives generated.
- [x] Cross-screen consistency tested.

#### Summit

- [x] Logo mark completed.
- [x] Monochrome mark completed.
- [x] Compact marker completed.
- [x] Text monogram completed.
- [x] Palette passes contrast review.
- [x] Shape remains recognizable without color.
- [x] Facility signage variant completed.
- [x] Report-header variant completed.
- [x] Audio motif completed.
- [x] Registry entries completed.
- [x] Source files committed.
- [x] Release derivatives generated.
- [x] Cross-screen consistency tested.

### Exit criteria

- Players can distinguish the three systems at a glance.
- Identity persists across map, report, facility, and event views.
- No identity depends on color alone.

---

## Milestone 2.2: Actor-family identity language

**Status:** Complete in v0.12.42
**Evidence:** `gui/actor-families.mjs`, `gui/actor-family-proof.html`, and
`tests/test_actor_families.py`.

### Actor families

- payer;
- regulator;
- labor;
- employer;
- community;
- board;
- policy coalition;
- independent provider.

### Deliverables

- Family icon.
- Family report frame.
- Family notification style.
- Optional sonic tag.
- Generic actor fallback.

### Checklist

- [x] Actor families finalized.
- [x] Icon set completed.
- [x] Notification frames completed.
- [x] Report-header treatments completed.
- [x] Generic fallback completed.
- [x] Semantic labels tested.
- [x] Color-independent recognition tested.
- [x] Registry coverage complete.
- [x] Unknown actor type handled safely.

### Exit criteria

- A player can distinguish the institutional source of a message before reading the full text.
- The actor-family system scales without creating a unique art package for every actor.

---

# Phase 3: Modular Facility and Regional Asset Kit

## Objective

Create the reusable graphical vocabulary needed to represent the regional market and facility-level consequences.

## Milestone 3.1: Facility component library

**Status:** Partial in v0.12.44; general hospital base and patient tower components complete
**Evidence:** `assets/source/visual/facilities/general-hospital-base.svg`,
`assets/release/visual/svg/general-hospital-base.svg`,
`gui/facility-components.mjs`, `gui/facility-proof.html`, and
`tests/test_general_hospital_base.py` plus
`tests/test_patient_tower.py`.

### Core modules

- general hospital base;
- patient tower;
- emergency department;
- ambulatory center;
- specialty center;
- rural clinic;
- administrative headquarters;
- parking structure;
- utility plant;
- research/education building;
- construction crane;
- undeveloped parcel.

### Optional later modules

- behavioral health;
- post-acute care;
- rehabilitation;
- imaging center;
- urgent care;
- physician office;
- logistics or supply facility.

### Layer model

Each facility should support:

1. Base structure.
2. System identity layer.
3. Capacity or service-line layer.
4. Project layer.
5. Operational-pressure layer.
6. Selection/focus layer.
7. Uncertainty or stale-observation layer.

### Checklist: General hospital base component

- [x] Source SVG completed.
- [x] Geometry uses shared grid.
- [x] ViewBox standardized.
- [x] System color variables supported.
- [x] Monochrome rendering tested.
- [x] Small-size rendering tested.
- [x] Pressure overlays tested.
- [x] Project overlays tested.
- [x] Accessibility label defined.
- [x] Registry entry complete.
- [x] No embedded external fonts.
- [x] SVG optimization verified.
- [x] Deterministic output hash recorded.

### Future component lanes

Emergency department, ambulatory center, specialty center, rural clinic,
administrative headquarters, parking structure, utility plant,
research/education building, construction crane, and undeveloped parcel remain
separate bounded component slices.

### Checklist: Patient tower component

- [x] Source SVG completed.
- [x] Geometry uses shared grid.
- [x] ViewBox standardized.
- [x] System color variables supported.
- [x] Monochrome rendering tested.
- [x] Small-size rendering tested.
- [x] Pressure overlays tested.
- [x] Project overlays tested.
- [x] Accessibility label defined.
- [x] Registry entry complete.
- [x] No embedded external fonts.
- [x] SVG optimization verified.
- [x] Deterministic output hash recorded.

### Exit criteria

- Facilities can be assembled from reusable components.
- Visual state changes do not require new one-off illustrations.
- Asset combinations remain visually coherent.

---

## Milestone 3.2: Regional map tile and environment kit

### Components

- road segments;
- intersections;
- population centers;
- river or water feature;
- commercial district;
- residential district;
- employer center;
- government district;
- undeveloped land;
- facility parcels;
- service-area overlay;
- relationship lines;
- uncertainty zones;
- event markers.

### Design rule

Geography must remain symbolic unless a scenario explicitly models geography. Spatial placement should organize relationships and strategic attention rather than imply unsupported real-world distances.

### Checklist

- [ ] Map grid specified.
- [ ] Road tile set completed.
- [ ] District tile set completed.
- [ ] Parcel system completed.
- [ ] Relationship-line styles completed.
- [ ] Service-area overlays completed.
- [ ] Uncertainty overlays completed.
- [ ] Event-marker set completed.
- [ ] Symbolic geography disclaimer documented.
- [ ] Layout works at target resolutions.
- [ ] Keyboard navigation order defined.
- [ ] Zoom behavior tested.
- [ ] Pan behavior tested if included.
- [ ] Registry complete.

### Exit criteria

- A scenario can render a coherent regional board without custom drawing.
- The board communicates institutional relationships without overstating geographic precision.
- Map interactions remain usable by keyboard and at large text scale.

---

## Milestone 3.3: Operational overlay library

### Required overlays

- staffing constraint;
- capacity constraint;
- demand pressure;
- active capital project;
- delayed project;
- project completion;
- payer/network change;
- regulatory review;
- community-trust concern;
- financial distress;
- operational recovery;
- uncertain or stale intelligence.

### Checklist per overlay

- [ ] Semantic role documented.
- [ ] Triggering visible field documented.
- [ ] Non-color representation implemented.
- [ ] Reduced-motion rendering defined.
- [ ] Text equivalent defined.
- [ ] Collision behavior tested.
- [ ] Multiple simultaneous overlays tested.
- [ ] Priority rule documented.
- [ ] Generic fallback exists.
- [ ] Registry complete.

### Exit criteria

- Major visible consequences have consistent graphical representations.
- Multiple pressures do not create unreadable visual clutter.
- Overlay priority is deterministic.

---

# Phase 4: Regional Strategy Board Integration

## Objective

Replace the current abstract map surface with the first production-quality strategic board.

## Milestone 4.1: Static regional board integration

### Deliverables

- Production scene adapter.
- SVG rendering integrated with existing GUI.
- Facility selection.
- Institutional focus.
- Visible overlay rendering.
- Report-to-map linking.
- Map legend.
- Static screenshot fixtures.

### Checklist

- [ ] Existing host DTOs mapped to scene data.
- [ ] No simulation-state changes required unless explicitly approved.
- [ ] Unknown IDs render generic assets.
- [ ] Selected detail and map remain synchronized.
- [ ] Status text remains visible.
- [ ] Source labels remain visible.
- [ ] Missingness remains explicit.
- [ ] Screen-reader order tested.
- [ ] Keyboard focus tested.
- [ ] Screenshot regression tests pass.
- [ ] Existing GUI tests pass.
- [ ] Static demo still functions.

### Exit criteria

- The regional board is usable in the first live competitive month.
- Existing accessibility and information-boundary guarantees are preserved.
- The graphical board materially improves system and facility recognition.

---

## Milestone 4.2: Visible consequence linkage

### Required interactions

- Selecting a report highlights the relevant facility or actor.
- Selecting a facility filters or emphasizes relevant reports.
- Completed projects visibly alter the facility.
- Observed rival expansions appear only when available to the player.
- Staffing and capacity pressure appear only from visible status.
- Month resolution updates the board and linked panels coherently.

### Checklist

- [ ] Report-to-entity links implemented.
- [ ] Entity-to-report links implemented.
- [ ] Project-state transitions render correctly.
- [ ] Rival observability delays respected.
- [ ] Unknown locations handled safely.
- [ ] Simultaneous updates use deterministic order.
- [ ] Focus state does not rely on animation.
- [ ] Historical state is not overwritten.
- [ ] Replay produces the same visual sequence.
- [ ] Integration tests cover first-month workflow.

### Exit criteria

- The board is not merely decorative.
- Players can trace major visible consequences across map and reports.
- Replay reproduces the same presentation state.

---

# Phase 5: Executive Desktop Visual Differentiation

## Objective

Reduce the uniform “card dashboard” appearance by giving major information classes distinct but restrained visual forms.

## Milestone 5.1: Semantic information containers

### Target containers

- board packet;
- operations ledger;
- intelligence report;
- regulatory letter;
- project sheet;
- news wire;
- executive action queue;
- after-action report.

### Design rules

- Differences should arise from structure, typography, iconography, and header treatment.
- Avoid fake paper textures unless extremely subtle.
- Do not reduce text density or accessibility.
- Maintain a shared grid and spacing system.

### Checklist per container

- [ ] Semantic purpose documented.
- [ ] Header treatment completed.
- [ ] Icon or marker completed.
- [ ] Compact and expanded variants completed.
- [ ] Accessibility semantics defined.
- [ ] Large-text layout tested.
- [ ] Narrow-width layout tested.
- [ ] Print or export behavior reviewed if applicable.
- [ ] Registry entry completed where assets are used.
- [ ] Existing source/status language retained.

### Exit criteria

- Players can distinguish observations, decisions, commitments, consequences, and retrospective explanations before reading full text.
- Visual differentiation does not fragment the interface.

---

## Milestone 5.2: Metric and trend visualization

### Scope

Introduce small, deterministic, actor-visible visualizations:

- sparklines;
- month-over-month deltas;
- capacity bars;
- staffing composition;
- project progress;
- payer-mix summaries;
- trust or legitimacy trend;
- visible uncertainty intervals where appropriate.

### Rules

- No chart should imply more precision than the model supplies.
- Missing or stale values must remain explicit.
- Exact values remain accessible.
- Animation must not be required to understand change.

### Checklist

- [ ] Metric visualization catalog defined.
- [ ] Data precision rules documented.
- [ ] Uncertainty rendering documented.
- [ ] Missingness rendering documented.
- [ ] Exact values available in text.
- [ ] Color-independent interpretation tested.
- [ ] Large-text behavior tested.
- [ ] Screenshot tests added.
- [ ] No hidden state consumed.

### Exit criteria

- Trends and constraints are easier to scan.
- Visualizations remain faithful to visible data and evidence limits.
- No chart introduces false precision.

---

# Phase 6: Consequence Animation and Temporal Presentation

## Objective

Use restrained motion to make the transition from decision to consequence easier to follow.

## Milestone 6.1: Motion specification

### Motion categories

- focus transition;
- report arrival;
- month transition;
- project progress;
- project completion;
- new visible rival action;
- status change;
- metric delta reveal;
- relationship-line change.

### Motion requirements

Each animation must define:

- semantic purpose;
- duration;
- easing;
- reduced-motion replacement;
- interruption behavior;
- replay behavior;
- and deterministic ordering.

### Checklist

- [ ] Motion catalog approved.
- [ ] Maximum simultaneous animations defined.
- [ ] Duration standards documented.
- [ ] Reduced-motion replacements documented.
- [ ] No animation blocks input unnecessarily.
- [ ] No motion reveals hidden information.
- [ ] Replay order deterministic.
- [ ] Animation interruption tested.
- [ ] Performance tested on baseline hardware.

### Exit criteria

- Motion improves causal comprehension.
- Reduced-motion mode retains all information.
- Month resolution does not become slower or more confusing.

---

## Milestone 6.2: First-month resolution sequence

### Recommended sequence

1. Player confirms action batch.
2. Actions move into a committed queue.
3. Host resolves the month.
4. Executive summary appears.
5. Critical visible consequences are presented first.
6. Map and facility states update.
7. Reports and observations arrive.
8. Metrics update.
9. Optional explanation or debrief links appear.
10. Control returns fully to the player.

### Checklist

- [ ] Sequence storyboard completed.
- [ ] Host/client state boundaries documented.
- [ ] Critical-event priority implemented.
- [ ] Map updates synchronized with reports.
- [ ] Metric changes synchronized with summary.
- [ ] Audio cues synchronized.
- [ ] Skip/advance control implemented.
- [ ] Reduced-motion sequence implemented.
- [ ] Replay sequence deterministic.
- [ ] No report is lost if animation is skipped.
- [ ] Keyboard-only completion tested.
- [ ] First-time user comprehension tested.

### Exit criteria

- A player can understand what changed during the month without manually comparing every panel.
- Skipping animation does not remove information.
- The sequence remains bounded and does not become cinematic overhead.

---

# Phase 7: Hybrid Audio Production

## Objective

Expand the current Web Audio system into a coherent, fatigue-resistant soundscape.

## Milestone 7.1: UI and event cue refinement

### Cue families

- selection;
- confirmation;
- rejection;
- add/remove action;
- submit;
- advance month;
- report received;
- save complete;
- project complete;
- staffing constraint;
- operating loss;
- operating recovery;
- payer decision;
- regulatory decision;
- rival expansion;
- affiliation milestone.

### Production path

Retain synthesis where appropriate, but improve:

- envelopes;
- filtering;
- harmonic balance;
- cue distinction;
- loudness consistency;
- and institutional motif integration.

### Checklist per cue

- [ ] Semantic purpose documented.
- [ ] Priority class assigned.
- [ ] Duration within standard.
- [ ] Loudness normalized.
- [ ] Peak ceiling respected.
- [ ] Cooldown behavior specified.
- [ ] Text equivalent exists.
- [ ] Cues-only mode tested.
- [ ] No ambiguity with another cue.
- [ ] Registry entry updated.
- [ ] Unit or integration test covers trigger.

### Exit criteria

- Important cues are distinguishable without being intrusive.
- Repeated action workflows do not cause fatigue.
- Cue triggers remain deterministic.

---

## Milestone 7.2: Environmental ambience library

### Initial ambience targets

- executive office;
- hospital lobby;
- hospital campus exterior;
- construction site;
- boardroom;
- press or policy event;
- regional city bed.

### Rules

- Environmental ambience should be subtle and optional.
- Clinical alarm sounds should be avoided.
- Sirens should be rare and distant.
- No sound should suggest unmodeled clinical severity.
- Loops should be long enough to avoid obvious repetition.

### Checklist per ambience asset

- [ ] Source or generation method documented.
- [ ] License approved.
- [ ] Source hash recorded.
- [ ] Release hash recorded.
- [ ] Noise floor reviewed.
- [ ] Loop points reviewed.
- [ ] Loudness normalized.
- [ ] No identifying speech included.
- [ ] No unintended copyrighted music included.
- [ ] No real institution names audible.
- [ ] Reduced-audio behavior tested.
- [ ] Registry entry approved.

### Exit criteria

- The world feels inhabited without becoming noisy.
- Ambience does not interfere with reading.
- All assets are legally distributable.

---

## Milestone 7.3: Adaptive music stem system

### Initial music states

- menu and planning;
- stable operations;
- pressure;
- regulatory scrutiny;
- competitive escalation;
- affiliation or negotiation;
- debrief.

### Recommended structure

```text
base pulse
+ institutional motif
+ visible pressure layer
+ policy layer
+ transition cadence
```

### State rules

- Inputs must come only from actor-visible state.
- Music identifies context and intensity, not moral valence.
- Multidimensional outcomes should not be reduced to simple victory/failure harmony.
- State transitions should use bounded crossfades.
- Music should be optional and independently adjustable.

### Checklist

- [ ] Music-state catalog approved.
- [ ] Visible-state trigger rules documented.
- [ ] Hidden-state leak review completed.
- [ ] Stem loop points verified.
- [ ] Crossfade durations defined.
- [ ] Institutional motifs integrated.
- [ ] Pressure escalation bounded.
- [ ] Debrief transition completed.
- [ ] Music-only mute control tested.
- [ ] Full mute tested.
- [ ] Registry complete.
- [ ] Replay produces same music-state sequence.

### Exit criteria

- Music responds coherently to the visible strategic situation.
- Music never reveals hidden state.
- The system remains unobtrusive during long reading periods.

---

## Milestone 7.4: Audio priority and fatigue manager

### Priority order

1. Critical visible consequence.
2. Major institutional decision.
3. Strategic milestone.
4. Report arrival.
5. Routine UI feedback.
6. Ambient detail.

### Required behaviors

- At most one critical cue per resolution batch.
- Minor reports may be aggregated into one cue.
- Repeated cues use cooldowns.
- Ambience ducks under major cues.
- Music ducks under critical cues.
- No uncontrolled cue stacking.
- User preferences persist locally.

### Checklist

- [ ] Priority queue implemented.
- [ ] Cooldowns implemented.
- [ ] Duplicate suppression implemented.
- [ ] Ducking implemented.
- [ ] Batch aggregation implemented.
- [ ] Maximum simultaneous voices defined.
- [ ] Preference persistence tested.
- [ ] Rapid-input stress test completed.
- [ ] Month-resolution stress test completed.
- [ ] Screen-reader and audio coexistence reviewed.

### Exit criteria

- Dense month resolutions remain understandable.
- The audio layer does not become fatiguing.
- Important cues are not masked by lower-priority sounds.

---

# Phase 8: AI-Generated Asset Pipeline

## Objective

Use local AI generation selectively for assets that benefit from custom identity while preserving consistency, provenance, and legal clarity.

## Milestone 8.1: Approved local generation workflow

### Recommended uses

- fictional executive portraits;
- concept exploration;
- report illustrations;
- event thumbnails;
- subtle textures;
- environmental source images;
- audio source material or sketches where model terms permit.

### Generally unsuitable uses

- core icons;
- precision map tiles;
- stateful facility modules;
- small UI glyphs;
- assets requiring exact geometry;
- anything that must vary deterministically from simulation parameters.

### Required metadata

- model name;
- model version or hash;
- model license;
- generation application;
- prompt;
- negative prompt;
- seed;
- sampler or generation settings;
- dimensions;
- generation date;
- contributor;
- post-processing history;
- source image references;
- source and release hashes.

### Checklist

- [ ] Approved local models listed.
- [ ] Model licenses reviewed.
- [ ] Prompt template established.
- [ ] Metadata capture automated.
- [ ] Seed capture automated.
- [ ] Source outputs preserved.
- [ ] Post-processing steps documented.
- [ ] Human review checklist implemented.
- [ ] Real-person resemblance review included.
- [ ] Logo and trademark review included.
- [ ] Clinical plausibility review included.
- [ ] Registry integration complete.

### Exit criteria

- AI-generated assets are reproducible enough for audit.
- Contributors can identify how each asset was created.
- No generated asset enters release without human review.

---

## Milestone 8.2: Fictional actor portrait set

### Initial portrait roles

- rival system executive;
- payer negotiator;
- regulator;
- labor representative;
- community leader;
- board chair;
- affiliation partner executive.

### Style

- editorial illustration;
- chest-up composition;
- consistent crop;
- neutral or institutional background;
- no public-figure resemblance;
- no photorealistic dependency;
- diverse but plausible fictional cast.

### Checklist per portrait

- [ ] Role defined.
- [ ] Prompt and seed recorded.
- [ ] Source image preserved.
- [ ] Crop and release derivative completed.
- [ ] Identity consistency reviewed.
- [ ] Real-person resemblance reviewed.
- [ ] Anatomy and artifact review completed.
- [ ] No protected marks present.
- [ ] Alt text written.
- [ ] Registry entry approved.
- [ ] Small-size rendering tested.
- [ ] Grayscale rendering tested.

### Exit criteria

- Portraits strengthen actor recognition without implying real persons.
- The set is stylistically coherent.
- The interface remains functional with portraits disabled.

---

# Phase 9: Licensing, Attribution, and Release Hardening

## Objective

Ensure that all visual and audio assets are safe for long-term open-source distribution and possible future educational or commercial packaging.

## Milestone 9.1: Asset license policy enforcement

### Allowed by default

- project-authored;
- CC0;
- CC BY 4.0;
- explicitly reviewed compatible GPL assets;
- locally generated assets from approved models and workflows.

### Rejected by default

- CC BY-NC;
- CC BY-ND;
- personal-use-only;
- unclear or missing license;
- preview images;
- assets copied from game screenshots;
- assets from Pinterest or unattributed aggregators;
- assets whose model or service terms are unclear;
- assets closely imitating protected game artwork.

### Checklist

- [ ] License allowlist encoded in validation.
- [ ] License denylist encoded in validation.
- [ ] Attribution text generated.
- [ ] Source URLs archived where practical.
- [ ] Retrieval dates present.
- [ ] Original licenses saved or referenced.
- [ ] Modification descriptions present.
- [ ] Approval status required.
- [ ] Third-party notices generated.
- [ ] Release package includes credits.
- [ ] In-game credits accessible.
- [ ] License audit completed before release.

### Exit criteria

- Every distributed asset has a clear legal basis.
- Future packaging is not blocked by noncommercial restrictions.
- Credits can be regenerated from registry data.

---

## Milestone 9.2: Asset security and integrity review

### Deliverables

- SVG sanitization.
- Metadata stripping where appropriate.
- Audio file validation.
- Decompression-bomb safeguards.
- Hash verification.
- Build reproducibility check.

### Checklist

- [ ] SVG scripts and external references rejected.
- [ ] Embedded raster images reviewed.
- [ ] External fonts rejected.
- [ ] Unexpected metadata stripped.
- [ ] Audio codec validation implemented.
- [ ] File-size limits enforced.
- [ ] Dimension limits enforced.
- [ ] Hashes verified in CI.
- [ ] Release build reproducibility checked.
- [ ] Asset loading failures degrade gracefully.

### Exit criteria

- Untrusted asset content cannot execute code.
- Corrupt or missing assets do not break the simulation.
- Release assets match approved hashes.

---

# Phase 10: Integrated Vertical Slice

## Objective

Deliver one polished, end-to-end visual/audio slice that demonstrates the complete recommended direction.

## Required slice

The slice should cover the first month of `competitive-regional-v1` and include:

- illustrated regional board;
- three health-system identities;
- at least three facility campuses;
- facility selection;
- action queue;
- one project state;
- one staffing or capacity pressure;
- one rival observation;
- one payer or policy event;
- month-resolution presentation;
- hybrid ambience;
- refined UI cues;
- one adaptive music transition;
- replay-consistent presentation;
- and end-of-month explanation.

## Milestone 10.1: Feature-complete slice

### Checklist

#### Regional board

- [ ] Three systems visible.
- [ ] Facilities visually distinct.
- [ ] Institutional identity consistent.
- [ ] Facility selection works.
- [ ] Uncertainty rendering works.
- [ ] Project overlay works.
- [ ] Pressure overlay works.
- [ ] Rival observation timing respected.

#### Executive desktop

- [ ] Briefing uses semantic container.
- [ ] Action queue uses semantic container.
- [ ] Reports use actor-family identities.
- [ ] Metrics use appropriate visualizations.
- [ ] Source and status labels remain visible.

#### Resolution

- [ ] Month sequence implemented.
- [ ] Critical event prioritization works.
- [ ] Map and reports update coherently.
- [ ] Skip behavior works.
- [ ] Reduced-motion behavior works.
- [ ] Replay is deterministic.

#### Audio

- [ ] UI cues refined.
- [ ] Environmental ambience available.
- [ ] Adaptive music transition works.
- [ ] Priority and cooldown manager works.
- [ ] Full mute works.
- [ ] Cues-only mode works.
- [ ] Text equivalents remain available.

#### Provenance

- [ ] Every asset registered.
- [ ] Every asset hashed.
- [ ] Every license approved.
- [ ] Credits generated.
- [ ] AI metadata complete where applicable.

### Exit criteria

- A new player can complete the first month without developer intervention.
- The player can identify the three systems and major facilities without repeatedly rereading labels.
- The player can explain the major visible consequence chain.
- The slice feels like a strategy game rather than a generic dashboard.
- No architectural, accessibility, replay, or provenance regression is introduced.

---

## Milestone 10.2: Structured evaluation

### Participants

- project owner and contributors;
- strategy-game players;
- health-policy or management experts;
- accessibility-oriented reviewers;
- first-time users.

### Evaluation dimensions

- institutional recognition;
- facility recognition;
- map legibility;
- consequence comprehension;
- information density;
- cognitive load;
- animation usefulness;
- audio usefulness;
- audio fatigue;
- perceived game identity;
- accessibility;
- and trust in information boundaries.

### Checklist

- [ ] Test protocol written.
- [ ] First-session tasks defined.
- [ ] Recognition tasks defined.
- [ ] Consequence-tracing tasks defined.
- [ ] Accessibility tasks defined.
- [ ] Audio preference feedback collected.
- [ ] Quantitative ratings collected.
- [ ] Qualitative interviews completed.
- [ ] Findings classified as defect, preference, or scope expansion.
- [ ] Revision log created.
- [ ] Go/no-go decision recorded.

### Exit criteria

- Most first-time users can correctly identify systems, facilities, and major event sources.
- Users can reconstruct the first-month consequence chain.
- Audio is helpful or neutral for most users and fully optional for others.
- No severe accessibility or information-leak issue remains.

---

# Phase 11: Production Expansion

## Objective

Extend the validated asset and interaction language to the remainder of the competitive campaign.

## Milestone 11.1: Complete competitive campaign coverage

### Scope

- all facility types used in the campaign;
- all major project categories;
- all major pressure categories;
- all recurring actor families;
- all critical month-resolution events;
- debrief and history views;
- save/load continuity;
- and full campaign audio-state coverage.

### Checklist

- [ ] Facility asset coverage complete.
- [ ] Overlay coverage complete.
- [ ] Actor-family coverage complete.
- [ ] Event cue coverage complete.
- [ ] Music-state coverage complete.
- [ ] History view updated.
- [ ] Debrief view updated.
- [ ] Save/load visual continuity tested.
- [ ] Replay visual continuity tested.
- [ ] Unknown content fallbacks tested.
- [ ] Asset registry coverage is 100%.
- [ ] Full campaign screenshot suite passes.

### Exit criteria

- No core competitive-campaign entity falls back to an unintended generic representation.
- Full runs remain visually and sonically coherent.
- Asset loading and rendering remain performant.

---

## Milestone 11.2: Performance and packaging hardening

### Targets to define

- initial GUI load size;
- asset cache size;
- SVG render time;
- month-resolution update time;
- audio decode time;
- memory use;
- and offline availability.

### Checklist

- [ ] Asset size budget defined.
- [ ] SVG optimization enabled.
- [ ] Raster derivatives appropriately sized.
- [ ] Audio compression reviewed.
- [ ] Lazy loading implemented where useful.
- [ ] Preloading limited to high-value assets.
- [ ] Offline operation verified.
- [ ] Missing-asset fallback tested.
- [ ] Low-power device test completed.
- [ ] Browser compatibility matrix completed.

### Exit criteria

- Asset richness does not materially degrade the first-session experience.
- The game remains usable offline from a normal checkout.
- The dependency-free client remains maintainable unless a future ADR explicitly changes that decision.

---

# Phase 12: Additional Campaigns and Educational Surfaces

## Objective

Extend the validated visual/audio language without redesigning the core asset system.

## Milestone 12.1: Stabilization campaign

### Checklist

- [ ] Campaign-specific map or facility needs identified.
- [ ] Reusable assets used where possible.
- [ ] New pressure states registered.
- [ ] Tutorial presentation updated.
- [ ] Audio-state mapping completed.
- [ ] Debrief presentation completed.
- [ ] Accessibility tests pass.
- [ ] Provenance audit passes.

### Exit criteria

- Stabilization mode gains graphical clarity without duplicating the competitive asset library.

---

## Milestone 12.2: Regional affiliation campaign

### Checklist

- [ ] Partner identity treatment completed.
- [ ] Negotiation-stage visualization completed.
- [ ] Commitment and review states completed.
- [ ] Integration-state visualization completed.
- [ ] Affiliation audio motif completed.
- [ ] Stage-transition sequence completed.
- [ ] Replay and debrief views updated.
- [ ] Provenance audit passes.

### Exit criteria

- The six-stage affiliation process is visually distinct and causally legible.
- Partnership uncertainty and commitment states remain explicit.

---

## Milestone 12.3: Instructor and debrief visualization

### Scope

- visible-versus-true-state comparison;
- decision timeline;
- causal graph;
- actor rationale view;
- counterfactual comparison;
- strategy comparison;
- and distributional outcome summaries.

### Checklist

- [ ] Instructor-only authority boundaries documented.
- [ ] True-state visual language distinct from player-visible state.
- [ ] Decision-time information recoverable.
- [ ] Causal attribution visualized.
- [ ] Counterfactual differences visualized.
- [ ] Distributional outcomes represented responsibly.
- [ ] Export behavior documented.
- [ ] Educational usability reviewed.

### Exit criteria

- Visual enhancements support debriefing rather than only play.
- Decision quality remains distinguishable from realized outcome quality.

---

# Phase 13: Public Release Readiness

## Objective

Prepare a stable visual/audio release suitable for public use, contributor review, and educational pilots.

## Milestone 13.1: Release candidate audit

### Product checklist

- [ ] First-session workflow complete.
- [ ] Competitive campaign coverage complete.
- [ ] Settings documented.
- [ ] Audio controls documented.
- [ ] Reduced-motion mode documented.
- [ ] Text scaling documented.
- [ ] Credits accessible.
- [ ] Troubleshooting updated.

### Technical checklist

- [ ] Rust tests pass.
- [ ] GUI tests pass.
- [ ] Screenshot tests pass.
- [ ] Asset validation passes.
- [ ] License validation passes.
- [ ] Hash validation passes.
- [ ] Accessibility checks pass.
- [ ] Offline operation passes.
- [ ] Replay verification passes.
- [ ] Save/load verification passes.
- [ ] Browser compatibility passes.

### Content checklist

- [ ] No real institution accidentally represented.
- [ ] No public-figure resemblance remains.
- [ ] No unsupported clinical implication introduced.
- [ ] No hidden-state leak found.
- [ ] Attribution complete.
- [ ] AI-generation metadata complete.
- [ ] Limitations statement updated.

### Exit criteria

- No critical or high-severity defect remains.
- The release package is reproducible.
- All distributed assets have approved provenance.
- A new user can install, launch, play, and understand the graphical mode from documentation.

---

## Milestone 13.2: Educational pilot readiness

### Checklist

- [ ] Pilot facilitator guide updated.
- [ ] Audio guidance for classrooms included.
- [ ] Low-distraction mode available.
- [ ] Screenshot and recording permissions clarified.
- [ ] Debrief visuals reviewed.
- [ ] Classroom hardware assumptions documented.
- [ ] Accessibility accommodation guidance documented.
- [ ] Feedback instrument prepared.

### Exit criteria

- The graphical/audio release can be used in a bounded educational pilot.
- Facilitators can disable or simplify presentation features as needed.
- Pilot feedback can distinguish gameplay, visual, audio, and educational issues.

---

# 4. Cross-Phase Bookkeeping

## 4.1 Milestone status template

Use the following for each milestone:

```markdown
### Milestone X.Y: Name

**Status:** Not started | In progress | Blocked | In review | Complete  
**Owner:**  
**Target release:**  
**Depends on:**  
**Started:**  
**Completed:**  

#### Deliverables

- [ ] ...

#### Verification

- [ ] Automated tests
- [ ] Manual review
- [ ] Accessibility review
- [ ] Provenance review
- [ ] Documentation update

#### Open issues

- ...

#### Exit decision

- [ ] Exit criteria met
- [ ] Deferred items recorded
- [ ] Follow-up issues created
```

---

## 4.2 Asset review checklist

Apply to every visual or audio asset:

### Identity

- [ ] Stable unique asset ID.
- [ ] Semantic role assigned.
- [ ] Owning system or actor identified if applicable.
- [ ] Source and release paths recorded.

### Provenance

- [ ] Creator recorded.
- [ ] Creation method recorded.
- [ ] Source URL recorded if external.
- [ ] Retrieval or creation date recorded.
- [ ] License recorded.
- [ ] License URL recorded.
- [ ] Attribution text recorded.
- [ ] Modifications recorded.
- [ ] Original hash recorded.
- [ ] Release hash recorded.

### AI-specific

- [ ] Model recorded.
- [ ] Model version or hash recorded.
- [ ] Model license recorded.
- [ ] Prompt recorded.
- [ ] Negative prompt recorded.
- [ ] Seed recorded.
- [ ] Generation settings recorded.
- [ ] Human review completed.

### Design

- [ ] Matches approved art/audio direction.
- [ ] Works at target size or loudness.
- [ ] Does not resemble protected source material.
- [ ] Does not resemble a real institution or person unintentionally.
- [ ] Has generic fallback where needed.

### Accessibility

- [ ] Text or visual equivalent exists.
- [ ] Meaning does not depend only on color.
- [ ] Reduced-motion behavior exists if animated.
- [ ] Reduced-audio or mute behavior exists if auditory.
- [ ] Contrast or audibility checked.

### Technical

- [ ] Optimized release derivative built.
- [ ] Asset validates.
- [ ] No unsafe SVG content.
- [ ] No unexpected embedded metadata.
- [ ] Loading failure degrades gracefully.
- [ ] Automated test or fixture added where appropriate.

### Approval

- [ ] Domain review complete where relevant.
- [ ] Design review complete.
- [ ] License review complete.
- [ ] Accessibility review complete.
- [ ] Approval status set to approved.

---

## 4.3 Pull-request checklist for visual/audio work

- [ ] Scope is presentation-only unless architecture change is explicitly documented.
- [ ] Simulation authority remains with the host.
- [ ] Only actor-visible data are consumed.
- [ ] Unknown values have safe fallbacks.
- [ ] New assets are registered.
- [ ] Hashes are updated.
- [ ] Credits are regenerated.
- [ ] License policy passes.
- [ ] Accessibility equivalents are included.
- [ ] Reduced-motion or reduced-audio behavior is included.
- [ ] Screenshot tests are updated.
- [ ] Audio trigger tests are updated where applicable.
- [ ] Documentation is updated.
- [ ] Release notes describe user-visible changes.
- [ ] No asset is copied from Capitalism 2 or another proprietary game.

---

# 5. Recommended Milestone Sequence

The recommended execution order is:

1. **Phase 0:** governance and asset pipeline.
2. **Phase 1:** art and audio prototypes.
3. **Phase 2:** institutional identity.
4. **Phase 3:** modular facility and map kit.
5. **Phase 4:** regional board integration.
6. **Phase 5:** executive desktop differentiation.
7. **Phase 6:** consequence animation.
8. **Phase 7:** hybrid audio production.
9. **Phase 8:** selective AI-generated assets.
10. **Phase 9:** licensing and release hardening.
11. **Phase 10:** integrated first-month vertical slice.
12. **Phase 11:** full competitive-campaign expansion.
13. **Phase 12:** additional campaigns and educational views.
14. **Phase 13:** public release and pilot readiness.

Some work can overlap, but the following dependencies should remain strict:

```text
asset governance
  -> art-direction decision
  -> modular asset kit
  -> regional board integration
  -> consequence animation
  -> full production expansion
```

```text
audio specification
  -> cue refinement
  -> ambience and music stems
  -> priority manager
  -> integrated resolution sequence
```

```text
AI-generation policy
  -> approved local workflow
  -> portrait or illustration generation
  -> provenance and human review
  -> release approval
```

---

# 6. Definition of the First Major Release

The visual/audio enhancement program should be considered successful when the following conditions are met:

## Product

- The GUI presents a coherent illustrated regional health-market environment.
- Riverside, Northlake, and Summit are immediately recognizable.
- Facilities visibly reflect projects and observed pressures.
- Major month-to-month consequences are easy to follow.
- The interface feels like a strategy simulation rather than a generic dashboard.

## Architecture

- The host remains authoritative.
- The browser remains presentation-only.
- Replay reproduces the same visible sequence.
- No hidden state is exposed through visuals, animation, or sound.
- Missing and uncertain information remain explicit.

## Accessibility

- Keyboard navigation remains complete.
- Color is not the sole information channel.
- Reduced-motion mode is complete.
- Audio is optional.
- Meaningful audio has text or visual equivalents.
- Supported text scaling remains usable.

## Asset governance

- Every asset is registered.
- Every asset has an approved license or generation basis.
- Every asset has source and release hashes.
- Attribution is generated automatically.
- AI-generated assets include model, prompt, seed, and review metadata.
- No proprietary Capitalism 2 assets are included or closely reproduced.

## Evaluation

- First-time users can identify institutions and facilities.
- Users can trace the main first-month consequence chain.
- Visual and audio features improve comprehension or atmosphere without increasing confusion.
- No severe fatigue, accessibility, or trust problem remains.

---

# 7. Immediate Next Actions

## Foundation sprint

- [x] Write and approve the visual/audio product brief.
- [x] Add the asset directory structure.
- [x] Define visual and audio registry schemas.
- [x] Add CI validation for registry completeness and hashes.
- [x] Write the asset licensing policy.
- [x] Write the local AI-generation policy.
- [x] Create the art-direction comparison board.
- [x] Create the SVG regional-board proof of concept.
- [x] Create the hybrid audio proof of concept.
- [x] Record an ADR selecting the production visual and audio direction.

## First production sprint

- [x] Create Riverside identity kit.
- [x] Create Northlake identity kit.
- [x] Create Summit identity kit.
- [x] Create the general-hospital base module.
- [ ] Create the emergency department module.
- [ ] Create the ambulatory-center module.
- [ ] Create construction and staffing overlays.
- [ ] Integrate one static regional board fixture.
- [ ] Add screenshot regression tests.
- [x] Refine the first five audio cues.
- [x] Add one environmental loop.
- [x] Implement the initial audio priority manager.

## Vertical-slice sprint

- [ ] Integrate the board with live competitive-session data.
- [ ] Link facilities and reports.
- [ ] Implement visible project progression.
- [ ] Implement first-month consequence presentation.
- [ ] Add adaptive planning and pressure music states.
- [ ] Complete asset provenance review.
- [ ] Run structured first-time-user evaluation.
- [ ] Record revision decisions.
- [ ] Approve or reject expansion to full campaign coverage.

---

## 8. Final Program Rule

> A visual or audio feature should enter production only when it makes a strategic relationship, information boundary, institutional identity, or consequence easier to perceive.

The project should not pursue graphical richness as an independent goal. Its strongest path is to make the simulated health-policy system more spatial, more institutional, and more causally legible while retaining the deterministic, transparent, and educational character that already defines the project.
