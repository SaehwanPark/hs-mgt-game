# Phase 11.1 Live Operational-Overlay Binding — Implementation Plan v0.12.90

## Task restatement

Bind directly supported actor-visible regional-world conditions to the existing
operational-overlay catalog while preserving raw metric overlays, host
authority, observation boundaries, and generic fallback behavior.

## Current understanding

- `src/mcp/regional_world.rs` projects five raw player-observation overlays.
- `gui/operational-overlays.mjs` already defines the twelve approved overlay
  semantics, but `gui/regional-board.mjs` does not consume that catalog for the
  live DTO.
- The live board must not infer severity, intent, causality, probability, or
  future outcome from a metric or catalog label.
- The next smallest useful slice is an optional host-shaped
  `operational_overlay_id` on `RegionalWorldOverlay`, populated only for
  conditions directly represented by `PlayerObservation`.

## Assumptions

- Adding one optional serialized presentation field is backward-compatible for
  existing adapters and does not alter simulation state or hashes.
- The following bindings are directly visible and safe: nonzero unmet demand
  to demand pressure, a reported in-flight project to active capital project,
  a strained cash runway or negative reported margin to financial distress,
  a watch community-trust summary to community-trust concern, and nonempty
  information gaps or a prior access revision to uncertain/stale intelligence.
- Raw `demand`, `access`, and `staffed-beds` metric overlays remain raw metrics
  and receive no inferred operational category.
- If these assumptions conflict with the codebase, stop and report the
  mismatch before broadening the design.

## Minimal implementation plan

1. Add the optional catalog binding to the regional-world overlay DTO and build
   a deterministic list of condition overlays from `PlayerObservation`.
2. Update the live regional-board adapter to resolve an explicit binding
   through `operationalOverlayFor`, preserve raw metric semantics, and expose
   the catalog ID, source, text equivalent, and generic fallback in the DOM.
3. Add focused Rust, Node/Python, and boundary tests for supported bindings,
   absent conditions, unknown IDs, deterministic ordering, and unchanged rival
   privacy.
4. Update the roadmap evidence, canonical project records, version projections,
   changelog, lessons, request/contract/QA/handoff artifacts, and registry hash
   projections.
5. Run focused checks, then the required repository checks before handoff.

## Files and functions likely to change

- `src/mcp/regional_world.rs`: overlay DTO field, condition projection, and
  visible-source helpers.
- `src/mcp/session.rs`: actor-visible projection assertions.
- `gui/regional-board.mjs`: catalog-aware overlay normalization.
- `gui/app.mjs`: data and accessible text for live overlay catalog semantics.
- `tests/test_phase11_live_operational_overlays.py`: focused integration and
  boundary probes.
- `tests/test_gui_regional_world.py`: live contract markers.
- `assets/registry/visual-assets.json`, `assets/ASSET_CREDITS.md`: hashes for
  changed presentation modules.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`,
  `ARCHITECTURE.md`, `LESSONS.md`, and
  `docs/visual_audio_enhancement_roadmap.md`: project records and evidence.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, and `_workspace/final/handoff.md`:
  durable handoffs.

## Tests and checks

- `python3 -m unittest tests/test_phase11_live_operational_overlays.py`
- `python3 -m unittest tests/test_gui_regional_world.py`
- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- JavaScript syntax checks for changed modules.

Expected result: all focused and repository checks pass, with no host/session
mutation and no hidden-state fields in the projected JSON.

## Acceptance criteria

- Directly supported visible conditions carry stable operational catalog IDs
  and source/equivalent text; unsupported raw metrics remain raw metrics.
- The browser resolves only explicit catalog IDs, preserves unknown IDs through
  the registered generic fallback, and exposes semantics without color, motion,
  or audio dependence.
- Reading the regional-world projection remains non-mutating; rival facilities,
  private rival operations, effect queues, event metadata, and resolved inputs
  remain unavailable.
- Existing regional-board fixtures, facility binding, replay, and documentation
  checks continue to pass.
- The Phase 11.1 roadmap evidence records only this bounded live overlay slice;
  full campaign coverage, screenshots, performance, compatibility, and human
  evaluation remain open.

## Non-goals

- Do not add new assets, dependencies, audio, screenshots, or browser network
  access.
- Do not infer a category from an arbitrary numeric threshold beyond the named
  visible conditions or expose true state.
- Do not change simulation transitions, stochastic inputs, commands, history,
  replay hashes, save format, rival observations, or debrief facts.
- Do not mark all Phase 11.1 or later roadmap items complete.
- Do not perform unrelated cleanup or reformat untouched files.

## Stop conditions

- Stop if the DTO change requires a new incompatible schema or migration.
- Stop if a condition needs hidden state, a client-side formula, or a new
  simulation mechanism to classify it.
- Stop if more than the named production files require broad architectural
  changes or if unrelated tests fail and cannot be isolated.

## Review checklist

- The diff is limited to explicit visible condition bindings and their tests.
- Raw metric overlays are not mislabeled as operational severity.
- Unknown and absent bindings have deterministic, text-complete fallbacks.
- The live browser remains presentation-only and network-free.
- Registry hashes and documentation projections match the changed files.
- One code-reviewer skill performs the required review passes; findings are
  fixed or explicitly deferred before merge.

## Risk label

Risk: medium

Reason: this adds a serialized host presentation field and changes live
regional-board semantics, but it does not alter simulation authority or public
commands.
