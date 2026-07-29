# Request Summary — Campaign decision-time observation recovery v0.13.61

## Authorized outcome

Continue the roadmap loop with a bounded browser-native recovery slice:
expose existing actor-visible observations paired with stabilization and
regional-affiliation committed decisions through the campaign-coverage history
and render them as optional written details.

## Target slice

- Add an optional observation-lines field to `TransitionSummary`, populated
  from existing visible host formatters for stabilization and affiliation.
- Add an accessible campaign-history disclosure tied to each committed
  turn/command, preserving fixtures without the field and competitive paths.
- Update the decision-time recovery ledger, roadmap/spec/guides, tests,
  version, generated records, QA, and handoff documentation to v0.13.61.

## Non-goals

- Do not add a route, schema version, asset, audio file, simulation rule,
  persistence behavior, replay regeneration, true-state field, resolved input,
  private rationale, causal graph, or instructor authority.
- Do not claim human comprehension, accessibility, educational value, or
  visual quality from technical disclosure tests.

## Validation target

Focused Rust/Node/Python observation-recovery tests, full Rust/Python suites,
release metadata, documentation links, asset/security/generation,
device-performance, offline, browser-compatibility, visual/audio contract,
and diff checks, followed by exactly one medium-effort code review and PR
handoff.

## Evidence limits

This slice proves only technical recovery of visible decision-time observation
text. Causal visualization, counterfactual/instructor surfaces, human
accessibility, educational usability, quality, persistence, and public-release
gates remain open.

# Request Summary — Direct campaign audio projection v0.13.60

## Authorized outcome

Continue the roadmap loop with a bounded direct campaign-audio projection:
carry optional host-sourced music/cue metadata through the existing
`campaign-coverage-v1` envelope for stabilization and regional affiliation,
honor it in the browser, and keep written/audio-off fallbacks complete.

## Target slice

- Add `CampaignCoverageAudio` using only existing catalog IDs and actor-visible
  stage, briefing, actor, process, and committed history-summary sources.
- Make the browser distinguish explicit empty cue metadata from omitted legacy
  metadata; preserve the older affiliation milestone fallback only when audio
  metadata is absent.
- Update current Phase 12 ledgers, roadmap/spec/guides, tests, version,
  generated records, QA, and handoff documentation to v0.13.60.

## Non-goals

- Do not add a new route, schema version, asset, audio file, catalog ID,
  simulation rule, hidden-state field, transition authority, or persistence.
- Do not infer severity, agreement, intent, probability, causality, or future
  outcome from audio metadata.
- Do not claim human listening, accessibility, educational, legal, provenance,
  device, or public-release approval.

## Validation target

Focused host/browser audio tests, full Rust/Python suites, release metadata,
documentation links, asset/security/generation, device-performance, offline,
browser-compatibility, and visual/audio contract checks, followed by exactly
one medium-effort code review and PR handoff.

## Evidence limits

This slice proves only the technical host-to-browser direct audio projection
and its visible-only/optional boundary. Campaign-specific audio quality,
listening, accessibility, educational, persistence, device, provenance/legal,
and public-release gates remain open.

# Request Summary — Visual/audio Phase 13.1 AI-generation metadata boundary v0.13.57

## Authorized outcome

Substantiate the open Phase 13.1 AI-generation metadata gate without
fabricating model, revision, seed, or human-review data. Preserve the seven
portrait previews as unreleased, unregistered, pending candidates and make the
next approved regeneration/promotion handoff explicit.

## Target slice

- Add a deterministic evaluation ledger for the current approved local model
  registry, generation workflow, capture/validation scripts, portrait previews,
  review queue, manifest, and visual registry boundary.
- Add a focused Python test that proves current technical metadata inputs pass,
  missing preview model/seed provenance remains blocked, and a promotion-shaped
  mutation fails closed.
- Update the roadmap, specification, changelog, lessons, presentation QA,
  handoff, and package version to v0.13.57.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 8.2 portrait and Phase
  13.1 AI-generation metadata gates.
- `assets/generation/approved-models.json` and
  `assets/generation/generation-workflow.json` — approved model and required
  metadata contracts.
- `scripts/capture_generation_metadata.py` and
  `scripts/validate_generation_metadata.py` — fail-closed capture and
  validation paths.
- `assets/generation/portrait-previews.json` and
  `assets/generation/portrait-review-queue.json` — current pending preview and
  human-review boundary.
- `_workspace/136_implementation_plan_phase13-1-ai-generation-metadata-boundary-v0.13.57.md`
  — bounded implementation plan.

## Non-goals

- Do not invent model identity, immutable revision, seed, sampler, or license
  metadata for existing Codex previews.
- Do not generate or promote portraits, add registry/release/manifest entries,
  add browser/runtime behavior, or alter simulation, history, replay,
  persistence, or authority.
- Do not claim human resemblance, artifact, accessibility, legal, ownership,
  training-data, clinical, educational, or public-release approval.

## Validation target

Focused AI-generation metadata boundary test and validator, release metadata,
asset/security/credits checks, documentation-link checks, Rust formatting,
Clippy, Rust tests, and the full Python test suite.

## Evidence limits

This slice proves the current technical readiness and fail-closed boundary for
portrait metadata only. It does not close the roadmap's actual prompt/seed
capture, per-portrait human review, release derivative, registry approval, or
public-release gates.

# Request Summary — Visual/audio Phase 11.1 live history handoff v0.12.94

## Authorized outcome

Expose the existing host-owned immutable history through a dedicated non-
mutating loopback GUI read and render it through the existing text-first history
surface. Preserve current presentation history on endpoint failure and keep
replay regeneration/save-load/full-campaign claims open.

## Target slice

- Add `competitive-history-v1` to the host history envelope.
- Add `GET /api/v1/sessions/{session_id}/history` and `getHistory` in the local
  adapter using `GameSessionStore::get_history` only.
- Add browser validation/client/render handoff and refresh the existing history
  list after a successful live presentation refresh when supported.
- Add deterministic Rust, transport, Node, and Python evidence plus
  project-record/version updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 history/replay view.
- `src/mcp/session.rs` — existing immutable host history read.
- `src/gui_server.rs` and `gui/host-adapter.mjs` — live loopback transport.
- `gui/app.mjs` — existing text-first history renderer and live action path.
- `_workspace/88_implementation_plan_visual-audio-phase11-live-history-v0.12.94.md`
  — bounded implementation and review plan.

## Non-goals

- Do not add replay regeneration/playback, save/load, new assets, hidden-state
  fields, simulation behavior, new hashes, debrief synthesis, screenshots,
  performance, compatibility, or client authority.
- Do not claim full campaign history/debrief/save-load/replay continuity or
  human-quality completion.

## Validation target

Focused live history, session, resolution, release metadata, asset/security/
credits, documentation, JavaScript, formatting, Clippy, and full Python/Rust
checks.

## Evidence limits

This slice proves one dedicated non-mutating live history handoff and safe
presentation fallback only. Full campaign history/debrief/save-load/replay
continuity, screenshots, performance, compatibility, asset quality, human
accessibility, legal clearance, and educational benefit remain open.

---

# Request Summary — Visual/audio Phase 11.1 live music-state projection v0.12.93

## Authorized outcome

Move the primary live competitive resolution music-state selection to an
explicit host-shaped presentation projection derived from committed
actor-visible resolution data. Preserve visible-only browser fallback for
older or malformed envelopes and keep broad campaign music coverage open.

## Target slice

- Add `music_state_id` to the competitive resolution envelope.
- Select one of the existing catalog IDs using committed events/effects,
  actor-visible after text/operating values, and the explicit terminal boundary.
- Prefer a valid explicit state in `gui/app.mjs`; use the existing visible
  classifier only when no usable host field is present.
- Add deterministic Rust, Node, and Python evidence plus project-record/version
  updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 music-state coverage.
- `src/mcp/resolution.rs` and `src/mcp/session.rs` — committed resolution
  summary and actor-visible snapshot authority.
- `gui/music-stem-contract.mjs`, `gui/audio.mjs`, and `gui/app.mjs` — existing
  catalog, visible classifier, optional playback, and live resolution path.
- `_workspace/87_implementation_plan_visual-audio-phase11-live-music-v0.12.93.md`
  — bounded implementation and review plan.

## Non-goals

- Do not add audio assets, dependencies, hidden-state fields, private rival
  detail, simulation behavior, history/hash changes, client authority,
  screenshots, performance, compatibility, or human-quality claims.
- Do not claim full campaign music/event/continuity coverage or audio
  usefulness/fatigue.

## Validation target

Focused live music, resolution, audio, release metadata, asset/security/
credits, documentation, JavaScript, formatting, Clippy, and full Python/Rust
checks.

## Evidence limits

This slice proves explicit host-shaped music IDs for currently supported live
resolution states and safe legacy fallback only. Full campaign music taxonomy,
screenshots, performance, compatibility, asset quality, human accessibility,
audio usefulness, legal clearance, and educational benefit remain open.

---

# Request Summary — Visual/audio Phase 11.1 live event-cue projection v0.12.92

## Authorized outcome

Move the primary live competitive event-cue selection to an explicit
host-shaped presentation projection derived from committed actor-visible
resolution data. Preserve a visible-only browser fallback for legacy
envelopes and keep broad campaign coverage open.

## Target slice

- Add `audio_cue_ids` to the competitive resolution envelope.
- Derive the eight currently supported event cues from committed events and
  effects, before/after visible operating margins, and actor-visible
  observation text.
- Prefer the explicit list in `gui/app.mjs`, including an explicit empty list;
  use `visibleEventCues` only when older envelopes omit the field.
- Add deterministic Rust, Node, and Python evidence plus project-record/version
  updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 event-cue coverage.
- `src/mcp/resolution.rs` and `src/mcp/session.rs` — committed resolution
  summary and actor-visible before/after projection.
- `gui/audio-cue-contract.mjs`, `gui/audio.mjs`, and `gui/app.mjs` — existing
  cue catalog, legacy visible classifier, and live resolution path.
- `_workspace/86_implementation_plan_visual-audio-phase11-live-event-cues-v0.12.92.md`
  — bounded implementation and review plan.

## Non-goals

- Do not claim full campaign event-cue or music-state coverage, screenshots,
  performance, compatibility, accessibility quality, or human evaluation.
- Do not add audio assets, dependencies, hidden-state fields, rival detail,
  simulation behavior, history/hash changes, client authority, or network
  access.

## Validation target

Focused event-cue, resolution, audio, release metadata, asset/security/credits,
documentation, JavaScript, formatting, Clippy, and full Python/Rust checks.

## Evidence limits

This slice proves explicit host-shaped cue IDs for currently supported visible
conditions and preserves legacy-envelope fallback semantics only. Full campaign
event/history/debrief/save-load/replay coverage, screenshots, performance,
compatibility, asset quality, human accessibility, audio usefulness, legal
clearance, and educational benefit remain open.

---

# Request Summary — Visual/audio Phase 11.1 live operational-overlay binding v0.12.90

## Authorized outcome

Bind directly supported actor-visible conditions in the competitive regional
world to the existing operational-overlay catalog. Preserve raw metric
overlays, source/equivalent text, generic fallback behavior, and the host/core
authority boundary.

## Target slice

- Add an optional `operational_overlay_id` to the host-projected regional-world
  overlay contract.
- Populate only visible conditions supported by `PlayerObservation`:
  unmet-demand pressure, active capital projects, financial distress,
  community-trust concern, and uncertain/stale intelligence.
- Resolve explicit IDs in the live regional-board adapter and expose catalog
  source/equivalent semantics with a generic fallback.
- Add deterministic Rust, Node, and Python evidence plus project-record/version
  updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 overlay coverage.
- `src/mcp/regional_world.rs` and `src/model/campaign.rs` — actor-visible
  observation projection.
- `gui/operational-overlays.mjs`, `gui/regional-board.mjs`, and `gui/app.mjs` —
  catalog and live presentation paths.
- `_workspace/84_implementation_plan_visual-audio-phase11-live-overlays-v0.12.90.md`
  — bounded implementation and review plan.

## Non-goals

- Do not claim full campaign overlay coverage, screenshot, performance,
  compatibility, accessibility quality, or human evaluation completion.
- Do not add assets, dependencies, hidden-state fields, rival facility detail,
  simulation behavior, client authority, or network access.
- Do not classify raw demand, access, or staffed-bed metrics as operational
  severity without a direct visible condition.

## Validation target

Focused overlay-binding, regional-world, GUI-contract, release metadata,
asset/security/credits, documentation, JavaScript, formatting, Clippy, and
full Python/Rust checks.

## Evidence limits

This slice proves explicit DTO-to-catalog binding and fallback semantics for the
currently supported live conditions only. Full campaign overlay/event/history/
debrief/save-load/replay coverage, screenshots, performance, compatibility,
asset quality, human accessibility, audio usefulness, legal clearance, and
educational benefit remain open.

---

