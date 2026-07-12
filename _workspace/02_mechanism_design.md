# Mechanism Design - Regional Affiliation Playtest Validation v0.12.1

## Goal and Roadmap Phase

Phase 7.5–7.7 validation evidence for the completed v0.12.0 affiliation
runtime. The slice tests the existing player-facing observation, command,
history, replay-summary, actor-response, and debrief boundaries without changing
the transition mechanism.

## Slice Boundary

- Setting: one fictional Riverside nonprofit system and one Pine Valley partner.
- Campaign: opt-in `regional-affiliation-v1`, six monthly stages.
- Matrix: independent, deferred, and pursuit policies × seeds 42, 43, and 44.
- Output: one JSON capture, one deterministic audit, one diagnostics report,
  and focused Python contract tests.
- Excluded: runtime tuning, balance, legal forecasting, human evaluation, GUI,
  AI-rival affiliation behavior, and generalized playtest infrastructure.

## Actors and Authority

- Riverside policy controls only its staged commands.
- Partner, review institution, labor representatives, commercial payer, and
  community coalition responses come from explicit resolved inputs and are
  reported as separate outcomes.
- The audit must not treat an actor response as Riverside utility or social
  welfare.

## State, Beliefs, and Observations

- Each captured turn stores the MCP observation and legal command hint before
  submission.
- Each accepted command stores a transition summary and state hash.
- The debrief stores final status, Riverside outcome deltas, stage-level actor
  response labels, actor rationales, and the alternatives prompt.
- The audit compares fields present in the typed `AffiliationObservation` with
  the MCP-rendered observation. Repeated omission of alternatives/assumptions
  is recorded as a bounded decision-time context gap.

## Commands, Events, and Effects

- Independent: `assess`, `posture choice=independent`, then `hold`.
- Deferred: `assess`, `posture choice=defer`, then `hold`.
- Pursuit: `assess`, `posture choice=pursue`, maximum legal commitment,
  `submit_review` when offered, `await_review` when offered, and
  `integrate decision=begin` when approved.
- Validation failures are captured separately; a complete matrix must not rely
  on retrying an invalid command.

## Strategic Interaction

The artifact is a policy probe, not a new actor decision procedure. It records
how the existing deterministic resolver exposes partner, review, labor, payer,
and community responses after Riverside's bounded choices. The policy labels
are descriptive and do not establish that any posture is optimal.

## Assumptions and Parameters

- Seeds are fixed reproducibility inputs.
- Maximum pursuit commitments use the existing legal range and total cap.
- Existing ruleset numbers remain untouched.
- Missing fields in an interface observation are treated as an evidence gap only
  when the typed observation contract documents them.

## Educational Debrief Hooks

- Does the decision trace preserve what Riverside could see before each command?
- Can the debrief distinguish organizational deltas from actor responses?
- Does the player-facing observation show the alternatives and assumptions that
  the debrief later asks the player to consider?

## Determinism and Replay Notes

- The runner records only deterministic outputs from the existing MCP server.
- It omits session identifiers and process-specific metadata from persisted
  output.
- State hashes, six-turn ordering, and debrief stage lines are validated for
  every matrix coordinate.

## Open Questions

- The next bounded implementation may expose the omitted observation context in
  MCP output, but that decision belongs to a separate slice after this audit.
- The capture cannot establish human comprehension, winnability, calibration,
  or legal plausibility.
