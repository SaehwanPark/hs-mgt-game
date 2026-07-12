# Lessons Learned

Use this file to record practical lessons that would save future contributors or
agents meaningful time. Keep entries factual, concise, and tied to prevention.

## Keep Release Checks Read-Only and Metadata-Scoped

- Context: The final release-readiness queue item called for one lightweight
  quality check before any packaging or publication work.
- Symptom: A release helper can quietly expand into registry, tag, or deployment
  automation and make local verification harder to reproduce.
- Resolution: Added one dependency-free checker for package-version projections,
  documented the same local command, and ran it in CI without touching runtime
  code or external services.
- Prevention: Keep early release checks read-only, compare only documented
  metadata, and require a separate authorized slice for publication workflows.

## Close Breadth Only With Scope-Matched Evidence

- Context: The breadth queue offered several attractive expansion directions,
  while the current competitive campaign already had multiple bounded tradeoffs.
- Symptom: Treating a broad queue label as permission for a new actor or patient
  model would expand scope without a demonstrated gameplay or learning need.
- Resolution: Audited the existing source boundaries and committed playtest
  artifacts, then removed the queue item while preserving public-payer, patient,
  actor, and equilibrium limits plus a concrete reopening condition.
- Prevention: Inventory implemented mechanisms first; require a concrete
  unexplained gap before adding state, actors, outcomes, or abstractions.

## Keep GUI Proofs Thin and Adapter-Owned

- Context: The GUI Future item called for one surface consuming existing game
  outputs without weakening core inspectability.
- Symptom: A browser prototype could accidentally duplicate command parsing,
  transitions, hidden state, or external asset/network assumptions.
- Resolution: Implemented rendering plus an injected `submitTurn` adapter,
  empty-input checking only, no external assets, and static contract tests; the
  unavailable browser backend was recorded as a verification limit.
- Prevention: Keep GUI state presentation-only, make the server authoritative,
  audit assets/network calls, and separate visual verification limits from user
  usability claims.

## Synchronize Queue Text With Completed Runtime Proposals

- Context: The v0.12.7 affiliation proposal was complete, but the related
  affiliation/acquisition item remained in the Future queue.
- Symptom: A stale queue entry could imply that a new runtime mechanism was
  still required and encourage scope expansion.
- Resolution: Revalidated the six contracts and 9-run/54-stage artifact, then
  removed the queue item while preserving broader acquisition deferral and a
  reopening condition.
- Prevention: After a proposal closes, audit all queue references and either
  remove the completed item or explicitly route it to a new evidence gap.

## Separate Pressure Evidence From Tuning Authorization

- Context: The v0.12.4 review found workforce-capacity counts rising across
  tested difficulty tiers, and v0.12.6 made the typed context visible.
- Symptom: A monotonic simulated signal could be mistaken for a causal balance
  diagnosis or general Expert winnability result.
- Resolution: Closed the queue item only after confirming exact observation
  controls, 15/15 named Expert clearability overlap, source-version limits, and
  no unexplained gap; no runtime values changed.
- Prevention: Treat descriptive pressure as routing evidence, require a new
  unexplained gap for tuning, and preserve clearability and provenance limits.

## Remove Completed Queue Items Without Making Learning Claims

- Context: The v0.12.3 cross-campaign teachability review had already found no
  structural gap, but its Future queue entry remained active text.
- Symptom: Leaving the item in the queue obscured the actual next work, while
  promoting trace coverage as learner evidence would overstate the result.
- Resolution: Added a closure artifact with source-specific coverage, 18 runs,
  270 transitions, and zero gaps; removed the item and recorded a concrete
  reopening condition without changing runtime behavior.
- Prevention: Close queue entries only with scope-matched evidence and preserve
  explicit limits and reopening criteria.

## Reconcile Runtime Proposals Before Adding Another Mechanism

- Context: The v0.12.7 SPEC item called for a separate affiliation runtime
  proposal, while ADR-0010 and the v0.12.0 implementation already supplied
  that boundary.
- Symptom: Treating the queue text as an unimplemented feature would duplicate
  runtime scope and risk expanding the actor model unnecessarily.
- Resolution: Audited source markers and the committed 9-run/54-stage artifact
  across state, observations, resolved inputs, transitions, replay, and debrief;
  closed the queue item as an existing-runtime confirmation with no new code.
- Prevention: Before promoting a Future item, reconcile SPEC, ADRs, runtime
  ownership, and committed evidence; authorize new runtime only for a concrete
  unexplained gap.

## Prove Observation-Only Changes With Immutable Transition Controls

- Context: v0.12.5 identified safe typed workforce fields that were absent from
  the competitive MCP observation.
- Symptom: A presentation fix could appear harmless while accidentally changing
  simulation behavior or actor-visible scope.
- Resolution: Added only formatter lines and a boundary test, then replayed the
  75-run/1,800-transition compatibility matrix against immutable all-tier and
  Expert artifacts; every history and state-hash sequence matched exactly.
- Prevention: For observation-boundary changes, count every rendered trace,
  compare complete histories as well as hashes, and assert excluded hidden
  markers remain absent before considering the gap closed.

## Separate Pressure Signals From Their Decision-Time Context

- Context: The v0.12.4 workforce-capacity signal was visible in operating
  consequences, but the MCP formatter omitted typed staffing and capacity
  counts that could help interpret it before a command.
- Symptom: Trust labels, labor guidance, and debrief attribution were present,
  while the numeric staffing/capacity context was absent from the player view.
- Resolution: Defined an observation-only follow-up from `PlayerObservation` and
  explicitly excluded targets, effective allocations, future hires, and rival
  private state.
- Prevention: Audit typed-vs-rendered fields after identifying a mechanism signal;
  route omissions to the owning presentation boundary before changing balance or
  difficulty values.

## Treat Difficulty Signals as Routing Evidence

- Context: The v0.12.4 review compared existing all-tier and standalone Expert
  artifacts before any difficulty tuning.
- Symptom: Workforce-capacity bottleneck counts rose from 0 Easy to 160 Expert,
  while Normal, Hard, and Expert scripted action counts were identical.
- Resolution: Reported workforce capacity as a candidate visible pressure signal
  and kept it behind a separate design gate; Expert completion remained a
  bounded clearability proxy for named profiles and seeds.
- Prevention: Recompute pressure from committed events/effects, preserve source
  versions, and never translate monotonic simulated counts into causal balance,
  winnability, or human-perceived difficulty claims.

## Compare Evidence Lanes Without Flattening Campaign Semantics

- Context: The v0.12.3 Phase 7 review joined the v0.12.2 affiliation post-fix
  artifact with the approved v0.11.12 competitive teachability capture.
- Symptom: Both lanes expose decision, transition, outcome, and debrief records,
  but their stage/month units and context vocabulary differ.
- Resolution: Used a shared structural audit with source-specific context and
  debrief markers, preserving pinned source versions and reporting 18 runs and
  270 transitions without a new capture.
- Prevention: Normalize only audit metadata. Keep campaign-specific contracts
  explicit, and never turn deterministic trace coverage into a comprehension,
  balance, winnability, or learning claim.

## Isolate Tests That Share User-Scoped Files

- Context: CI ran persistence tests in parallel against the shared
  `competitive_session.save` path.
- Symptom: A delete-idempotency test could remove the file while a round-trip
  test was loading it, producing a missing-file failure that serial tests hid.
- Resolution: Added a test-module mutex around the shared-path tests without
  changing production persistence behavior.
- Prevention: Run the default parallel test command before handoff and isolate
  tests that mutate user-scoped filesystem paths.

## Audit Typed Observations Against Rendered Interfaces

- Context: The v0.12.1 regional-affiliation capture compared the typed
  `AffiliationObservation` with the MCP observation lines used by scripted
  policies.
- Symptom: The runtime retained alternatives, assumptions, and commitments,
  but the player-facing MCP rendering omitted them while the debrief later
  asked the player to compare alternatives.
- Resolution: Recorded the structural gap in v0.12.1, then rendered only the
  existing safe typed fields through the MCP boundary in v0.12.2 without
  changing transitions, rulesets, or replay/hash contracts.
- Prevention: When validating a new campaign, compare the typed observation
  fields with every rendered CLI/MCP surface before making balance or learning
  claims; keep omitted fields as an interface slice rather than leaking hidden
  state into the player view.

## Keep New Campaign Contracts Separate from Competitive Golden Paths

- Context: The regional affiliation slice needed new state, inputs, replay, and
  debrief behavior while the competitive campaign has a frozen seed-42 contract.
- Resolution: Kept affiliation state, canonical hashing, replay artifact version,
  scenario fields, and transition modules campaign-specific; only the campaign
  router and shared interface surfaces were extended.
- Prevention: Before sharing a new field or hash schema, prove that it is truly
  campaign-neutral. Otherwise add a narrow typed boundary and regression-test the
  unchanged golden path.

## Consolidation Design Must Precede Consolidation Runtime

- Context: The next roadmap candidate after the v0.11.12 validation checkpoint
  was regional affiliation/acquisition work.
- Resolution: Narrowed the first slice to one affiliation-first design gate and
  kept acquisition, runtime state, legal outcomes, and transaction finance out
  of scope.
- Prevention: Require evidence mapping, explicit actor/observation boundaries,
  domain QA, and debrief contracts before promoting any consolidation mechanic
  into `SPEC.md` Present or runtime code.

## Current-Code Teachability Captures Should Reuse Policy and Retry Contracts

- Context: The v0.11.12 continuation needed current-code observation and pacing
  evidence after the broader v0.11.11 all-tier matrix.
- Resolution: Reused the historical observation-driven policy and retry-aware
  MCP boundary while adapting only the versioned artifact and audit contract.