# Historical Request Summary — Visual/audio Phase 11.1 live facility binding v0.12.89

## Authorized outcome

Bind the current actor-visible competitive facility groups to stable existing
facility-component catalog IDs in the regional board and selected facility
detail view. Close only this bounded live binding evidence; keep full campaign
facility coverage and human-quality claims open.

## Target slice

- Add explicit `component_id` values to the four player facility groups in the
  `competitive-regional-v1` regional-world DTO.
- Resolve IDs through `FACILITY_COMPONENTS`, expose source/equivalent semantics
  and release paths, and use the registered generic fallback for missing or
  unknown IDs.
- Preserve the rival privacy boundary and add deterministic Rust, Node, and
  Python evidence plus project-record/version updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 facility coverage.
- `src/mcp/regional_world.rs` — actor-visible facility projection.
- `gui/facility-components.mjs`, `gui/regional-board.mjs`, `gui/scene.mjs`,
  and `gui/app.mjs` — catalog and presentation paths.
- `_workspace/83_implementation_plan_visual-audio-phase11-live-facilities-v0.12.89.md`
  — bounded implementation and review plan.

## Non-goals

- Do not claim full campaign facility taxonomy, asset-registry completeness,
  screenshot, performance, compatibility, accessibility quality, or human
  review completion.
- Do not add assets, dependencies, hidden-state fields, rival facility detail,
  simulation behavior, client authority, or network access.
- Do not treat the emergency/ICU group as an exact ICU-specific asset; it uses
  an explicitly documented emergency-department presentation equivalent.

## Validation target

Focused facility-binding, regional-board, GUI-contract, release, full Python/
Rust, asset/security/credits, documentation, JavaScript, formatting, and
Clippy checks.

## Evidence limits

This slice proves current live DTO-to-catalog binding, accessible metadata,
selected-detail semantics, and generic fallback behavior only. Full campaign
facility coverage and remaining Phase 11.1/11.2+ gates remain open.

---

# Historical Request Summary — Visual/audio Phase 11.1 campaign-coverage evidence v0.12.88

## Authorized outcome

Record a machine-checkable, bounded technical coverage ledger for the current
`competitive-regional-v1` presentation catalogs and first-month continuity
surfaces. Close only actor-family catalog and unknown-content fallback items
that are directly evidenced; keep full-campaign and human-quality claims open.

## Target slice

- Add `docs/evaluation/phase11.1-campaign-coverage-ledger.json` with exact live
  facility, overlay, actor-family, event-marker, event-cue, and music-state IDs.
- Add a Node-backed regression test for ledger parity, visible source/
  equivalent semantics, unknown fallbacks, and bounded continuity paths.
- Reconcile only the supported Phase 11.1 checklist entries and update project
  records/version projections without changing runtime behavior or assets.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 coverage scope.
- `gui/facility-components.mjs`, `gui/operational-overlays.mjs`,
  `gui/actor-families.mjs`, `gui/map-event-markers.mjs`,
  `gui/audio-cue-contract.mjs`, and `gui/music-stem-contract.mjs`.
- `gui/first-month.mjs`, `gui/resolution-sequence.mjs`,
  `gui/consequence-links.mjs`, `gui/playtest.mjs`, `gui/app.mjs`, and existing
  Phase 10.1 integration evidence.

## Non-goals

- Do not claim full competitive-campaign facility, overlay, event, history,
  debrief, save/load, replay, screenshot, performance, or browser coverage.
- Do not add assets, dependencies, host fields, simulation rules, hidden-state
  projections, client authority, or a second runtime path.
- Do not infer asset quality, accessibility quality, audio usefulness, legal
  clearance, educational benefit, or human review from catalog presence.

## Validation target

Focused campaign-coverage tests, full Python/Rust tests, asset/security/
release/credits/version/documentation checks, formatting, Clippy, JavaScript
syntax, and diff checks.

## Evidence limits

This slice proves catalog parity and bounded fallback semantics only. Full
campaign continuity, screenshot/performance/compatibility gates, and human
evaluation remain open.

---

# Historical Request Summary — Visual/audio Phase 10.2 evaluation preparation v0.12.87

## Authorized outcome

Prepare a privacy-bounded, machine-readable and facilitator-readable
structured evaluation protocol for the Phase 10.1 first-month visual/audio
slice. Close only the preparation items that can be evidenced in the
repository; keep participant evidence, findings, and go/no-go authorization
open.

## Target slice

- Add a canonical JSON protocol with stable task IDs, rating dimensions,
  finding categories, privacy restrictions, and a blank decision record.
- Add a facilitator guide covering first-session, recognition,
  consequence-tracing, accessibility, and audio tasks.
- Add an empty anonymized revision-log template and a regression test that
  prevents fabricated human evidence or premature roadmap closure.
- Update project records, version projections, CI, and lessons without adding
  runtime behavior or collecting participant data.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 10.2 evaluation gates.
- `docs/evaluation/phase10.2-evaluation-protocol.json` — canonical task and
  decision schema.
- `docs/guides/phase10.2-structured-evaluation.md` — facilitator sequence.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation
  contract and QA record.

## Non-goals

- Do not conduct or simulate sessions, fabricate ratings/interviews/findings,
  or record a go/no-go decision.
- Do not collect or commit names, contact details, health information,
  identifying recordings, private game state, or external participant data.
- Do not claim legal clearance, universal accessibility, educational benefit,
  clinical validity, policy forecasting accuracy, or human approval.
- Do not add assets, dependencies, runtime behavior, host fields, simulation
  rules, hidden-state projections, or client authority.

## Validation target

Focused evaluation-preparation and release-metadata tests, full Python/Rust
tests, asset/security/release/credits/version/documentation checks, formatting,
Clippy, JavaScript syntax, and diff checks.

## Evidence limits

This slice establishes evaluation readiness only. It contains no participant
results, and human evaluation, finding classification, revision approval, and
go/no-go remain separately authorized gates.

---

# Historical Request Summary — Visual/audio Phase 10.1 first-month slice v0.12.86

## Authorized outcome

Add a machine-checkable acceptance contract for the integrated first-month
`competitive-regional-v1` visual/audio path while preserving host authority,
deterministic replay, actor-visible information boundaries, and explicit Phase
10.2 human-evaluation limits.

## Target slice

- Add `tests/test_phase10_first_month.py` with exact Phase 10.1 checklist
  coverage, live GUI/source markers, no-authority checks, and deterministic
  first-month/music/skip probes.
- Reconcile the Phase 10.1 technical checklist and record the integration
  evidence without adding a duplicate runtime path or new asset.
- Keep Phase 10.2 first-time-user, accessibility-quality, audio-fatigue, and
  educational-usability evaluation as explicit human gates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 10.1 and the v0.12.86
  first-month technical-evidence target slice.
- `assets/registry/visual-assets.json` and `audio-assets.json`.
- `gui/app.mjs`, `gui/index.html`, `gui/first-month.mjs`,
  `gui/resolution-sequence.mjs`, `gui/music-stem-contract.mjs`, current GUI
  tests, and the Rust host/replay contracts.
- `docs/design_principles.md`, `LESSONS.md`, and the current presentation QA.

## Non-goals

- Do not mark any portrait approved, add portrait registry/release entries, or
  populate the generation manifest.
- Do not download or add external assets, infer legal clearance, or treat
  automated checks as legal advice or a human license audit.
- Do not claim first-time-user comprehension, accessibility quality, audio
  usefulness/fatigue, educational usability, legal clearance, or portrait
  approval.
- Do not add assets, dependencies, host fields, simulation rules, hidden-state
  projections, registry/release changes, or a duplicate runtime path.
- Do not change live GUI authority, host DTOs, simulation, history, replay,
  state hashes, debrief facts, or actor observations.

## Validation target

Phase 10.1 integration tests, existing GUI/host/replay/audio tests, full
Python/Rust tests, asset/security/release/credits/version/documentation checks,
formatting, Clippy, JavaScript, and diff checks.

## Evidence limits

The slice establishes technical integration and deterministic boundary checks
only; it does not establish first-time-user comprehension, accessibility
quality, audio usefulness/fatigue, educational usability, legal clearance,
ownership, or human review. Phase 10.2 remains an explicit external gate.
# Request Summary — Visual/audio Phase 11.1 live debrief handoff v0.12.91

## Authorized outcome

Continue the roadmap loop with a bounded live-session continuity slice. Make
the host-owned final competitive debrief available to the browser together
with the immutable committed history and replay metadata that support it.

## Target slice

- Extend the existing terminal host envelope with schema, turn bounds, history,
  and replay metadata aligned to the generated debrief.
- Add the loopback GUI end-session route and adapter method.
- Render a text-first terminal debrief view, preserve state hashes, and disable
  further action after successful host termination.
- Add deterministic Rust, transport, Node, and Python evidence plus project
  record/version updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 history, debrief,
  replay, and continuity gaps.
- `src/mcp/session.rs` — host terminal/debrief authority and transition history.
- `src/gui_server.rs` and `gui/host-adapter.mjs` — live loopback transport.
- `gui/app.mjs` and `gui/index.html` — existing history/debrief presentation.
- `_workspace/85_implementation_plan_visual-audio-phase11-live-debrief-v0.12.91.md`
  — bounded implementation and review plan.

## Non-goals

- Do not add save/load, screenshot suites, new assets, audio files, hidden
  state, rival detail, client simulation, or a second debrief implementation.
- Do not mark broad Phase 11.1 history/debrief/save-load/replay coverage,
  performance, compatibility, or human-quality gates complete.

## Validation target

Focused terminal debrief, live transport, GUI contract, release metadata,
asset/security/credits, documentation, JavaScript, formatting, Clippy, and
full Python/Rust checks.

## Evidence limits

This slice proves only the current live terminal handoff and its aligned
history/replay/debrief presentation. It does not prove full-campaign
continuity, persistence, screenshots, performance, compatibility, audio
usefulness, human accessibility, legal clearance, or educational benefit.

---
# Request Summary — Visual/audio Phase 11.1 live replay continuity v0.12.95

## Authorized outcome

Expose the existing host-owned immutable history and replay metadata through a
dedicated non-mutating loopback GUI read, rendering it through the existing
text-first history/replay surface. Preserve the current view on endpoint or
validation failure and keep save/load, replay regeneration, and full-campaign
claims open.

## Target slice

- Add `competitive-replay-v1` with session/campaign/seed, transition count,
  latest visible hash, and immutable transition summaries.
- Add `GET /api/v1/sessions/{session_id}/replay`, MCP exposure, and `getReplay`
  in the local adapter using the existing history source only.
- Add browser validation/client/render handoff after successful live reads.
- Add deterministic Rust, transport, Node, and Python evidence plus project
  record/version updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 replay continuity.
- `src/mcp/session.rs` — existing history and historical-resolution reads.
- `src/mcp/server.rs` and `src/gui_server.rs` — host transport boundaries.
- `gui/app.mjs` and `gui/host-adapter.mjs` — existing history/replay surface.
- `_workspace/89_implementation_plan_visual-audio-phase11-live-replay-v0.12.95.md`
  — bounded implementation and review plan.

## Non-goals

- Do not add save/load persistence, replay regeneration/playback simulation,
  new assets, hidden-state fields, stochastic behavior, new hashes, audio,
  screenshots, performance, compatibility, or client authority.
- Do not claim full campaign history/debrief/save-load/replay continuity or
  human-quality completion.

## Validation target

Focused replay, history, resolution, session, release metadata, asset/security/
credits, documentation, JavaScript, formatting, Clippy, and full Python/Rust
checks.

## Evidence limits

This slice proves one dedicated non-mutating live replay handoff and safe
history-view continuity only. Full campaign save/load/replay continuity,
screenshots, performance, compatibility, asset quality, human accessibility,
legal clearance, and educational benefit remain open.

---
# Request Summary — Visual/audio Phase 11.1 live checkpoint continuity v0.12.96

## Authorized outcome

Expose an explicit host-owned in-memory checkpoint save/restore operation for
the live competitive GUI. Refresh visible host presentation, action catalog,
history, replay, and regional-world reads after a successful restore; preserve
the current view on failure and keep durable persistence/full-campaign claims
open.

## Target slice

- Add `competitive-save-v1`, `save_session`, and `load_session` over cloned
  host sessions.
- Add loopback save/load routes and `saveSession`/`loadSession` adapter methods.
- Add accessible browser controls, strict envelope validation, and a host-read
  refresh after restore.
- Add deterministic Rust, transport, Node, and Python evidence plus project
  record/version updates.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.1 save/load continuity.
- `src/model/session_save.rs` and `src/cli/persistence.rs` — existing durable
  save-artifact contract and its explicit verification boundary.
- `src/mcp/session.rs` and `src/gui_server.rs` — live ephemeral host store.
- `gui/app.mjs`, `gui/index.html`, and `gui/host-adapter.mjs` — live browser
  launch/read/action surface.
