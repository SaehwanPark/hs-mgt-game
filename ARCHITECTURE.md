# Architecture

The project is currently a playable CLI prototype with bounded stabilization,
competitive, and opt-in regional-affiliation campaign modes. This document
records the intended architecture boundaries that future implementation should
preserve.

## Current State

- Language: Rust
- Interface: command-line first
- Package: single Rust package, `hs-mgt-game`, with `src/lib.rs` module tree
- Executable: thin `src/main.rs` entry calling `cli::run()`
- MCP executable: `src/bin/hs-mgt-game-mcp.rs` serving a local stdio MCP server
  for bounded autonomous-agent play
- GUI executable: `src/bin/hs-mgt-game-gui.rs` serving the dependency-free
  browser client and a loopback-only API over an in-memory session store
- Library modules:
  - `model/` — typed world state, commands, competitive and affiliation state,
    resources, history, session types, campaign types
  - `affiliation/` — six-stage partner interaction genesis, observation,
    validation, deterministic transition, and replay
  - `competitive/` — competitive campaign mock fixtures and validation demos
  - `inputs/` — seeded stochastic input resolution
  - `sim/` — deterministic transition core
  - `actors/` — non-player actor decisions
  - `replay/` — replay verification and state hashing
  - `artifact/` — replay artifact serialize/deserialize/verify
  - `debrief/` — educational debrief generation
  - `cli/` — terminal I/O, parsers, session loop, display
  - `mcp/` — MCP session store, tool DTOs, and stdio server adapter
  - `gui_server.rs` — embedded static assets and same-origin HTTP adapter over
    the existing session store
- Canonical design docs: `README.md` and `docs/`

Last Reviewed: 2026-07-15
Status: Verified

The current implementation includes a competitive campaign path with genesis
multi-system state, action-economy validation, simultaneous monthly batch
resolution (`sim/resolve.rs`), `transition_competitive()`, bounded AI player batches
(`actors/ai_player.rs`, `sim/observe_ai.rs`), and observation-only rival intel with
1-month lag (`sim/observe_competitive.rs`), monthly event/delay ticks, annual
policy inputs, Stata-like competitive command parsing, and a 24-month
competitive CLI loop with help-command catalog output, colored command prompt
tokens, and Tab autocomplete for verbs, argument keys, and enum values.
It also includes a local stdio MCP server (`hs-mgt-game-mcp`) with in-memory
sessions for `stabilization-v1`, `competitive-regional-v1`, and
`regional-affiliation-v1`.

The current implementation is a playable prototype and compact architecture
proof, not a production simulation or calibrated policy model. It demonstrates a
pure transition function in `sim/transition.rs`, explicit resolved inputs from
`inputs/resolve.rs`, actor-specific observation and decisions, attributed
effects, append-only history, stable per-transition state hashes in
`replay/hash.rs`, replay verification, deterministic educational debrief in
`debrief/report.rs`, optional replay artifact export in `artifact/`, and CLI
play modes in `cli/session.rs`.

## Intended System Shape

The simulation should grow around a deterministic core transition model:

```text
previous state + actions + resolved external inputs + versioned ruleset
  -> events + attributed effects + next state
```

The core should not read randomness, wall-clock time, filesystem state, network
state, terminal input, or global mutable state during transition evaluation.

## Boundaries

### Core Simulation

Responsible for:

- typed world state
- actor actions
- ruleset evaluation
- deterministic state transitions
- emitted events and attributed effects
- immutable snapshots and append-only history records

The core should be testable without terminal I/O.

Current proof location: `sim/transition.rs` and `sim/validate.rs`. Each committed
transition records a stable 64-bit FNV-1a state hash over a canonical, labeled
state record in `replay/hash.rs`. This is a deterministic replay check, not a
cryptographic integrity guarantee.

Last Reviewed: 2026-06-23
Status: Verified

### Stochastic Input Resolution

Responsible for:

- seeded exogenous events
- measurement noise
- delayed or missing observations
- bounded-rationality draws where needed

Random draws should become explicit inputs before the deterministic transition
core is evaluated.

Current proof: `ResolvedInputs` are derived in `inputs/resolve.rs` from a run
seed, turn index, prior state, and named streams for measurement noise, delayed
access reporting, labor pressure, policy signal values, coalition leverage,
prior-period access measurement revisions, and competitor market signal.

Last Reviewed: 2026-06-24
Status: Verified

### Actor Information

The architecture must distinguish:

- true state
- actor-specific beliefs
- observations and public reports
- later corrections or revised estimates

Players and non-player actors should make decisions from available information,
not omniscient state.

Current proof: the player observation uses reported access and quality; later
turns may include prior-period access measurement revisions in the briefing
without rewriting committed history. The commercial insurer, state-policy,
coalition, workforce, and competitor decisions use actor-visible values and
record rationales. The educational debrief reports those rationales from
committed history rather than recomputing hidden actor knowledge.

Last Reviewed: 2026-06-24
Status: Verified

### Interface

The initial player interface is a CLI. Terminal rendering, input parsing,
display formatting, MCP protocol handling, and any future GUI rendering should
remain outside the deterministic simulation core.

Current proof: `cargo run` invokes `cli::run()` for a starting executive
dashboard and strategy commitment previews, play-mode and seed selection,
per-turn interactive command entry or preset strategy paths, executive
briefings, turn-resolution summaries, replay, debrief, and optional replay
artifact export.

`cargo run --bin hs-mgt-game-mcp` invokes a local stdio MCP server that exposes
tools for starting a bounded session, reading actor-visible observations,
submitting one turn/month of commands, inspecting committed transition
summaries, and ending a session. The MCP layer reuses existing parsers,
observation helpers, validation, and transition functions; it does not read
randomness or mutate the core directly.