- Prevention: Keep historical evidence immutable, preserve rejected-command
  metadata, and use a focused profile/seed matrix when the active question is
  teachability rather than difficulty breadth.

## Re-run the Full Matrix After Difficulty Changes

- Context: The v0.11.9 Expert capture and v0.11.10 source synthesis did not
  establish current all-tier behavior after the v0.11.7 risk-posture and v0.11.8
  rival-resource changes.
- Resolution: Reran the five-profile, three-seed, four-tier matrix on current
  code and audited 1,440 committed months while preserving the Normal hold
  control hash.
- Prevention: Do not infer current all-tier clearability or trajectory behavior
  from a pre-change matrix plus an Expert-only post-change capture.

## Preserve Source-Specific Evidence Contracts

- Context: The v0.11.10 synthesis combined the v0.11.6 strategy audit with the
  v0.11.9 Expert capture, which expose different trace shapes and metadata.
- Resolution: Validated each artifact independently and summarized only shared
  coverage facts without normalizing raw evidence into a new schema.
- Prevention: Treat cross-artifact continuity as a source-boundary audit; do not
  infer causal outcome comparisons or shared fields that a source does not declare.

## Revalidate Expert After Difficulty Surface Changes

- Context: The v0.11.7 and v0.11.8 slices changed AI risk posture and rival
  starting resources, so older Expert clearability evidence no longer covered
  the current difficulty surface.
- Resolution: Ran a fresh Expert-only matrix over five deterministic policy
  lanes and three named seeds while preserving the Normal seed-42 control hash.
- Prevention: Treat difficulty changes as needing post-change clearability
  evidence before claiming Expert remains severe but playable; do not tune
  balance from a completion matrix alone.

## Compare Strategy Traces Across the Latest Frozen Matrix

- Context: The v0.11.6 continuation needed to test whether the v0.11.5
  operating-outcome evidence supported profile-level strategy comparison.
- Resolution: Reused the latest frozen v0.11.4 capture, composed the existing
  observation/debrief contract, and grouped traces by profile, seed, and
  difficulty without launching new sessions or changing runtime behavior.
- Prevention: Treat trajectory and signal-response differences as descriptive
  evidence only; require a concrete unexplained product or domain gap before
  promoting runtime work.

## Re-run Evidence After a Debrief Surface Fix

- Context: The v0.11.2 audit identified 469 operating signal-months with no
  month-specific outcome line, and v0.11.3 added the missing player-owned
  debrief output.
- Resolution: Re-ran the unchanged five-profile, three-seed, four-difficulty
  matrix and audited 1,440 monthly sections instead of treating focused report
  tests as complete evidence.
- Prevention: Keep post-fix matrix validation separate from runtime changes;
  require exact month-level coverage and preserve the golden control hash.

## Render Committed Monthly Outcomes Beside Monthly Decisions

- Context: The v0.11.2 audit found that operating signal-months had complete
  decision and transition attribution but only a global debrief mechanism list.
- Resolution: Render the player-owned operating result from each committed
  transition next state inside its month section, while leaving active
  observations and global attribution separate.
- Prevention: Keep post-run outcome lines explicitly labeled as realized
  game-unit results; do not treat them as decision-time knowledge, calibrated
  dollars, or causal proof.

## Separate Month-Level Debrief Links From Global Attribution

- Context: The v0.11.2 audit found complete decision and transition traces for
  469 operating signal-months, but no month-specific operating-outcome lines in
  the debrief; global attribution summaries appeared in all 60 runs.
- Resolution: Count month-level decision links, month-level outcome links, and
  global attribution summaries as separate evidence dimensions.
- Prevention: Never treat an aggregated debrief mechanism list as proof that a
  specific month’s loss or bottleneck was explained retrospectively.

## Preserve a Golden Control Beside New Policy Matrices

- Context: The v0.11.1 matrix intentionally submits different commands from the
  existing seed-42 competitive preset, so its transition hashes differ.
- Resolution: Run a separate hold-policy control and assert the known month-one
  hash while keeping new policy trajectories in their own evidence artifact.
- Prevention: Do not compare a changed-policy trajectory directly with a golden
  hash; preserve an unchanged control path when validating runtime compatibility.

## Operating Diagnostics Must Separate Traceability From Causality

- Context: The v0.11.1 matrix exposed repeated losses, bottlenecks, and threshold
  crossings across deterministic policy lanes.
- Resolution: Report ranges and candidate signals while explicitly deferring
  causal marginal-effect, dominance, balance, calibration, and learning claims.
- Prevention: Use controlled follow-up evidence before tuning an operating rule
  or promoting a player-facing change.

## Close the Consequence Loop Before Expanding Content

- Context: External review found that competitive cash funded actions but had
  no recurring operating-income source despite extensive capacity and staffing.
- Resolution: Add one aggregate demand-to-volume-to-margin cycle using existing
  state before adding actors, commands, or service lines.
- Prevention: A new operational domain should identify how it changes demand,
  staffed production, revenue, cost, cash, quality, or access; otherwise defer it.

## AI Playtests Do Not Become Human Evidence Through Repetition

- Context: Recruitment and participant-study costs make structured human
  playtests infeasible for the current personal project.
- Resolution: Use bounded MCP AI playtests as the active gameplay-validation
  path and retain a separate funded approval gate for any future human study.
- Prevention: Never translate AI completion, explanation, pacing, or diversity
  into claims about enjoyment, comprehension, cognitive load, or learning.

## Decision-to-Debrief Audits Need Source-Specific Retry Contracts

- Context: Auditing decision-time context, retries, delayed observations,
  outcomes, and debrief framing for v0.10.58 across the v0.10.43, v0.10.50,
  v0.10.51, and v0.10.54–v0.10.56 artifacts.
- Symptom: A shared retry rule treated the v0.10.51 resource-probe artifact as
  incomplete because that source records the pre-submit observation rather than
  an `observation_after_failure` field.
- Resolution: Keep source-specific contracts, accept the declared pre-submit
  observation only when the source also records the expected failure, and treat
  malformed or mismatched retry state as limited evidence.
- Prevention: Do not normalize heterogeneous evidence into a shared schema or
  infer successful recovery from absent fields; preserve each source's declared
  observation and retry boundary.

## Event-Specific Debrief Coverage Is Still Traceability Evidence

- Context: Auditing v0.10.43, v0.10.50, v0.10.51, and v0.10.54–v0.10.56
  artifacts for debrief use in v0.10.57.
- Symptom: A source can contain observations, commands, hashes, and a debrief
  while still appearing to prove more educational value than it does.
- Resolution: Check each source-specific visibility, response,
  follow-through, outcome, and explanation step; preserve missing fields as
  explicit evidence gaps and keep runtime promotion deferred.
- Prevention: Do not infer debrief clarity, comprehension, learning, strategy
  quality, or causal value from event-specific trace continuity alone.

## Response-Conditioned Recovery Is Still Simulated-Policy Evidence

- Context: Testing whether the existing project-limit error surface supports a
  response-conditioned recovery path in v0.10.56.
- Symptom: A scripted policy can branch on a plain error and recover cleanly,
  which may look like evidence that the interface is comprehensible.
- Resolution: Record the allowed observation/error surface, exclude structured
  fields from the recovery branch, preserve rejected-turn and hash continuity,
  and label the result as traceability evidence.
- Prevention: Do not promote validation hints, schema changes, or human-learning
  claims from deterministic simulated-policy recovery alone.

## Missing Structured Hints Need Recovery Evidence Before Promotion

- Context: Narrowing the v0.10.51 concurrent-project trace fact in v0.10.54.
- Symptom: A stable validation code without a structured resource hint can look
  like an interface defect even when the plain error, unchanged turn, visible
  project state, safe retry, and debrief explanation remain available.
- Resolution: Capture the full rejected-turn surface across named seeds and
  separate response-shape evidence from actual repeated decision friction.
- Prevention: Do not promote validation wording or schema changes from field
  asymmetry alone; require a player-facing, instructor-facing, or domain-review
  artifact that demonstrates unexplained recovery failure.

## Cross-Artifact Synthesis Should Preserve Source Boundaries

- Context: Synthesizing the v0.10.50–v0.10.52 Phase 7 evidence chain for
  v0.10.53.
- Symptom: Different artifacts expose different trace shapes, so a synthesis can
  accidentally imply a shared schema or stronger claim than the sources support.
- Resolution: Validate each source using its declared fields, verify only the
  shared control and matrix identities, and report continuity separately from
  product-gap promotion.
- Prevention: Do not normalize heterogeneous evidence into a generalized
  analytics layer or infer causality, strategy quality, learning, or balance
  from a complete continuity check.

## Turn-Level Traces Are Required for Pacing Proxies

- Context: Auditing v0.10.50 observation-driven traces for v0.10.52.
- Symptom: Aggregate action totals hid whether commands were concentrated in
  particular months or spread across the campaign.
- Resolution: Derive action, hold, active-month, and multi-action metrics from
  the recorded turn trace while preserving the raw source artifact.
- Prevention: Treat temporal command concentration as a descriptive pacing or
  action-overload proxy only; do not infer human cognitive burden or promote
  runtime changes without player-facing, instructor-facing, or domain evidence.

## Expected Validation Failures Need Separate Run Status

- Context: Probing cash, action-point, and concurrent-project limits for
  v0.10.51.
- Symptom: A complete campaign can contain validation failures intentionally
  submitted as part of a resource-boundary probe.
- Resolution: Store expected probe failures separately from unexpected failures,
  verify the rejected turn remains unchanged, and record the safe retry that
  advances the campaign.
- Prevention: Do not count intentional probes as final replay failures or infer
  exploit value, balance, or comprehension from their presence alone.

## Zero-Retry Observation Captures Are Compatibility Evidence

