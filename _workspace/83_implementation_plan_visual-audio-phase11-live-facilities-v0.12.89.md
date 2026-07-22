# Implementation Plan — Visual/audio Phase 11.1 live facility binding v0.12.89

## Task restatement

Bind the current actor-visible competitive facility groups to stable existing
facility-component catalog IDs so the regional board and selected facility
detail view can name their visual equivalent without exposing hidden state or
claiming full-campaign asset coverage.

## Target slice

- Add a stable `component_id` to the host-projected regional facility DTO for
  the four current player-visible facility groups.
- Resolve that ID through the existing facility-component catalog in the
  regional-board and SVG scene adapters, with the registered generic fallback
  for missing or unknown IDs.
- Expose component label, source, equivalent, and release-path metadata in
  the accessible board contract and selected facility detail view.
- Add deterministic Rust, Node, and Python regression evidence, update the
  Phase 11.1 roadmap limits and project records, and keep all broader campaign
  gates open.

## Assumptions

- The current live facility vocabulary is the four groups emitted from
  `PlayerObservation`: inpatient beds, outpatient clinics, emergency and ICU,
  and specialty lines.
- `emergency-department` is a bounded presentation equivalent for the combined
  emergency/ICU group; it does not assert an ICU-specific asset or hidden
  facility topology.
- Rival facilities remain unavailable because the projection must preserve the
  actor-visible public-information boundary.
- Existing catalog source/equivalent fields and `facilityComponentFor` remain
  authoritative; no asset bytes or registry entries are added.

## Minimal implementation plan

1. Extend `RegionalWorldFacility` and the player projection with explicit
   component IDs.
2. Normalize IDs through the existing catalog in the board and scene adapters;
   render the component ID and accessible source/equivalent semantics.
3. Add selected-detail component presentation and focused fallback/authority
   tests; refresh the deterministic board snapshot.
4. Update the roadmap, request/contract/QA records, SPEC, ARCHITECTURE,
   README, CHANGELOG, LESSONS, version projections, and CI.
5. Run the full verification matrix, use the same single code reviewer, merge
   the PR into `main`, remove the temporary branch locally and remotely, then
   stop this target slice as requested.

## Acceptance criteria

- The four current player facility groups serialize exact stable component IDs.
- Missing and unknown IDs normalize to the registered `generic-facility`
  descriptor with explicit source/equivalent text.
- The board exposes `data-component-id` and component-aware accessible labels;
  selected detail shows component label, source, and equivalent semantics.
- No rival private facilities or core state fields are added to the DTO or
  presentation path.
- Focused and full tests pass; roadmap language closes only the bounded live
  binding evidence and keeps full facility coverage open.

## Non-goals and stop conditions

- Do not mark full campaign facility coverage, asset registry completeness,
  screenshot, performance, browser, accessibility-quality, or human-review
  gates complete.
- Do not add runtime network access, client authority, simulation behavior,
  new assets, or hidden-state fields.
- Stop after the v0.12.89 branch has been reviewed, merged, and deleted.

## Review checklist

- Exact four-ID host projection and unchanged rival privacy boundary.
- Catalog resolution, generic fallback, and visible source/equivalent checks.
- Board accessibility attributes and selected-detail semantics.
- No authority/network imports in the presentation path.
- Exactly one existing code reviewer inspects the final diff.

## Risk label

Risk: low

Reason: the slice adds a small explicit field to an existing read-only DTO and
binds it to an existing pure presentation catalog; it does not change the
simulation, assets, or client authority.