The `gui/` proof renders an injected session envelope or the typed
`competitive-read-only-v1` projection through
`window.HsMgtGameReadOnlyAdapter`. When a
`window.HsMgtGameActionAdapter` is supplied, the Phase 3/4 page renders a host
catalogue, keeps draft rows locally, validates canonical batches through the
host, calls `submitTurn` only for an unchanged valid batch, and reads the typed
`competitive-resolution-v1` envelope through `getResolution` after a commit.
Phase 13 adds a local text-first rail over the existing launch, inspection,
draft, validation, submission, resolution, and refreshed-presentation handoffs.
The included demo envelope is a display fixture, not a browser-owned
simulation.

`cargo run --bin hs-mgt-game-gui` binds only to a loopback address, embeds the
same browser files, and injects `host-adapter.mjs` into the served index. The
adapter maps same-origin `/api/v1/sessions` requests to the existing
`GameSessionStore` operations for competitive start, presentation, action
catalog, validation, submission, resolution, and regional-world reads. The
store remains in memory for the lifetime of the process. Static/direct serving
does not inject the adapter and remains fixture or external-adapter mode.

Last Reviewed: 2026-07-15
Status: Verified

Future GUI work should be a thin client over the same scenario, observation,
command-validation, history, replay, and debrief surfaces used by CLI and MCP.
It must not introduce a second simulation state model, hidden randomness,
network-dependent core behavior, or GUI-only transition semantics. Asset loading
and license attribution belong at the interface/distribution boundary, not in
the core engine.

### Presentation Asset Repository

Visual and audio source, generated, release, and registry files live under
`assets/` at the presentation/distribution boundary. The dependency-free
`scripts/validate_assets.py` gate owns manifest completeness, semantic-role and
license policy, approval, source/release hashes, and release-file coverage.
`scripts/generate_asset_credits.py` derives attribution from the registries.
These tools do not read or mutate simulation state; asset paths, licenses,
playback rules, and accessibility metadata must never enter deterministic
transitions, state hashes, replay artifacts, or debriefs.

The v0.12.35 art-direction record selects a flat institutional SVG vocabulary
for the next rendering proof. Its schematic relationship layouts are design
references, not true geography; rejected terrain and dashboard variants remain
comparison evidence and are not runtime semantics.

The v0.12.36 SVG proof lives in `gui/scene.mjs` and `gui/svg-proof.html` as a
fixture-only renderer. It accepts visible scene fields, normalizes unknown
values to explicit fallbacks, and owns only local selection/reduced-motion
presentation state. It is not imported by the live host path and cannot submit
commands or alter simulation/replay state.

The v0.12.37 audio direction proof lives in `gui/audio-direction.mjs` and
`gui/audio-proof.html` as a fixture-only generated Web Audio vocabulary. It
records visible sources, text equivalents, bounded loudness/peak/duration/loop
targets, and unsupported-audio fallback behavior. It is not imported by the
live audio client and cannot read hidden state, create host/session state, or
alter commands, transitions, history, hashes, replay, or debrief output.

The v0.12.38 extension keeps the policy local to that fixture proof. Its
priority, -8 dB music-ducking, cooldown, mode, and reduced-audio decisions use
only declared cue metadata and local controls. They are not host settings,
simulation transitions, history, hashes, replay artifacts, or debrief facts.

The v0.12.39 Riverside identity kit lives in the source/release asset boundary
and `gui/identity-kits.mjs`/`gui/identity-proof.html`. It provides fictional
surface variants and a generic fallback without being imported by the live GUI;
the asset registry owns provenance and the identity module owns only local
fixture labels, not host identity facts.

The v0.12.40 Northlake kit extends the same fixture-only contract with a
separate fictional vocabulary and source/release pair. Its identity and audio
motif references remain local labels; they do not infer rival state, alter
observability, or enter host/session, simulation, history, replay, or debrief
contracts.

The v0.12.41 Summit kit completes the three-system fixture vocabulary with a
third distinct source/release pair and motif reference. The shared proof remains
local presentation state; no identity token becomes a host fact or live
simulation signal through this asset slice.

The v0.12.42 actor-family language catalog extends the same fixture-only
boundary to payer, regulator, labor, employer, community, board, policy
coalition, and independent-provider IDs. Its glyphs, frame patterns,
notification styles, optional identity-sonic tags, written equivalents, and
generic fallback are local presentation vocabulary; they consume no private
actor state and are not imported by the live GUI.

The v0.12.43 general-hospital base component adds a registry-backed source and
release SVG pair plus a fixture layer catalog for base, identity, capacity,
project, pressure, selection, and uncertainty presentation. Layer sources are
visible fields or local focus state; the component does not create facility
facts, infer hidden status, or enter live board rendering.

The v0.12.44 patient-tower component reuses that layer contract with a distinct
vertical silhouette and shared selector proof. Its type cue is a presentation
label only; it does not assert bed count, service capacity, ownership, or any
other unobserved facility fact.

The v0.12.45 emergency-department component reuses the same contract with a
distinct entrance-wing silhouette and explicit type-only description. Its ED
marker does not imply service performance, acuity, staffing, or hidden outcome.

The v0.12.46 ambulatory-center component reuses the same contract with a
distinct low-rise arc silhouette and explicit type-only description. Its shape
does not imply throughput, service quality, ownership, or hidden outcome.

The v0.12.47 specialty-center component reuses the same contract with a
distinct peaked-canopy silhouette and explicit type-only description. Its shape
does not imply clinical scope, capacity, ownership, or hidden outcome.

The v0.12.48 rural-clinic component reuses the same contract with a distinct
compact pitched-roof silhouette and explicit type-only description. Its shape
does not imply geographic access, quality, ownership, or hidden outcome.

The v0.12.49 administrative-headquarters component reuses the same contract
with a distinct stepped office silhouette and explicit type-only description.
Its shape does not imply authority, performance, ownership, or hidden outcome.

The v0.12.50 parking-structure component reuses the same contract with a
distinct tiered-deck silhouette and explicit type-only description. Its shape
does not imply parking availability, access, ownership, or hidden outcome.

The v0.12.51 utility-plant component reuses the same contract with a distinct
pipe-and-tank silhouette and explicit type-only description. Its shape does not
imply reliability, safety, service, ownership, or hidden outcome.