- Context: Capturing nine observation-driven Hard competitive runs for v0.10.50.
- Symptom: Complete runs with no validation failures can look like proof that
  the command surface is comprehensible or educationally effective.
- Resolution: Preserve the full observation, legal-hint, command, retry,
  history, hash, and debrief trace, then label zero retries as capture
  compatibility only.
- Prevention: Do not promote command, guidance, difficulty, or debrief changes
  without a concrete player-facing or instructor-facing gap.

## Synthesize Evidence Without Promoting Runtime Work

- Context: Closing the v0.10.45–v0.10.48 competitive teachability evidence
  chain.
- Symptom: Several supported artifacts can look like cumulative justification
  for a runtime change even when each artifact reports only traceability or
  descriptive variation.
- Resolution: Check source continuity and declared evidence dimensions in a
  read-only synthesis, then route runtime promotion only from a concrete gap
  that existing observations, histories, diagnostics, and debriefs cannot
  explain.
- Prevention: Keep source-specific trace shapes and evidence limits visible;
  do not infer causality, strategy value, balance, winnability, or learning
  from a complete chain.

## Separate Visible Monitor Response From Monitor Exposure

- Context: Adding the v0.10.43 rival-information follow-through matrix.
- Symptom: A monitored and unmonitored comparison can show information
  exposure without showing whether a later decision used that information.
- Resolution: Pair monitor-reactive and monitor-ignoring arms with an
  unmonitored control, and record the signal source month beside the exact next
  turn command.
- Prevention: Treat endpoint differences from intentionally different policy
  commands as descriptive only; require actor-visible signal-to-command
  traceability before discussing monitor value or debrief usefulness.

## Evidence Synthesis Must Close Promotion Gates

- Context: Synthesizing the v0.10.39–v0.10.41 consultant-advice evidence chain.
- Symptom: A sequence of successful traceability and simulated-policy captures
  can look like justification for adding a richer advisor system.
- Resolution: Close the chain with an explicit synthesis that separates
  visibility and continuity evidence from advice quality, learning, causality,
  and advisor-market value.
- Prevention: Keep generic decision-support baselines in place until a later
  artifact identifies a concrete teachability or strategy limitation that the
  proposed runtime expansion would solve.

## Pair Advice-Aware Evidence With Hash-Matched Controls

- Context: Adding the v0.10.41 consultant-advice usage matrix.
- Symptom: Advice-aware commands can change cash runway and make an inherited
  scripted command invalid later in the campaign.
- Resolution: Record advice-aware selection and fallback signals separately,
  guard commands using visible resources, and compare advice-ignoring control
  hashes with the prior traceability artifact.
- Prevention: Never infer advice value from endpoint differences when the policy
  itself changed; require exact observation/history/debrief continuity and a
  matching control before interpreting the evidence.

## Build the Local MCP Binary Before Wrapper Evidence Runs

- Context: Adding the v0.10.40 consultant-advice traceability matrix.
- Symptom: The wrapper launched an existing `target/debug/hs-mgt-game-mcp`
  binary, which can be older than the checked-out source and produce misleading
  evidence about current MCP output.
- Prevention: Evidence runners that invoke the local MCP binary must run
  `cargo build --quiet --bin hs-mgt-game-mcp` before starting sessions, then
  record the package version from the same worktree.

## Test Recurring Costs Against Every Scenario Cash Scale

- Context: Evaluating a future in-house advisor market with monthly salaries.
- Symptom: A recurring cost can appear modest against a high-cash exemplary
  scenario while consuming a large share of the default 60-cash campaign, which
  has no general recurring operating-income flow.
- Prevention: Before promoting a recurring-cost mechanic, test its full campaign
  burden against every supported scenario cash scale and document when a
  month-start tick must occur before observation and command validation.

## Separate Future Queue Ranking From Promotion Rules

- Context: Re-ranking `SPEC.md` Future items after several validation and
  proposal-review slices had accumulated.
- Symptom: The Future queue mixed ranked product work, evidence analysis,
  platform support, architecture discipline, and release readiness as if they
  were equivalent next actions.
- Cause: Cross-cutting guardrails and promotion criteria were stored as ranked
  tracks, making it harder to see the next bounded slice.
- Resolution: Move promotion rules and architecture/documentation discipline
  above the ranked queue, then rank only actionable future tracks.
- Prevention: When updating `SPEC.md` Future, keep the ranked list focused on
  promotable work. Put phase gates, evidence requirements, non-goals, and
  architecture freezes in separate guardrail text.

## Expansion Ideas Need Proposal Gates Before SDD Promotion

- Context: Reviewing future difficulty, regional M&A, and GUI expansion ideas
  after the competitive campaign already had substantial validation evidence.
- Symptom: Large attractive features can look ready for implementation because
  the current architecture can plausibly support them.
- Cause: Difficulty tuning, consolidation mechanics, and GUI work each carry
  different evidence, domain, licensing, and architecture risks that should not
  be collapsed into one implementation track.
- Resolution: Add a proposal-review artifact first, then update roadmap and SDD
  Future tracks while keeping runtime behavior unchanged.
- Prevention: For future broad product ideas, write the review gate before
  promoting work into `SPEC.md` Present. Name the smallest slice, evidence
  limits, non-goals, and stop conditions before editing runtime code.

## Preserve Live-Agent Retry and Replacement Metadata

- Context: Adding the v0.10.15 live LLM/sub-agent difficulty gate after the
  v0.10.14 independent reviewer-agent matrix.
- Symptom: A completed replay artifact can look cleaner than the live decision
  process that produced it, especially when delegated runs retry invalid
  commands or one delegated session does not complete.
- Cause: The replay script validates accepted command streams, while the live
  process includes wrapper mistakes, cash-overrun retries, and occasional
  incomplete delegated sessions.
- Resolution: Store `live_validation_retries` and `decision_source` in the
  artifact, and document the replacement Competitive Analyst Normal stream
  explicitly in the findings.
- Prevention: Future live-decision evidence should preserve retry and source
  metadata even when the final replay has zero validation failures.

## Do Not Read Difficulty Effects From Non-Adaptive Policies

- Context: Adding the v0.10.14 independent reviewer-agent live-capture matrix
  after the v0.10.13 static-vs-adaptive comparison.
- Symptom: A Normal/Hard matrix can look like it should explain difficulty
  balance simply because both difficulty labels are present.
- Cause: If the submitted player policy does not branch on difficulty and the
  observed endpoint metrics are identical, the artifact mainly tests policy
  completion and capture workflow, not difficulty pressure.
- Resolution: Label the reviewer-policy artifact as simulated-agent evidence and
  explicitly state that identical Normal/Hard endpoints do not isolate
  difficulty balance.
- Prevention: Future difficulty evidence gates should either use policies that
  intentionally react to difficulty-visible pressure, live month-by-month LLM or
  human decisions, or a separate analysis that explains why the difficulty
  setting is expected to change outcomes.

## Encode Evidence Matrix Coordinates in Run Metadata Before Expanding Diagnostics

- Context: Adding the v0.10.13 static-vs-adaptive live-capture comparison after
  the v0.10.12 difficulty-pressure matrix.
- Symptom: A new comparison axis can look like it requires changes to shared
  diagnostic tooling before the evidence question is answered.
- Cause: Existing live-capture diagnostics already summarize runs by
  `profile_name`; the missing piece was clear per-run variant metadata and
  readable matrix labels.
- Resolution: Add `policy_variant` metadata to the artifact and include variant,
  difficulty, and seed in `profile_name`, preserving the existing diagnostic
  script.
- Prevention: For future Phase 7 evidence matrices, first test whether the new
  axis can be represented in artifact metadata and labels. Change shared
  diagnostics only when repeated evidence work needs aggregation that labels
  cannot support.

## Reuse Existing Playtest Policies for Evidence Slices Before Inventing New Ones

- Context: Adding the v0.10.12 live difficulty-pressure capture slice after the
  v0.10.11 conservative live-capture matrix.
- Symptom: A new evidence slice can look like it needs new scripted command
  policies, which increases validation risk and duplicates prior playtest
  logic.
- Cause: The pressure and difficulty-adaptive policies already existed in
  `scripts/run_automated_playtests.py`; the missing piece was the
  observation-by-observation live capture artifact, not new gameplay behavior.
- Resolution: Reuse the existing automated policies through `play_session` with
  `capture_trace=True`, and fail fast when a run has validation failures or does
  not complete 24 transitions.
- Prevention: For future Phase 7 evidence work, first check existing automated
  policies and diagnostics before adding new policy logic or runtime exports.

## Capture MCP Evidence at the Wrapper Boundary First

- Context: Adding the v0.10.9 live MCP capture evidence slice after v0.10.7
  replayed preplanned sub-agent commands.
- Symptom: It was tempting to treat observation-by-observation evidence as a new
  Rust MCP DTO or runtime export requirement.
- Cause: The existing Python MCP wrapper already receives observations, legal
  command hints, submitted commands, validation failures, transition summaries,
  and debriefs during normal play.
- Resolution: Add optional trace capture to `scripts/play_game.py` and keep the
  Rust MCP interface unchanged.
- Prevention: For future playtest evidence gaps, first check whether the Python
  wrapper can record the needed actor-visible data. Change Rust MCP DTOs only
  when a specific required field is not already crossing the boundary.

## Access-Loop Diagnostics Should Precede Runtime Cooldowns

- Context: The v0.10.1 free-form Hard seed-variation findings showed access-heavy
  operator policies repeatedly issuing public access commitments under persistent
  scrutiny cues.
- Symptom: The repeated commands could be mistaken for a balance problem or a
  need for automatic runtime cooldowns.
- Cause: The operator policies reacted to recurring observation language without
  remembering recent pledges or requiring a high-access threshold before
  pledging again.
