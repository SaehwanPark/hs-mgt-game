# Evidence Map - Project-Limit Recovery

## Scope

Capture Phase 7 evidence about whether the current project-limit validation
surface preserves enough decision-time and retrospective information to inspect
a rejected third project and a safe retry. This slice does not add or
reinterpret a health-policy mechanism.

## Sources Reviewed

- `README.md`, `docs/roadmap.md`, `docs/design_principles.md`, and `SPEC.md`.
- `docs/playtest-findings-v0.10.51.md` and its generated artifact.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.
- Current validation code, MCP error mapping, project help, observation, and
  debrief wording.

## Mechanisms and Institutions

- The maximum of two concurrent projects is an existing game resource rule and
  design abstraction, not a calibrated real-world constraint.
- The capture observes validation, rejected-turn preservation, retry behavior,
  actor-visible project state, and retrospective explanation.
- It does not add an actor, policy, market, service line, or transition
  mechanism.

## Actor Incentives and Information

- The probe uses only the actor-visible MCP observation, legal command hints,
  submitted commands, and returned validation payload.
- Histories and debriefs are retrospective evidence and are not treated as
  decision-time knowledge.

## Assumptions

- A stable error code and unchanged turn establish machine-readable recovery
  traceability, not human comprehension.
- Absence of a structured resource hint is a trace fact until repeated recovery
  evidence identifies a concrete unexplained gap.
- A successful `hold` retry establishes a safe continuation path, not that it is
  the only or preferred player response.

## Unresolved Questions

- Whether the current error payload, observation, legal hints, and debrief make
  the two-project limit sufficiently inspectable for agent or instructor review.
- Whether any later evidence warrants a player-facing hint change.

## Design Implications

- Preserve raw response fields and same-turn state rather than inferring missing
  information from rendered prose.
- Keep runtime, difficulty, balance, scoring, and debrief behavior unchanged.
- If a concrete gap is found, record one separate follow-up slice instead of
  implementing it in this evidence PR.

## Risks

- Deterministic simulated-policy traces cannot establish human learning,
  strategy value, balance, winnability, calibration, or policy validity.
- Treating a known rule, successful fallback, or complete run as proof of
  player clarity would overstate the evidence.
