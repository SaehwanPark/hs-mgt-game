# Request Summary — Visual/audio Phase 12 visual identity and marker provenance v0.12.28

## User request

Continue implementing the planned items in `SPEC.md` and
`docs/visual_audio_upgrade_proposal.md` through the repository workflow:
design the next bounded slice, implement it, perform exactly one general code
review, hand it off through a PR, merge `main`, and re-audit the remaining
SPEC queue.

## Current context

- Phase 11 first-session launch/load is merged on `main` at `c89d93a` as
  version `0.12.27`; its SPEC record needs post-merge closure bookkeeping.
- The GUI already renders the competitive presentation, regional world,
  contextual action, resolution, audio, campaign, settings, and recovery
  surfaces through host-shaped contracts.
- The current regional projection uses generic Unicode entity/facility marks
  and does not preserve a small, explicit visual identity vocabulary across
  map cards, detail, overlays, and processes.
- The proposal's first vertical slice requires system identities, facility and
  process markers, status/severity language, and asset provenance before broad
  decorative production.

## Selected bounded slice

Add a presentation-only visual catalog for three system identities, the
first-slice facility/metric/process marker set, and the existing status
vocabulary. Use it across the regional map, selected entity detail, overlays,
and visible process rows. Record the generated visual primitives in a
machine-readable registry and credits file. The host remains authoritative for
all values, observations, commands, transitions, and hidden-state boundaries.

## User/use context

The primary user is a first-time executive player who must recognize Riverside
and distinguish public rivals while scanning a dense first-month desktop. AI
testplay reviewers and contributors need the same identity and marker labels to
remain stable without reading raw JSON. The symbols are orientation aids, not
new game facts or severity calculations.

## Scope

- Add a small `visual-catalog-v1` module/registry with three system identities,
  facility/demand/capacity/project/staffing/payer-policy/timeline markers, and
  the existing non-color status tokens.
- Add accessible visual tokens to the map, selected entity/facility detail,
  regional overlays, and visible process rows.
- Derive identity and marker selection only from actor-visible IDs, names,
  kinds, or explicit presentation labels; fall back to a generic token.
- Add focused tests for catalog coverage, rendering markers, semantic labels,
  missing/unknown fallback, and no-network/no-simulation boundaries.
- Close the merged Phase 11 SPEC bookkeeping and bump version to `0.12.28`.

## Non-goals

- No Rust simulation, MCP DTO/schema, command, transition, stochastic,
  history/hash/replay, or debrief change.
- No downloaded images, external fonts, licensed assets, map geography,
  animation, audio source, network, browser transport, or new dependency.
- No client-side severity formula, hidden-state inference, new actor identity
  field, scenario picker, campaign expansion, or human usability claim.

## Branch and workflow constraint

- Branch: `feat/visual-audio-phase12-visual-identity-v0.12.28`.
- Exactly one general code-review pass is permitted for this item; fix its
  actionable findings and do not invoke a second pass.

## Validation target

Focused visual-catalog/GUI tests, full Python tests, Node syntax, formatting,
Clippy, Rust tests, release metadata, and diff checks must pass before PR
handoff. CI must pass before squash-merging `main`.
