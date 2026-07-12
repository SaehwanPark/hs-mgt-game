# Evidence Map - Regional Affiliation Playtest Validation v0.12.1

## Scope

This artifact validates the first post-runtime playtest surface for the
opt-in `regional-affiliation-v1` scenario. It is Phase 7 evidence, not a new
health-policy mechanism or a calibration exercise.

## Sources Reviewed

- `SPEC.md` ranked queue and promotion rules.
- `docs/roadmap.md` Phase 7.5–7.7 validation gates.
- `docs/proposal.md` and `docs/design_principles.md` deterministic,
  observation, actor-utility, social-welfare, and debrief boundaries.
- `docs/decision-records/0010-regional-affiliation-runtime-slice.md`.
- `src/model/affiliation.rs`, `src/inputs/resolve_affiliation.rs`,
  `src/affiliation/`, `src/mcp/session.rs`, and `src/debrief/report.rs`.
- The bundled `scenarios/regional-affiliation-v1.toml` fixture.

## Mechanisms and Institutions

- One Riverside nonprofit system chooses independence, deferral, or pursuit of
  one neighboring nonprofit affiliation.
- Pursuit proceeds through commitments, partner response, review, actor
  responses, and an integration decision.
- Partner, review, labor, payer, and community outcomes are explicit resolved
  inputs and are not controlled by the Riverside command alone.
- The capture uses the existing MCP observation and transition summaries; it
  does not infer unexposed true-state values.

## Actor Incentives and Information

- The player policy uses only the MCP observation and legal command hints.
- The typed affiliation observation contains reported partner condition,
  commitments, alternatives, and assumptions, while the MCP formatter exposes
  only a subset of those fields.
- Actor response labels are read from committed transition/debrief output and
  remain separate from Riverside cash, access, quality, workforce, community,
  and market-share outcomes.

## Assumptions

- Seeds 42, 43, and 44 are deterministic replay coordinates, not a statistical
  sample or calibration basis.
- The three policies are scripted observation-driven probes: independent and
  deferred hold after their posture choice; pursuit submits a maximum legal
  commitment package and begins integration only when the legal surface allows.
- A missing decision-time field is a product/evidence gap only when it is absent
  across the captured observation matrix and the typed model makes the field
  available; it is not evidence that the underlying mechanism is wrong.

## Unresolved Questions

- Whether displaying alternatives, assumptions, commitments, and actor response
  context at decision time improves human comprehension is not measured here.
- Whether the numeric commitment thresholds produce multiple defensible paths
  is not established by this nine-run capture.
- No legal, financial, policy, winnability, balance, or educational-effect claim
  follows from the artifact.

## Design Implications

- Preserve runtime promotion deferral for balance or ruleset changes.
- Treat the repeated omission of typed observation context from the MCP
  formatter as one bounded candidate for the next interface slice.
- Any follow-up must add focused MCP observation tests and preserve competitive
  golden hashes and affiliation replay determinism.

## Risks

- The matrix is small and scripted; it can expose structural trace gaps but not
  general player behavior.
- Debrief text is a rendered evidence surface, so its parsing contract must stay
  explicit and deterministic.
- Do not convert the observation-context gap into a claim about learning or
  require a GUI or generalized analytics layer.
