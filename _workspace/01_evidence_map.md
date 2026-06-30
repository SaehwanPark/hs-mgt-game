# Evidence Map: Feedback-Aligned SDD Future Planning

## Scope

Map the supplied external feedback into bounded project planning implications.
This artifact supports documentation updates only; it does not approve runtime
mechanics, schemas, parameters, or new actors.

## Sources Reviewed

- User-supplied feedback about project maturity, strengths, risks, and next
  priorities
- Canonical docs: `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`
- SDD docs: `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`
- Active validation docs: `docs/agent-playtest-protocol.md`,
  `docs/mcp-playtesting-guide.md`, `docs/playtest-findings-v0.1.42.md`
- Evidence docs: `docs/evidence-registry.md`
- Harness spec: `docs/harness/health-policy-strategy-game/team-spec.md`

## Mechanisms and Institutions

- The feedback affirms the current thesis: health-policy outcomes should emerge
  from strategic interaction among institutions rather than direct policy levers.
- Determinism, actor-specific observations, immutable history, simultaneous
  competitive resolution, and debriefing remain durable strengths.
- The main planning implication is not more architectural breadth. The next
  evidence need is whether repeated play produces difficult, legible, and
  interesting decisions.
- Content authoring is a likely bottleneck. Scenario design should be treated as
  a teaching-case craft problem before broad runtime tooling.
- Game-theoretic machinery should remain local and interpretable. Institutional
  heuristics, routines, constraints, aspiration levels, and attention limits are
  preferred over global optimization.

## Actor Incentives and Information

- Player-facing transparency should remain layered: role-appropriate reports
  during play, proximal causal explanations after turns, and full trace
  inspection for post-campaign analysis or instructor review.
- AI-agent playtesters are useful for reproducible exploration but tolerate
  dense reports more easily than human learners; findings must remain labeled as
  simulated-player evidence.
- Actor utility, organizational success, social welfare, gameplay success, and
  educational evaluation remain distinct.

## Assumptions

- The current architecture is credible enough to validate bounded gameplay
  before adding major abstractions.
- The first-release priority order is educational strategy simulation, engaging
  gameplay, reusable modeling platform, then research-grade policy model.
- A docs-only SDD refresh should bump the patch version and changelog but should
  not change Rust behavior.

## Unresolved Questions

- Which strategy-space diagnostics will prove most useful after the next
  versioned agent batch?
- Which current debrief gaps will be observed in playtest evidence rather than
  anticipated abstractly?
- Which scenario-authoring friction appears first when trying to make one
  exemplary scenario excellent?
- Which mechanisms need confidence labels before any formula or balancing work?

## Design Implications

- Add falsifiable gameplay validity hypotheses to the active agent-playtest
  protocol.
- Add strategy-space diagnostics as a Future track before any analytics
  platform or automated optimizer.
- Treat debrief quality as a primary product surface tied to committed history,
  observations, alternatives, assumptions, and uncertainty.
- Gate scenario-tooling expansion on one exemplary scenario and concrete
  authoring friction.
- Add model-confidence labels to evidence planning without introducing runtime
  schema.
- Freeze major abstractions by default unless playtest, authoring, debrief, or
  domain-review evidence names a concrete need.

## Risks

- **Scope expansion:** feedback could be misread as approval for a broader
  platform; docs should instead add gates.
- **False precision:** diagnostics and confidence labels must not imply
  empirical calibration.
- **Educational overclaim:** AI-agent evidence must not become a human learning
  claim.
- **Strategic opacity:** debrief and actor-rationale work should keep actor
  observations and true state distinct.