- `_workspace/90_implementation_plan_visual-audio-phase11-live-checkpoint-v0.12.96.md`
  — bounded implementation and review plan.

## Non-goals

- Do not add durable files, cross-process import, browser serialization,
  replay regeneration, hidden-state fields, stochastic behavior, new hashes,
  assets, audio, screenshots, performance, compatibility, or client authority.
- Do not claim durable persistence, full campaign save/load/replay continuity,
  or human-quality completion.

## Validation target

Focused checkpoint, replay, history, resolution, session, release metadata,
asset/security/credits, documentation, JavaScript, formatting, Clippy, and
full Python/Rust checks.

## Evidence limits

This slice proves one in-memory host checkpoint and visible refresh path only.
Durable save files, cross-process recovery, full campaign continuity, replay
regeneration, screenshots, performance, compatibility, asset quality, human
accessibility, legal clearance, and educational benefit remain open.

---
# Request Summary — Visual/audio Phase 11.2 asset-size budget v0.12.97

## Authorized outcome

Define and machine-check explicit byte and file-count budgets for the tracked
release asset package. Emit a deterministic report that makes the current
release SVG class and total release package size inspectable without claiming
runtime performance.

## Target slice

- Add `asset-budget-v1` with named release SVG and complete-release classes.
- Add a dependency-free checker and deterministic JSON report.
- Add focused Python coverage for schema, counts, limits, path boundaries, and
  script behavior.
- Update Phase 11.2 roadmap evidence and project records/version projections.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.2 asset-size budget.
- `assets/ASSET_RELEASE_MANIFEST.json` — current tracked release files and
  byte/hash manifest.
- `assets/registry/README.md` and `scripts/validate_assets.py` — existing
  registry/provenance boundary.
- `_workspace/91_implementation_plan_visual-audio-phase11-performance-budget-v0.12.97.md`
  — bounded implementation and review plan.

## Non-goals

- Do not optimize or rewrite assets, add dependencies, change audio playback,
  claim cache/decode/render/memory performance, or claim offline/device/
  compatibility completion.
- Do not include source-only references or generated portrait previews in the
  tracked release budget.

## Validation target

Focused budget/checker tests, full Rust/Python checks, release metadata,
documentation links, asset registry/release/credits/security/generation
checks, and the visual/audio contract audit.

## Evidence limits

This slice proves only a versioned byte/file-count budget and current report for
tracked release files. It does not establish runtime performance, browser
cache behavior, low-power suitability, offline operation, compatibility, asset
quality, legal clearance, or human comprehension.

---
# Request Summary — Visual/audio Phase 11.2 SVG optimization v0.12.98

## Authorized outcome

Normalize the tracked release SVG derivatives with a conservative,
dependency-free whitespace-only pass and machine-check that the result is
idempotent, hash-aligned, and semantically text-preserving at the repository
contract level.

## Target slice

- Add an optimizer/checker for `assets/release/visual/svg/*.svg`.
- Collapse inter-tag formatting whitespace only; preserve text, attributes,
  styles, dimensions, titles/descriptions, and source files.
- Refresh registry release hashes and the deterministic release manifest.
- Add focused tests and update Phase 11.2/project records and version
  projections.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.2 SVG optimization.
- `assets/asset-budget.json` — tracked release-asset scope and size evidence.
- `assets/registry/visual-assets.json` and
  `assets/ASSET_RELEASE_MANIFEST.json` — release hash authority.
- `_workspace/92_implementation_plan_visual-audio-phase11-svg-optimization-v0.12.98.md`
  — bounded implementation and review plan.

## Non-goals

- Do not alter SVG geometry, text nodes, styles, URLs, accessibility content,
  source files, raster assets, audio, browser loading, or runtime behavior.
- Do not claim render-time, cache, memory, device, offline, compatibility,
  screenshot, or human-quality completion.

## Validation target

Focused optimizer/checker tests, full Rust/Python checks, release metadata,
documentation links, asset registry/release/credits/security/generation
checks, and the visual/audio contract audit.

## Evidence limits

This slice proves only an idempotent whitespace-normalized release SVG
derivative and aligned hashes/manifest. It does not establish semantic SVG
equivalence beyond the tested text/attribute boundary or any runtime
performance outcome.

---
# Request Summary — Visual/audio Phase 11.2 missing-asset fallback v0.12.99

## Authorized outcome

Extend machine-checked missing-asset fallback coverage from selected examples
to every tracked facility and fictional institution release descriptor. Keep
the existing written generic fallback boundary and registry/GUI authority
unchanged.

## Target slice

- Enumerate facility and identity catalogs through their live JavaScript
  exports.
- Align every catalog release path to the canonical visual asset registry.
- Exercise missing, failed, and malformed availability for every descriptor;
  require fallback mode, null release path, and written equivalents.
- Update Phase 11.2 evidence and project records/version projections.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.2 missing-asset
  fallback checklist item.
- `gui/asset-availability.mjs`, `gui/facility-components.mjs`, and
  `gui/identity-kits.mjs` — existing fallback and catalog boundaries.
- `assets/registry/visual-assets.json` — canonical release-path registry.
- `_workspace/93_implementation_plan_visual-audio-phase11-missing-asset-fallback-v0.12.99.md`
  — bounded implementation and review plan.

## Non-goals

- Do not change fallback implementation, add/remove assets, optimize files,
  change audio/simulation/browser authority, or add network access.
- Do not claim full campaign coverage, browser/device compatibility, runtime
  performance, human accessibility, or asset-quality completion.

## Validation target

Focused fallback/catalog/registry Node coverage, full Rust/Python checks,
release metadata, documentation links, asset registry/release/credits/security
/generation checks, and the visual/audio contract audit.

## Evidence limits

This slice proves catalog-level fallback coverage for current tracked facility
and institution release descriptors. It does not prove every future campaign
asset, browser rendering quality, device behavior, or human comprehension.

---
# Request Summary — Visual/audio Phase 11.2 raster scope and bounds v0.13.0

## Authorized outcome

Define and machine-check the current raster boundary: release packages contain
no raster derivatives, and the seven unverified portrait preview PNGs remain
within explicit dimension/byte bounds and outside release eligibility.

## Target slice

- Add `raster-scope-v1` with explicit release prohibition and preview limits.
- Add a deterministic JSON checker/report for release and preview surfaces.
- Add focused coverage for current report, malformed/promoted/oversized paths,
  and no-release-raster enforcement.
- Update Phase 11.2 evidence and project records/version projections.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 11.2 raster derivatives.
- `assets/generation/portrait-previews.json` and
  `scripts/validate_generation_metadata.py` — existing preview-only boundary.
- `assets/release` and `assets/registry` — approved release surface.
- `_workspace/94_implementation_plan_visual-audio-phase11-raster-scope-v0.13.0.md`
  — bounded implementation and review plan.

## Non-goals

- Do not resize, compress, promote, or add raster assets; do not change source
  hashes, preview provenance, browser loading, audio, simulation, or network.
- Do not claim raster quality, decode/render/cache/memory performance, offline,
  device, compatibility, screenshot, legal, or human-quality completion.

## Validation target

Focused raster-scope tests/checker, full Rust/Python checks, release metadata,
documentation links, asset registry/release/credits/security/generation
checks, and the visual/audio contract audit.

## Evidence limits

This slice proves only the current release-raster absence and preview bounds;
it does not establish a future raster derivative pipeline or runtime behavior.

---
# Request Summary — Visual/audio Phase 11.2 audio packaging review v0.13.1

## Scope

Close the Phase 11.2 `Audio compression reviewed` checklist item for the
current presentation package. The current GUI uses repository-authored Web
Audio recipes and the release tree contains no file-backed audio. Add a
machine-checked packaging-scope document and deterministic report that records
this as an explicit not-applicable compression decision while failing closed if
audio files are later placed in the release tree without a new reviewed scope.

## Non-goals

- Do not add, transcode, compress, or promote an audio file.
- Do not change browser playback, audio semantics, simulation, host DTOs,
  commands, history, hashes, replay, or debriefs.
- Do not claim runtime decode, loudness, device, offline, or compatibility
  performance.
- Do not close lazy loading, preload, offline, low-power-device, browser
  compatibility, screenshot, asset-quality, or human-evaluation gates.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.2.
- `assets/registry/audio-assets.json` and `gui/audio-catalog.json`.
- `assets/README.md`, `ARCHITECTURE.md`, `SPEC.md`, and `LESSONS.md`.
- User-authorized continuation of the roadmap loop, bounded to the next
  unmet technical slice.

## Expected files

- `assets/audio-packaging-scope.json`
- `scripts/check_audio_packaging.py`
- `tests/test_audio_packaging.py`
- `_workspace/02_presentation_contract.md`
- `_workspace/03_presentation_qa.md`
- roadmap, canonical records, lessons, changelog, release metadata, and
  handoff projections for v0.13.1.

## Validation target

The report must pass with zero release audio files, zero release audio bytes,
and explicit runtime-generated entries. A temporary release audio file,
unsupported path, malformed scope, or non-null release path must fail closed.
Run the focused Python test, the checker CLI, Rust formatting/tests, asset and
release metadata checks, and the project visual/audio contract audit.

## Generic skills

`simple-code-writer`, `preferred-workflow`, `plan-designer`, and one
`code-reviewer` are used for implementation and handoff. The repo-local
presentation contract designer and presentation domain QA are used because the
  slice changes presentation asset governance, not the live simulation.

---
# Request Summary — Visual/audio Phase 11.2 loading-policy audit v0.13.2

## Scope

Address the next Phase 11.2 packaging gaps for lazy loading and preloading.
The current live GUI renders the regional scene as inline/generated SVG and
uses runtime-generated Web Audio, with no file-backed asset tags or preload
directives. Add a machine-checked loading policy that records the current
no-lazy/no-preload decision and fails closed if future file-backed presentation
assets appear without explicit high-value loading metadata.

## Non-goals

- Do not change the live browser loading path, host adapter, simulation, or
  audio behavior.
- Do not add lazy-loading or preload code where the current surface has no
  file-backed asset demand.
- Do not claim browser, cache, decode, memory, device, offline, or human
  performance evidence.
- Do not close offline, low-power-device, compatibility, screenshot, asset
  quality, human-evaluation, or full-campaign coverage gates.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.2.
- `gui/index.html`, `gui/app.mjs`, `gui/scene.mjs`, and `gui/audio.mjs`.
- `assets/audio-packaging-scope.json`, visual/audio registries, and the
  current release tree.
- User-authorized continuation of the roadmap loop, bounded to the next
  actionable packaging slice.

## Expected files

- `assets/loading-policy.json`
- `scripts/check_loading_policy.py`
- `tests/test_loading_policy.py`
- `_workspace/02_presentation_contract.md`
- `_workspace/03_presentation_qa.md`
- roadmap, canonical records, lessons, changelog, release metadata, and
  handoff projections for v0.13.2.

## Validation target

The report must pass with zero live preload directives and zero file-backed
asset-loading markers in the current live entrypoint/modules. A temporary
preload tag, file-backed media reference, unlisted loading source, malformed
policy, or path escape must fail closed. Run focused Python tests, full Rust and
Python checks, asset/release checks, documentation links, and the visual/audio
contract audit.

## Generic skills

`simple-code-writer`, `preferred-workflow`, `plan-designer`, and one
`code-reviewer` remain in use. The repo-local presentation contract designer
and presentation domain QA apply because this slice governs actor-visible
asset loading without changing simulation authority.

---

# Request Summary — Visual/audio Phase 11.2 browser compatibility matrix v0.13.5

## Scope

Close the Phase 11.2 browser-compatibility evidence item for the current
dependency-free loopback GUI. Document one supported evergreen Chromium
desktop target, explicitly list non-certified engines, and audit the existing
loading/offline policies, JavaScript syntax, and presentation-only boundary.

## Non-goals

- Do not claim Firefox/WebKit certification, universal browser support, or
  low-power-device suitability.
- Do not add a browser framework, service worker, external asset, or network
  dependency.
- Do not change simulation, host authority, commands, stochastic inputs,
  history, hashes, replay, debrief, or audio semantics.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.2 compatibility gate.
- `assets/loading-policy.json` and `assets/offline-policy.json`.
- `gui/index.html`, the declared live module graph, and `src/gui_server.rs`.
- Existing `_workspace/02_presentation_contract.md` handoff records.
- User-authorized continuation of the roadmap loop.

## Expected files

- `assets/browser-compatibility-policy.json`
- `scripts/check_browser_compatibility.py`
- `tests/test_browser_compatibility.py`
- CI, release metadata, changelog, roadmap, SDD, and final QA evidence.

## Validation target

The matrix must be schema-valid and deterministic. Its supported target must
list every required capability exactly once, optional capabilities must have
visible fallbacks, the compatibility entrypoint must match the loading policy,
and all current live modules must pass syntax and authority-boundary checks.
The available local browser must load the host-served GUI and expose the
documented written/text fallbacks.

## Generic skills

