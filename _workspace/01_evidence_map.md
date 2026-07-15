# Evidence Map — Visual and Audio Phase 3 Contextual Action Submission v0.12.19

## Scope

Phase 3 adds the first graphical decision-to-submit path for one
`competitive-regional-v1` month. It reuses canonical command parsing,
validation, costs, and transition submission; it does not resolve or animate a
month in the browser.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 3 requirements and exit gate.
- Phase 0 alignment, Phase 1 static desktop, Phase 2 live read-only document,
  ADR-0011, and merged GUI.
- `src/cli/competitive_parse.rs`, `src/model/competitive_command.rs`,
  `src/model/resources.rs`, `src/sim/validate_competitive.rs`,
  `src/mcp/session.rs`, and existing command/transition tests.
- README, SPEC, architecture, design principles, and project harness spec.

## Mechanisms and Institutions

The player drafts institutional commands for workforce, capacity, intelligence,
payer, policy/pledge, and project decisions. The host supplies the action
catalog and validates the entire batch against current resources/rules. The
browser only composes canonical text from host-provided templates and keeps a
local draft until validation and submission.

## Actor Incentives and Information

The player sees selected action parameters, canonical previews, host-derived
AP/cash/political-capital totals, visible constraints, delays, and uncertainty.
The player does not see hidden rival actions, resolved stochastic inputs, future
outcomes, or a client-calculated “best” action. A rejected batch leaves the
current observation/history/hash untouched.

## Assumptions

- Existing seven competitive command families are the complete Phase 3 catalog.
- Host action metadata is descriptive presentation information; validation and
  costs remain model/host-owned.
- Draft actions are local and reversible; submit is a single host operation.
- A successful submit returns the existing committed session envelope; monthly
  resolution animation and causal explanation remain Phase 4.

## Unresolved Questions

- Which command family should receive the first contextual default for later
  taskplay without implying an optimal strategy?
- How should Phase 4 sequence a committed response when a batch has multiple
  action families and delayed effects?
- Which action metadata requires domain review before broader campaign support?

## Design Implications

- A separate non-mutating validation read is safer than using a rejected submit
  as a preview and gives the browser recoverable errors.
- Canonical templates must be host-supplied or derived from the existing parser
  vocabulary; the browser must not recreate enum lists or numeric bounds.
- Aggregate costs must be returned by the host using existing command cost
  methods so the client cannot drift from simulation legality.
- The UI must distinguish draft, host-validated, submitted, rejected, and
  committed states; only the last two can reference transition history.

## Risks

The action builder can appear authoritative if it labels a draft as accepted or
predicts an outcome. Contract tests must require canonical command previews,
host validation, no local cost formulas, no submit before validation, and
unchanged state after rejection. Technical task checks do not prove human
usability, learning, strategic quality, or policy validity.
