# Presentation Contract — Phase 3.3 operational overlays v0.12.63

## Goal and Authorization

Complete the reusable operational-overlay library for the twelve required
visible categories. The output is a fixture catalog and proof only; it must not
be promoted into the live regional board or create a browser legality,
simulation, or outcome engine.

## Player Questions and Consequences

- Which visible field/category does this overlay summarize?
- Can several visible pressures share a readable, deterministic stack?
- Which overlay is displayed first when space is limited?
- Can meaning survive color removal, motion reduction, missing data, or an
  unknown overlay ID?
- Does the overlay describe a committed/observed fact without claiming hidden
  severity, intent, causality, or future outcome?

## Actor-Visible Source Ledger

| Overlay | Triggering visible field | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Staffing constraint | `ReadOnlyObservation.staffing` / `PlayerObservation.nurses` and related visible staffing fields | Hidden staffing cause, quality, or future labor outcome | Staffing label, hatch pattern, and source text |
| Capacity constraint | `ReadOnlyObservation.capacity` / visible facility capacity metrics | Unobserved throughput, access, or clinical performance | Capacity label, double-line pattern, and exact visible metric |
| Demand pressure | `ReadOnlyObservation.operations.unmet_demand` / `PlayerObservation.monthly_unmet_demand` | Causal attribution, future demand, or population geography | Demand label, wave pattern, and visible value text |
| Active capital project | `ReadOnlyObservation.in_flight_projects` | Funding success, completion, or private project detail | Active-project label and text timeline |
| Delayed project | Host-provided visible project timing/status within `ReadOnlyObservation.in_flight_projects` | Hidden reason, risk, or eventual completion | Delayed label, dashed pattern, and timing text |
| Project completion | `ReadOnlyPresentation.latest_transition` committed visible effects | Unobserved benefit, causality beyond host text, or future performance | Completion label, double-ring pattern, and effect text |
| Payer/network change | `ReadOnlyObservation.market_bullets` / visible payer or market bullet | Private negotiation intent or guaranteed rate/outcome | Payer/network label and written market signal |
| Regulatory review | `ReadOnlyObservation.annual_policy_review` / `policy_bullets` | Regulatory decision, probability, or compliance outcome | Review label, dotted frame, and review text |
| Community-trust concern | `ReadOnlyObservation.community_trust` | Hidden sentiment cause, legitimacy, or future response | Trust label, crosshatch pattern, and visible trust text |
| Financial distress | `ReadOnlyResources.cash` + `ReadOnlyObservation.cash_runway_signal` | Insolvency forecast, private finances, or optimal action | Financial label, diagonal hatch, and visible runway/cash text |
| Operational recovery | `ReadOnlyObservation.operations.margin` / visible monthly operating result | Durable recovery, causal certainty, or future trend | Recovery label, ascending pattern, and exact result text |
| Uncertain or stale intelligence | `ReadOnlyObservation.information_gaps` / `prior_access_revision` | Hidden probability, severity, truth, or future outcome | Uncertainty label, dot-dash pattern, and missingness text |

## Visual, Motion, and Audio Semantics

- Every overlay has a stable ID, semantic role, glyph, shape/pattern, visible
  source, and written equivalent.
- Non-color patterns are the primary semantic fallback; color is supplementary.
- Every overlay has `severity_encoding: "none"` and `motion: "none"`.
- Display priority is a deterministic ordering aid only. It is explicitly not
  severity, urgency, probability, or strategic importance.
- Collision behavior uses a bounded stacked layout with deterministic
  ID-based tie-breaking and an explicit overflow count; hidden overlays are
  summarized as `N additional visible overlays` rather than discarded.
- The proof contains no audio and no consequence animation. Reduced motion is
  the same static layout and text.

## Accessibility and Fallbacks

- Exact visible values remain in text; unknown or missing values are not
  fabricated.
- Every overlay has a text equivalent, non-color pattern, and generic fallback.
- Simultaneous overlay cards expose their source and collision state.
- The proof uses semantic headings, labels, focus-visible cards, compact/wide
  responsive layout, and reduced-motion CSS.
- Unknown IDs normalize to `operational-overlay-generic`; invalid max-visible
  values use a safe default.

## Authority, History, and Replay Boundaries

The catalog accepts fixture IDs/visible field labels only. Sorting and layout
are local presentation functions. They do not read host state, submit
commands, evaluate transitions, resolve stochastic inputs, mutate history,
produce hashes, alter replay, drive audio, or write debrief facts.

## Asset Provenance and Release Requirements

`visual.runtime-operational-overlays` is a hand-authored project-generated
semantic asset with registry coverage, source hash, accessible equivalent,
visible source, modification note, and approved status. It has no external or
release image file.

## Verification and Evidence Limits

Focused tests must cover all twelve categories, all required contract fields,
generic fallback, no-severity/no-motion semantics, deterministic priority and
ID tie-breaking, bounded collision/overflow layout, simultaneous rendering,
registry/hash/credits, and syntax. These are technical checks only; they do
not substitute for human design, lived accessibility, learning, calibration,
policy validity, or live-browser evaluation.

## Non-Goals and Open Questions

- Do not alter live host DTOs or integrate the catalog into `gui/app.mjs`.
- Do not infer an overlay trigger from hidden state or client-derived severity.
- Do not add animation, audio, external assets, or a second operational model.
- Future Phase 4 integration must map each overlay from actor-visible data and
  preserve host-provided timing, missingness, and history semantics.
