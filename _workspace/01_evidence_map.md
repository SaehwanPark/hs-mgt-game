# Evidence Map - Regional Affiliation Observation Context v0.12.2

## Scope

Close the v0.12.1 structural MCP observation-context gap without changing the
affiliation mechanism or making a learning claim.

## Sources Reviewed

- `docs/playtest-findings-v0.12.1.md` and
  `_workspace/experiments/v0.12.1-affiliation-playtest-validation/diagnostics.md`.
- `src/model/affiliation.rs` and `src/affiliation/observe.rs`.
- `src/mcp/session.rs` formatter and session tests.
- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and ADR-0010.

## Mechanisms and Institutions

- The typed `AffiliationObservation` already computes player-safe commitments,
  current-stage alternatives, and stylized assumptions.
- The MCP adapter currently renders only the compact state summary, so the
  missing fields are an interface projection gap rather than a missing model
  mechanism.
- Rendering these values does not alter partner, review, labor, payer, or
  community response authority.

## Actor Incentives and Information

- Commitments are Riverside's already-committed public/player state.
- Alternatives are the scenario's staged choices, not hidden actor actions.
- Assumptions explicitly label stylized inputs and the boundary of Riverside
  authority; they do not reveal private partner condition or future outcomes.

## Assumptions

- The typed observation is the authoritative safe source for this rendering.
- Existing line labels are stable enough for focused tests and deterministic
  artifact auditing.
- The v0.12.1 matrix is the compatibility baseline; the new v0.12.2 artifact is
  additive and leaves the historical v0.12.1 artifact unchanged.

## Unresolved Questions

- Whether the additional context improves human comprehension is not measured.
- The slice does not establish that any affiliation posture is optimal or
  winnable.
- Numeric thresholds, actor responses, legal abstractions, and balance remain
  outside scope.

## Design Implications

- Render only fields already present in `AffiliationObservation`.
- Add tests at the MCP session envelope boundary, not only formatter unit
  details, so the actual player-facing surface is protected.
- Rerun the same capture and require the prior structural gap to close while
  keeping runtime promotion deferred for balance and transition changes.

## Risks

- A future formatter change could accidentally expose a hidden field; tests and
  review must inspect the source of every new line.
- Rendered text is a compatibility surface for the evidence runner, so labels
  should be explicit and stable.