The v0.12.52 research-and-education-building component reuses the same contract
with a distinct wing-and-tower silhouette and explicit type-only description.
Its shape does not imply research or education outcome, ownership, or hidden
capacity.

The v0.12.53 construction-crane component reuses the same contract with a
distinct boom-and-tower silhouette and explicit type-only description. Its shape
does not imply project status, completion, ownership, or hidden outcome.

The v0.12.54 undeveloped-parcel component reuses the same contract with a
distinct dashed parcel-boundary silhouette and explicit type-only description.
Its shape does not imply development potential, ownership, future use, or
hidden outcome.

The v0.12.55 regional map grid is a deterministic fixture-only coordinate
contract for symbolic layout. Its 24px cells organize relationships and
attention; they do not assert real-world distance or geography.

The v0.12.56 road tile set adds deterministic horizontal, vertical, and
quarter-curve symbolic segments with a generic fallback. It organizes visual
relationships and does not assert real-world road geometry or travel time.

The v0.12.57 district tile set adds deterministic commercial, residential,
employer-center, and government tokens on the shared 24px grid. Its block,
campus, and civic patterns organize symbolic relationships and do not assert
real-world land use, population, ownership, zoning, travel time, or
jurisdiction.

The v0.12.58 parcel system adds deterministic facility and undeveloped-land
placement tokens on a shared 24px grid. Its boundary, footprint, and open-area
patterns organize symbolic placement and do not assert ownership, availability,
development potential, land value, zoning, geography, or future use.

The v0.12.59 relationship-line catalog adds deterministic peer, service,
policy, and uncertain styles with non-color patterns, round caps, and no
arrowheads. The catalog organizes actor-visible relationships without inferring
hidden intent, causality, strength, direction, distance, or future outcome.

The v0.12.60 service-area overlay catalog adds deterministic primary, shared,
and coordinated symbolic contours with metric-free, non-directional defaults.
The overlays organize actor-visible service relationships without establishing
real-world catchment, distance, travel time, population, access, jurisdiction,
or performance.

The v0.12.61 uncertainty-overlay catalog adds deterministic stale, missing, and
revised visible-information patterns with no severity encoding and static
reduced-motion behavior. The catalog identifies explicit information status
without quantifying hidden risk, severity, probability, truth, or future
outcome.

The v0.12.62 event-marker catalog adds deterministic policy, workforce,
community, and project visible-category tokens with no severity or priority
encoding, static reduced-motion behavior, and a generic fallback. The composed
`gui/map-environment-proof.html` demonstrates the shared symbolic vocabulary at
declared compact, standard, and wide target sizes with a fixed keyboard order
and bounded local zoom/pan state. The proof remains fixture-only: symbolic
coordinates and viewport controls do not assert geography, distance, travel
time, ownership, jurisdiction, host facts, commands, transitions, history,
hashes, replay, or debrief output.

The v0.12.63 operational-overlay catalog adds twelve fixture-only data tokens
for staffing, capacity, demand, projects, payer/network, regulatory,
community-trust, financial, recovery, and uncertain/stale intelligence. Each
token names its actor-visible triggering field, non-color/text equivalent,
static reduced-motion behavior, collision rule, and display-only priority.
`layoutOperationalOverlays` uses stable priority/ID ordering, a bounded stack,
and explicit overflow counts; it cannot enter host DTOs, simulation transitions,
stochastic inputs, history, hashes, replay, audio, or debrief output.

The v0.12.64 Phase 4.1 static regional-board integration adds
`gui/regional-board.mjs`, a pure adapter from the existing
`competitive-regional-world-v1` actor-visible DTO into the SVG scene vocabulary.
`gui/app.mjs` mounts the deterministic SVG beside the existing semantic map and
detail panels, keeping institution/facility focus, report links, status/source
labels, missingness, generic identity/facility fallbacks, and keyboard order in
the browser presentation layer. The adapter and board remain non-authoritative:
they do not mutate simulation state, commands, transitions, stochastic inputs,
history, hashes, replay, audio, or debrief output.

The v0.12.65 Phase 4.2 consequence-link projection adds
`gui/consequence-links.mjs` for deterministic links from actor-visible regional
signals/processes, host-committed resolution effects, and replay turn/hash
metadata. `gui/app.mjs` renders those links beside the board, connects report
and entity focus in both directions, and leaves effects without host-provided
targets targetless rather than guessing. Public rival signals retain their
observed month and private-detail boundary; historical sequence helpers return
immutable turn/hash snapshots. These are local presentation projections and do
not overwrite history or enter host, simulation, stochastic, audio, or debrief
authority.

The v0.12.66 Phase 5.1 semantic-container catalog adds eight restrained
information classes—board packet, operations ledger, intelligence report,
regulatory letter, project sheet, news wire, executive action queue, and
after-action report. Each class has structural header/marker, compact and
expanded, accessibility, large-text, narrow-width, print, reduced-motion, and
source/status rules. `gui/index.html` applies the shared semantic-container
classes and non-color markers to existing panels; the catalog and proof remain
presentation-only and do not consume hidden state or change host authority.

The v0.12.67 Phase 5.2 metric-visualization catalog adds eight deterministic
actor-visible visual forms: sparklines, month-over-month deltas, capacity bars,
staffing composition, project progress, payer mix, trust/legitimacy trend, and
visible uncertainty interval. `gui/metric-visualizations.mjs` preserves source
precision, explicit uncertainty/missingness, exact text, and non-color
interpretation; `gui/app.mjs` renders only a metric descriptor that explicitly
supplies a visualization, so visual geometry never becomes a second host or
simulation source.

The v0.12.68 Phase 6.1 motion catalog defines nine restrained presentation
categories with explicit duration/easing, reduced-motion replacement,
interruption, replay order, input, simultaneous-load, and declared frame-budget
rules. `gui/motion-catalog.mjs` plans local presentation events only; the
fixture proof demonstrates the policy without timers or host transitions, so
motion remains supplementary to text and actor-visible state.

