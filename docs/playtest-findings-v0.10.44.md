# Information-to-Action Comparison Evidence v0.10.44

- **Status:** Phase 7 competitive teachability and validation synthesis
- **Date:** 2026-07-10
- **Code version:** 0.10.44
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:** v0.10.37, v0.10.40, v0.10.41, v0.10.42, and v0.10.43

This synthesis connects two existing decision-support surfaces: generic
consultant advice and delayed rival-monitor intelligence. It gives instructors
and reviewers one compact way to compare what information was visible, what a
simulated policy did next, whether the action was operationally followed
through, and what the debrief can explain afterward.

It adds no new runs and changes no runtime behavior.

## Evidence Chain

| Surface | Existing evidence | What is traceable | What remains unproven |
| --- | --- | --- | --- |
| Generic consultant advice | v0.10.40–v0.10.42 | Four visible options, exact observation/history/debrief continuity, selected or ignored options, and resource-safe fallback | Advice quality, human uptake, causal benefit, or learning |
| Rival-monitor intelligence | v0.10.37 and v0.10.43 | Visible signal source month, observation turn, next-turn response, ignored control, and observation-only hash behavior | Monitor value, decision quality, balance, or Expert winnability |

The two surfaces are not interchangeable. Consultant options are non-binding
state-conditioned suggestions retained for later review. Monitor records are
delayed observations of rival activity. Both can be followed by a submitted
command, but neither command stream is a randomized treatment or a validated
human decision process.

## Information-to-Action Review Surface

Use the following sequence when comparing two or more completed competitive
runs:

| Review step | Evidence to inspect | Question | Guardrail |
| --- | --- | --- | --- |
| 1. Visibility | Monthly observations, advice options, monitor lines, source months, legal resource hints | What did the policy actually know when it acted? | Do not use later revealed state to judge the earlier decision |
| 2. Response | Submitted command, selected option, ignored signal, or safe `hold` fallback | Did the policy respond to visible information, and was the response affordable? | A response is traceability evidence, not proof of good reasoning |
| 3. Follow-through | Recruitment, investment, projects, negotiations, monitoring, access pledges, and delayed effects | Did the action become durable operational capacity or remain a stated intention? | Do not reduce strategy quality to one metric or one commitment |
| 4. Outcome | Cash, access, workforce trust, community trust, political capital, market pressure, and final hash | Which tradeoffs did the run realize? | A favorable endpoint does not prove a generally superior strategy |
| 5. Explanation | Transition summaries, actor rationales, committed history, and final debrief | Can the run explain why the outcome occurred and what was knowable? | Debrief traceability is not measured learning evidence |

## Instructor Comparison Prompts

1. Which visible cue or information source preceded the decision, and which
   parts of the situation remained hidden or uncertain?
2. Did the policy choose, ignore, or safely defer the available advice or
   rival signal? What resources constrained the response?
3. Did the response create durable staffing, capacity, payer, monitoring, or
   coalition follow-through, or did it remain primarily a public commitment?
4. Which endpoint tradeoffs were consistent with the stated strategy, and
   which depended on delayed effects or rival behavior?
5. Would the decision still look reasonable if judged from the actor-visible
   observation rather than the final outcome?
6. Does the debrief distinguish a poor decision from an unfavorable realization
   of uncertainty?

Compare contrasting runs before asking which strategy was “better.” Strategy
labels remain discussion handles rather than hidden game classes, validated
learner archetypes, equilibrium results, or scores.

## Interpretation and Routing

The existing evidence is sufficient to trace visible information to later
simulated-policy actions and to inspect continuity through history and debrief
surfaces. It does not identify a concrete runtime information, advice, monitor,
difficulty, balance, or scoring defect.

Retain generic advice and monitor mechanics unchanged. Keep the advisor market,
runtime difficulty expansion, and broad strategy taxonomy deferred. A future
runtime change requires a separate artifact showing that current observations,
history, diagnostics, and debriefs cannot explain a concrete player-facing or
instructor-facing problem.

## Evidence Limits

- Inputs are deterministic simulated-agent and scripted-policy artifacts, not
  human or classroom sessions.
- Advice-aware and monitor-reactive policies intentionally submit different
  commands from their controls; endpoint differences are therefore not causal
  treatment effects.
- Information visibility and response records support inspectability, not
  advice quality, monitor value, learning, balance, calibration, or policy
  forecasting claims.
- Actor utility, organizational outcomes, social welfare, and educational
  evaluation remain distinct questions.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.40-consultant-advice-evidence/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.41-consultant-advice-usage/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.43-rival-info-follow-through/results.json >/dev/null
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