Use `preferred-workflow`, `spec-driven-developer`, `simple-code-writer`,
`fp-developer`, and exactly one `code-reviewer` handoff. Use the presentation
contract and presentation QA skills because this slice governs actor-visible
fallbacks and replay-safe delivery boundaries.

---
# Request Summary — Visual/audio Phase 11.2 offline package completeness v0.13.3

## Scope

Close the Phase 11.2 offline-operation gate for the live GUI from a normal
checkout. The loopback Rust GUI host currently embeds the entrypoint and only
part of the local module graph; add the missing embedded module/catalog routes
and a deterministic audit proving that the live graph is served locally.

## Non-goals

- Do not add a service worker, CDN, browser cache, or external dependency.
- Do not change the host API, simulation, command validation, history, replay,
  debrief, or audio semantics.
- Do not claim offline support for proof pages, external documentation, or a
  deployed production environment.
- Do not claim browser/device compatibility or human usability evidence from a
  static package audit.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.2 offline operation.
- `src/gui_server.rs`, `gui/index.html`, `gui/host-adapter.mjs`, and the
  v0.13.2 live loading-policy module graph.
- User-authorized continuation of the roadmap loop, bounded to the next
  actionable offline package slice.

## Expected files

- `assets/offline-policy.json`
- `scripts/check_offline_availability.py`
- `tests/test_offline_availability.py`
- `src/gui_server.rs`
- `_workspace` request/contract/QA/plan/handoff records, roadmap, canonical
  docs, lessons, changelog, and version projections for v0.13.3.

## Validation target

Every live entrypoint module and catalog must have a repository-embedded local
route in the loopback GUI host. Missing route coverage, external source,
non-loopback binding, path escape, or malformed policy must fail closed. Run
focused and full Python/Rust checks plus release, asset, documentation, and
visual/audio contract audits.

## Generic skills

`simple-code-writer`, `preferred-workflow`, `plan-designer`, and one
`code-reviewer` remain in use. The repo-local presentation contract designer
and presentation domain QA apply because this slice changes the actor-visible
delivery boundary without changing simulation authority.

---

# Request Summary — Visual/audio Phase 11.1 facility asset coverage v0.13.6

## Scope

Close only the Phase 11.1 `Facility asset coverage complete` item by joining
the live file-backed facility catalog to source SVGs, release SVGs, and
approved visual registry entries with exact hashes. Preserve the generic
facility fallback as a no-asset boundary.

## Non-goals

- Do not add new facility art or change runtime rendering, host DTOs,
  simulation, audio, history, hashes, replay, debrief, or campaign placement.
- Do not claim full campaign placement/use, screenshot, device, browser,
  accessibility, or human visual-quality evidence.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.1.
- `gui/facility-components.mjs` and
  `assets/registry/visual-assets.json`.
- User-authorized continuation of the roadmap loop, bounded to the next
  actionable technical coverage slice.

## Expected files

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `tests/test_phase11_campaign_coverage.py`
- `_workspace` plan/contract/QA/handoff records, roadmap, SDD, lessons,
  changelog, and version projections for v0.13.6.

## Validation target

Every file-backed facility has existing source/release paths, maps exactly once
to `visual.facility.<id>`, and has approved registry hashes. The generic
fallback has no asset paths. Run focused/full Python and Rust checks plus
release, asset, security, documentation, and visual/audio audits.

## Generic skills

Use `preferred-workflow`, `spec-driven-developer`, `simple-code-writer`,
`fp-developer`, and exactly one `code-reviewer` handoff. Use presentation
contract and presentation-domain QA because this slice governs actor-visible
asset/fallback coverage without changing simulation authority.

---

# Request Summary — Visual/audio Phase 11.1 event-cue coverage v0.13.7

## Scope

Close only the current Phase 11.1 event-cue coverage item by proving exact
parity among the eight event-channel entries in `AUDIO_CUE_CONTRACT`, the host
`visible_event_cue_ids` projection, and the legacy visible-only
`visibleEventCues` fallback.

## Non-goals

- Do not add cues, recorded audio, host events, simulation rules, or client
  authority.
- Do not claim broader event taxonomy, audio usefulness/fatigue, music
  continuity, screenshots, device/browser compatibility, accessibility, or
  human quality evidence.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.1.
- `gui/audio-cue-contract.mjs`, `gui/audio.mjs`, and
  `src/mcp/resolution.rs`.
- User-authorized continuation of the roadmap loop, bounded to the next
  actionable technical coverage slice.

## Expected files

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `tests/test_phase11_campaign_coverage.py`
- `_workspace` plan/contract/QA/handoff records, roadmap, SDD, lessons,
  changelog, and version projections for v0.13.7.

## Validation target

The event-channel catalog, host projection, and browser fallback must contain
the same eight IDs exactly once. Every cue must retain a visible trigger source,
text equivalent, and cues-only metadata; explicit empty and unknown paths stay
safe. Run focused/full Python and Rust checks plus release, asset, security,
documentation, and visual/audio audits.

## Generic skills

Use `preferred-workflow`, `spec-driven-developer`, `simple-code-writer`,
`fp-developer`, and exactly one `code-reviewer` handoff. Use presentation
contract and presentation-domain QA because this slice governs actor-visible
audio equivalents without changing simulation authority.

---

# Request Summary — Visual/audio Phase 11.1 music-state coverage v0.13.8

## Scope

Close only the current Phase 11.1 music-state coverage item by proving parity
among all seven `MUSIC_STEM_CONTRACT` states, the six host resolution states,
and the browser-only `menu` state.

## Non-goals

- Do not add stems, audio assets, timing, host events, simulation rules, or
  client-owned authority.
- Do not claim broader campaign music taxonomy/continuity, musical usefulness,
  fatigue, screenshots, device/browser compatibility, accessibility, or human
  quality evidence.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.1.
- `gui/music-stem-contract.mjs` and `src/mcp/resolution.rs`.
- User-authorized continuation of the roadmap loop, bounded to the next
  actionable technical coverage slice.

## Expected files

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `tests/test_phase11_campaign_coverage.py`
- `src/mcp/resolution.rs` runtime fixture assertions.
- `_workspace` plan/contract/QA/handoff records, roadmap, SDD, lessons,
  changelog, and version projections for v0.13.8.

## Validation target

Every state has visible source, text-equivalent, fallback, and ordered stem
metadata. The host emits only its six allowlisted resolution states; the
browser classifier covers all seven with `menu` explicit. Run focused/full
Python and Rust checks plus release, asset, security, documentation, browser,
and visual/audio audits.

## Generic skills

Use `preferred-workflow`, `spec-driven-developer`, `simple-code-writer`,
`fp-developer`, and exactly one `code-reviewer` handoff. Use presentation
contract and presentation-domain QA because this slice governs actor-visible
audio state semantics without changing simulation authority.

---

# Request Summary — Visual/audio Phase 11.1 history-view coverage v0.13.9

## Scope

Close only the current Phase 11.1 `History view updated` checklist item by
recording and testing the existing live `competitive-history-v1` host-to-browser
handoff. Preserve aligned turn/state-hash rows, text-first rendering, and the
last valid view when a history read fails.

## Non-goals

- Do not change the history store, transition logic, hash generation, replay
  semantics, save/load persistence, host authority, or simulation behavior.
- Do not claim full campaign history/debrief coverage, durable save/load/replay
  continuity, screenshots, device/browser compatibility, accessibility, or
  human quality evidence.

## Sources and authorization

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.1.
- `src/mcp/session.rs`, `src/gui_server.rs`, `gui/host-adapter.mjs`,
  `gui/app.mjs`, and `tests/test_phase11_live_history.py`.
- User-authorized continuation of the roadmap loop, bounded to this next
  technical coverage slice.

## Expected files

- `_workspace/100_implementation_plan_visual-audio-phase11-history-v0.13.9.md`
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `tests/test_phase11_campaign_coverage.py`
- Roadmap, SPEC, presentation contract/QA, lessons, changelog, and v0.13.9
  release projections.

## Validation target

The ledger and focused campaign test must bind the host schema/route to the
browser adapter/renderer, prove aligned rows and explicit failure recovery, and
retain the read-only boundary. Run focused/full Python and Rust checks plus
release, asset, security, documentation, browser, and visual/audio audits.

## Generic skills

Use `preferred-workflow`, `spec-driven-developer`, `simple-code-writer`,
`fp-developer`, and exactly one `code-reviewer` handoff. Use presentation
contract and presentation-domain QA because this slice governs actor-visible
history without changing simulation authority.

---

# Request Summary — Phase 8.3 reproducible distribution v0.13.10

## Scope

Define the canonical reproducible distribution path as an exact Git
source-checkout built with stable Rust/Cargo. Document required tracked inputs,
CLI and loopback-GUI support boundaries, first-build dependency access, and
the existing read-only validation commands.

## Non-goals

- Do not add runtime, simulation, GUI, MCP, history, replay, asset, or CI
  behavior.
- Do not add prebuilt binaries, archives, installers, containers, registry
  publication, release tags, hosted deployment, or external runtime assets.
- Do not claim Firefox/WebKit certification, low-power-device support, human
  accessibility, usability, learning, or classroom effectiveness.

## Sources and authorization

- `docs/roadmap.md`, Phase 8 initial-release preparation.
- `README.md`, `docs/guides/contributor-release-check.md`,
  `assets/offline-policy.json`, and `assets/browser-compatibility-policy.json`.
- User-authorized continuation of the roadmap loop, bounded to the v0.13.10
  release/documentation slice.

## Expected files

- `docs/guides/reproducible-distribution.md` and contributor documentation
  links.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`,
  `docs/roadmap.md`, and `LESSONS.md`.
- This request summary, an implementation plan, and the final handoff under
  `_workspace/`.

## Validation target

Version metadata, documentation links, existing release/asset/offline/browser
audits, Python tests, formatting, Clippy, and Rust tests pass without tracked
generated-file changes. The PR must merge to `main`, and its temporary branch
must be absent locally and remotely after verified merge.

## Generic skills

Use `preferred-workflow`, `spec-driven-developer`, `simple-code-writer`, and
the independent `code-reviewer` loop. No simulation, mechanism, or
presentation-contract skill is required because this slice changes no runtime
or actor-visible behavior.
# Request Summary — Visual/audio Phase 11.2 low-power profile evidence v0.13.11

## Scope

Continue the visual/audio roadmap with the next technically verifiable unmet
item: Phase 11.2 `Low-power device test completed`. Define and check one
bounded reduced-capability browser profile for the current dependency-free
loopback GUI, using the local browser smoke measurement available in this
environment.

## Target slice

- Profile: 1024×768 viewport, reduced-motion preference, audio off, optional
  local storage unavailable, loopback-only host.
- Evidence: static live-file source audit plus local browser smoke measurements
  for initial shell reload, host-session start, and adapter command response.
- Pass/fail: source size, DOM/SVG surface, and local wall-clock measurements
  remain under explicit conservative limits.

## Sources

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.2.
- `assets/loading-policy.json` and `assets/browser-compatibility-policy.json`.
- `gui/index.html` and the current live module graph.
- Local browser smoke measurement at `http://127.0.0.1:7878/`.

## Expected files

- `assets/device-performance-policy.json`
- `scripts/check_device_performance.py`
- `tests/test_device_performance.py`
- `_workspace/02_presentation_contract.md`
- `_workspace/03_presentation_qa.md`
- `_workspace/105_implementation_plan_visual-audio-phase11-low-power-v0.13.11.md`
- Roadmap, `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`, and
  `_workspace/final/handoff.md`.

## Non-goals and evidence limits

- Do not add a browser dependency, runtime performance instrumentation, or a
  device farm.
- Do not claim real low-power hardware certification, battery impact, thermal
  behavior, lived accessibility, or human usability.
- Do not change simulation, host projections, audio semantics, assets, or
  browser authority boundaries.

## Validation target

`python3 scripts/check_device_performance.py`, focused Python tests, the full
Python suite, Rust format/tests/Clippy, release/documentation/asset checks, and
one presentation QA record. A passing result closes only the bounded Phase
11.2 low-power-profile evidence item; real-device validation remains explicit
follow-up evidence.

# Request Summary — Visual/audio Phase 11.1 operational-overlay coverage v0.13.12

## Scope

Continue the visual/audio roadmap with the next technically verifiable unmet
item: current supported operational-overlay coverage in the live competitive
regional-world projection. The catalog already contains twelve entries, while
the host currently binds only five.

## Target slice

- Bind all twelve registered operational-overlay IDs to direct visible
  `PlayerObservation` fields or explicit visible market/policy/project text.
- Preserve raw metric overlays, host authority, written equivalents, static
  reduced-motion behavior, non-color semantics, and generic unknown fallback.
- Record exact catalog-to-host condition coverage in the Phase 11.1 ledger.

## Sources

- `docs/visual_audio_enhancement_roadmap.md`, Phase 11.1.
- `gui/operational-overlays.mjs` and the existing regional-board/browser
  resolver.