The v0.12.69 Phase 6.2 resolution sequence adds a pure
`gui/resolution-sequence.mjs` storyboard over the host-owned
`competitive-resolution-v1` envelope. It maps the eight committed stages to
display-only attention priority, regional-board/report/metric synchronization
targets, and optional audio cue IDs. `gui/app.mjs` renders all stage text before
local play, pause, advance, skip, review, or reduced-motion emphasis. The
planner preserves unknown stages and explicit fallbacks, and cannot submit
commands, resolve randomness, mutate history, write hashes, or infer causality.

The v0.12.70 Phase 7.1 audio cue contract adds
`gui/audio-cue-contract.mjs` as the single standards catalog for the existing
16 generated interface/event cues. `gui/audio.mjs` decorates runtime entries
from that catalog and uses one bounded normalization gain, duration, and peak
ceiling recipe; its local `full`/`cues-only` mode suppresses only music and
ambience in cues-only mode. Cue metadata, cooldown timestamps, and playback
never enter host payloads, simulation state, history, hashes, replay artifacts,
or debriefs. Every cue retains visible source and written equivalents.

The v0.12.71 Phase 7.2 ambience library adds
`gui/ambience-contract.mjs` as the provenance and safety catalog for seven
fictional environmental settings. `gui/audio.mjs` maps the catalog into the
optional runtime audio surface and selects only the actor-visible regional city
bed by default. Recipes are deterministic filtered-noise beds generated at
playback time; there is no release audio file or release hash. The per-setting
GUI catalog repeats the source hash. Setting selection, recipe metadata, timers, and
playback remain local presentation details and never enter host payloads,
simulation state, history, hashes, replay artifacts, or debriefs. Each entry
retains source/generation, license, source-hash basis, loop/noise/loudness,
no-speech/music/name/alarm constraints, written equivalent, and reduced-audio
fallback metadata.

The v0.12.72 Phase 7.3 music stem contract adds
`gui/music-stem-contract.mjs` as the seven-state/five-role visible-context
catalog. `gui/audio.mjs` plays its generated base pulse, institutional motif,
visible pressure, policy, and transition cadence recipes with bounded local
fades; `gui/app.mjs` supplies only actor-visible stage/presentation envelopes.
The classifier and replay planner never read true state, private rival detail,
resolved inputs, or client formulas. Music-only mute, full mute, cues-only,
focus, reduced, and unavailable-audio behavior preserve written content.
Stem state, recipes, crossfade metadata, timers, and playback never enter host
payloads, simulation state, history, hashes, replay artifacts, or debriefs.

The v0.12.73 Phase 7.4 priority manager adds
`gui/audio-priority-contract.mjs` as a pure fixed policy for critical, major,
routine, and ambient cue ordering. `gui/audio.mjs` batches synchronous visible
cue requests, selects at most one critical cue per batch, aggregates routine
requests, caps transient queue/voice counts, and applies bounded local ducking
to background music/ambience. Explicit local audio preferences may persist in
browser storage, but queue state, timers, ducking, and preferences never enter
host payloads, simulation state, history, hashes, replay artifacts, or debriefs.
Written visible consequences remain complete under mute, reduction, storage
failure, focus loss, and unavailable audio.

The v0.12.74 Phase 8.1 generation workflow adds a contributor/release-only
boundary under `assets/generation/`. The approved-model registry, prompt
templates, review checklist, capture CLI, validation CLI, and empty manifest
record model/license identity and immutable repository commit SHA, prompt and
seed/settings, source/release hashes,
post-processing, accessible equivalents, and human approval before any bridge
to the existing visual/audio asset registries. Unknown or incomplete records
fail closed. Generation metadata, model files, outputs, approvals, and release
paths never enter host payloads, simulation state, actor observations,
history, hashes, replay artifacts, or debriefs; no model weights or generated
asset are committed in this slice.

The v0.12.76 Phase 8.2 portrait slice preserves one preview for each of the
seven canonical roles under `assets/generation/portrait-previews/`,
extending the v0.12.75 contract beyond the initial rival-system-executive
candidate. Every preview is deliberately outside the visual registry, release
directory, runtime GUI, and generation manifest because the preview tool does
not expose the approved local model revision or actual seed. Portraits require
written identity, generic actor-marker fallback, small-size/grayscale checks,
and per-portrait human review before a host-shaped presentation may use them.
The v0.12.77 review queue binds each role to its preview path/hash and keeps
human reviewer decisions, release derivatives, and registry bridges explicit;
the worksheet is not runtime authority and does not perform human approval.

The v0.12.78 Phase 9.1 release-hardening slice makes canonical visual/audio
registry provenance explicit with repository-authored, local-generation, and
external kinds. Source URLs, retrieval dates, license references, allowlist/
denylist checks, and path/hash bindings are validated without network access.
Credits and third-party notices are deterministic projections of registry data;
they remain contributor/release artifacts and do not enter host payloads,
simulation state, actor observations, history, replay artifacts, or debriefs.
No current entry is external or release-distributed, and this automation does
not substitute for a human legal audit.

The v0.12.79 Phase 9.1 in-game credits surface consumes only the generated
`gui/asset-credits.mjs` registry projection. A pure text renderer exposes
source, license, attribution, approval, provenance, release status, and written
equivalents in a disclosure available without a host session. The panel is a
static presentation surface: it uses no network or commands and cannot enter
host payloads, simulation state, actor observations, history, hashes, replay,
or debrief artifacts.

The v0.12.80 Phase 9.2 security gate scans bounded asset roots and registered
source/release paths with dependency-free signature and content checks. It
rejects executable or external SVG constructs, oversized files, excessive
dimensions, malformed raster headers, and mismatched audio signatures without
rewriting bytes. The scanner is a contributor/release boundary and cannot
enter host payloads, simulation state, actor observations, history, hashes,
replay artifacts, or debriefs.

The v0.12.81 Phase 9.2 release-hardening gate audits metadata only on approved
release image/audio paths and generates a sorted, hash-bound release manifest
from the canonical registries. It fails closed on stale output, missing files,
changed hashes, and metadata markers without stripping or rewriting bytes. The
manifest and audit remain contributor/release artifacts and cannot enter host
payloads, simulation state, actor observations, history, hashes, replay, or
debrief artifacts.