- Resolution: The v0.10.2 diagnostic compared unchanged baseline policies
  against cooldown and reported-access-threshold variants. Both variants reduced
  access pledges while completing all sessions, but also changed access and
  community-trust endpoints for access-heavy profiles.
- Prevention: Treat repeated pledge loops as guidance or operator-policy
  diagnostics first. Do not tune pledge effects or add runtime cooldowns without
  stronger human, LLM, or domain-review evidence.

## Post-Guidance Validation Can Change Endpoint Tradeoffs

- Context: The v0.10.4 post-guidance validation compared unchanged free-form
  Hard policies against a guidance-aware variant that suppressed repeated or
  high-access pledges.
- Symptom: Aggregate access pledges fell sharply, but access-heavy profiles also
  ended with lower access and/or community trust.
- Cause: Redirecting repeated pledges toward neutral payer negotiation reduced
  public legitimacy effects while preserving legal command completion.
- Prevention: Treat lower repetitive-command counts as a behavior signal, not
  automatically as an improved gameplay outcome. Document endpoint tradeoffs
  before promoting guidance heuristics into runtime cooldowns, formula tuning,
  or default playtest policies.

## Phase 7 Synthesis Must De-Duplicate Repeated Controls

- Context: The v0.10.5 synthesis combined the v0.10.0-v0.10.4 free-form Hard
  competitive artifacts.
- Symptom: Raw session totals can look stronger than the evidence actually is
  because the same seed/profile baseline matrix is intentionally repeated across
  artifacts as a control.
- Cause: Validation slices reuse baseline policies to compare guidance or
  operator-policy variants. Those repeated controls are useful for regression
  and comparison, but they are not independent player samples.
- Prevention: When synthesizing playtest evidence, report artifact session
  counts and overlap caveats together. Do not use repeated controls to justify
  runtime cooldowns, balance tuning, human-learning claims, or empirical
  calibration.

## Targeted Project Playtests Must Account for Scenario Delays

- Context: Adding the v0.9.7 `project-coverage` automated MCP playtest target.
- Symptom: Early project-heavy policies failed with `concurrent projects 3
  exceed limit 2`, even when commands appeared spaced apart.
- Cause: Scenario mechanics such as CON legal objections can delay project
  completion, so a later project command may overlap with more in-flight work
  than a simple duration count suggests.
- Prevention: For targeted project-command playtests, use minimal divisible
  budgets, keep no more than two plausible concurrent projects including
  scenario delays, and rerun the full target before documenting findings.

## Scripted MCP Policies Must Budget for Long-Run Cash Draws

- Context: Extending competitive scripted playtest policies beyond month 3 for
  v0.9.6.
- Symptom: Early versions of the extended policies failed around months 5, 10,
  12, 19, or 22 with validation errors such as cash required exceeding
  available cash.
- Cause: The validator correctly includes active project monthly draws and
  current command costs. A policy can become invalid many months after an early
  project or recruitment decision if later commands assume cash that no longer
  exists.
- Prevention: When writing scripted 24-month policies, keep project commands
  rare, prefer low-cost direct investments for coverage slices, and rerun the
  full `python3 scripts/run_automated_playtests.py --json-output ...` batch
  before documenting findings.

## Clinical Service Line Expansion Checklist

- Context: Implementing the Ambulatory Surgery Center (ASC) service line in the competitive regional campaign.
- Symptom: Compile-time errors for missing fields/variants or missing match arms, state hash mismatches in integration tests, and display/transition calculation drifts.
- Cause: Clinical service lines touch almost all layers of the game engine (state, observations, commands, parser, autocompletion, resolver, effects engine, AI, display dashboard, scenario loader, state hashing, and test fixtures).
- Prevention: When adding any new clinical service line, ensure you update the following modules in a single consistent change:
  1. **Core Models**: Add capacity field to `HealthSystemState` in `src/model/competitive_world.rs` and enum variants to `InvestDomain`/`ProjectKind` in `src/model/competitive_command.rs`.
  2. **Observations**: Add capacity to `PlayerObservation` in `src/model/campaign.rs` and map it in both `src/sim/observe_ai.rs` and `src/sim/observe_competitive.rs`. Update test fixtures in `src/competitive/fixtures.rs`.
  3. **Effects Engine**: Register the capacity variant in `effects_competitive.rs` (under strike suspension lists and resolution).
  4. **CLI Parser & Autocomplete**: Add parsing rules in `competitive_parse.rs`, register REPL autocompletes (and update completion unit tests) in `repl.rs`, and document commands in `guidance.rs`.
  5. **Resolution Formatting**: Update command string formatters in `resolution.rs` and `debrief/report.rs`.
  6. **Rival AI**: Include the new capacity in target staffing calculations and `InvestDomain` command scoring in `src/actors/ai_player.rs`.
  7. **Genesis & Scenarios**: Initialize the capacity in `src/competitive/genesis.rs` rival templates, and load it from TOML configs in `src/scenario/mod.rs`.
  8. **Simulation & Display Kernels**: Update target staffing formulas, priority greedy allocation loops, strike adjustments, overflow/diversion/deferral rules, and total capacity calculations in both `transition_competitive.rs` and `display/executive_report.rs` in tandem.
  9. **State Hashing**: Bump schema version in `competitive_hash.rs`, append the new capacity to the hashed string format, and update golden test hashes in `tests/golden_competitive_seed42.rs`.


## Exhaustive Enum Match Updates for Command Vocabularies

- Context: Adding the Cardiology service line and CardiologyUnit project kind to the command vocabularies.
- Symptom: Compilation failures on unmatched patterns in `src/competitive/resolution.rs` and `src/debrief/report.rs`.
- Cause: Match expressions on `InvestDomain` and `ProjectKind` enums in serialization and debrief report formatters were not updated to include the new variants.
- Prevention: When extending command or project enums (`InvestDomain`, `ProjectKind`, etc.), perform a global repository search or run `cargo check` early to guarantee that all match arms in serialization wrappers, command-to-string formatters, REPL autocomplete registries, parser modules, and debrief report generators are exhaustively populated.


## Maintain Original Execution Sequence for Dynamic Timeline Events

- Context: Refactoring hardcoded timeline events to run dynamically from parsed scenario TOML.
- Symptom: An integration test for Month 10 strike action failed because a capital project ended up delayed by 4 months (resolve month 19) instead of 3 (resolve month 18).
- Cause: The refactored trigger logic executed dynamic timeline events before ongoing scenario tick effects (such as active nurse strike costs and project delays). Since the timeline event set the strike active flag to `true`, the active nurse strike logic immediately executed and added an extra 1-month delay in the same turn, which differed from the original sequential ordering where the active nurse strike check ran before the Month 10 strike trigger.
- Prevention: When externalizing or dynamically refactoring sequential transition logic, ensure ongoing condition evaluations run *before* event trigger checks in the turn-start phase to match the exact original execution sequence.


## Direct Investment Limits in Tests

- Context: Adding the Intensive Care Unit (ICU) service line with direct investment commands.
- Symptom: A test for direct ICU investment failed validation with `InvestAmountTooHigh { amount: 60, max: 40 }`.
- Cause: The competitive ruleset defines `max_invest_amount = 40` as the maximum allowed direct investment per turn to keep resource consumption bounded.
- Prevention: When writing unit or integration tests that verify capacity expansion, ensure that direct `Invest` commands do not exceed the ruleset's single-turn investment limit (e.g., 40). For larger expansions, split investments across multiple turns or use capital projects (`ProjectKind`).


## Default Capacities in Backward-Compatible Scenarios to Avoid Staffing Deficits

- Context: Adding the Emergency Department (ED) service line with staffing targets to existing scenario models.
- Symptom: Adding default non-zero `emergency_capacity` at genesis/scenario mapping induced turn-1 staffing deficits and access/quality penalties for existing scenarios because start-of-month systems lacked the nurses and physicians to staff the new ED bays.
- Cause: Scenario structures (e.g. `ScenarioSystemState`) mapped and parsed TOML objects. When defaults are hardcoded to positive values for new fields, they apply immediately to old test files/fixtures, altering their operational assumptions and failing regression tests.
- Prevention: Always set new capacity or service-line default parameters to `0` unless scenario-specific data exists. This allows systems to begin without initial staffing deficits, preserving legacy test runs while allowing players to expand into the new service lines in subsequent turns.


## Keep Scenario Briefs Parameter-Complete to Avoid Downstream Gaps

- Context: Drafting the `competitive-exemplary-v1` scenario brief under Track 2.
- Symptom: Initial drafts of the scenario timeline referred to delayed consequences for underfunded EHR projects and nurse staffing ratios, but lacked initial parameters for starting staffing ratios or definitions of EHR project costs, duration, and Action Point requirements in the brief.
- Cause: Scenario authoring sometimes relies on mechanism-design documents or core codebase defaults without reflecting those constraints explicitly in the student/instructor-facing brief.
- Prevention: Every scenario brief must explicitly specify starting parameters, project costs, duration, Action Point requirements, and immediate vs. delayed consequences of events (such as strikes or underfunding) to remain actionable for future scenario developers.

## Post-Milestone SDD Reviews Should Rank, Not Expand

- Context: After the public playable prototype reached v0.2.0, the repo had a
  thorough runnable stabilization slice, a bounded competitive preview, MCP
  playtest evidence, and a long Future backlog.
- Symptom: Future work was specific but still read as a broad menu, making it
  too easy for the next agent to pick platform expansion, balance tuning, or
  new actors before the product risk was re-evaluated.
- Cause: Milestone completion changed the main uncertainty from "can the game
  run end to end?" to "is repeated play explainable, teachable, and strategically
  interesting?"
