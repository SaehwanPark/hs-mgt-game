# Evidence Map — Visual/audio first-month contract audit v0.12.30

## Scope

Audit the existing technical first-month `competitive-regional-v1` contract
after the Phase 13 merge. This is a source-and-test evidence task, not a new
simulation or user-study claim.

## Sources Reviewed

- `SPEC.md`, `docs/visual_audio_upgrade_proposal.md`, and the Phase 0–13
  protocol documents.
- `gui/app.mjs`, `gui/audio.mjs`, `gui/first-month.mjs`, `gui/visual.mjs`,
  `gui/index.html`, and focused GUI tests.
- The merged Phase 13 handoff and current `main` history/PR state.

## Mechanisms and Institutions

- The executive uses one presentation path to inspect the regional market,
  owned facilities, workforce/capacity pressure, and public payer/rival
  context before choosing actions.
- The host/core remains the authority for command legality, costs, delays,
  stochastic resolution, committed effects, observations, history, replay, and
  debriefs.
- The browser only presents host-visible data, local drafts/settings/pacing,
  and visible audio equivalents.

## Actor Incentives and Information

- The player acts on actor-visible observations, not true or private rival
  state. Public rival information remains limited by the existing host
  projection.
- The audit records interface-task traceability, not player utility, social
  welfare, or educational learning.

## Assumptions

- The merged Phase 0–13 contracts are the current implementation of the
  proposal's bounded technical sequence.
- Source/test marker checks are appropriate for a dependency-free repository
  audit; they do not replace browser execution or human evaluation.
- The existing release metadata checker is the version authority.

## Unresolved Questions

- Browser transport, visual rendering at real viewports, contrast measurement,
  screen-reader behavior, and live audio hardware remain unverified here.
- Human usability, lived accessibility, learning, engagement, calibration,
  balance, policy validity, and domain-expert agreement remain separately
  authorized work.

## Design Implications

- Close the bounded technical sequence only with a deterministic audit artifact
  that fails closed when an obligation loses its source or test evidence.
- Keep deferred human and asset-production work visible as explicit limits rather
  than turning technical coverage into a product-success claim.

## Risks

- Marker audits can overfit source text. Mitigate with focused behavioral Node
  tests, existing host-boundary tests, and a review of the surrounding code.
- A closed technical sequence can be mistaken for a polished or validated
  release. Mitigate with claim-class and evidence-limit fields in the artifact
  and closure document.