The v0.12.82 Phase 9.2 fallback contract maps only caller-supplied local
availability results into loaded or generic presentation descriptors. Missing,
failed, malformed, and unknown results retain visible requested labels and
written equivalents while clearing the release path. The adapters and proof
do not fetch, decode, inspect host/session data, enter commands, or influence
simulation state, observations, history, hashes, replay, or debriefs.

The v0.12.83 Phase 9.2 audio fallback reuses that pure availability boundary
for the existing generated Web Audio catalog. Unsupported setup and thrown
playback expose local fallback status and preserve catalog source/equivalent
text; retryable local cue failure does not enter host payloads, commands,
simulation state, observations, history, hashes, replay, or debriefs.

The v0.12.84 Phase 9.2 SVG metadata sanitizer is a dependency-free release
boundary for explicit derivatives. It validates SVG/XML with the standard
library and removes only parsed `<metadata>` elements while preserving
`<title>`, `<desc>`, geometry, and other bytes. Its approved-release check is
read-only, reuses canonical registry path/hash checks, rejects removable
metadata and unsafe paths, and never changes canonical assets, manifests,
runtime presentation, host payloads, simulation state, observations, history,
hashes, replay, or debriefs.

The v0.12.85 Phase 9 closure records the existing automated release gates as a
machine-checked technical evidence set. The roadmap test requires the Phase
9.1/9.2 technical checklists to remain fully evidenced and requires explicit
language that automated validation is not legal clearance, decoder safety,
quality, accessibility, ownership, portrait approval, or human review. This
audit changes no runtime or simulation authority and no canonical asset bytes.

The v0.12.86 Phase 10.1 slice adds an acceptance ledger over the existing
first-month `competitive-regional-v1` presentation path. It binds regional
board and facility identity, semantic desktop surfaces, host resolution,
optional audio, accessibility controls, replay/hash metadata, fallback, and
provenance evidence without adding a second runtime path. Phase 10.2 human
comprehension, quality, fatigue, educational, legal, ownership, and review
questions remain outside the technical contract.

The v0.12.87 Phase 10.2 preparation slice adds repository-safe evaluation
protocol, facilitator, and revision-log artifacts only. Stable tasks reference
the existing actor-visible first-month path; ratings and findings remain human
evidence, and the decision record remains pending. No participant data,
recordings, asset, runtime behavior, host field, simulation rule, hidden-state
projection, history, replay, or debrief authority is added.

Last Reviewed: 2026-07-21
Status: Verified

### Planned Visual and Audio Presentation Architecture

Phase 0 alignment is accepted, Phase 1 implements a dependency-free,
fixture-driven static executive desktop, Phase 2 adds a typed, read-only
host/MCP projection, Phase 3 adds host-catalogued contextual action submission,
Phase 4 adds a host-derived monthly resolution envelope, Phase 5 adds
optional generated browser audio, Phase 6 adds a bounded actor-visible
schematic regional-world projection for `competitive-regional-v1` in `gui/`,
Phase 7 adds bounded campaign coverage for stabilization and affiliation, and
Phase 8 adds local readiness controls, recovery, and allowlisted AI-agent
testplay capture/diagnostics. The GUI remains a non-authoritative thin client;
broad map/world assets remain future work outside the bounded sequence, while
Phase 9 adds deterministic capture comparison and decision logging outside the
client/core,
Phase 10 adds local accessibility/visual-language presentation controls, Phase
11 adds launch/load, Phase 12 adds generated visual identity, and Phase 13 adds
first-month continuity evidence without changing authority. The v0.12.30
first-month contract audit closes the bounded Phase 0–13 technical sequence;
all future work should follow
this one-way authority flow:

```text
deterministic simulation and committed history
  -> actor-visible projection
  -> stable presentation DTO or host adapter
  -> non-authoritative client state
  -> rendering, animation, and audio playback

client action form
  -> canonical command preview
  -> existing validation and transition boundary
  -> committed result or non-mutating rejection
```

The host boundary remains authoritative for scenario genesis, observations,
legal-command validation, resolved stochastic inputs, transitions, pending
effects, history, replay hashes, and debriefs. The client may own navigation,
selection, draft batches, viewport state, animation progress, audio playback,
and local accessibility/settings preferences. It may not own or infer true
simulation state.

Candidate serializable presentation contracts are:

- campaign and executive summary;
- regional map, institution, and facility views;
- executive briefing;
- action catalog and validated action preview;
- pending-process timeline;
- monthly resolution and direct causal attribution;
- replay and debrief views; and
- audio presentation events.

These are contract responsibilities, not a license to expose simulation state.
Phase 2 promoted the narrowest typed read-only projection needed for the first
competitive slice. Phase 3 adds only the action catalog and validation fields
needed to remove command-entry friction, and Phase 4 adds only the committed
resolution read needed to explain one completed month. Both reuse existing
parser, validator, observation, history, effect, cost, and submission
boundaries rather than introducing a second command or outcome engine. Phase 5
keeps audio classification and playback in the browser, derives it only from
visible conditions or explicit UI outcomes, and records generated provenance
outside the core. Phase 6 keeps the regional-world projection additive and
read-only: the host filters owned player detail and lagged public rival signals
into `competitive-regional-world-v1`, while the browser owns schematic layout,
selection, overlay display, and navigation only. Layout slots are not geography,
and no private rival metrics, project queues, effect queues, or map formulas
cross the standard player boundary.

Phase 7 keeps campaign semantics separate while reusing presentation primitives:
the host supplies `campaign-coverage-v1` stage, briefing, visible metrics,
actors, processes, host-shaped decisions, history, replay metadata, and debrief
for `stabilization-v1` and `regional-affiliation-v1`; the browser owns only
forms, rendering, audio playback, and recoverable presentation state. Campaign
decision submission continues through the canonical `submit_turn` boundary.