- Resolution: Keep `SPEC.md` `Present` empty, record the progress-review slice
  as completed, and rank Future tracks so debrief/instructor analysis,
  exemplary scenario authoring, and evidence-confidence work lead runtime
  expansion.
- Prevention: After major runnable milestones, perform an SDD review that
  explicitly names the next risk, ranks Future tracks, and refreshes stale
  companion docs before promoting a new implementation slice.

## End-Session Metrics Belong In Debrief, Not Active Observation

- Context: Closing the v0.1.49 competitive MCP evidence gap by exposing final
  player tradeoff metrics.
- Symptom: Competitive playtest findings could compare commands and hashes but
  could not make outcome-distribution claims.
- Cause: The active MCP observation surface correctly avoids omniscient state,
  but the end-session debrief had not yet summarized the final human-system
  metrics available in committed history.
- Resolution: Add final player tradeoff and resource lines to competitive
  `end_session` debrief only, derived from genesis and final committed human
  system state.
- Prevention: Put post-run analysis metrics in debrief or instructor surfaces,
  not active-play observations, unless a design explicitly changes the actor's
  information boundary.

## Playtest Policies Need Campaign-Stable Detection

- Context: Running the v0.1.49 automated MCP playtest batch after the AI-agent
  validation pivot.
- Symptom: The batch appeared to hang on the first stabilization `submit_turn`.
- Cause: Scripted policies detected stabilization by checking for the Turn 1
  `staffed_beds` legal-command hint. From Turn 2 onward the policies fell into
  the competitive branch, submitted invalid competitive commands to the
  stabilization parser, and retried forever.
- Resolution: Detect stabilization by the MCP legal-command surface shape,
  launch the built stdio MCP binary, and make scripted validation failures raise
  with campaign, turn, command, and error context.
- Prevention: In playtest automation, branch on stable campaign/session
  metadata or legal-command surface shape, not one turn-specific hint. Scripted
  policies should fail fast on validation errors rather than silently retrying.

## SDD Status Drift Needs A Cross-Doc Scan

- Context: Cleaning up `SPEC.md` after competitive preview, scenario-loader, MCP,
  and playtest slices had landed.
- Symptom: `SPEC.md` and `ARCHITECTURE.md` reflected the current runtime, while
  companion docs still described competitive work as design-only, stubbed, or
  planned I1-I8 runtime.
- Cause: Slice completion updated release history faster than older design docs
  that originally framed the implementation sequence.
- Resolution: Refresh `SPEC.md` Future into gated actionable tracks, archive
  displaced completion detail, and scan canonical/companion docs for stale
  status phrases before final verification.
- Prevention: For SDD cleanup PRs, run a targeted `rg` over `SPEC.md`,
  `README.md`, `ARCHITECTURE.md`, and `docs/*.md` for old version numbers,
  "stub", "design only", "runtime deferred", and completed slice names before
  calling the docs aligned.

## Broad Feedback Should Become Gates Before Features

- Context: Translating external assessment into future SDD planning after the
  architecture, MCP interface, scenario loader, and competitive preview already
  existed.
- Symptom: Strong conceptual feedback can invite broad new abstractions,
  diagnostics, scenario tooling, or calibration frameworks before gameplay has
  proved the need.
- Cause: The project can represent sophisticated health-policy simulation, but
  the next risk is whether repeated play is difficult, legible, interesting, and
  teachable.
- Resolution: Convert feedback into falsifiable playtest hypotheses,
  strategy-space diagnostics, debrief QA, canonical-scenario gates, and
  model-confidence labels rather than runtime expansion.
- Prevention: For future SDD planning updates, ask which finding would justify
  implementation. If no playtest, authoring, debrief, or domain-review evidence
  exists, keep the item in Future and label the needed evidence.

## Agent Playtests Need Evidence Labels

- Context: Replacing planned external human playtest recruitment with AI-agent
  and sub-agent playtests.
- Symptom: It is easy for validation language to drift from "agent traces show
  the debrief is inspectable" into "players learned the intended material."
- Cause: Agent runs are reproducible and useful, but they are simulated-player
  evidence rather than human educational measurement.
- Resolution: Added an active agent-playtest protocol, ADR-0009, glossary terms,
  and roadmap language that separate command/gameplay evidence from human
  learning and policy-validation claims.
- Prevention: When adding playtest findings, label the actor type, seed,
  profile or prompt, observations, commands, and evidence limits before making
  follow-up recommendations.

## MCP SDK Schema Derives Need Direct Dependencies

- Context: Adding the first local MCP stdio server with the official `rmcp`
  Rust SDK.
- Symptom: `JsonSchema` derives failed even though the SDK re-exports schema
  helpers.
- Cause: Derive macros resolve the `schemars` crate name directly.
- Resolution: Add `schemars` as a direct dependency and keep MCP DTOs in
  `src/mcp/` instead of adding serialization/schema derives to core model types.
- Prevention: For protocol adapter DTOs, depend directly on the derive macro's
  crate and keep schema-facing structs at the adapter boundary.

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

## First Engine Proof Should Stay Scripted

- Context: Replacing the placeholder CLI with the first deterministic
  architecture proof.
- Symptom: It is tempting to add scenario loading, interactive menus, richer
  actor frameworks, or hash libraries immediately.
- Cause: The roadmap asks for vertical slices before broad frameworks, and the
  codebase had no existing architecture to constrain abstractions.
- Resolution: The first proof uses one scripted command, explicit resolved
  inputs, simple integer metrics, deterministic replay, and no dependencies.
- Prevention: Add loaders, modules, dependencies, and broader actor frameworks
  only when a later slice has at least two concrete examples that need the same
  boundary.

## Second Slice Can Still Stay Single-File

- Context: Adding the first state-policy response after the initial
  payer-negotiation proof.
- Symptom: A second command and second actor decision can make a module split
  feel immediately attractive.
- Cause: The design boundary is now visible, but the prototype still has one
  compact transition function and no reusable scenario, CLI, or persistence
  boundary.
- Resolution: The policy response reused the existing command, observation,
  event, effect, history, and replay shapes without adding dependencies or
  modules.
- Prevention: Split modules when reuse or independent testing needs become
  concrete, not merely because a second branch exists in the demo.

## Debriefing Can Start From Committed History

- Context: Adding the first educational debrief to the deterministic demo.
- Symptom: It is tempting to design a general reporting framework, scenario
  schema, or instructor export format before the first debrief exists.
- Cause: The existing transition history already contains observations, actor
  rationales, attributed effects, and final state needed for a useful teaching
  summary.
- Resolution: The first debrief is a deterministic report over committed
  history, with no new dependency, loader, or persistent artifact format.
- Prevention: Add reporting structure only when repeated debrief outputs need a
  shared format or external consumers.

## First Playability Step Can Be Hard-Coded

- Context: Adding the first player-facing CLI choice after the scripted
  deterministic demo and debrief were working.
- Symptom: It is tempting to add a command parser, scenario schema, or save/load
  path as soon as stdin appears.
- Cause: The immediate roadmap need is to test whether different strategic
  paths produce understandable outcomes, not to define durable content formats.
- Resolution: The first playable slice uses three compiled strategy paths and a
  small input boundary that selects among existing deterministic transitions.
- Prevention: Add parsers and scenario loaders only when repeated playable
  content needs external authoring or persistence.

## Seeded Inputs Belong Outside The Transition Core

- Context: Replacing per-path hard-coded `ResolvedInputs` with a seeded
  stochastic input boundary.
- Symptom: It is tempting to call RNG helpers inside `transition()` once
  exogenous variation is needed.
- Cause: The architecture requires stochasticity to be resolved before the
  deterministic core evaluates state changes.
- Resolution: Added `resolve_inputs(seed, prior, ruleset)` with named streams
  and splitmix64 outside `transition()`, then committed resolved inputs into
  history for replay and debrief.
- Prevention: Keep all random draws, measurement noise, and exogenous shocks in
  explicit pre-transition resolution steps; never hide RNG inside the core.

## Third Turn Can Reuse Command And Actor Patterns

- Context: Adding a workforce pressure turn after payer and policy interactions.
- Symptom: A third command and third actor decision can invite a general
  campaign framework or module split.
- Cause: The demo already has command validation, actor rationales, effects,
  history, replay, and debrief patterns that extend cleanly.
- Resolution: Added `RespondToWorkforcePressure` with a nursing workforce
  representative decision, extended strategy presets with `third_command`, and
  kept everything in `src/main.rs` without new dependencies.
- Prevention: Extend the existing command and actor-decision shapes turn by turn
  until reuse boundaries justify extraction into modules.

## Fourth Turn Can Reuse Coalition Patterns

- Context: Adding a regional access coalition turn after payer, policy, and
  workforce interactions.
- Symptom: A fourth command and fourth actor decision can invite a general
  coalition framework or module split.
- Cause: The demo already has command validation, actor rationales, effects,
  history, replay, and debrief patterns that extend cleanly.
- Resolution: Added `JoinRegionalAccessCoalition` with a coalition liaison
  decision, extended strategy presets with `fourth_command`, and kept everything
  in `src/main.rs` without new dependencies.
- Prevention: Extend the existing command and actor-decision shapes turn by turn
  until reuse boundaries justify extraction into modules.

## Observation Revisions Can Stay In Briefings

- Context: Adding prior-period access measurement revisions after the coalition
  turn without rewriting committed history.
- Symptom: It is tempting to retroactively edit prior transition observations
  when later data arrives.
- Cause: The architecture requires immutable committed observations while still
  teaching the difference between reported and revised estimates.
- Resolution: Added `access_measurement_revision` to resolved inputs and
  `prior_access_revision` to observations; debrief notes revisions while history
  remains append-only.
- Prevention: Keep revisions as explicit briefing inputs or notes; never mutate
  prior committed transition records.

