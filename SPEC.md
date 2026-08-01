# Project Specification

This is the concise spec-driven-development index for the Health Policy
Strategy Game. It records what is true, what is being changed, and what is
intentionally deferred. Detailed release history remains in `CHANGELOG.md`,
dated findings remain under `docs/history/` and `_workspace/`, and architectural
decisions remain in `docs/decision-records/`.

Canonical product and domain direction lives in:

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/visual_audio_enhancement_roadmap.md`

## Spec maintenance rule

Keep `Present` small. Every active item must state `Done`, `Not Yet Done`, and
`Deferred / Non-Goals`. Move completed slices to `Past` after verification;
never use `SPEC.md` as a per-commit journal.

## Past

### Project foundation and deterministic simulation

- Rust CLI, deterministic state transitions, explicit stochastic inputs,
  actor-specific observations, immutable history, replay verification, and
  state hashes are implemented and tested.
- Stabilization, competitive regional-market, and regional-affiliation
  campaigns are implemented with scenario selection and educational debriefs.
- The MCP adapter exposes bounded agent playtesting and typed actor-visible
  reads, validation, resolution, history, replay, and debrief surfaces.
- Campaign persistence includes host checkpoints, per-session archives,
  discovery, opaque checkpoint references, save-artifact download, recovery,
  and deterministic continuation for all three GUI campaigns.

### GUI and presentation baseline

- The dependency-free browser client is served by a loopback Axum host and
  remains a thin presentation layer over the Rust/MCP contracts.
- The GUI supports all three campaigns, progressive Setup/Brief/Decide/
  Resolve/Review workspaces, host-ordered contextual actions, direct and
  competitive decision flows, visible consequence/resolution views, history,
  replay, debrief, settings, reduced motion, text scaling, mute/audio
  fallbacks, and checkpoint recovery.
- Visual/audio catalogs, asset registries, credits, release hashes, loading and
  offline policies, and missing-content fallbacks are machine-checked.
- Chromium evergreen desktop is the active supported target. Codex in-app
  browser inspection is development evidence. Firefox, WebKit/Safari, mobile,
  and legacy browsers remain deferred.

Historical boundary note: Phase 0 acceptance does not promote structured DTOs;
later GUI DTOs are promoted only through the current host contracts and ADRs.
Historical phase labels retained for evidence indexing: Phase 1 static executive desktop; Phases 8–9 remain sequentially gated; those labels are not current
promotion gates and remain future work only in their dated evidence records.

### GUI-focused documentation and SDD alignment (v0.14.3)

- Maintained Markdown was classified and aligned with the implemented
  three-campaign loopback GUI, deterministic host boundary, AI-native
  progression rules, and Chromium-default browser policy.
- Root SDD files were compacted into current-state indexes; release journals,
  historical reports, accepted ADR bodies, generated credits, and versioned
  workspace evidence remain preserved in their source roles.
- A repository-wide currentness checker, focused tests, and CI command now
  enforce document roles, current GUI facts, browser scope, and human-evidence
  claim limits.

## Present

The documentation baseline is complete for this release. Present work is
limited to the ranked GUI-first Future queue below; each item advances through
agent-executable evidence and automated/domain QA rather than a human stop gate.

## Future

Future work is promoted only when an AI-agent trace, authoring failure,
debrief mismatch, domain-QA finding, accessibility-mode failure, or release
check identifies a bounded unmet need.

### 1. GUI task-workspace quality

Refine Setup/Brief/Decide/Resolve/Review sequencing, action-card density,
focus/recovery behavior, large text, reduced motion, and three-campaign wording
using host-backed DOM/transport tests and AI-agent task traces.

### 2. Actor-visible consequence legibility

Improve map, facility, process, resolution, history, and debrief relationships
only from existing actor-visible fields or a separately justified host
projection. Do not infer private intent, true-state severity, or causal
certainty in the browser.

### 3. Registered visual/audio production

Add only assets or audio that answer a strategic or explanatory question, have
machine-readable provenance and hashes, preserve text/mute/reduced-motion
fallbacks, and fail closed to generic presentation when metadata is incomplete.

### 4. Default-browser release hardening

Maintain Chromium evergreen desktop and loopback source-checkout evidence,
offline/loading policy, performance proxy, and deterministic GUI smoke coverage.
Do not promote non-default browser or device support without a separately
authorized decision.

### 5. Agent-native validation and revision

Run reproducible profiles across campaigns, seeds, action paths, failure
recovery, keyboard, large-text, reduced-motion, and audio-off modes. Use
technical/domain/presentation QA to prioritize revisions. Keep human-learning,
legal, calibration, and policy-validity claims explicitly unestablished.

## Promotion rules

Before a Future item becomes Present, record the concrete evidence gap, the
smallest artifact or behavior to change, source/authority boundaries,
verification commands, and non-goals. A passing automated check may close a
technical contract; it may not be described as human outcome evidence.

## Deferred / non-goals

- Network multiplayer, remote hosting, browser-owned simulation state, GUI-only
  rules, general visual editors, patient/interior simulation, and broad model
  generalization.
- Firefox, WebKit/Safari, mobile, legacy-browser, and real-device certification.
- Human usability, learning, classroom effectiveness, lived accessibility,
  legal clearance, empirical calibration, balance, and policy validity claims.
- Unregistered, unverifiable, or resemblance-risk assets in the runtime release.
