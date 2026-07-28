# Implementation Plan — Visual/audio Phase 11.1 operational-overlay coverage v0.13.12

## Task restatement

Complete the current supported operational-overlay vocabulary in the live
competitive regional-world projection. Every catalog entry must have a direct,
actor-visible trigger condition, host-provided source/equivalent text, stable
browser binding, and safe non-color fallback. This slice closes only current
overlay coverage; it does not expand simulation mechanics or claim full
campaign, screenshot, accessibility, or human-quality completion.

## Current understanding

- `gui/operational-overlays.mjs` defines twelve registered overlay IDs plus a
  generic fallback and explicitly prohibits hidden severity, intent, causality,
  probability, or future-outcome inference.
- `src/mcp/regional_world.rs` currently emits five of those IDs from
  `PlayerObservation`; the remaining seven catalog entries have no live host
  binding.
- `gui/regional-board.mjs` and `gui/app.mjs` already resolve registered IDs,
  preserve source/equivalent text, and provide an unknown overlay fallback.
- The campaign-coverage ledger and tests currently prove catalog parity and
  five live bindings, but leave Phase 11.1 overlay coverage unchecked.

## Target slice

Bind all twelve current catalog IDs to direct visible conditions already present
in `PlayerObservation`:

- staffing and capacity fields;
- explicit in-flight project text, including delayed/completed wording;
- visible market and policy/annual-review bullets;
- visible community trust, cash/runway, monthly margin, and information-gap
  fields.

Conditions must be text- or field-derived and must not infer hidden severity,
intent, causality, probability, or future outcomes. Raw metric overlays remain
raw; operational overlays remain optional labels over the same host projection.

## Assumptions

- A condition is eligible when the relevant `PlayerObservation` field is
  present and explicitly indicates the catalog category; no new threshold is
  introduced unless the field already has a visible categorical value.
- Positive monthly margin can support the existing “Operational recovery”
  presentation because it is a direct visible result, not a prediction.
- Project and payer/regulatory categories can bind only when their visible text
  explicitly contains the category signal; absence preserves the current
  no-overlay behavior.

If a catalog entry cannot be bound without inventing a hidden rule, stop and
record it as an unresolved evidence gap instead of adding a proxy classifier.

## Minimal implementation plan

1. Extend `operational_overlays` in `src/mcp/regional_world.rs` with direct
   visible bindings for the seven currently uncovered catalog IDs.
2. Keep the registered IDs, visible source strings, text equivalents, stable
   ordering, generic fallback, browser resolver, and authority boundary intact.
3. Extend the Rust regional-world fixture to exercise all twelve bindings and
   absence behavior; extend the Python live/coverage tests and ledger to prove
   exact catalog-to-host coverage and no forbidden client authority.
4. Update the roadmap checklist/status, canonical spec/architecture/changelog,
   request/contract/QA/final handoff records, lessons, and patch version.
5. Run focused, full, release, documentation, asset, Rust, browser, and
   presentation checks before PR handoff.

## Files and functions likely to change

- `src/mcp/regional_world.rs`: direct binding conditions and fixture tests.
- `tests/test_phase11_live_operational_overlays.py` and
  `tests/test_phase11_campaign_coverage.py`: live parity and authority tests.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: overlay coverage
  status, host condition/source map, and evidence boundaries.
- `gui/operational-overlays.mjs`: only if a source/equivalent contract needs
  correction; do not alter the catalog IDs or fallback semantics needlessly.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  and `_workspace/final/handoff.md`: additive handoff records.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `Cargo.toml`, and `Cargo.lock`.

## Tests and checks

- `python3 -m unittest tests.test_phase11_live_operational_overlays`
- `python3 -m unittest tests.test_phase11_campaign_coverage`
- `cargo test mcp::regional_world::tests::operational_overlay_bindings_use_only_direct_visible_conditions -- --exact`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets --all-features -- -D warnings`
- release, documentation, offline, browser-policy, asset, and visual/audio
  contract checks.

## Acceptance criteria

- All twelve registered operational-overlay IDs have an explicit direct host
  condition or the plan stops with a documented unresolved gap.
- Host projection source strings are `PlayerObservation` fields or explicit
  visible text; no hidden state, transition input, effect queue, or client
  classifier is introduced.
- Raw metric overlays remain unbound raw metrics, and unknown IDs preserve the
  generic text/non-color fallback.
- Rust and browser tests cover all twelve IDs, no-condition absence, fallback,
  source/equivalent preservation, and forbidden authority markers.
- The roadmap marks only the bounded current operational-overlay coverage item
  complete; save/load, replay, debrief, screenshots, registry completeness,
  device/human quality, and later phases remain open.

## Non-goals

- Do not add new simulation fields, transition rules, stochastic inputs,
  severity scores, hidden-state projections, or campaign mechanics.
- Do not turn operational overlays into optimization advice or future-outcome
  prediction.
- Do not add assets, audio files, browser dependencies, screenshot tooling,
  runtime telemetry, durable persistence, or human evaluation.
- Do not claim complete full-campaign overlay placement or screenshot coverage
  beyond the current supported actor-visible projection.

## Stop conditions

Stop if any remaining catalog ID requires a hidden threshold or an inferred
causal/intent label, if a browser change would become authoritative, if a
simulation state change is required, or if the current observation fields do
not support truthful source/equivalent text.

## Review checklist

- Every catalog ID is mapped once and remains stable.
- Conditions read only direct visible fields or explicit visible bullets.
- No raw metric is relabeled as an inferred operational category without an
  explicit condition.
- Project, market, policy, staffing, capacity, recovery, and uncertainty text
  retain source/equivalent semantics.
- Browser fallback, reduced-motion, non-color, and unknown behavior remain
  intact.
- Tests and ledger prove exact coverage and authority boundaries.
- Diff contains no unrelated asset, audio, persistence, or simulation changes.

## Risk label

Risk: medium

Reason: The slice changes a host presentation projection and its tests, but no
simulation transition or hidden-state boundary. The main risk is overlabeling
visible fields, controlled by explicit string/field conditions and fail-closed
coverage tests.