## Phase 2 Docs Should Constrain Before They Format

- Context: Expanding the system-boundary and ontology draft after the first
  four-turn vertical-slice prototype.
- Symptom: It is tempting to introduce scenario schemas, actor-card templates,
  or parameter ledgers while documenting the conceptual boundary.
- Cause: The roadmap calls for ontology and causal boundaries before broader
  implementation conventions.
- Resolution: The Phase 2 document names actors, authority, observations,
  commands, causal categories, exclusions, and deferred ontology work without
  defining a file format or calibration process.
- Prevention: Use boundary docs to stabilize vocabulary and scope first; create
  loaders, schemas, and ledgers only when a later slice needs executable or
  evidence-backed artifacts.

## Actor And Scenario Docs Should Gate Runtime Expansion

- Context: Continuing from the Phase 2 boundary draft into the first Phase 3
  design artifacts.
- Symptom: It is tempting to add a fifth turn, a new actor, or a scenario
  schema as soon as the current demo has a coherent four-turn loop.
- Cause: The next roadmap need is to clarify actor authority, information,
  objectives, and learning goals before expanding runtime content.
- Resolution: Added an actor-card template and first scenario brief without
  changing Rust behavior, adding a loader, or introducing a runtime schema.
- Prevention: Before adding a strategic actor or scenario mechanism, write the
  actor card and scenario rationale first; only implement when the slice can be
  tested deterministically and explained in debrief.

## Replay Hashing Should Stay Canonical And Bounded

- Context: Adding stable state hashes to the deterministic replay proof.
- Symptom: It is tempting to add a serializer, save format, cryptographic hash
  dependency, or durable replay artifact as soon as hashes appear.
- Cause: The immediate Phase 4 need is drift detection during replay, not
  persistence or tamper-proof storage.
- Resolution: Added a labeled canonical state record and local 64-bit FNV-1a
  hash for committed transition checks without changing gameplay mechanics.
- Prevention: Keep replay hash inputs explicit and versioned; add external
  replay artifacts or stronger hash guarantees only when save/load, analysis,
  or release requirements make them necessary.

## CLI Playability Can Improve Without New Input Semantics

- Context: Adding a starting executive dashboard and strategy previews after
  the replay hash proof.
- Symptom: It is tempting to make the preview step a command parser, forecast
  engine, or per-turn choice system.
- Cause: The first Phase 5 playability need is better pre-run context, while
  the existing compiled strategy paths still provide the bounded behavior under
  test.
- Resolution: Added pure dashboard and commitment-preview helpers derived from
  existing state and `StrategyPlan` values, without changing transitions,
  resolved inputs, actor decisions, or replay hashes.
- Prevention: Keep CLI affordance improvements at the display boundary until
  the scenario action vocabulary justifies interactive per-turn command entry.

## Per-Turn Play Can Reuse Existing Command Shapes

- Context: Adding per-turn interactive command entry after the dashboard preview
  slice.
- Symptom: It is tempting to add a general command grammar, scenario schema, or
  per-turn posture menus before the first interactive loop exists.
- Cause: The four-turn demo already has typed commands, validation, observation
  briefings, actor decisions, and replay hashes that can be driven turn by turn.
- Resolution: Added play-mode selection, pure per-command parsers with
  access-stabilization defaults, executive briefings from observation data only,
  and concise turn summaries while preserving preset strategy paths for
  regression.
- Prevention: Add parsers and posture menus only when repeated playable content
  needs external authoring or more than numeric parameter entry.

## Replay Artifacts Can Stay Human-Readable and Dependency-Free

- Context: Adding deterministic replay artifact export after interactive play.
- Symptom: It is tempting to add JSON crates, cryptographic hashes, or a general
  save/load framework as soon as external replay is mentioned.
- Cause: The committed history already stores commands, resolved inputs, and
  per-turn state hashes needed for verification.
- Resolution: Added a versioned line-oriented `replay-artifact-0.1.15` format
  with pure serialize, deserialize, and verify helpers plus an optional
  post-run export prompt.
- Prevention: Keep artifact formats explicit and versioned; add stronger
  integrity guarantees or mid-run persistence only when analysis or classroom
  workflows require them.

## Competitive Track Justifies Scoped Command Parser

- Context: Designing the competitive regional market campaign with Stata-like CLI.
- Symptom: Earlier lessons deferred general command parsers for the stabilization
  vertical slice, which uses numeric prompts and turn-locked commands.
- Cause: The competitive sketch requires verb+argument entry, help, and
  autocomplete at a scale numeric prompts cannot support.
- Resolution: ADR-0006 limits the parser to the competitive campaign I/O layer
  only; stabilization demo unchanged; parse output is typed commands feeding the
  existing validation and transition boundary.
- Prevention: Do not generalize the REPL to stabilization until a concrete need
  appears; keep parser logic out of `transition()` per ADR-0001.

## Rustyline Helper Types Need Full Trait Set

- Context: Adding competitive verb Tab-autocomplete using `rustyline`.
- Symptom: Compilation fails with trait-bound errors even when a custom
  completer compiles in isolation.
- Cause: In `rustyline`, `Helper` requires `Completer + Hinter + Highlighter +
  Validator` on the same helper type.
- Resolution: Implemented empty/default `Hinter`, `Highlighter`, and `Validator`
  traits on the completer helper struct.
- Prevention: When introducing a new `rustyline` helper, scaffold all required
  helper trait impls first, then add completer logic.

## Scenario Loading Should Start As A Data Boundary

- Context: Adding the first runtime scenario loader after the scenario format
  draft was approved for a narrow slice.
- Symptom: It is tempting to make scenario files own presets, transition logic,
  arbitrary paths, competitive campaigns, or migration policy immediately.
- Cause: The first proven need is to externalize the existing stabilization
  genesis and schedule, not to create a general authoring platform.
- Resolution: Added `scenario-toml-0.1.40` with one bundled
  `stabilization-v1` TOML fixture and validation before fresh runs; transitions,
  replay artifacts, and session saves stayed unchanged.
- Prevention: Extend scenario loading only when playtest or authoring evidence
  identifies a concrete repeated need; keep executable logic out of scenario
  files.

## Interactive Terminal Tests Can Hang Without Stdin Redirection

- Context: Running `cargo test` in a pseudo-terminal (PTY) runner or workspace sandbox.
- Symptom: Tests that read standard input for campaigns (e.g. `competitive_month_loop_runs_three_months_in_non_tty_context`) hang or timeout.
- Cause: `std::io::stdin().is_terminal()` returns `true` inside a PTY, causing the game to block waiting for human command input instead of executing the fallback non-TTY batch.
- Resolution: `stdin_uses_fallback_input()` in `src/cli/io.rs` treats `cfg!(test)` like non-TTY stdin so competitive campaign tests use preset fallback batches instead of rustyline. Stdin redirection (`cargo test < /dev/null`) still works for manual runs.
- Prevention: Route any new CLI stdin prompts through `stdin_uses_fallback_input()` (or equivalent) so unit tests never block on terminal detection inside PTYs.

## Clippy CI Check Prevents Code Quality Decay

- Context: Integrating `cargo clippy --all-targets -- -D warnings` into the CI workflow.
- Symptom: The repository had accumulated 32 clippy errors (including manual prefix stripping, complex type signatures, collapsible ifs) because clippy was not enforced in the pipeline.
- Cause: The original `.github/workflows/ci.yml` only executed `cargo fmt` and `cargo test` without checks for code quality and compiler lints.
- Resolution: Resolved all 32 clippy issues across production and test code, and added a lint checking step to the CI pipeline.
- Prevention: Run `cargo clippy --all-targets -- -D warnings` locally before committing and always include clippy checks in the CI runner to catch lints early.

## Centralize Post-Run Debriefing Logic for Shared CLI/MCP Surface

- Context: Adding instructor-visible summaries and decision quality reviews for stabilization and competitive campaigns.
- Symptom: It is tempting to write separate CLI-only or MCP-only report string formatting functions or duplicate logic between the MCP session handler and the CLI campaign loop.
- Cause: The CLI campaign and MCP session end endpoint need the same structured information. Duplicating code violates modularity and invites drift.
- Resolution: Consolidated both stabilization and competitive campaign debriefing functions (including the new instructor run summaries) into the `src/debrief/report.rs` module. The CLI campaign runner and the MCP session end endpoint call the exact same module functions, sharing the same representations.
- Prevention: Keep all report formatting and debrief generation code in `src/debrief` and have other layers (CLI and MCP) consume it, ensuring a single source of truth for debriefing text.

## write_to_file Scopes and Parameter Mismatch Scrutiny

- Context: Updating workspace pipeline files (`_workspace/*`) under the harness team spec.
- Symptom: `write_to_file` returned a tool error when writing to `_workspace/00_input/request-summary.md` with `ArtifactMetadata` specified.
- Cause: Specifying `ArtifactMetadata` flags the file as an agent artifact, which the tool restricts to the absolute path `/home/saehwan/.gemini/antigravity-cli/brain/`.
- Resolution: Omit `ArtifactMetadata` entirely when creating or modifying standard workspace and codebase files outside the conversation-specific artifacts directory.
- Prevention: Do not include `ArtifactMetadata` in `write_to_file` arguments unless writing a conversation report/plan directly to the chat artifacts directory.

## Scenario starting parameters should be complete to prevent initial deficits

- Context: Implementing clinical capacity and staffing requirements (nurses, physicians, admins) in the competitive campaign.
- Symptom: A unit test for the nurse staffing deficit failed because workforce trust dropped more than the isolated nurse deficit.
- Cause: The system genesis template initialized administrator counts below their target ratio, creating a starting admin deficit that triggered immediate burnout penalties in turn 0/genesis calculations.
- Prevention: Ensure that all starting staffing headcounts are set to at least their target ratio levels in the genesis template unless a starting deficit is intentionally part of the scenario. In unit tests, explicitly set target counts for all supporting headcounts (like admins) to isolate the testing of a specific deficit (like nurses).

