# Evidence Map

## Scope

Test whether current v0.11.12 code preserves actor-visible observation capture,
command/retry traceability, pacing proxies, operating-event boundaries, and
debrief continuity for three observation-driven Hard-difficulty profiles.

## Sources Reviewed

- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and the active
  agent-playtest protocol.
- The v0.11.11 current-code all-tier validation artifact.
- The v0.10.50 observation-driven teachability capture and v0.10.52 pacing
  audit, reused as historical implementation patterns only.

## Mechanisms and Institutions

- The competitive campaign, MCP boundary, rival behavior, operating loop, and
  debrief surface are existing runtime mechanisms and remain unchanged.
- The capture treats the human-owned observation and command trace as the
  decision-time surface; committed history and debriefs are retrospective
  evidence.
- Operating events owned by rivals are excluded from player-owned evidence.

## Actor Incentives and Information

- The three profiles are deterministic simulated policies, not learner types,
  validated strategy classes, or utility functions.
- Policies receive only actor-visible observations and legal command hints.
- True history, rival rationales, and instructor-revealed information must not
  be interpreted as information available at decision time.

## Assumptions

- The current package version is `0.11.12`; ruleset and state-hash schema remain
  `competitive-ruleset-0.2.0` and `competitive-state-hash-v9`.
- Hard difficulty is sufficient for this focused teachability slice because the
  v0.11.11 artifact already covers all four tiers with five strategic profiles.
- Historical artifacts remain immutable; the new artifact launches current-code
  sessions rather than comparing historical endpoint hashes causally.

## Unresolved Questions

- Whether these three profiles represent broad player strategy space remains
  unresolved.
- Whether action cadence or retry counts indicate actual comprehension or
  cognitive burden remains unresolved.
- Human learning, classroom effectiveness, calibration, and policy validity
  require separate evidence.

## Design Implications

- Reuse the existing MCP wrapper and retry-aware capture boundary.
- Keep structural gaps separate from descriptive retry and pacing signals.
- Preserve runtime promotion deferral unless a later review identifies a
  concrete unexplained player-facing, instructor-facing, or domain gap.

## Risks

- A generated artifact can appear clean if retries or incomplete traces are
  dropped; the runner must retain those fields.
- Aggregate operating events can leak rival state into player evidence; the
  audit must count ownership explicitly.
- Profile and seed repetition does not establish general gameplay validity.
