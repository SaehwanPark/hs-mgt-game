# Mechanism Design - Live Consultant Advice and Advisory History

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation slice following the v0.10.38
advisor-market proposal review.

## Slice Boundary

- Generate exactly four options (`A`–`D`) for each human competitive
  observation, with visible tradeoffs and no ranking or optimal label.
- Use one shared deterministic generator for genesis, live CLI, and MCP
  observations.
- Store the exact options shown on the corresponding competitive transition for
  instructor debrief comparison.

## State, Beliefs, and Observations

- Advice uses only the owning system's `PlayerObservation`, including reported
  cash runway, workforce/community summaries, and visible intelligence gaps.
- Options are state-conditioned by visible categories but never expose hidden
  rival actions or predict a guaranteed outcome.
- A report contains four total attributed advisory options and labels them
  `Advisory — not binding`.

## Commands, Events, and Effects

- No commands, events, effects, payroll, or actor utility changes are introduced
  by this slice.
- The stored advisory list is explanatory history only and cannot alter
  validation or transition results.

## Determinism and Replay Notes

- `resolve_competitive_month` captures advice from the same prior world and prior
  aggregated actions used to render the pre-decision observation, before the
  month-start tick mutates the working copy.
- The advisory field is serialized with a default empty value for legacy
  competitive transition JSON; state hashing remains based on world state.

## Open Questions

- The deferred advisor market remains gated on evidence that this generic
  advice baseline is insufficient for a documented learning or strategy need.

## Educational Debrief Hooks

- Retain monthly option titles and tradeoff bullets beside the actual player
  commands.
- Show the available advice and chosen action without scoring compliance or
  treating any option as correct.
- Preserve enough history for instructor discussion of decision quality versus
  outcome quality.

## Conclusion

Promote only the generic advice baseline. Keep differentiated advisors,
employment state, payroll, and AI parity outside this slice.
