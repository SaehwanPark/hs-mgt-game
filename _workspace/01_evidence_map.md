# Evidence Map — Visual and Audio Phase 9 AI-Agent Evaluation and Revision v0.12.25

## Scope

Phase 9 evaluates repeated Phase 8 capture artifacts as technical and
interface-task evidence. It adds deterministic comparison and decision logging;
it does not run agents, infer cognition, or alter the game.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 9 gate and AI-agent testplay
  testing strategy.
- `SPEC.md`, `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, `ARCHITECTURE.md`, and the harness team spec.
- Phase 8 protocol/documentation, `gui/playtest.mjs`,
  `scripts/diagnose_gui_playtests.py`, the valid capture fixture, and focused
  tests.

## Mechanisms and Institutions

The mechanism is evidence comparison across interface-task traces, not a new
health-policy mechanism. Existing campaign institutions, actor authority,
observations, and debrief meanings remain the source of any policy content
that appears in a capture. The analyzer treats campaign, role, task, seed,
interface mode, and accessibility mode as declared context so it does not pool
stabilization, competitive, and affiliation meanings into one score.

## Actor Incentives and Information

- The capture producer controls which declared role/task and input artifacts are
  submitted; the analyzer cannot know whether a role declaration describes a
  real cognitive profile.
- Product/contributor reviewers use summaries to decide whether a visible
  interface hypothesis deserves a bounded revision.
- The analyzer sees only allowlisted event evidence, failure classes, and
  declared metadata. It must not recover hidden state, raw payloads, model
  reasoning, or private rival actions.
- No actor utility, organizational objective, social welfare, or educational
  score is computed. A revision priority is an operational triage label only.

## Assumptions

- Phase 8 diagnostics is the single capture-schema authority; Phase 9 consumes
  its result rather than reimplementing hidden browser or simulation rules.
- Repeated fixture/capture sets can reveal coverage gaps and artifact failures,
  but not why a person or agent behaved as it did.
- Stable ordering by declared file/session key is sufficient for reproducible
  comparison without timestamps or random sampling.
- A product decision log is the appropriate boundary for hypotheses and
  deferred revisions because capture analysis must not mutate the product.

## Unresolved Questions

- Which future real-agent traces, if authorized, will supply evidence beyond
  contract fixtures and static checks?
- How should repeated interpretation mismatches be investigated without
  converting them into unsupported human or policy claims?
- Which product owner should approve a UI revision when a finding is only a
  technical proxy rather than an observed human problem?

## Design Implications

- Add one small standard-library Python analyzer that consumes paths or a
  directory of Phase 8 captures and calls the existing validator.
- Report coverage dimensions, per-run counts, failure classes, evidence lanes,
  deterministic comparisons, and prioritized revision candidates with an
  explicit hypothesis/limit field.
- Keep invalid captures visible as data-quality findings and keep valid
  unresolved human questions separate from technical completion.
- Check that recommended revisions are deduplicated and sorted by fixed
  priority/category keys; never auto-edit GUI or simulation files.

## Risks

The main risk is false interpretation: a missing event may reflect a harness
omission, an adapter failure, or a task mismatch rather than interface friction.
The analyzer must label these as hypotheses, retain source capture IDs, and
route decisions to a human/contributor log. It must also fail closed on invalid
captures and preserve the Phase 8 hidden-field boundary.
