# Visual and Audio Phase 9 — AI-Agent Evaluation and Revision

Status: Implemented, verified, reviewed once, and merged in PR #176.

Phase 9 closes the current visual/audio sequence with a deterministic comparison
surface for repeated `gui-playtest-v1` artifacts. It reports declared coverage,
observable evidence gaps, and revision hypotheses without running a browser,
model, network service, or simulation transition.

## Evaluation contract

`analyze_gui_playtests.py` accepts one or more capture files or directories. It
validates every JSON artifact through the Phase 8 validator, preserves declared
campaign/role/task/seed/interface/accessibility dimensions, counts allowlisted
events and failure classes, and emits `gui-playtest-analysis-v1` JSON with:

- stable capture records and valid/invalid counts;
- declared coverage and matrix rows;
- event-union visibility and Phase 8 evidence lanes;
- fixed-priority revision findings with source capture, observable evidence,
  bounded hypothesis, and evidence limit; and
- explicit limits forbidding strategy, causal, calibration, balance, policy,
  human-usability, learning, and engagement claims.

The analyzer never emits raw event payloads, true/private state, resolved
inputs, effect queues, model reasoning, or a strategy score. Invalid captures
remain findings and cannot count as valid task evidence.

## Matrix fixture

The repository fixture matrix contains five protocol captures representing
declared, synthetic contract coverage—not completed real-agent sessions:

| Campaign | Role | Task | Seed | Accessibility | Result |
| --- | --- | --- | --- | --- | --- |
| stabilization-v1 | first-time | complete-first-decision | 42 | standard | complete with committed history |
| stabilization-v1 | access-check | complete-first-decision | 42 | reduced-motion | complete with settings/audio evidence |
| stabilization-v1 | first-time | complete-first-decision | 45 | standard | P2 history evidence gap |
| competitive-regional-v1 | strategy-review | inspect-committed-result | 43 | standard | complete with committed history |
| regional-affiliation-v1 | recovery-check | recover-from-rejected-decision | 44 | muted | rejected and recovered without false history finding |

The deterministic report has five valid task-evidence captures, three campaigns,
four roles, four seeds, three accessibility modes, and one P2
`command_without_history`
finding for the intentionally incomplete evidence fixture. The rejected
affiliation command is not treated as a missing committed history because a
rejection is expected to leave history unchanged.

## Product decision log

| ID | Evidence | Decision | Status | Limit |
| --- | --- | --- | --- | --- |
| P9-1 | Rejected command plus recovery retry has no committed history | Make history-gap analysis conditional on adapter/submission failure classes | Accepted and implemented in the analyzer | This improves artifact interpretation; it is not proof of recovery usability |
| P9-2 | One valid synthetic trace lacks history after an accepted command event | Retain a P2 evidence-completeness recommendation for future harness runs | Accepted as a protocol revision | It does not establish that a user or agent misunderstood the result |
| P9-3 | Matrix contains only static/synthetic contract fixtures and no real browser run | Do not change onboarding, layout, audio, simulation, or campaign rules from this evidence | Deferred pending authorized real-agent/browser evidence | Human usability, lived accessibility, learning, engagement, calibration, balance, and policy validity remain unresolved |

## Priority rules

1. `P0 capture_contract`: invalid schema, forbidden, or malformed artifacts.
2. `P1 task_recovery`: missing controls, incomplete tasks, or failures without
   a retry/recovery event.
3. `P2 evidence_completeness`: missing semantic/history evidence when the task
   context makes that evidence expected.

These are deterministic triage labels, not scores. Findings are deduplicated
and sorted by priority, category, issue code, and capture path.

## Reproducibility and authority

The analyzer uses no timestamps, randomness, network, model, browser, or game
engine calls. It processes sorted paths and emits stable JSON; running it twice
on unchanged inputs produces byte-identical output. The host remains the only
authority for commands, transitions, observations, stochastic inputs, history,
hashes, replay, and debriefs. The decision log cannot mutate any product or
simulation behavior.

## Verification and limits

The matrix and focused tests verify valid/invalid/incomplete propagation, coverage
preservation, context-aware rejection handling, deterministic output, and the
absence of strategy/human scoring fields. Existing Phase 2–8 contracts and the
Rust simulation remain regression gates.

This phase provides technical and interface-task proxy evidence only. It does
not evaluate people, prove task comprehension, establish accessibility lived
experience, measure learning or engagement, validate policy/domain claims, or
authorize a future product revision without additional evidence.

Phase 9 is the final currently specified visual/audio upgrade item. Any later
work requires a new bounded proposal and promotion gate.