## Competitive Staffing and Capacity Design Safeguards

- Context: Addressing senior code reviewer findings for Track 5 clinical service line capacity and staffing.
- Symptoms: Compounding exponential decay of access/quality metrics; AI players unable to recruit physicians/admins; immediate understaffing penalties due to instant construction vs. delayed recruitment; leaking rival private events in CLI summaries; integer division budget exploits.
- Causes & Resolutions:
  - **In-place Metric Mutation vs. Additive Penalties:** Direct multiplication of state metrics (`access_index`, `quality_index`) by utility ratios compounds exponentially to 0. Resolved by replacing multiplication with a linear monthly additive drop proportional to the staffing deficit severity.
  - **AI Competitor Completeness:** AI players were restricted to `RecruitRole::Nurse`. Resolved by extending AI candidate command generation to check and generate recruitment options for physicians and admins when their counts fall below target ratios.
  - **Physical Capacity Construction Delays:** Instant physical bed expansion paired with delayed nurse recruitment resulted in immediate, unavoidable turn-0 penalties. Resolved by queuing bed capacity additions with a 1-month delay, matching outpatient clinics, allowing players to recruit beforehand.
  - **Rival Event Filtering:** Rival private operational events (burnout, etc.) were displayed to the player. Resolved by filtering player-facing summaries to skip events starting with competitor names.
  - **Budget Division Exploits:** Players could buy projects with non-multiple budgets, under-paying total costs due to integer truncation. Resolved by validating that project budgets must be a multiple of the duration.
- Prevention: Always use additive drops for ongoing penalties, ensure AI player vocabulary handles all roles, keep construction and recruitment delays aligned, maintain observation boundaries in displays, and validate budget divisibility.

## Scenario Deserialization Backward Compatibility & Systems Length Validation

- Context: Implementing competitive scenario loading and validation (Track 1 / Phase 6.2).
- Symptom: Extending the `Scenario` struct with new required fields broke parsing of the existing stabilization scenario TOML file. Also, difficulty selection had to align with the number of systems in the custom file.
- Cause: TOML deserializers using `#[serde(deny_unknown_fields)]` reject input when fields are added unless they are marked optional. Difficulty choice also determines how many AI rival controllers are initialized.
- Resolution: Wrapped all new competitive-specific fields (`initial_market`, `systems`) and existing stabilization-specific fields (`initial_state`, `turn_schedule`, `actor_stubs`) in `Option`. Validated in `validate_stabilization_scenario` and `validate_competitive_scenario` that the required fields for each campaign are present. In the CLI session runner, verified that `systems.len() == 1 + difficulty.k_rivals()` before initializing.
- Prevention: Make all campaign-specific scenario fields optional in the shared deserialization struct and enforce campaign-specific schema requirements during separate validation passes.

## Competitive Campaign Length Extension & Autosave Implementation

- Context: Extending the competitive regional campaign from a 3-month preview to a full 24-month horizon with mid-campaign serialization, autosave, and reload.
- Symptom: Serializing structs with `'static str` references (e.g. `AiProfile`, `Event`, `AttributedEffect`) causes compilation or runtime issues with serde, and simultaneous loop progression requires keeping track of the historical transition chain.
- Cause: Serde cannot directly deserialize `'static str` since it represents memory leaked references. Additionally, resuming a competitive campaign requires restoring both the starting state and all resolved transitions to date.
- Resolution: Derived `Serialize` and `Deserialize` on all competitive types. For structs with `'static str` fields, serialized them as standard strings, and manually leaked them using `Box::leak` on deserialization to reconstruct stable `'static str` references. Bounded campaign execution to 24 months, auto-saved the transition history on early quit (`q`/`quit`) into `.config/hs-mgt-game/competitive_session.save`, and added a resume menu selection to reload it. Finally, enabled exporting the complete `CompetitiveHistory` as a replay JSON file upon campaign completion.
- Prevention: Separate save structures (`session.save` and `competitive_session.save`) to isolate serialization logic. When deserializing lifetime-bound static strings, deserialize into owned strings and use `Box::leak` to construct stable `'static str` references safely. Ensure complete unit/integration tests cover round-trip serialization and delete-on-completion paths.


## Keep Changelog and Versioning Policy Aligned with Repository Rules

- Context: Updating `CHANGELOG.md` to align with the new versioning policy (0.0.1 bump per PR/PR-equivalent change, 0.1 minor bump for major features/milestones with lower digits reset).
- Symptom: Commit history shows versions (like `0.5.0`) merged to `main` in PRs without corresponding entries in `CHANGELOG.md`, causing a mismatch between `Cargo.toml` and the changelog.
- Cause: Developers sometimes bump `Cargo.toml` version during PR development but forget to add the changelog section for that version.
- Resolution: Added the release notes for `0.5.0` (campaign extension, autosave, replay export), bumped the package version to `0.5.1` in both `Cargo.toml` and `CHANGELOG.md` for the alignment change itself, and aligned `docs/versioning-policy.md` to match the exact rules in `AGENTS.md`.
- Prevention: Always check that `CHANGELOG.md` includes the entry for the version in `Cargo.toml` before merging a PR, and perform a `0.0.1` bump for every PR-equivalent change (including changelog/documentation updates).


## Prevent Test Suite and Automated Playtest Hangs / Crashes

- Context: Running standard cargo test and python automated playtests after campaign loop extension.
- Symptom: Test execution blocks indefinitely waiting for stdin in PTY/terminal-like test environments, and automated playtests crash with `IndexError` on turn index >= 4.
- Cause: Directly calling `std::io::IsTerminal::is_terminal(&io::stdin())` inside campaign completion checks bypassing the `stdin_uses_fallback_input()` safeguard, and fixed 3-command arrays in playtest policies when the competitive loop runs for 24 months.
- Resolution: Swapped `is_terminal` checks with `!stdin_uses_fallback_input()` in `src/cli/campaign.rs` and `src/cli/session.rs`. Modified `scripts/run_automated_playtests.py` policy functions to return `"hold"` once turns exceed the defined command sequence.
- Prevention: Never bypass fallback checks with direct terminal state checks in interactive prompt paths. Ensure automated scripts gracefully scale commands when campaign configurations (like loop duration) change.


## Keep Offline Replay Fixtures Up to Date via Integration Tests

- Context: Developing offline diagnostic scripts that parse replay JSON files which match the current Rust models.
- Symptom: Hardcoded offline JSON files quickly become out-of-date and cause parsers to fail when Rust models are updated or serialized keys change.
- Cause: Manually exporting and updating JSON replay files is slow and easily overlooked.
- Resolution: Created an integration test `generate_mock_replay_fixture` under `tests/golden_competitive_seed42.rs` that automatically builds a full 24-month `CompetitiveHistory` and writes it out as a pretty JSON file at `tests/fixtures/mock_replay.json` on every test run.
- Prevention: Leverage standard test runners to dynamically export serialization fixtures to maintain parity between engine structures and diagnostic tool inputs.

## Avoid Shared-File Race Conditions in Parallel Test Runners

- Context: Running standard Rust `cargo test` suites containing tests that read/write/delete shared configuration files in the user's config directory.
- Symptom: Sporadic test failures in `competitive_persistence_write_load_delete_round_trip` with `No such file or directory` errors.
- Cause: Rust tests run in parallel by default. A cleanup step in one test (like `delete_competitive_session_save`) can run concurrently and delete the file written by another test before it gets loaded.
- Resolution: Run the tests sequentially using `cargo test -- --test-threads=1` when verifying shared file interactions.
- Prevention: Avoid writing tests that point to hardcoded global config files; use unique temporary files or directories (e.g. using `tempfile` crate) to isolate test states.


## Differentiate Timeline Decounters from Event Activation Triggers

- Context: Implementing scheduled timeline events with finite durations (like the nurse strike).
- Symptom: Strike duration decremented immediately in the same month-start tick it was activated, reducing a 2-month strike to 1 month on the first turn.
- Cause: Execution of activation logic and time-decay counters within the same sequential tick processing loop without checking if the event was just created.
- Resolution: Guarded the strike decrement logic to run only when the current month is strictly greater than the activation month (`month_index > 10`).
- Prevention: Ensure state decrements or decay steps check that they do not run in the same tick the state is initialized, or guard them with index constraints.


## Exhaustive Match Patterns for Domain Model Enums

- Context: Adding new PledgeType variants to support Workforce pledges.
- Symptom: Rust compilation error (E0004) for non-exhaustive match patterns on PledgeType and CompetitiveCommand.
- Cause: Adding a new enum variant without updating all matching structures in the codebase (e.g., AI command scoring, serialization helpers, and debrief reports).
- Prevention: When introducing new command verbs or enum variants, search the workspace for all pattern matches on that type and explicitly update AI, report generation, and formatting match arms.


## PR Creation under Sandboxed Credentials

- Context: Attempting to automate pull request creation using `gh pr create` inside a sandboxed agent environment.
- Symptom: `gh pr create` fails with exit code 1 and permission errors (`Permission denied for gh command`).
- Cause: The agent's token/environment lacks permissions to execute `gh` pull request operations on GitHub directly.
- Resolution: Push the git branch to the remote origin (`git push -u origin HEAD`) and report the blocker to the user, providing the direct URL to open the PR manually via the GitHub web interface.
- Prevention: Document this limitation and fallback to manual PR creation rather than blocking the handoff flow.


## Sequential Run Target for Persistence Tests

