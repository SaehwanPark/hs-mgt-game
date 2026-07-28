# Implementation Plan — Visual/audio Phase 11.1 terminal debrief coverage v0.13.13

## Task restatement

Record and verify the current competitive terminal debrief view as a bounded
Phase 11.1 coverage item. The existing host `competitive-end-session-v1`
envelope already carries aligned immutable history, replay metadata, and
host-authored debrief lines; the browser already renders a text-first final
view and disables further actions. This slice adds the explicit ledger,
contract, and coverage evidence without claiming full-campaign or human
educational completion.

## Current understanding

- `src/mcp/session.rs` builds the terminal envelope from the host-owned session
  history and competitive debrief function before removing the session.
- `src/gui_server.rs`, `gui/host-adapter.mjs`, and `gui/app.mjs` expose,
  validate, and render the terminal envelope through the loopback boundary.
- `tests/test_phase11_live_debrief.py` covers aligned history/replay/debrief
  rendering, schema/count/hash rejection, terminal controls, host route markers,
  syntax, and the unchanged client-authority boundary.
- Phase 11.1 still has `Debrief view updated` unchecked because the existing
  evidence is not yet represented as a dedicated coverage ledger section.

## Target slice

Define `debrief_view_coverage` for the current competitive terminal view with:

- `competitive-end-session-v1` schema and loopback end-session route;
- immutable history rows aligned to replay transition count/latest hash;
- host-authored debrief lines rendered as written text;
- terminal action disablement and failure-preserving validation; and
- explicit non-goals for full-campaign debrief taxonomy, instructor views,
  counterfactuals, accessibility, usability, and learning.

## Assumptions

- The current competitive terminal envelope is the authoritative bounded
  debrief surface for Phase 11.1; no new debrief fields are needed.
- Host-authored debrief lines are presentation evidence only and remain distinct
  from replay metadata, immutable history, and simulation authority.
- A dedicated ledger record plus existing focused tests is sufficient evidence
  for this bounded checklist item; broader visual continuity remains separate.

If the existing terminal test does not cover a stated field or failure behavior,
stop and add only the smallest focused assertion needed before closing the
item.

## Minimal implementation plan

1. Add `debrief_view_coverage` to the Phase 11.1 campaign ledger with exact
   schema, host/route/browser sources, row/debrief contracts, and limits.
2. Extend `tests/test_phase11_campaign_coverage.py` to require the ledger shape,
   source markers, and linkage to `tests/test_phase11_live_debrief.py`.
3. Update the Phase 11.1 roadmap checklist/status and add v0.13.13 evidence;
   synchronize `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`,
   version projections, and additive request/contract/QA/handoff records.
4. Run focused/full Python and Rust checks plus all release/documentation,
   asset, offline, browser, and visual/audio contract checks.
5. Stop before adding new debrief mechanics, instructor-only data, persistence,
   replay regeneration, screenshot tooling, or human evaluation.

## Files and functions likely to change

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`.
- `tests/test_phase11_campaign_coverage.py` and, only if a gap is found,
  `tests/test_phase11_live_debrief.py`.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  `_workspace/107_implementation_plan_visual-audio-phase11-debrief-v0.13.13.md`,
  and `_workspace/final/handoff.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, and
  generated package-version projections.

Avoid changing Rust runtime, GUI, adapter, or asset behavior unless focused
inspection proves the existing contract is incomplete.

## Tests and checks

- `python3 -m unittest tests.test_phase11_live_debrief`
- `python3 -m unittest tests.test_phase11_campaign_coverage`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets --all-features -- -D warnings`
- release, documentation, asset, offline, browser-policy, device-policy, and
  visual/audio contract checks.

## Acceptance criteria

- The ledger explicitly records current terminal debrief schema, sources, row
  alignment, host-authored text, terminal control behavior, and failure limits.
- Coverage tests link the ledger to the live terminal debrief test and require
  the host/browser authority markers without introducing client-owned data.
- The roadmap closes only the current supported terminal debrief-view item;
  full-campaign debrief, instructor views, save/load/replay continuity,
  screenshots, accessibility, usability, and learning remain open.
- Package version increments to v0.13.13 and all generated metadata remains
  consistent.

## Non-goals

- Do not add debrief content, simulation mechanics, true-state fields,
  counterfactuals, instructor exports, durable persistence, replay playback,
  screenshot tests, assets, audio files, browser dependencies, or telemetry.
- Do not claim that current terminal rendering proves learning, usability,
  accessibility, audio usefulness, or full campaign coverage.

## Stop conditions

Stop if the ledger would require claiming data outside the host envelope, if
history/replay/debrief alignment is not directly testable, if the browser
would become authoritative, or if the work requires a runtime behavior change.

## Review checklist

- Schema, route, adapter, renderer, and test sources match exactly.
- History rows, transition count, latest hash, and debrief lines remain aligned.
- Missing/unknown/malformed envelopes fail closed without mutating the view.
- Terminal controls are disabled only after a valid host envelope succeeds.
- Host-authority, hidden-state, provenance, reduced-motion, written-equivalent,
  and optional-audio boundaries remain explicit.
- Full-campaign and human-quality limits are recorded rather than implied away.

## Risk label

Risk: low

Reason: The slice adds a read-only ledger contract and coverage assertions over
existing tested terminal behavior; no runtime or asset behavior is intended to
change.