- `src/mcp/regional_world.rs` and `PlayerObservation` visible fields.
- `tests/test_phase11_live_operational_overlays.py` and
  `tests/test_phase11_campaign_coverage.py`.

## Expected files

- `src/mcp/regional_world.rs`
- `gui/operational-overlays.mjs`
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `tests/test_phase11_live_operational_overlays.py`
- `tests/test_phase11_campaign_coverage.py`
- `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  `_workspace/106_implementation_plan_visual-audio-phase11-overlay-v0.13.12.md`,
  and `_workspace/final/handoff.md`.
- Roadmap, `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`, and
  patch-version projections.

## Non-goals and evidence limits

- Do not add hidden-state thresholds, inferred severity/intent/causality,
  simulation mechanics, new assets/audio, browser dependencies, persistence,
  screenshot tooling, or human evaluation.
- Do not claim full campaign placement/use, screenshot, accessibility, or
  educational completion from catalog/projection parity.

## Validation target

Focused Rust/browser/ledger tests, full Python/Rust/Clippy checks, release,
documentation, asset, offline, browser-policy, and visual/audio contract checks.
The bounded result closes only current supported operational-overlay coverage.

# Request Summary — Visual/audio Phase 11.1 terminal debrief coverage v0.13.13

## Scope

Continue the roadmap with the next unmet Phase 11.1 checklist item: `Debrief
view updated`. Formalize the existing competitive terminal debrief host/browser
handoff as a dedicated coverage record.

## Target slice

- Record the `competitive-end-session-v1` schema, loopback route, adapter,
  browser validator/renderer, history-row contract, replay metadata, and
  host-authored written debrief lines.
- Verify terminal action disablement and failure-preserving validation through
  the existing focused terminal-debrief test.
- Close only current competitive terminal debrief coverage; keep full-campaign,
  instructor, counterfactual, human, and educational claims open.

## Sources and expected files

- `src/mcp/session.rs`, `src/gui_server.rs`, `gui/host-adapter.mjs`, and
  `gui/app.mjs` existing terminal handoff.
- `tests/test_phase11_live_debrief.py` and
  `docs/evaluation/phase11.1-campaign-coverage-ledger.json`.
- `tests/test_phase11_campaign_coverage.py`, roadmap/spec/architecture/
  changelog/lessons, version projections, and additive presentation handoffs.

## Non-goals and validation

- Do not add debrief content, runtime fields, persistence, replay regeneration,
  instructor exports, screenshots, browser dependencies, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 stabilization tutorial presentation v0.13.25

## Scope

Record the current five-turn stabilization beginner/tutorial presentation and
its boundary from the shared campaign-coverage renderer and live GUI launcher.

## Target slice

- Bind the CLI beginner menu, five-turn/three-choice fields, player guide,
  beginner tests, written equivalents, and host-owned command boundary.
- Record that the shared GUI can render supplied stabilization coverage while
  the current live GUI launcher remains competitive-only.
- Close only current stabilization tutorial-presentation evidence.

## Sources and expected files

- `src/cli/beginner.rs`, `src/cli/beginner_tests.rs`,
  `docs/guides/how-to-play.md`, `gui/README.md`, and the campaign inventory.
- New tutorial ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive presentation
  contract/QA/handoff records.

## Non-goals and validation

- Do not add browser stabilization integration, tutorial copy, direct audio,
  assets, screenshots, persistence, instructor views, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 current pressure-state registration v0.13.24

## Scope

Register the current actor-visible pressure/recovery taxonomy across existing
operational overlays, statuses, optional event cues, and music states.

## Target slice

- Bind eight visible-field categories to exact source IDs and written,
  non-color, reduced-motion, fallback, and optional-audio boundaries.
- Keep campaign-specific pressure registration empty and name open tutorial,
  direct audio mapping, quality, and human-review work.
- Close only current shared pressure-state registration evidence.

## Sources and expected files

- `gui/operational-overlays.mjs`, `gui/visual-catalog.json`,
  `gui/audio-cue-contract.mjs`, `gui/music-stem-contract.mjs`, and the
  current Phase 12 campaign inventory.
- New pressure-state ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive presentation
  contract/QA/handoff records.

## Non-goals and validation

- Do not add pressure mechanics, hidden-state fields, campaign-specific IDs,
  direct audio mapping, tutorial copy, animation, assets, screenshots,
  instructor views, persistence, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 campaign map/facility asset-need decision v0.13.23

## Scope

Identify current map/facility needs for `stabilization-v1` and
`regional-affiliation-v1` and record the bounded no-new-asset decision.

## Target slice

- Join the decision to the current campaign inventory, reuse matrix, facility
  catalog, and generic fallback test.
- Record text-complete equivalents and future reopen triggers for geography,
  placement, and causal legibility.
- Close only the current Phase 12.1 and 12.2 map/facility-needs items.

## Sources and expected files

- Current campaign inventory/reuse ledgers, `gui/facility-components.mjs`, and
  `tests/test_asset_fallback.py`.
- New asset-need decision/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive presentation
  contract/QA/handoff records.

## Non-goals and validation

- Do not create or promote map, facility, portrait, stage-art, raster, audio,
  or registry assets; do not add placement, runtime, screenshot, persistence,
  instructor, quality, or human-review behavior.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 campaign presentation reuse matrix v0.13.22

## Scope

Record exact reuse decisions for existing visual, generated-audio, facility,
fallback, and written-equivalent primitives across the current stabilization
and regional-affiliation campaign surfaces.

## Target slice

- Bind shared identity, semantic-marker, status, facility-fallback, UI-cue,
  stabilization-audio, and affiliation-audio catalog IDs.
- Record `current-contract-eligible`, `fallback-only`, and
  `eligible-but-not-directly-mapped` decisions without claiming direct audio
  mapping or campaign-specific quality.
- Close only the Phase 12.1 and 12.2 reusable-assets checklist items.

## Sources and expected files

- `gui/visual-catalog.json`, `gui/audio-catalog.json`,
  `gui/facility-components.mjs`, and the current Phase 12 inventory ledger.
- New reuse matrix/parity test, existing asset/provenance/accessibility/audio
  tests, and the campaign-coverage contract.
- Roadmap/spec/architecture/changelog/lessons, version projections, generated
  credits, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not create or promote map, facility, portrait, stage-art, or file-backed
  audio assets; do not add direct audio mapping, tutorial, pressure, stage,
  persistence, instructor, screenshot, or human-review behavior.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 campaign-specific presentation inventory v0.13.21

## Scope

Record the current campaign-specific presentation inventory for the existing
`stabilization-v1` and `regional-affiliation-v1` campaign-coverage surface.

## Target slice

- Bind the current campaign IDs and shared briefing, metric, actor, process,
  decision, history/replay, debrief, and optional-audio host/browser sources.
- Record the current abstract/stage boundary that requires no new map or
  facility asset, while preserving open tutorial, pressure-state, stage-art,
  campaign-audio, replay/debrief, and human-review work.
- Keep the slice design/evidence-only: no runtime, asset, audio, authority,
  screenshot, true-state, or educational behavior changes.

## Sources and expected files

- `src/mcp/campaign_coverage.rs`, `src/mcp/session.rs`, `src/mcp/server.rs`,
  and `gui/app.mjs` existing campaign-coverage contract.
- `tests/test_gui_campaign_coverage.py`, accessibility/audio tests, asset
  validators, and the new Phase 12 campaign presentation ledger/test.
- Roadmap/spec/architecture/changelog/lessons, version projections, generated
  credits, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not create campaign art/audio, tutorial or pressure-state mechanics,
  stage animation, durable replay, instructor true-state views, screenshots,
  browser dependencies, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Phase 13.1 current technical-release coverage v0.13.20

## Scope

Aggregate the current source-checkout technical evidence into one bounded
Phase 13.1 contract without calling it public-release readiness.

## Target slice

- Join current Rust and Python/GUI suites, screenshot/structural regression,
  asset/license/hash/security, accessibility-contract, offline, Chromium,
  replay, and in-memory checkpoint evidence.
- Record commands, source paths, and narrower limits for each check.
- Keep product/content completion, full-campaign raster coverage, durable
  persistence, cross-browser/device certification, human review, educational
  readiness, and release approval open.

## Sources and validation

- `docs/evaluation/phase13.1-technical-coverage.json` and
  `tests/test_phase13_technical_coverage.py`.
- Existing Rust/Python tests, asset/generation/release validators, offline,
  browser/device, replay, checkpoint, and screenshot ledgers.
- Run full Python/Rust/lint/release/documentation/generation/asset/offline/
  browser/device/visual-audio checks.

## Non-goals

Do not add a release artifact, campaign content, screenshot runner, browser
engine, durable storage, human evaluation, educational pilot material, or new
authority path.

# Request Summary — Phase 8.2 current portrait-preview inventory integrity v0.13.18

## Scope

Record the current seven fictional actor portrait previews as a bounded
inventory/source-integrity contract. Preserve their unverified, pending,
unreleased state and do not infer approval from preserved bytes or hashes.

## Target slice

- Bind the seven canonical role IDs to seven repository-relative source PNGs,
  source hashes, square dimensions, written equivalents, and generic
  fallbacks.
- Bind the same IDs to the seven pending review-queue entries and empty
  generation manifest.
- Close only current preview-inventory/source-hash integrity; human review,
  model/seed provenance, quality, legal, release, registry, and runtime gates
  remain open.

## Sources and expected files

- `assets/generation/portrait-set.json`, `portrait-previews.json`,
  `portrait-review-queue.json`, and `generation-manifest.json`.
- `tests/test_portrait_workflow.py`, `scripts/validate_generation_metadata.py`,
  and `docs/evaluation/portrait-preview-coverage.json`.
- Roadmap/spec/architecture/changelog/lessons, version projections, generated
  credits, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not generate or modify portrait bytes, add model/seed metadata, approve
  human review, create release derivatives, add registry IDs, wire portraits
  into the GUI, or claim legal/accessibility/quality approval.
- Run focused/full Python and Rust checks plus generation, release,
  documentation, asset, offline, browser-policy, device-policy, and
  visual/audio checks.

# Request Summary — Phase 8.2 current portrait metadata gates v0.13.19

## Scope

Close only the three current machine-checkable portrait metadata gates:
defined role, preserved source preview, and written accessible equivalent.

## Target slice

- Require all seven role definitions to retain IDs, labels, families, and
  generic fallbacks.
- Require all seven preview source paths to exist and match SHA-256 hashes.
- Require all seven previews to retain non-empty identity-only equivalents and
  generic fallbacks.
- Keep prompt/seed, derivative, identity, quality, lived accessibility,
  legal, release, registry, runtime, and human-review gates open.

## Sources and validation

- `assets/generation/portrait-set.json`, `portrait-previews.json`, and
  `docs/evaluation/portrait-preview-coverage.json`.
- `tests/test_portrait_workflow.py` and existing generation/release validators.
- Run full Python/Rust/lint/release/documentation/generation/asset/offline/
  browser/device/visual-audio checks.

## Non-goals

Do not modify portrait bytes or generation records, add model/seed claims,
create derivatives, perform human review, approve release/registry promotion,
or integrate portraits into runtime.

# Request Summary — Visual/audio Phase 11.1 current screenshot-surface contract v0.13.17

## Scope

Continue the roadmap's screenshot gate with a bounded contract for the current
supported actor-visible GUI surface. The local browser smoke path is evidence
of live composition, while deterministic SVG and structural tests remain the
repeatable regression boundary.

## Target slice

- Record the executive desktop shell, briefing/regional board, deterministic
  regional scene, decision/consequence views, and
  resolution/history/replay/debrief views.
- Link each surface to its GUI source, deterministic/structural/live-handoff
  tests, and local browser smoke evidence.
- Close only current supported screenshot-surface evidence; keep full-campaign
  raster goldens, cross-browser/device capture, pixel-level quality,
  accessibility quality, and human review open.

## Sources and expected files

- `gui/index.html`, `gui/app.mjs`, `gui/regional-board.mjs`, existing GUI
  surface modules, and the local loopback browser route.
- `tests/test_phase11_campaign_coverage.py`, the regional SVG snapshot test,
  structural GUI tests, live handoff tests, and playtest/accessibility/audio
  checks.
- The Phase 11.1 ledger, roadmap/spec/architecture/changelog/lessons,
  version projections, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not add PNG/JPEG goldens, a browser dependency, screenshot uploads,
  telemetry, new campaign states, runtime transitions, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation,
  offline, browser-policy, device-policy, and visual/audio contract checks.

## Evidence boundary

The local browser capture is inspected but not persisted or hashed. The ledger
does not claim that a single desktop viewport establishes full-campaign
coverage, pixel-level quality, accessibility quality, device compatibility, or
human comprehension.

# Request Summary — Visual/audio Phase 11.1 current asset-registry coverage v0.13.16

## Scope

Continue the roadmap with the next unmet Phase 11.1 item: asset registry
coverage. Formalize completeness of the current tracked visual and audio
registry documents as a bounded release/presentation contract.

## Target slice

- Record all 38 visual and 7 audio entries, approval/ID closure, and the
  `asset-registry-v1` source documents.
- Distinguish 15 file-backed release paths from 30 intentional null-release
  runtime/catalog entries and link registry, release, security, and credits
  checks.
- Close only current tracked registry completeness; future campaign inventory,
  placement/use, asset/audio quality, screenshots, and human claims remain open.

## Sources and expected files

- `assets/registry/visual-assets.json`, `assets/registry/audio-assets.json`,
  `scripts/validate_assets.py`, `scripts/verify_asset_release.py`,
  `scripts/validate_asset_security.py`, and
  `scripts/generate_asset_credits.py`.
- `tests/test_asset_registry.py`, `tests/test_phase11_campaign_coverage.py`,
  and the Phase 11.1 ledger.
- Roadmap/spec/architecture/changelog/lessons, version projections, generated
  credits, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not add/remove assets, promote runtime-generated audio, create screenshots,
  add browser dependencies, or make quality/human-evaluation claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  security, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 11.1 replay visual continuity v0.13.15

## Scope

Continue the roadmap with the next unmet Phase 11.1 item: replay visual
continuity. Formalize the existing live competitive replay metadata/history
projection as a bounded presentation contract.

## Target slice

- Record the `competitive-replay-v1` host/MCP envelope, loopback route, adapter,
  browser validation/renderer, immutable visible rows, and aligned metadata.
- Verify empty and committed views, hash/count alignment, and last-valid-view
  preservation on missing or failing reads through the existing replay test.
- Close only current live replay visual continuity; playback, regeneration,
  durable persistence, screenshots, and human claims remain open.

## Sources and expected files

- `src/mcp/session.rs`, `src/mcp/server.rs`, `src/gui_server.rs`,
  `gui/host-adapter.mjs`, and `gui/app.mjs` existing replay handoff.
- `tests/test_phase11_live_replay.py`,
  `tests/test_phase11_campaign_coverage.py`, and the Phase 11.1 ledger.
- Roadmap/spec/architecture/changelog/lessons, version projections, generated
  credits, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not add playback controls, replay regeneration, durable serialization,
  browser storage, new runtime fields, screenshots, assets, audio, browser
  dependencies, telemetry, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 11.1 checkpoint visual continuity v0.13.14

## Scope

Continue the roadmap with the next unmet Phase 11.1 item: save/load visual
continuity. Formalize the existing in-memory host checkpoint save/restore view
as a bounded presentation contract.

## Target slice

- Record the `competitive-save-v1` host/MCP envelope, loopback routes, adapter,
  browser validation, presentation refresh, and aligned transition/hash metadata.
- Verify missing/failing checkpoint and refresh paths preserve a recoverable
  current view through the existing focused checkpoint test.
- Close only current in-memory host checkpoint continuity; durable persistence,
  cross-process/browser-refresh recovery, replay, screenshot, and human claims
  remain open.

## Sources and expected files

- `src/mcp/session.rs`, `src/mcp/server.rs`, `src/gui_server.rs`,
  `gui/host-adapter.mjs`, and `gui/app.mjs` existing checkpoint handoff.
- `tests/test_phase11_live_checkpoint.py`,
  `tests/test_phase11_campaign_coverage.py`, and the Phase 11.1 ledger.
- Roadmap/spec/architecture/changelog/lessons, version projections, generated
  credits, and additive presentation contract/QA/handoff records.

## Non-goals and validation

- Do not add durable serialization, browser storage, cross-process recovery,
  replay regeneration/playback, new runtime fields, screenshots, assets, audio,
  browser dependencies, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 stabilization audio-state mapping v0.13.26

## Scope

Map the current eight shared stabilization pressure/recovery categories to
existing optional music, event-cue, and audio-direction contracts.

## Target slice

- Join the pressure-state registration to exact music/cue/direction IDs,
  visible trigger sources, and written equivalents.
- Preserve the text-first CLI tutorial and competitive-only live GUI boundary;
  close only current shared audio-state mapping evidence.

## Sources and expected files

- `docs/evaluation/phase12-pressure-state-registration.json`,
  `gui/music-stem-contract.mjs`, `gui/audio-cue-contract.mjs`,
  `gui/audio-direction.mjs`, and campaign coverage.
- New mapping ledger/parity test, roadmap/spec/architecture/changelog/lessons,
  version projections, generated credits, and additive contract/QA/handoff.

## Non-goals and validation

- Do not add direct campaign-envelope audio, new IDs/files/routes, assets,
  screenshots, persistence, instructor views, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 stabilization debrief presentation v0.13.27

## Scope

Record the current deterministic stabilization debrief across CLI output,
host-authored history/replay/end-session data, shared browser renderers, and
optional-audio fallback.

## Target slice

- Bind run-level tradeoffs, actor rationales, attributed effects, reflection,
  decision/outcome separation, revision notes, and the existing CLI instructor
  appendix to source markers.
- Preserve completion gating, host ownership, written fallback, and the live
  competitive-only GUI boundary; close only current debrief evidence.

## Sources and expected files

- `src/cli/display/interactive.rs`, `src/debrief/report.rs`,
  `src/mcp/campaign_coverage.rs`, `src/mcp/session.rs`, `gui/app.mjs`, and
  `gui/README.md` existing debrief sources/renderers.
- New debrief ledger/parity test, roadmap/spec/architecture/changelog/lessons,
  version projections, generated credits, and additive contract/QA/handoff.

## Non-goals and validation

- Do not add debrief copy, browser routes, runtime fields, persistence, replay
  regeneration, assets, audio files, screenshots, instructor exports, or human
  evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 stabilization accessibility evidence v0.13.28

## Scope

Record current shared technical accessibility checks relevant to stabilization:
keyboard/focus, text/non-color status, text scale, reduced motion, written
equivalents, optional-audio fallback, and semantic campaign coverage.

## Target slice

- Join existing GUI accessibility, first-month, audio-fallback, and campaign
  coverage tests to explicit source markers and passing check entries.
- Preserve local presentation-only settings, text-first stabilization, and the
  competitive-only live GUI boundary; close only technical evidence.

## Sources and expected files

- `tests/test_gui_accessibility.py`, `tests/test_gui_first_month.py`,
  `tests/test_audio_fallback.py`, `tests/test_gui_campaign_coverage.py`,
  `gui/index.html`, `gui/app.mjs`, and the Phase 10 technical-boundary doc.
- New accessibility ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive contract/QA/
  handoff records.

## Non-goals and validation

- Do not add accessibility behavior, a browser stabilization launcher, routes,
  runtime fields, assets, audio files, screenshots, persistence, instructor
  views, screen-reader/device certification, or human evaluation.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  offline, browser-policy, device-policy, and visual/audio contract checks.

# Request Summary — Visual/audio Phase 12 stabilization provenance audit v0.13.29

## Scope

Record current technical provenance for reusable stabilization visual/audio/
facility sources, release checks, the no-new-asset decision, and the
unreleased portrait-preview boundary.

## Target slice

- Join the reuse matrix, asset-need decision, visual/audio catalogs, registries,
  generated credits/notices, release checks, and portrait review boundary.
- Close only current technical provenance evidence while retaining legal,
  human-quality, future-asset, and public-release gates.

## Sources and expected files

- `docs/evaluation/phase12-campaign-reuse-matrix.json`,
  `docs/evaluation/phase12-campaign-asset-need-decision.json`,
  `gui/visual-catalog.json`, `gui/audio-catalog.json`, asset registries,
  credits, notices, and validation scripts.
- New provenance ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive contract/QA/
  handoff records.

## Non-goals and validation

- Do not promote portrait previews or add assets, audio files, registry entries,
  routes, screenshots, runtime fields, legal clearance, human review, or
  public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio bounded content boundary QA v0.13.51

## Scope

Review current player-facing policy/safety wording and browser presentation
sources for unsupported clinical implications, false precision, and
actor-observation boundary drift. Record a bounded QA result without adding
runtime behavior or claiming human or expert approval.

## Target slice

- Verify the fictional educational-simulation and non-forecast boundary is
  visible beside first-session guidance.
- Check current GUI modules for unsupported clinical-advice language.
- Preserve source/status, written precision, fallback, host authority, and
  hidden-state boundaries.

## Sources and expected files

- `README.md`, `docs/guides/gui-how-to-play.md`, `gui/*.mjs`, `gui/index.html`,
  `gui/metric-visualization-proof.html`, and `gui/semantic-containers.mjs`.
- New `docs/evaluation/phase13.1-content-boundary-qa.json` and
  `tests/test_phase13_1_content_boundary_qa.py`.
- Additive domain/presentation QA, contract, handoff, roadmap, SDD, changelog,
  and release-metadata updates.

## Non-goals and validation

- Do not add assets, portraits, audio, routes, commands, host fields,
  simulation rules, stochastic inputs, persistence, replay changes, clinical
  recommendations, policy forecasts, or human approval claims.
- Run the focused QA test plus the repository's full Python/Rust and release,
  documentation, asset, generation, offline, browser/device-policy, and
  visual/audio checks.

# Request Summary — Visual/audio Phase 13.1 limitations statement v0.13.48

## Scope

Add a player-facing limitations statement distinguishing the fictional
educational simulation from calibrated policy forecasting and real-world
operational, clinical, financial, regulatory, or legal advice.

## Target slice

- Bind the guide language to a small release evidence ledger and contract test.
- Preserve actor-visible and host-authoritative boundaries.
- Name remaining human, provenance, browser/device, full-campaign, persistence,
  and public-release gates without claiming they are complete.

## Non-goals and validation

- Do not add runtime behavior, simulation fields, authority paths, assets,
  audio, persistence, or educational approval claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  device, and diff checks.

# Request Summary — Visual/audio vertical-slice technical evidence v0.13.49

## Scope

Join existing live host/browser evidence for the current vertical slice:
competitive board data, facility/report linkage, visible projects, first-month
consequences, and visible-input-driven planning/pressure music.

## Target slice

- Mark only the five bounded technical roadmap items supported by current
  source contracts and tests.
- Record explicit full-campaign, provenance, first-time-user, and human-review
  limits.

## Non-goals and validation

- Do not add hidden state, new authority, new assets/audio, or human approval.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  device, and diff checks.

# Request Summary — Visual/audio hidden-state boundary v0.13.50

## Scope

Record the current browser/DTO technical boundary against simulation-world,
resolved-input, and effect-queue fields.

## Target slice

- Scan current presentation modules and read-only DTO tests for forbidden hidden
  fields and authority paths.
- Mark only the technical hidden-state content gate.
- Keep human content, provenance, accessibility, educational, and public-release
  review separate.

## Non-goals and validation

- Do not expose true state, resolved inputs, private rationale, or new runtime
  fields; do not claim human content approval.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  device, and diff checks.

# Request Summary — Visual/audio Phase 13.2 low-distraction mode v0.13.47

## Scope

Add the dedicated local GUI low-distraction presentation mode already prepared
by the pilot recipe.

## Target slice

- Add a settings toggle that forces reduced motion, Large text, written cue
  explanations, muted audio, and reduced notifications.
- Lock conflicting presentation/audio controls while active and restore the
  prior local preferences when disabled.
- Keep the mode outside host commands, validation, transitions, history, replay,
  persistence, and simulation authority; add source-linked behavior evidence.

## Non-goals and validation

- No new host game mode, observation/debrief route, asset, network path,
  classroom multiplayer, or human accessibility/educational claim.
- Run focused browser-module behavior tests plus the standard Rust, Python,
  metadata, documentation, formatting, clippy, and generated-credit checks.

# Request Summary — Visual/audio Phase 13.2 pilot-preparation boundary v0.13.46

## Scope

Prepare the existing human-evaluation workflow for a bounded classroom or
facilitated pilot without recording participant results or making a go/no-go
claim.

## Target slice

- Add facilitator preflight, classroom hardware assumptions, audio guidance,
  accessibility accommodations, low-distraction recipe boundaries, and
  screenshot/recording consent guidance to the existing evaluation guide.
- Add a structured privacy-preserving feedback instrument with task states,
  ratings, finding categories, and a pending human decision field.
- Source-link the preparation evidence and update only the feasible Phase 13.2
  documentation checklist items.

## Non-goals and validation

- Do not add participant results, raw media, personal data, human approval,
  educational-effectiveness claims, or a dedicated runtime low-distraction
  mode in this slice.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, and presentation-boundary checks.

# Request Summary — Visual/audio Phase 13.1 player-facing settings/help boundary v0.13.45

## Scope

Make the existing live GUI settings, optional audio controls, reduced-motion
and text-scale choices, credits disclosure, and troubleshooting path
discoverable for first-time players and facilitators.

## Target slice

- Update the existing GUI guide with the settings panel's current controls,
  storage/fallback behavior, audio channel choices, credits disclosure, and
  actionable recovery steps.
- Source-link the guide to the existing DOM controls, presentation settings
  client, audio panel, and asset-credit renderer.
- Preserve local presentation ownership: no host command, transition, replay,
  asset, audio, or authority behavior changes.

## Non-goals and validation

- Do not claim human accessibility, educational usability, audio usefulness,
  classroom readiness, or public-release approval.
- Run the source-linked documentation test plus the standard Rust, Python,
  metadata, documentation, formatting, clippy, and generated-credit checks.

# Request Summary — Visual/audio Phase 12.3 distributional outcome summary v0.13.43

## Scope

Implement the next Phase 12.3 item: represent committed competitive outcomes
by health system in the existing post-run instructor summary.

## Target behavior

Render a stable, text-first table of each system's committed change in access,
quality, workforce trust, community trust, and market share. Label the view
instructor-only/descriptive, keep metrics separate, and never rank systems or
collapse them into a welfare score.

## Non-goals and validation

- No new player-observation field, browser route, asset, audio, export format,
  persistence, or simulation transition.
- No aggregate welfare score, strategy ranking, causal claim, or calibration.
- Do not expose data outside the existing post-run instructor-summary boundary.
- Run focused/full Rust and Python checks plus release metadata, documentation,
  formatting, clippy, and generated-credits checks.

# Request Summary — Visual/audio Phase 12.3 export behavior boundary v0.13.44

## Scope

Document and source-link the existing post-run replay export behavior across
stabilization, competitive, and regional-affiliation CLI paths.

## Target behavior

Record which export format/version each campaign uses, how empty input skips
export, where verification exists, and why exports remain analysis artifacts
rather than mid-run saves or browser authority inputs.

## Non-goals and validation

- No new export format, persistence path, browser download, route, asset, audio,
  simulation, or replay-authority change.
- Do not claim that the competitive JSON export has the same versioned parser
  contract as the stabilization and affiliation replay artifacts.
- Run source-linked Python tests plus the standard Rust, metadata, docs,
  formatting, clippy, and generated-credit checks.

# Request Summary — Visual/audio Phase 12.3 counterfactual difference view v0.13.42

## Scope

Implement the smallest next Phase 12.3 slice: a deterministic, text-first
post-run comparison over existing stabilization `History` values.

## Target behavior

Compare two committed histories from the same genesis, show aligned commands,
committed next-state metric differences, attributed-effect differences, and
resolved-input parity, with written fallbacks for incompatible histories. Make
the view reachable from the existing preset post-run CLI demo.

## Non-goals

- No browser route, instructor authorization route, or new host authority.
- No true-state, resolved-input, or private actor disclosure to the player.
- No causal inference, probability, calibration, strategy ranking,
  distributional claim, asset, audio, dependency, persistence, or export format.

## Sources and validation

- `docs/visual_audio_enhancement_roadmap.md`, Phase 12.3.
- `docs/design_principles.md`, `ARCHITECTURE.md`, and the harness team spec.
- Run focused/full Rust and Python checks plus release metadata, documentation,
  formatting, clippy, and generated-credits checks.

# Request Summary — Visual/audio Phase 12.3 instructor-only authority boundaries v0.13.38

## Scope

Document current instructor/post-run authority boundaries across the
stabilization, competitive, and regional-affiliation contracts without adding
an instructor route or live true-state view.

## Target slice

- Separate player-visible observations from existing post-run CLI/typed
  debrief detail, host ownership, shared read-only rendering, and the
  competitive-only live GUI boundary.
- Record no-new-surface, no-authority-expansion, no-counterfactual,
  no-distributional-view, and human-review limits.

## Sources and expected files

- Existing stabilization debrief ledger, `src/debrief/report.rs`,
  `src/mcp/session.rs`, `gui/app.mjs`, `gui/README.md`, and current campaign
  replay/debrief evidence.
- New authority-boundary ledger/parity test, roadmap/spec/architecture/
  changelog/lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add instructor routes, true-state fields, resolved-input controls,
  counterfactual/distributional views, persistence, screenshots, assets, audio
  files, authority paths, educational claims, or public-release approval.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation provenance audit v0.13.37

## Scope

Record the current machine-checkable provenance boundary for
`regional-affiliation-v1` without promoting assets or claiming legal, human,
training-data, or public-release approval.

## Target slice

- Join reusable visual/audio/fallback catalog and registry sources to registry,
  security, release-manifest, generation-metadata, credits, reuse, asset-need,
  and audio-packaging checks.
- Record third-party/release-audio counts, no-new-asset decision, unreleased
  portrait-preview gate, future reopen triggers, and written/public limits.

## Sources and expected files

- `docs/evaluation/phase12-campaign-reuse-matrix.json`,
  `docs/evaluation/phase12-campaign-asset-need-decision.json`,
  `gui/visual-catalog.json`, `gui/audio-catalog.json`, asset registry/credits,
  portrait review queue, and existing validation scripts/tests.
- New provenance ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add maps, facilities, portraits, stage art, raster, audio, routes,
  runtime assets, authority paths, legal claims, human review claims, or
  public-release approval.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation replay/debrief views v0.13.36

## Scope

Record current technical replay/debrief evidence for
`regional-affiliation-v1` without claiming browser-native affiliation views,
durable persistence, or educational effectiveness.

## Target slice

- Join versioned replay artifact serialization/verification and state/hash
  integrity to host history/replay metadata and terminal debrief content.
- Record decision-quality language, alternative prompt, written history/debrief
  renderers, CLI/export boundary, optional audio, no-new-asset, and live-GUI
  boundaries.

## Sources and expected files

- `src/model/affiliation.rs`, `src/artifact/affiliation.rs`,
  `src/affiliation/transition.rs`, `src/mcp/session.rs`,
  `src/mcp/campaign_coverage.rs`, `src/debrief/report.rs`,
  `src/cli/affiliation.rs`, `gui/app.mjs`, and existing campaign ledgers/tests.
- New replay/debrief ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add browser replay/debrief routes, animation, persistence, screenshots,
  instructor views, assets, audio files, runtime fields, authority paths,
  hidden-state controls, human review, or public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation stage-transition sequence v0.13.35

## Scope

Record the current deterministic host-projected stage sequence for
`regional-affiliation-v1` without claiming browser-native affiliation
sequencing or exposing resolved inputs.

## Target slice

- Join the typed Assess partner → Choose posture → Negotiate commitments →
  Submit review → Resolve review → Integrate or decline → Affiliation complete
  chain to its successor mapping and one-transition advancement contract.
- Record legal command gates, visible stage/process labels, uncertainty,
  committed history/replay alignment, shared-sequence scope, optional audio,
  no-new-asset, and live-GUI boundaries.

## Sources and expected files

- `src/model/affiliation.rs`, `src/affiliation/transition.rs`,
  `src/mcp/campaign_coverage.rs`, `src/mcp/session.rs`, `gui/app.mjs`,
  `gui/resolution-sequence.mjs`, and existing campaign presentation ledgers/
  tests.
- New stage-sequence ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add browser animation, routes, runtime fields, persistence,
  screenshots, instructor views, assets, authority paths, hidden inputs,
  private rationale, human review, or public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation audio motif v0.13.34

## Scope

Record the current reusable affiliation-audio motif for
`regional-affiliation-v1` without claiming direct browser-native campaign
audio integration or adding new audio content.

## Target slice

- Bind the existing `affiliation_negotiation` music state and
  `event.affiliation-milestone` cue to visible affiliation/partner/coalition/
  negotiation/commitment context and committed milestone text.
- Record generated-audio properties, visible triggers, written equivalent,
  audio-off fallback, competitive-only live-GUI boundary, and no-new-asset
  decision.

## Sources and expected files

- `gui/music-stem-contract.mjs`, `gui/audio-cue-contract.mjs`,
  `gui/audio.mjs`, `gui/audio-catalog.json`, `src/mcp/resolution.rs`, and
  existing campaign-presentation, audio, and asset-need ledgers/tests.
- New audio-motif ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add recorded/release audio, new stems/cues/routes/runtime fields,
  registry entries, screenshots, persistence, instructor views, authority
  paths, direct campaign integration, hidden meaning, human listening, or
  public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation partner identity v0.13.30

## Scope

Record the current regional-affiliation partner identity treatment without
promoting an unverified portrait preview or claiming browser-native coverage.

## Target slice

- Join host-reported partner name, condition, stage, and status with the
  existing actor-family/generic fallback, written equivalent, and
  identity-only portrait-preview boundary.
- Close only current partner-identity evidence while retaining partner-specific
  art/audio, browser integration, provenance, legal, human-quality, and
  public-release gates.

## Sources and expected files

- `src/mcp/campaign_coverage.rs`, `gui/actor-families.mjs`,
  `gui/app.mjs`, portrait inventory/generation metadata, and existing
  campaign presentation and asset-need ledgers/tests.
- New partner-identity ledger/parity test, roadmap/spec/architecture/changelog/
  lessons, version projections, generated credits, and additive contract/QA/
  handoff records.

## Non-goals and validation

- Do not add or promote partner art, portraits, audio, routes, screenshots,
  runtime fields, persistence, instructor views, authority paths, or human,
  legal, educational, or public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation negotiation-stage visualization v0.13.31

## Scope

Record current `NegotiateCommitments` stage presentation for
`regional-affiliation-v1` without claiming a browser-native affiliation route,
stage-specific art/audio, or hidden-state access.

## Target slice

- Join the host-owned stage/process label, commitment decision fields, parameter
  bounds, visible commitment values, stakeholder signals, and written
  uncertainty.
- Record the shared process/decision renderer, optional affiliation-negotiation
  audio eligibility, no-new-asset decision, and current live-GUI boundary.

## Sources and expected files

- `src/model/affiliation.rs`, `src/mcp/campaign_coverage.rs`,
  `gui/app.mjs`, `gui/music-stem-contract.mjs`, and existing campaign
  presentation/asset-need ledgers and tests.
- New negotiation-stage ledger/parity test, roadmap/spec/architecture/
  changelog/lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add stage art, maps, facilities, portraits, audio files, routes,
  runtime fields, persistence, screenshots, instructor views, authority paths,
  hidden thresholds, true responses, human review, or public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation commitment and review states v0.13.32

## Scope

Record current host-projected commitment and institutional-review states for
`regional-affiliation-v1` without exposing private review authority or claiming
browser-native affiliation coverage.

## Target slice

- Join visible community/workforce/continuity commitment metrics and partner
  response statuses to the pending institutional-review process, submit/await
  decisions, and reported review response/status values.
- Record shared process/decision rendering, written fallback, optional
  affiliation-negotiation audio, no-new-asset decision, and live-GUI boundary.

## Sources and expected files

- `src/mcp/campaign_coverage.rs`, `src/model/affiliation.rs`,
  `src/affiliation/transition.rs`, `gui/app.mjs`,
  `gui/music-stem-contract.mjs`, and existing campaign presentation and
  asset-need ledgers/tests.
- New commitment/review ledger/parity test, roadmap/spec/architecture/
  changelog/lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add state art, maps, facilities, portraits, audio files, routes,
  runtime fields, persistence, screenshots, instructor views, authority paths,
  private review deliberation, hidden thresholds, legal validity, human review,
  or public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12 regional-affiliation integration-state visualization v0.13.33

## Scope

Record current host-projected integration-state presentation for
`regional-affiliation-v1` without exposing resolved hidden inputs or claiming
browser-native affiliation integration.

## Target slice

- Join the `IntegrateOrDecline` stage, `integration-obligation` process,
  begin/decline decision, visible integrated/declined statuses, and written
  consequence language.
- Record the visible status/effect boundary versus resolved integration drag
  and continuity shock, plus shared renderer, optional audio, no-new-asset,
  and live-GUI boundaries.

## Sources and expected files

- `src/mcp/campaign_coverage.rs`, `src/model/affiliation.rs`,
  `src/affiliation/transition.rs`, `gui/app.mjs`,
  `gui/music-stem-contract.mjs`, and existing campaign presentation and
  asset-need ledgers/tests.
- New integration-state ledger/parity test, roadmap/spec/architecture/
  changelog/lessons, version projections, generated credits, and additive
  contract/QA/handoff records.

## Non-goals and validation

- Do not add integration art, maps, facilities, portraits, audio files, routes,
  runtime fields, persistence, screenshots, instructor views, authority paths,
  hidden integration inputs, private approval basis, human review, or
  public-release claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12.3 true-state language boundary v0.13.39

## Scope

Record the current textual distinction between player-visible observations,
post-run true-state labels, and instructor-only detail without adding a
browser-native true-state view or expanding presentation authority.

## Target slice

- Join source-linked `Observed`, `True Prior`, `True Outcome`, and
  `REVEALED FOR INSTRUCTOR REVIEW` labels to the existing decision-quality
  boundary.
- Record host ownership, read-only shared rendering, written fallback, and
  the competitive-only live-GUI boundary.

## Sources and expected files

- `src/debrief/report.rs`, `docs/evaluation/phase12-instructor-authority-boundaries.json`,
  `gui/app.mjs`, and `gui/README.md`.
- New true-state language-boundary ledger/parity test, roadmap/spec/
  architecture/changelog/lessons, version projections, generated credits,
  and additive contract, QA, and handoff records.

## Non-goals and validation

- Do not add browser routes, true-state fields, player controls, persistence,
  screenshots, assets, audio files, counterfactuals, distributional views,
  export formats, instructor authority paths, or human educational claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12.3 decision-time recovery boundary v0.13.40

## Scope

Record how the existing immutable core/CLI history recovers the observation
available before each command, how host history/replay summaries remain aligned,
and where the current text-first browser summary stops short of full
per-decision observation playback.

## Target slice

- Join the core `Transition` observation/command pairing to debrief timing and
  revision language.
- Record host history/replay count/hash alignment, browser turn/command/hash
  rendering, written fallback, and the competitive-only live-GUI boundary.

## Sources and expected files

- `src/model/history.rs`, `src/debrief/report.rs`, `src/mcp/session.rs`,
  `gui/app.mjs`, and `gui/README.md`.
- New decision-time recovery ledger/parity test, roadmap/spec/architecture/
  changelog/lessons, version projections, generated credits, and additive
  contract, QA, and handoff records.

## Non-goals and validation

- Do not add observation fields, browser timeline controls/routes, persistence,
  screenshots, assets, audio files, true-state views, causal graphs,
  counterfactuals, distributional views, export formats, or human educational
  claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio Phase 12.3 causal attribution boundary v0.13.41

## Scope

Record the existing host-sourced direct-effect and before/after resolution
presentation contract without adding causal inference or expanding authority.

## Target slice

- Join typed `ResolutionEffect` source/metric/delta/text fields to ordered
  before/after, response, process, direct-effect, information, and pending
  resolution stages.
- Record source-linked consequence rendering, descriptive debrief attribution,
  written fallback, and the competitive-only live-GUI boundary.

## Sources and expected files

- `src/mcp/resolution.rs`, `src/debrief/report.rs`, `gui/app.mjs`,
  `gui/consequence-links.mjs`, `gui/README.md`, and the Phase 4 resolution
  contract.
- New causal-attribution ledger/parity test, roadmap/spec/architecture/
  changelog/lessons, version projections, generated credits, and additive
  contract, QA, and handoff records.

## Non-goals and validation

- Do not add causal inference, hidden-state fields, probability/calibration,
  counterfactuals, distributional views, exports, assets, audio files,
  persistence, routes, or human educational claims.
- Run focused/full Python and Rust checks plus release, documentation, asset,
  generation, offline, browser-policy, device-policy, and visual/audio checks.

# Request Summary — Visual/audio technical attribution boundary v0.13.52

## Scope

Record current repository-owned attribution completeness across canonical
visual/audio registries, generated static credits/notices, runtime credits,
release-manifest parity, and the exclusion of unverified portrait previews.

## Target slice

- Verify every current registry entry has attribution, source/generation,
  legal-basis, accessible-equivalent, approval, and hash fields.
- Verify release paths and hashes join the deterministic release manifest and
  generated credits projections.
- Keep portrait previews without approved model/seed metadata and human review
  outside release, registry, and runtime attribution surfaces.

## Sources and expected files

- `assets/registry/*.json`, `assets/ASSET_CREDITS.md`,
  `assets/THIRD_PARTY_NOTICES.md`, `gui/asset-credits.mjs`, and
  `assets/ASSET_RELEASE_MANIFEST.json`.
- `assets/generation/portrait-previews.json` and
  `assets/generation/portrait-review-queue.json`.
- New `docs/evaluation/phase13.1-attribution-boundary.json` and
  `tests/test_phase13_1_attribution_boundary.py`.
- Additive domain/presentation QA, contract, handoff, roadmap, SDD, changelog,
  lessons, and release-metadata updates.

## Non-goals and validation

- Do not promote portraits, add assets/audio, fabricate model/seed metadata,
  change runtime authority, or claim legal, ownership, training-data,
  resemblance, accessibility, educational, or public-release approval.
- Run the focused attribution test plus full Python/Rust, asset, generation,
  security, release, credits, documentation, offline, browser/device-policy,
  and visual/audio contract checks.

# Request Summary — Visual/audio technical first-session boundary v0.13.53

## Scope

Record the current repository-owned first-session path from host-bound
launch/load through actor-visible inspection, contextual drafting and
validation, committed resolution review, continuation, and written recovery.

## Target slice

- Bind launch/load controls and adapter calls to the host authority boundary.
- Bind the seven-stage first-month path to existing GUI sources and tests.
- Preserve written recovery, actor-visible limitations, local presentation
  preference boundaries, and non-authoritative browser behavior.

## Sources and expected files

- `gui/index.html`, `gui/app.mjs`, `gui/first-month.mjs`, and
  `docs/guides/gui-how-to-play.md`.
- `tests/test_gui_session_launch.py`, `tests/test_gui_first_month.py`, and new
  `tests/test_phase13_1_first_session_boundary.py`.
- New `docs/evaluation/phase13.1-first-session-boundary.json` plus additive
  roadmap, SDD, architecture, changelog, lessons, contract, QA, handoff, and
  release metadata updates.

## Non-goals and validation

- Do not add browser-owned session or simulation state, routes, persistence,
  assets, audio, replay authority, or human evaluation results.
- Run the focused first-session test plus full Python/Rust, GUI, release,
  documentation, asset, browser/device-policy, and visual/audio checks.

# Request Summary — Visual/audio technical competitive campaign boundary v0.13.54

## Scope

Record the current repository-owned `competitive-regional-v1` campaign
boundary without treating host duration or shared presentation contracts as
full-campaign product/content approval.

## Target slice

- Bind the host-owned 24-month completion path to existing Rust tests.
- Bind typed campaign-coverage briefing, metrics, actors, processes, decisions,
  history, replay, checkpoint, resolution, debrief, and written fallback
  surfaces to existing sources/tests.
- Preserve the host/core authority boundary and keep full-campaign visual,
  audio, screenshot, human, and expansion gates open.

## Sources and expected files

- Existing `src/mcp/session.rs`, `src/cli/campaign.rs`, GUI campaign-coverage,
  history, replay, checkpoint, and debrief sources/tests.
- New `docs/evaluation/phase13.1-competitive-campaign-boundary.json` and
  `tests/test_phase13_1_competitive_campaign_boundary.py`.
- Additive roadmap, SDD, architecture, changelog, lessons, QA, contract,
  handoff, generated credits, and release-metadata updates.

## Non-goals and validation

- Do not add runtime behavior, routes, simulation rules, assets, audio files,
  persistence, replay authority, or human evaluation results.
- Run the focused campaign-boundary test plus full Python/Rust, asset,
  generation, security, release, documentation, offline, browser/device,
  and visual/audio contract checks.

# Request Summary — Visual/audio technical debrief visual boundary v0.13.55

## Scope

Record the current repository-owned terminal debrief presentation contract
without treating technical rendering evidence as human visual or educational
review.

## Target slice

- Bind terminal host history, replay transition count, latest state hash,
  written debrief, direct effects, snapshots, consequence links, and read-only
  controls to existing GUI sources/tests.
- Preserve descriptive direct-attribution and host-authority boundaries.
- Preserve complete written behavior when optional audio or motion is
  unavailable, while keeping human visual/accessibility/educational review
  open.

## Sources and expected files

- Existing `src/mcp/session.rs`, `gui/app.mjs`,
  `gui/consequence-links.mjs`, `gui/README.md`, and live debrief/causal tests.
- New `docs/evaluation/phase13.2-debrief-visual-boundary.json` and
  `tests/test_phase13_2_debrief_visual_boundary.py`.
- Additive roadmap, SDD, architecture, changelog, lessons, QA, contract,
  handoff, generated credits, and release-metadata updates.

## Non-goals and validation

- Do not add debrief copy, routes, runtime fields, assets, audio files,
  persistence, replay regeneration, causal graphs, or human evaluation results.
- Run the focused Node renderer/parity test plus full Python/Rust, asset,
  generation, security, release, documentation, offline, browser/device,
  and visual/audio contract checks.
# Request Summary — Direct campaign audio projection v0.13.60

## User request

Continue the roadmap loop after v0.13.59. Implement the next unmet technical
item: direct browser-native audio integration for the existing stabilization and
regional-affiliation `campaign-coverage-v1` envelope.

## Target slice

- Add optional host-sourced `music_state_id` and `audio_cue_ids` metadata to the
  existing typed campaign-coverage projection.
- Derive IDs deterministically from actor-visible stage/briefing/actor/process
  text and committed visible transition summaries only.
- Make the browser prefer explicit host music and post-refresh cue IDs, while
  preserving omitted-field legacy classification and explicit-empty behavior.

## Scope boundary

No new audio asset, catalog ID, route, schema version, simulation rule,
transition, persistence path, hidden-state field, or local authority is allowed.
Audio remains optional and all written campaign meaning must survive mute,
unavailable audio, reduced notifications, and unsupported metadata.

## Evidence target

Update both Phase 12 audio ledgers, live campaign-coverage evidence, focused
Rust/Node/Python tests, guides, roadmap/spec/changelog/lessons, package version,
generated metadata, and current request/contract/QA/handoff records to v0.13.60.

---

# Request Summary — Campaign-aware first-month rail v0.13.59

## User request

Continue the visual/audio enhancement roadmap loop. After merging v0.13.58,
implement the next unmet technical item: make the GUI first-session rail
accurately distinguish competitive action drafting from the existing
stabilization and regional-affiliation campaign-coverage handoff.

## Target slice

- Preserve the competitive `competitive-first-month-v1` seven-stage rail.
- Add a separate campaign-coverage first-session rail for
  `stabilization-v1` and `regional-affiliation-v1`.
- Show start/load, visible inspection, host-shaped decision selection,
  committed-stage review, and continuation in text-first presentation.
- Advance only after the existing canonical host submission and coverage
  refresh succeed; rejected decisions remain recoverable at decision selection.

## Scope boundary

This is a local presentation-state and documentation change. It must not add a
host route, simulation rule, hidden-state field, client transition authority,
asset, audio file, persistence behavior, or human-evaluation claim. Human
accessibility, educational usability, campaign-specific visual/audio quality,
and public-release gates remain open.

## Evidence target

Add focused derivation/renderer/live-handoff tests and update the current
Phase 13.1 first-session evidence ledger, roadmap, guides, version projections,
request/contract/QA/handoff records, and lessons for v0.13.59.

---

# Request Summary — Live campaign-coverage handoff v0.13.58

## Authorized outcome

Continue the visual/audio roadmap by closing the current technical browser
integration gap for the existing `campaign-coverage-v1` envelope. Make
stabilization and regional-affiliation sessions launchable from the loopback
GUI and route their actor-visible decisions through the existing campaign
coverage renderer and host-owned `submit_turn` boundary.

## Target slice

- Add the loopback campaign-coverage route.
- Add a non-mutating host session-envelope read for existing-session campaign
  identification after a fresh page load.
- Allow the two existing campaign-coverage campaigns in the launcher.
- Add local-adapter campaign tracking and `getCampaignCoverage`.
- Fall back from competitive-only presentation/action reads to campaign
  coverage for noncompetitive sessions.
- Preserve the competitive seven-stage action path and all authority limits.
- Preserve the current campaign panel when a replacement coverage envelope is
  malformed or unavailable.
- Update technical evidence, docs, version, and release metadata to v0.13.58.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 12.1/12.2 browser-native
  integration gaps and Phase 13 full-campaign boundary.
- `src/mcp/session.rs` and `src/mcp/campaign_coverage.rs` — existing typed
  host-owned campaign projections and canonical transition route.
- `src/gui_server.rs` — loopback GUI transport boundary.
- `gui/host-adapter.mjs`, `gui/app.mjs`, and `gui/index.html` — current
  launcher, action-client fallback, and campaign-coverage renderer.
- `_workspace/137_implementation_plan_live-campaign-coverage-v0.13.58.md` —
  bounded implementation plan.

## Non-goals

- Do not change simulation rules, transitions, commands, hidden state, or
  browser authority.
- Do not add assets, audio files, screenshots, persistence, or true-state
  projections.
- Do not claim human visual/audio/accessibility/educational, legal, or release
  approval.

## Validation target

Focused Rust transport and JavaScript fallback tests, full Python/Rust checks,
Clippy, formatting, release metadata, asset/security/credits, documentation
links, and one medium-effort code review.

## Evidence limits

This slice proves only that the existing typed campaign-coverage projection is
reachable and usable through the loopback GUI for the two supported campaigns.
Campaign-specific quality, screenshots, replay playback, durable persistence,
human evaluation, and public-release gates remain open.

# Request Summary — Visual/audio Phase 13.1 AI-generation metadata boundary v0.13.57