Visible observations and committed effects are the only sources for graphical
status, animation, advisory bottleneck text, music mood, and event cues. Missing,
delayed, revised, uncertain, or unavailable information must remain explicit.
Validation failure must not advance a turn, and presentation changes must not
change commands, histories, replay artifacts, state hashes, or deterministic
outcomes.

Audio cue classification should be a deterministic presentation mapping that
can be tested with a recording sink without loading or playing assets. Playback,
crossfades, focus behavior, volume, mute, and asset paths remain client concerns.
Music must derive only from actor-visible conditions or explicit campaign stage;
replay may regenerate cues from committed visible history without recording
playback as simulation history.

Visual/audio assets require a machine-readable provenance and license registry
plus generated or derivable credits. Processed release assets belong at a
documented presentation/distribution path; original sources and large-file
storage require an explicit Phase 0 decision. The simulation core must never
contain asset paths, licenses, volumes, or playback rules.

Accessibility is part of the presentation contract: semantic and keyboard
operation, color-independent status, readable scaling, reduced motion,
skippable/reviewable resolution, visual equivalents for audio, complete muted
play, and independent audio controls must be designed into the first slice.
AI-agent and static accessibility checks provide development evidence only and
must not be presented as lived human accessibility validation.

Phase 8 capture is an optional browser-side evidence boundary, not a second
simulation state. It may record declared role/task metadata, visible control
snapshots, canonical command text, validation outcomes, visible audio
equivalents, and committed history/hash metadata. Its allowlist and deterministic
diagnostic reject raw adapter payloads, true or private state, resolved inputs,
effect queues, hidden DOM content, and model hidden reasoning. Local settings and
retry controls cannot submit commands or alter transitions, hashes, replay, or
debriefs; externally supplied screenshot references remain harness metadata and
are never generated or uploaded by the game.

Shared presentation primitives may later support stabilization and affiliation,
but campaign-specific observations, commands, stages, and debrief meanings must
remain intact. A future instructor or analytic true-state view requires a
separate authorization boundary and must not weaken the standard player's
historical observation boundary.

Phase 9 analysis consumes only validated `gui-playtest-v1` artifacts. It groups
declared role/task/campaign/seed/accessibility context, emits fixed-priority
artifact/recovery/evidence hypotheses, and records product decisions without
ranking strategies or automatically changing the browser, simulation, history,
hashes, replay, or debriefs. The analyzer is a test-evidence boundary, not a
new authority or causal model.

Phase 10 keeps keyboard navigation, status symbols/labels, text scaling, and
optional cue-explanation visibility in the browser presentation boundary. The
client's `text_scale`, `text_equivalents`, and `reduced_motion` settings are
local-only preferences. They are applied through DOM/CSS attributes and never
enter host requests, canonical commands, audio-source classification,
transitions, histories, state hashes, replay artifacts, or debriefs. Targeted
status/live nodes are used instead of making the whole desktop a live region;
host-provided status categories remain the source of truth.

Phase 11 adds only a browser-side launch/load handoff for the existing host
`start_session` operation. The optional adapter accepts the existing campaign,
seed, and difficulty inputs, returns a host session envelope with `session_id`,
and then reuses the existing typed presentation/action reads. Failed or
malformed replacement loads preserve the current view. The launcher never
submits a command, creates a transition, owns a simulation state, or changes
history, hashes, replay, audio classification, or debrief output.

Phase 12 adds only a browser-side `visual-catalog-v1` for generated system
identity, facility/metric/process markers, and status-language provenance. The
catalog maps visible IDs, names, kinds, labels, and categories to text-plus-
symbol tokens with an explicit generic fallback. It does not calculate status,
read hidden fields, add host DTO data, or enter commands, transitions, state
hashes, replay artifacts, audio classification, or debrief output.

Phase 13 adds only a browser-side `competitive-first-month-v1` stage projection.
The seven stages are derived from local confirmed handoffs and visible text;
the two-draft threshold is orientation guidance, not a command limit. The rail
advances only after existing adapter operations succeed, keeps validation and
resolution/refresh failures recoverable, and never enters host payloads,
client-side legality or outcome formulas, transitions, stochastic inputs,
histories, hashes, replay artifacts, audio classification, or debrief output.

The v0.12.30 audit at
[`docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md`](docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md)
records source/test evidence for the complete bounded first-month path. It is a
read-only repository check and does not claim browser transport, human
usability, lived accessibility, learning, engagement, calibration, balance,
policy validity, or domain-expert agreement.

The v0.12.31 live-host repair reopens only the browser-transport evidence gap
identified by real launch behavior. It adds a local I/O edge around the existing
session store; it does not add a second simulation state, remote service,
persistence, authentication, cross-origin access, or GUI-only rules. The live
host currently routes `competitive-regional-v1` only, while CLI and stdio MCP
campaign coverage remain unchanged.

Last Reviewed: 2026-07-15
Status: Verified

