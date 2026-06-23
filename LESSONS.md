# Lessons Learned

Use this file to record practical lessons that would save future contributors or
agents meaningful time. Keep entries factual, concise, and tied to prevention.

## Canonical Docs Define Scope Before Structure

- Context: Initiating the spec-driven-development baseline for an early research
  and design repository.
- Symptom: It would be easy to invent implementation, CI, scenario, or release
  conventions before the roadmap calls for them.
- Cause: The repository already has canonical proposal, roadmap, design
  principles, and harness documents that define durable boundaries and phase
  order.
- Resolution: Root SDD documents were initiated as lightweight indexes and
  boundary records, not as detailed process or architecture commitments.
- Prevention: Before major changes, read `README.md`, `docs/proposal.md`,
  `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/harness/health-policy-strategy-game/team-spec.md`; document deferred
  conventions instead of filling them in prematurely.
