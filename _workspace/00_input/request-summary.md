# Request Summary — Visual and Audio Phase 5 Foundational Audio v0.12.21

## Scope

- Continue the merged Phase 4 resolution surface with a bounded optional audio
  layer for one `competitive-regional-v1` month.
- Add four visible-state music modes (`menu`, `stable_operations`, `pressure`,
  and `debrief`) plus the eight approved interface/event cue IDs.
- Keep audio browser-owned and generated through the Web Audio API so the first
  implementation adds no downloaded assets or network dependency.
- Provide master/music/interface/event/ambience controls, mute, focus behavior,
  reduced notifications, missing-audio fallback, registry metadata, credits,
  and deterministic recording-sink tests.

## Sources

- `docs/visual_audio_upgrade_proposal.md` Phase 5 requirements and audio test
  strategy.
- Phase 0 cue catalog and asset/license policy, ADR-0011, and the merged Phase
  1–4 presentation contracts.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`, and the Phase 4 resolution
  envelope as the visible input boundary.
- Canonical product docs, architecture, design principles, versioning policy,
  lessons, and the harness team spec.

## Expected files

- Browser audio catalog/classifier/playback module and generated-audio registry.
- GUI controls/status integration with the existing action/resolution surface.
- Static contract tests for visible-only mapping, controls, mute/focus,
  reduced notifications, throttling, fallback, and no-network behavior.
- Phase 5 contract document, SPEC/architecture/version records, tests, evidence,
  domain QA, lessons, and final handoff.

## Validation target

- Every cue has an approved visible source and textual/visual equivalent.
- Music classification uses only explicit page stage or actor-visible summary;
  private rivals, true state, resolved stochastic inputs, and hidden effects are
  never read.
- Audio settings and playback do not alter commands, transitions, histories,
  replay hashes, or resolution content. Muted play is complete.
- Repeated committed events are throttled; focus loss and reduced notifications
  are recoverable; absent audio support falls back to visual/text presentation.
- Registry and credits state that all first-slice audio is generated in-repo,
  with no third-party asset claim or unrecorded source.

## Explicit non-goals

No simulation changes, audio in Rust, downloaded/licensed audio files, dynamic
music composition, spatial or pitch-only signaling, other campaigns, broad
asset production, general settings framework, human-usability claim, or Phase
6 map/world work.

## Global workflow

Use the repo orchestrator, evidence mapper, mechanism designer, domain QA, and
end-user experience workflow; use simple-code/spec-driven/plan-design skills and
the preferred workflow with exactly one code reviewer. Implement on this branch,
verify, open a PR, review once, merge into `main`, and then design Phase 6 only
after the Phase 5 gate closes.
