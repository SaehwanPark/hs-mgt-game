# Implementation Plan — Visual/audio Phase 10.2 evaluation preparation v0.12.87

## Task restatement

Prepare an authorized, privacy-bounded structured evaluation protocol for the
Phase 10.1 first-month visual/audio slice, including task definitions,
accessibility/audio instruments, finding categories, revision-log template, and
an explicitly blank go/no-go decision record.

## Current understanding

- Phase 10.1 technical integration is complete and machine-checkable.
- Phase 10.2 still lacks a current protocol and canonical task/rating artifact.
- No participant data or authorized human review is available in the current
  task, so preparation must not fabricate results.

## Assumptions

- The protocol uses only fictional seeded runs and actor-visible presentation.
- A repository-safe evaluation artifact excludes personal/health data,
  identifying recordings, private game state, and unapproved claims.
- Preparation items can close technically; collection, interviews, findings,
  and go/no-go remain human-gated.

## Minimal implementation plan

1. Add the canonical JSON task/rating/privacy/decision schema.
2. Add a facilitator guide and empty revision-log template.
3. Add a regression test for exact task categories, rating dimensions, privacy
   restrictions, blank decision state, and absence of fabricated findings.
4. Mark only protocol/task preparation items complete in the roadmap; keep
   collection/interview/classification/decision items open.
5. Update project records, version projections, CI, and lessons, then run the
   full matrix and sole-review workflow.

## Acceptance criteria

- First-session, recognition, consequence-tracing, accessibility, and audio
  tasks are explicit and use stable IDs.
- All roadmap rating dimensions are represented.
- Finding categories are exactly defect, preference, or scope expansion.
- Privacy constraints and human authorization are explicit.
- Revision log and go/no-go decision remain blank/pending.
- No participant result, legal conclusion, or educational claim is added.

## Non-goals and stop conditions

- Do not conduct or simulate participant sessions.
- Do not collect or commit personal data, recordings, private state, or human
  results.
- Do not mark evaluation outcomes or go/no-go as complete.
- Stop if the protocol requires new runtime behavior, external services, or
  changes to simulation/host authority.

## Review checklist

- Task schema matches the roadmap and facilitator guide.
- Privacy, evidence limits, and blank decision state are preserved.
- Exactly one existing code reviewer inspects the final diff.

## Risk label

Risk: low

Reason: this creates evaluation preparation artifacts only and does not alter
runtime, simulation, asset, or authority behavior.
