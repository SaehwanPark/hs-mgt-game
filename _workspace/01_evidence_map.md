# Evidence Map — Visual and Audio Phase 7 Campaign Coverage v0.12.23

## Scope

Phase 7 extends the validated presentation boundary to the existing
`stabilization-v1` and `regional-affiliation-v1` campaigns. It is a presentation
and host-projection slice, not a new campaign or simulation framework.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 7 campaign-coverage section.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `SPEC.md`, and the harness team spec.
- Existing stabilization `WorldState`, `Observation`, `PlayerCommand`,
  `History`, and `educational_debrief` sources.
- Existing affiliation `AffiliationObservation`, stage/status/commitments,
  canonical commands, `AffiliationHistory`, and `affiliation_debrief` sources.
- Merged Phase 1–6 typed presentation, resolution, audio, and regional-world
  contracts.

## Mechanisms and Institutions

Stabilization is an onboarding-oriented executive loop: the player sees current
cash/capacity and reported access/quality/policy/market information, then
chooses a stage-specific resource or commitment response. Its teaching value is
the sequence of workforce, policy, coalition, and competitive pressures rather
than a regional map.

Affiliation is a bounded institutional-fit and obligation process: Riverside
assesses a partner, chooses an independent/deferred/pursue posture, proposes
commitments, passes review, and chooses integration or decline. Partner,
review, labor, payer, and community responses remain separate actor-visible
signals rather than one affiliation score.

## Actor Incentives and Information

- Stabilization exposes only the existing player observation and stage-appropriate
  command surface. Resolved measurement inputs remain behind the established
  observation boundary even when their reported effects are visible.
- Affiliation exposes the existing reported partner condition, commitments,
  stage/status, and stakeholder response observations. Private true condition,
  resolved response inputs, and future outcomes remain unavailable.
- The host supplies command templates, parameter labels, uncertainty, and
  constraints; the browser does not derive legality or outcome formulas.

## Assumptions

- An additive `campaign-coverage-v1` read can reuse existing observation,
  history, hash, command, and debrief functions without widening competitive
  DTOs.
- Host-shaped parameter metadata reduces command syntax friction while leaving
  parsing, validation, stochastic resolution, and transitions authoritative.
- A shared stage/briefing/metric/process/history shell can carry both campaigns
  if role labels and campaign-specific actor/obligation sections remain explicit.
- Phase 7 audio can reuse generated recipes: visible campaign stage/status maps
  to existing music states, and committed affiliation stage changes may use the
  existing affiliation milestone cue.

## Unresolved Questions

- What onboarding evidence would justify defaults or stronger guidance beyond
  host-provided command constraints?
- Which stabilization and affiliation responses deserve distinct event cues
  without making unfavorable outcomes sound like failure or success signals?
- Does the shared shell remain legible when affiliation commitments and actor
  responses are shown together at narrow viewports?

## Design Implications

- Add a typed coverage envelope with campaign role, stage, source-labeled
  briefing, metrics, campaign actors, processes/obligations, decisions,
  committed history, replay metadata, and terminal debrief lines.
- Use explicit visibility/uncertainty text and a stable campaign role label.
- Render forms from host parameter metadata and submit only host-shaped command
  text through the existing adapter; refresh the coverage envelope afterward.
- Keep the competitive action/resolution/regional-world paths unchanged and
  make campaign coverage optional when its adapter is absent.

## Risks

The shared shell could flatten campaign semantics, turn assumptions into hidden
rules, expose resolved affiliation responses, or make an affiliation stage look
like a competitive monthly turn. Use campaign roles, stage-specific labels,
source fields, explicit unavailable notes, and tests that reject hidden fields.