Phase 0 alignment is accepted in
[`docs/history/initiatives/visual-audio/visual-audio-phase0-alignment-v0.12.16.md`](docs/history/initiatives/visual-audio/visual-audio-phase0-alignment-v0.12.16.md)
and ADR-0011. Phase 1 static-desktop scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase1-static-desktop-v0.12.17.md`](docs/history/initiatives/visual-audio/visual-audio-phase1-static-desktop-v0.12.17.md).
Phase 2 live read-only scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase2-live-read-only-v0.12.18.md`](docs/history/initiatives/visual-audio/visual-audio-phase2-live-read-only-v0.12.18.md).
Phase 3 contextual action scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase3-contextual-actions-v0.12.19.md`](docs/history/initiatives/visual-audio/visual-audio-phase3-contextual-actions-v0.12.19.md).
Phase 4 resolution scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase4-resolution-causal-v0.12.20.md`](docs/history/initiatives/visual-audio/visual-audio-phase4-resolution-causal-v0.12.20.md).
Phase 5 foundational audio scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase5-foundational-audio-v0.12.21.md`](docs/history/initiatives/visual-audio/visual-audio-phase5-foundational-audio-v0.12.21.md).
Phase 6 regional-world scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase6-regional-world-v0.12.22.md`](docs/history/initiatives/visual-audio/visual-audio-phase6-regional-world-v0.12.22.md).
Phase 7 campaign-coverage scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase7-campaign-coverage-v0.12.23.md`](docs/history/initiatives/visual-audio/visual-audio-phase7-campaign-coverage-v0.12.23.md).
Phase 8 AI-agent testplay-readiness scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase8-ai-agent-testplay-v0.12.24.md`](docs/history/initiatives/visual-audio/visual-audio-phase8-ai-agent-testplay-v0.12.24.md).
Phase 9 AI-agent evaluation/revision scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase9-ai-agent-evaluation-v0.12.25.md`](docs/history/initiatives/visual-audio/visual-audio-phase9-ai-agent-evaluation-v0.12.25.md).
Phase 10 accessibility and visual-language scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase10-accessibility-v0.12.26.md`](docs/history/initiatives/visual-audio/visual-audio-phase10-accessibility-v0.12.26.md).
Phase 11 first-session launch/load scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase11-session-launch-v0.12.27.md`](docs/history/initiatives/visual-audio/visual-audio-phase11-session-launch-v0.12.27.md).
Phase 12 visual identity/marker scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase12-visual-identity-v0.12.28.md`](docs/history/initiatives/visual-audio/visual-audio-phase12-visual-identity-v0.12.28.md).
Phase 13 first-month continuity scope is documented in
[`docs/history/initiatives/visual-audio/visual-audio-phase13-first-month-continuity-v0.12.29.md`](docs/history/initiatives/visual-audio/visual-audio-phase13-first-month-continuity-v0.12.29.md).
The bounded first-month audit is documented in
[`docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md`](docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md).
The projection remains display-only, while the action catalog/validation tools
and `get_resolution` are non-mutating; `submit_turn` remains the sole
transition boundary. Generated audio playback and registry metadata remain
presentation/distribution concerns; third-party asset acquisition and broad
asset-backed production remain explicitly outside this bounded closure.

## Durable Constraints

- Model strategic interaction among institutions, not direct policy levers alone.
- Preserve meaningful tradeoffs; do not collapse the game into one score.
- Keep actor utility, organizational goals, social welfare, and educational
  assessment distinct.
- Prefer narrow vertical slices before general frameworks.
- Make assumptions, causal mechanisms, and debrief explanations inspectable.
- Treat history as immutable after committed transitions.
- Keep prototype formulas visibly labeled as abstractions until evidence and
  calibration work justify stronger claims.
- Freeze major new abstractions unless playtest, scenario-authoring, debrief, or
  domain-review evidence identifies a concrete need that current structures
  cannot satisfy.
- Keep visual rendering, animation, audio, assets, and client settings outside
  deterministic transitions; derive presentation only from actor-visible or
  committed information.
- Treat simultaneous resolution as a semantic contract. System-local actions
  may be applied in canonical order only while permutation tests prove order
  independence. Before adding contested hiring, shared capacity, negotiation
  conflicts, or demand diversion, split resolution into prior-snapshot intent
  evaluation, central conflict resolution, and effect application.

Last Reviewed: 2026-06-23
Status: Verified

### Future Architecture Posture

The current architecture is sufficiently expressive for validation of the
bounded stabilization and competitive campaign slices. Future work should avoid
adding generalized actor frameworks, analytics platforms, calibration
structures, GUI platform layers, or broader scenario-authoring infrastructure
until a documented finding shows that gameplay, authoring, debriefing, audience
reach, or validation is blocked by the current narrower shape.

When a new abstraction is justified, the implementing slice should name the
evidence source, keep deterministic replay and actor-observation boundaries
intact, and leave unrelated platform goals deferred.

A future advisor-market slice is deferred as a narrow decision-support
candidate. If later justified, it would require shared market and roster state, advisor-generated
recommendations derived from each owning system's observation, explicit resolved
inputs for outside arrivals and contested hires, and append-only records of
payroll, advice, and employment changes. It must not expose hidden state,
create a generic worker framework, or claim that advisor quality predicts
outcomes. See `docs/design/expansion-proposal-review.md`.

Last Reviewed: 2026-07-09
Status: Verified; future advisor-market boundary documented

A `regional-affiliation-v1` slice is implemented outside the current
competitive runtime. It reuses the transition, observation, history, and
debrief boundaries through a localized six-stage partner interaction, stores
affiliation-specific resolved inputs before transition evaluation, preserves
actor-specific observations, and leaves the default competitive campaign
unchanged. See ADR-0010.

Last Reviewed: 2026-07-12
Status: Verified; regional-affiliation runtime boundary documented

The v0.12.1 Phase 7 capture compared the typed affiliation observation to the
MCP rendering boundary and found that alternatives, assumptions, and
commitments were omitted. v0.12.2 renders those existing typed fields through
the MCP observation without changing transition semantics, rulesets, or
replay/hash contracts. The projection remains outside the deterministic core.

The v0.12.3 Phase 7 review audits the v0.12.2 affiliation post-fix artifact
against the approved v0.11.12 competitive teachability capture. It compares
decision-context, action/response, transition/hash, outcome, debrief, and
source-specific context coverage without merging campaign semantics or
changing runtime behavior. Runtime promotion remains deferred.

The v0.12.4 difficulty-depth review reads the v0.11.11 all-tier and v0.11.9
Expert artifacts without changing the simulation. It identifies a candidate
workforce-capacity pressure signal across the tested tiers while preserving the
source-version and scripted-policy limits; any difficulty tuning remains behind
a separate design gate.

The v0.12.5 workforce-capacity design gate found that the typed competitive
observation owns safe staffing and physical-capacity fields that the MCP
formatter does not currently render. It specifies a two-line observation-only
follow-up while excluding hidden targets, effective allocations, future hires,
and rival private state; no difficulty or transition change is authorized.

