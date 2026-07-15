# Evidence Map — Visual/audio Phase 11 first-session launch/load v0.12.27

## Scope

This slice addresses the first remaining product-contract gap after Phase 10:
the planned competitive first-month experience begins with starting or loading
a campaign, while the current GUI requires a preconfigured adapter session ID.
The proposed behavior is a presentation-to-host handoff, not a new game
mechanism.

## Sources Reviewed

- User objective and `_workspace/00_input/request-summary.md`.
- `SPEC.md` Future sections for product contract, first competitive vertical
  slice, presentation/action boundary, and verification.
- `docs/visual_audio_upgrade_proposal.md` sections 7, 8, 14, 15, and 16.
- `docs/mcp-agent-interface.md` and `src/mcp/session.rs` for the existing
  `start_session` request/envelope and non-transitioning session creation.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`, and existing GUI tests.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team spec.

## Mechanisms and Institutions

- No health-policy actor, institution, utility, policy lever, or transition
  mechanism is added.
- Existing host session creation selects a campaign, seed, difficulty, and
  optional validated scenario path, then creates a session at its initial
  state. It does not submit a command or resolve a month.
- The GUI needs only a browser adapter mapping for the existing host operation:
  `startSession({ campaign, seed, difficulty })` returns the existing
  session-envelope shape or an explicit error.
- Existing `getPresentation(sessionId)` and optional action/regional/resolution
  reads remain the source of the first briefing and first-month surfaces.

## Actor Incentives and Information

- The executive chooses a campaign-start parameter set, not an operating
  strategy. Seed and difficulty are session setup inputs and must not be
  presented as performance choices.
- The player sees only the host-returned session/presentation envelope after a
  successful start or load. The browser must not infer resources, rivals,
  policy pressure, or outcomes from the selected seed/difficulty.
- No rival, payer, labor, regulator, community, or AI actor is changed. No
  private information becomes available through the launcher.

## Assumptions

- A supplied browser adapter can map `startSession` to the existing MCP
  `start_session` operation and expose the returned `session_id`.
- The existing presentation/action clients can reload from a replacement
  session ID without changing their host contracts.
- An unavailable `startSession` method is a supported adapter capability gap,
  not a reason to fabricate a local session.
- The first target is `competitive-regional-v1`; the launcher does not broaden
  campaign coverage in this slice.

## Unresolved Questions

- Which future browser transport or host integration will implement the
  adapter in a deployed environment is not decided here.
- Whether scenario selection should be exposed to human players remains a
  separate scenario-authoring and release decision.
- Whether a launch flow improves human onboarding or learning requires later
  browser/human evidence and is not established by static tests.

## Design Implications

- Keep launch controls in the existing readiness/onboarding region so the user
  reaches the briefing through one visible path.
- Use native select/number/input controls and clear host-boundary status text.
- On start success, replace the client session ID and call the existing read
  path; do not render a predicted fixture as a substitute for host data.
- On load failure, preserve the current surface and offer retry; a failed
  start/load must not call `submitTurn` or alter an existing session.
- Reuse existing `session_loaded` capture behavior after the presentation read;
  no new raw session or true-state capture event is needed.

## Risks

- A browser adapter may implement `startSession` with a different response
  shape; tests must require the explicit existing `session_id` field and show a
  recoverable error for malformed responses.
- Replacing an active session ID could desynchronize action, regional, and
  campaign clients if only one client updates. The shared launcher callback
  must route through each client's existing `load` function.
- Static tests cannot establish a real MCP/browser transport, authentication,
  browser usability, or first-time human comprehension.
