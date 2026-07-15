# Evidence Map — Visual/audio Phase 12 visual identity and marker provenance v0.12.28

## Scope

This slice addresses the next narrow gap after the merged first-session
launch/load boundary: the first-month regional desktop has generic symbols but
no explicit, reusable visual vocabulary connecting system identity, facility
type, visible pressure, and process category. The change is a browser
presentation contract, not a health-policy mechanism.

## Sources Reviewed

- User objective and `_workspace/00_input/request-summary.md`.
- `SPEC.md` product contract, intended experience, visual/motion language,
  presentation/action boundary, asset/accessibility rules, and first
  competitive vertical-slice requirements.
- `docs/visual_audio_upgrade_proposal.md` sections 6, 7, 8, 9, 12, 13, 15,
  and 16.
- `docs/visual-audio-phase0-alignment-v0.12.16.md` asset and hidden-state
  policy.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`, `gui/audio.mjs`, and
  existing GUI/asset tests.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team spec.

## Mechanisms and Institutions

- No policy, workforce, payer, regulator, rival, or community mechanism is
  added. Riverside, Northlake, and Summit remain the existing actor-visible
  systems.
- A visual identity token is a stable presentation mapping for an existing
  visible system ID/name. It does not assert ownership, private activity, or
  outcome quality beyond the host-provided status.
- A marker token labels an already displayed facility, metric, process, or
  timeline category. It is a semantic index, not a new measurement.
- The registry records generated text/glyph/CSS primitives. It deliberately
  contains no third-party asset or downloadable path.

## Actor Incentives and Information

- The executive needs to locate the owned system, public rivals, facilities,
  capacity/workforce pressures, and pending processes while preserving the
  distinction between owned detail and lagged public signals.
- The browser may use visible identity IDs, names, kinds, labels, and marker
  fields already present in the presentation envelope. It may not inspect true
  state, private rival data, resolved inputs, or infer severity from a number.
- Unknown entities and marker kinds must use a clearly labeled generic token so
  missingness remains visible rather than silently becoming a known identity.

## Assumptions

- Existing entity IDs and presentation labels are stable enough for a small
  first-slice mapping; if a host uses an unknown ID, the generic fallback is
  correct and no host schema change is justified.
- Unicode symbols plus text labels are sufficient for the current dependency-
  free browser surface and satisfy the non-color requirement when paired with
  existing status text/patterns.
- The current status vocabulary remains the single source of status meaning;
  this slice only gives it a registry entry and does not change its mapping.

## Unresolved Questions

- Whether later campaigns need campaign-specific identity catalogs remains a
  separate coverage decision.
- Whether generated primitives should later be replaced with licensed SVG or
  raster assets requires a separate provenance/release decision.
- Human recognition, visual comfort, lived accessibility, and learning remain
  unresolved questions; static semantic checks are only technical proxies.

## Design Implications

- Keep the visual catalog dependency-free and pure; DOM rendering belongs in
  existing `app.mjs` functions.
- Render a text label and symbol together, with `aria-label`/visible source
  context, so color and shape are never the only distinction.
- Apply tokens only at existing regional-world/detail/process/overlay surfaces;
  do not create a new navigation metaphor or map geometry.
- Keep the generic fallback explicit and source-linked so unknown or missing
  actor-visible data cannot be mistaken for a known institution.
- Record the visual registry and credits as project-generated primitives; do not
  introduce a third-party asset pipeline for this slice.

## Risks

- Name-based fallback could accidentally classify a future entity. Prefer exact
  known IDs first, use conservative aliases, and fall back to generic.
- Replacing existing icons too aggressively could reduce compatibility with
  fixture tests or obscure source labels. Preserve existing text and add the
  catalog token alongside it.
- A registry can create false confidence about polished visual design. Keep the
  phase explicitly limited to identity/marker consistency and technical
  provenance.