The v0.12.6 follow-up renders those two lines from `PlayerObservation` at the
MCP boundary. A compatible 75-run/1,800-transition capture shows exact history
and state-hash equality against the immutable all-tier and Expert controls, so
the change remains outside the deterministic transition core. Difficulty,
balance, scoring, and winnability promotion remain deferred.

The v0.12.7 affiliation boundary proposal reconciles the existing opt-in
`regional-affiliation-v1` implementation with its design contract. The runtime
keeps true state, actor observations, resolved stochastic inputs, deterministic
transitions, append-only replay/history, and debrief utility/welfare separation
as explicit boundaries. No new affiliation mechanism or generic actor
framework is authorized by this proposal.

The v0.12.8 teachability closure keeps the existing decision-context,
action/response, transition/hash, outcome, debrief, and strategy-comparison
contracts as validation surfaces rather than adding a new runtime mechanism.
The source-specific affiliation and competitive context boundaries remain
explicit, and any future change requires a concrete evidence gap.

The v0.12.9 difficulty closure keeps the workforce-capacity signal as a
descriptive evidence route only. The visible observation controls and bounded
Expert clearability evidence do not alter the deterministic core or authorize
difficulty, balance, scoring, or winnability changes.

The v0.12.10 affiliation queue closure synchronizes the Future queue with the
already implemented six-stage opt-in runtime. It adds no state or transition;
broader acquisition remains outside the current architecture boundary until a
new evidence-backed proposal is approved.

The v0.12.11 GUI proof remains an interface adapter over existing MCP-shaped
outputs. It owns rendering only; command legality, transition evaluation,
history, replay, and debrief semantics remain outside the browser surface.

The v0.12.12 breadth closure inventories the existing competitive capacity,
operating, capital, payer, rival-information, and debrief boundaries. It found
no concrete unexplained gap authorizing a new strategic actor, individual
patient model, public-payer utility model, or generalized framework. Those
expansions remain evidence-gated.

The v0.12.13 release metadata check is a repository-boundary quality check. It
compares the package version with the lockfile, README milestone, and latest
changelog heading, and does not enter the simulation or release-publication
boundary.

### Scenario and Actor Design

Responsible for:

- actor-card fields before strategic actor expansion
- first-scenario scope and learning objectives
- educational debrief hooks
- explicit scenario non-goals and evidence gaps

Current design artifacts include `docs/design/actor-cards.md`,
`docs/design/first-scenario-brief.md`, `docs/design/competitive-scenario-brief.md`,
`docs/design/core-loop-spec.md`, and `docs/design/gameplay-competitive-sketch.md`. Runtime
scenario loading is implemented for `stabilization-v1`,
`competitive-regional-v1`, and `regional-affiliation-v1`; scenario migration
tooling and broader authoring workflows remain deferred until a bounded slice
is approved.

Last Reviewed: 2026-07-12
Status: Verified

## Competitive Campaign

Implemented modules for `competitive-regional-v1`:

| Module | Responsibility | Status |
| --- | --- | --- |
| `CampaignRouter` | Select stabilization vs competitive entry in CLI | Verified |
| `PolicyCalendar` | Month index, year boundary labels for reports | Verified |
| Executive report renderer | Six-section monthly briefing from `PlayerObservation` | Verified |
| `CompetitiveCommand` + validation | AP/cash/PC batch validation per action catalog | Verified |
| `CompetitiveWorldState` + genesis | K+1 health systems, player slots, difficulty fixtures | Verified (I4) |
| `SimultaneousActionResolver` | Aggregate monthly player batches before transition | Verified (`sim/resolve.rs`, v0.1.32) |
| `transition_competitive()` | Competitive monthly state transition | Verified (`sim/transition_competitive.rs`, v0.1.32) |
| `EffectScheduler` | Delayed/project effect queue and annual tick | Verified (v0.1.34) |
| `CommandRepl` | Stata-like parse/display layer (I/O only, ADR-0006), with help catalog rendering and command autocomplete | Verified |
| `CompetitiveCampaignLoop` | 24-month CLI loop over evolving competitive world state | Verified (v0.5.0) |

Genesis world, observation derivation, and validation demos live in
`src/competitive/`; the competitive campaign loop lives in
`src/cli/campaign.rs` and reuses `resolve_competitive_month()` for each month.
The 24-month campaign loop features autosave/resume, scenario loading, and replay export.

Last Reviewed: 2026-07-07
Status: Verified (router, report, validation, genesis, resolver, AI, events, CLI, campaign loop, autosave, scenario loader)

## Open Architectural Decisions

- Durable replay artifact format: `replay-artifact-0.1.15` stores ruleset id,
  seed, play mode, genesis state, and committed transitions with explicit
  resolved inputs for external verification. This is analysis/reproducibility,
  not cryptographic integrity or mid-run save/load.
- Mid-run interactive save: **addressed** by `session-save-0.1.27` and
  [ADR-0002](docs/decision-records/0002-mid-run-session-save.md). Autosave on
  voluntary quit and resume on startup now cover current interactive campaign
  modes; save state remains separate from replay artifacts.
- Module boundaries for the deterministic core, CLI, scenario loading, and
  educational debriefing are now established in `src/lib.rs`. Characterization
  tests are colocated with owning modules under `#[cfg(test)]`; a crate-root
  golden integration test lives in `tests/golden_seed42.rs`.
- Ruleset and scenario versioning format: design draft at
  `docs/design/scenario-format-draft.md`; the accepted runtime loader parses and validates
  both stabilization and competitive scenario files.
- Decision-record convention: **addressed** by
  `docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`.
- Competitive campaign boundaries: **addressed** by ADRs
  [0003](docs/decision-records/0003-simultaneous-monthly-player-actions.md)–[0006](docs/decision-records/0006-stata-like-cli-layer.md);
  I1–I8 and the competitive campaign loop landed.
- Data and licensing policy.
- MCP interface boundary: **addressed** by
  [ADR-0008](docs/decision-records/0008-mcp-agent-interface.md). Local stdio
  tools are accepted for bounded agent play; HTTP transport, auth, persistence,
  and long-running multi-client sessions remain deferred.
