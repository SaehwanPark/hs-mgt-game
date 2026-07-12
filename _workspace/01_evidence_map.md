# Evidence Map - Phase 7 Teachability Evidence Review v0.12.3

## Scope

Audit whether the current affiliation post-fix and competitive artifacts keep
the full decision-to-debrief chain inspectable across two campaign shapes,
without changing either mechanism or making a learning claim.

## Sources Reviewed

- `_workspace/experiments/v0.12.2-affiliation-observation-context/results.json`
  and `diagnostics.md`.
- `_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/results.json`
  and `diagnostics.md`.
- `docs/playtest-findings-v0.12.1.md`,
  `docs/playtest-findings-v0.12.2.md`, `SPEC.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.
- `src/mcp/session.rs`, `src/affiliation/observe.rs`, and existing artifact
  validation tests.

## Evidence lanes

| Lane | Source | Contract | Scope |
| --- | --- | --- | --- |
| affiliation context | v0.12.2 post-fix artifact | 9 runs × 6 stages; commitments, alternatives, assumptions, stage commands, hashes, and debrief | regional affiliation |
| competitive strategy | v0.11.12 current-code capture | 9 runs × 24 months; actor-visible observations, commands, hashes, consultant/advisory markers, and debrief | competitive regional |

The source versions remain explicit. The competitive artifact is the last
approved current-code capture for that unchanged campaign surface; this audit
does not silently relabel it as a new v0.12.3 capture.

## Review dimensions

- Decision context: actor-visible observation, legal command surface, and the
  submitted command are present before each committed transition.
- Action response: validation failures/retries are represented honestly, with
  zero unexpected failures in these source artifacts.
- Transition follow-through: each trace entry points to its accepted history
  transition and state hash.
- Outcome context: complete history, final hash, and run completion are
  present.
- Debrief explanation: source-specific retrospective markers connect actions
  and outcomes to decision-quality review.
- Context lane: affiliation checks its post-fix typed context; competitive
  checks consultant options and the advisory comparison surface.

## Assumptions

- Existing artifacts are immutable source records and their declared batch IDs,
  campaigns, profiles, seeds, and trace schemas are authoritative.
- Cross-campaign comparison is structural, not a claim that stage and month
  semantics are interchangeable.
- Absence of a structural gap does not establish comprehension, debrief
  clarity, strategy quality, balance, winnability, or educational effect.

## Unresolved Questions

- Whether the aligned trace is usable or understandable to people is not
  measured.
- Whether either campaign is balanced, winnable, or strategically optimal is
  outside this audit.
- A future concrete gap may require a source-specific follow-up rather than a
  generalized cross-campaign change.

## Design Implications

- Normalize only audit metadata; preserve source-specific fields and wording.
- Report counts by source and by review dimension so a supported aggregate
  cannot hide a lane-specific omission.
- Treat missing markers as evidence gaps, not reasons to infer or synthesize
  hidden actor information.

## Risks

- A permissive marker check could overstate traceability; tests must reject
  malformed or incomplete source records.
- Similar debrief concepts use different wording across campaigns; contracts
  must be source-specific rather than forcing false textual uniformity.
- A historical competitive artifact could be mistaken for a fresh runtime
  capture; its pinned version and provenance must remain visible.