- Context: Running `cargo test` in parallel when tests read or write global configuration states.
- Symptom: Persistence tests such as `competitive_persistence_write_load_delete_round_trip` fail intermittently when run in parallel.
- Cause: Parallel test execution triggers race conditions where a cleanup step in one thread deletes the session file expected by another thread.
- Resolution: Enforce sequential execution for tests interacting with shared files by running them with `cargo test -- --test-threads=1`.


## Query Pending Effect Queue to Enrich Observations

- Context: Deriving rich observations for in-flight operations (like active capital projects).
- Symptom: Dashboard displays generic labels like `1 active project(s)` which hides crucial details (project name, remaining duration, monthly cash drain).
- Cause: Observation mapping relied on the simple count field (`human.resources.active_projects`) rather than inspecting the pending effects queue.
- Resolution: Updated `in_flight_projects_label` in `src/sim/observe_competitive.rs` to query `world.effect_queue` for matching system effects, calculate remaining months, and extract project names and cash draws.
- Prevention: When displaying status of delayed or multi-turn commitments, query the queue containing the details instead of only presenting state accumulator values.
## Hierarchical Staffing Priority Insertion

- Context: Adding the Obstetrics/L&D service line as a second-priority service line after ICU and before Med-Surg/Outpatient.
- Symptom: If priority queues are not kept aligned between the transition simulation (`src/sim/transition_competitive.rs`) and the user dashboard display (`src/cli/display/executive_report.rs`), the dashboard will show incorrect/inconsistent effective capacities compared to the actual state transitions.
- Cause: The simulation uses a hierarchical greedy allocation to distribute nurses and physicians to ICU, Obstetrics, Med-Surg Beds, Outpatient Clinics, and ED in a specific sequence. This sequence must be mirrored exactly in the display formatting code.
- Prevention: Ensure that any change to the hierarchical allocation rules (such as inserting a new service line like Obstetrics) is updated identically in both `apply_staffing_constraints` and the CLI dashboard report renderer.


## Psychiatric ED Boarding Interaction & Testing Constraints

- Context: Implementing Psychiatric Service Line with ED holding boarding and diversion mechanics.
- Symptom: Unit tests failed to trigger the psychiatric ED boarding path because overflow patients were constantly diverted instead of boarded.
- Cause: ICU critical care patients board in the ED unconditionally (even when ED effective capacity is 0), which depletes all available ED bays before psychiatric patients (who board conditionally based on remaining ED bays) are processed. Furthermore, under normal staffing, ED staffing is only possible if higher-priority specialty units (like psychiatric beds) are fully staffed, leaving no psychiatric overflow.
- Resolution: To test psychiatric ED boarding, set starting `staffed_beds` to `0` to prevent ICU boarding, and activate the scenario-specific RNA strike (under a matching `scenario_id` like `exemplary-competitive-v1`) to halve a single psychiatric bed to `0` effective capacity (creating 1 overflow patient) while leaving the ED staffed with positive capacity.
- Prevention: When testing conditional resource-sharing code (like psychiatric ED holding), isolate the target resource by zeroing out higher-priority demands (like Med-Surg staffed beds / ICU) and use scenario strike/event logic to create capacity-staffing mismatches while maintaining positive holding capacity.


## Keep Display and Transition Ratios Aligned for Dashboard Integrity

- Context: Adding the Neurology inpatient service line with capacity, commands, priority staffing allocation, and ED holding boarding/diversion mechanics.
- Symptom: Incorrect or inconsistent effective capacity numbers printed on the REPL dashboard.
- Cause: The logic to calculate effective capacities (including strike-time halving, target nurse/physician/admin ratios, priority allocation queues, and ED boarding math) was updated in the simulation kernel (`src/sim/transition_competitive.rs`) but not in the display formatting engine (`src/cli/display/executive_report.rs`).
- Prevention: Whenever adding or modifying service lines, targets, strike adjustments, or boarding mathematics, modify both the transition simulation kernel and the CLI/REPL display report formatter in tandem. Write exhaustive unit tests verifying the alignment of targets, effective capacities, and ED boarding/diversion outcomes.
## Advice Validation Must Separate Traceability From Advice Quality

- Context: Validating the repaired deterministic consultant baseline after the
  v0.10.39 live observation and history slice.
- Resolution: Capture observations and debriefs at the MCP wrapper boundary,
  assert exact A-D option and month coverage, and preserve submitted commands
  beside the retained options without scoring adherence.
- Prevention: Treat simulated-agent advice traces as evidence of visibility and
  inspectability only. Do not infer learning, advice quality, calibration,
  difficulty value, or advisor-market value from this matrix.

## Compare Information-to-Action Traces Without Claiming Causality

- Context: Synthesizing consultant-advice and rival-monitor evidence into an
  instructor-facing comparison surface.
- Symptom: A visible cue followed by a different command can look like proof
  that the cue improved a decision or outcome.
- Cause: Advice-aware and monitor-reactive policies intentionally submit
  different commands from their controls, while deterministic traces do not
  represent human decision-making.
- Resolution: Compare visibility, response, resource feasibility, operational
  follow-through, realized tradeoffs, and debrief continuity as separate review
  steps. Label endpoint differences and strategy labels as non-causal,
  interpretive evidence.
- Prevention: Keep actor utility, organizational outcomes, social welfare, and
  educational evaluation distinct; require a new concrete gap before changing
  runtime information, difficulty, balance, or advisor mechanics.

## Audit Evidence Coverage Before Promoting Runtime Work

- Context: Continuing the Phase 7 information-to-action comparison after the
  v0.10.44 synthesis.
- Symptom: A comparison surface can appear complete while its supporting
  artifacts use different field names and trace shapes.
- Resolution: Added a small read-only audit that checks visibility, response,
  follow-through, outcome, and explanation coverage across the existing source
  artifacts without launching new sessions or normalizing them into a broader
  schema.
- Prevention: Verify field coverage and deterministic regeneration first; keep
  supported trace fields separate from human clarity, learning, causal value,
  balance, and runtime-promotion claims.

## Treat Expert Completion as a Bounded Clearability Proxy

- Context: Capturing the v0.10.46 Expert completion matrix across four existing
  simulated-policy profiles and seeds 42, 43, and 44.
- Symptom: A complete 24-month run can be read too broadly as proof that Expert
  difficulty is generally winnable or balanced.
- Resolution: Record completion status, validation failures, histories, hashes,
  and debriefs while labeling the result as a bounded clearability proxy for
  the tested policies and seeds.
- Prevention: Do not promote difficulty values, scoring, balance, or runtime
  mechanics from completion alone. Require broader evidence or a concrete
  player-facing explanation gap before changing the simulation.

## Semantic Command Coverage Must Follow Field Coverage

- Context: Continuing Phase 7 evidence review after the v0.10.45 field-coverage
  audit and v0.10.46 Expert completion matrix.
- Symptom: A trace can contain command, history, and debrief fields while still
  leaving the action-specific event/effect relationship untested.
- Resolution: Added a read-only audit that normalizes each submitted command,
  matches it to player-owned event/effect signatures or an explicit neutral
  classification, and verifies the monthly `Player:` debrief record.
- Prevention: Treat semantic command coverage as traceability evidence only;
  do not convert matched event/effect text into causal, decision-quality,
  learning, balance, or policy-validity claims.

## Strategy Signatures Are Descriptive, Not Dominance Evidence

- Context: Continuing Phase 7 validation after the v0.10.47 command-to-effect
  traceability audit.
- Symptom: Different command trajectories can be mistaken for proof that one
  profile or action is strategically superior.
- Resolution: Added a read-only audit that reports normalized action families,
  trajectories, hold rates, first-turn signals, and existing final tradeoffs
  without assigning utility or comparing outcomes causally.
- Prevention: Treat common actions and distinct profiles as descriptive evidence
  only; require a concrete player, instructor, or domain-review gap before
  changing runtime, balance, difficulty, or scoring.

## Pending Project Effects Must Have Observation Coverage

- Context: Extending project-limit recovery evidence to an accepted ASC
  project exposed a mismatch between the active-project counter and the human
  observation text.
- Symptom: `AscCapacity` consumed a concurrency slot and monthly draw but was
  omitted from the `In-flight projects` label because the formatter had no
  matching branch.
- Resolution: Added the missing `AscCapacity` observation branch and a focused
  Rust regression test, then reran the three-seed capture with state-hash
  continuity checks.
- Prevention: When adding a pending project effect, update actor-visible
  formatters and test name, remaining duration, and monthly draw alongside
  validation and transition coverage.

## Operating-Outcome Use Must Preserve Temporal Alignment

- Context: Auditing whether the v0.11.4 operating-result surface connects
  visible prior-month outcomes to later commands and exact debrief results.
- Symptom: A complete current-month debrief line can appear to support a
  response claim even when the observation belongs to the preceding transition
  or when the campaign has already ended.
- Resolution: Compare month-two-plus observations to the preceding committed
  transition, compare debrief results to the current transition, and classify
  final-month signals as expected terminal cases rather than missing responses.
- Prevention: Keep signal-to-command counts descriptive, preserve player/rival
  boundaries, and do not infer causality, strategy quality, or human learning
  from deterministic trace continuity.

## Runtime Proposals Must Freeze the Observation Contract First

- Context: Promoting the v0.11.13 affiliation design gate toward a future
  runtime slice.
- Symptom: A staged institutional mechanic can appear small while silently
  expanding state, actor authority, stochastic inputs, replay, and debrief
  surfaces.
- Resolution: Define the opt-in scenario boundary, minimum state and
  observations, explicit resolved-input categories, and debrief distinctions
  before adding commands or Rust types.
- Prevention: Keep proposal PRs separate from runtime implementation, preserve
  the default campaign golden path, and stop when a design requires a generic
  actor or deal-market framework.
