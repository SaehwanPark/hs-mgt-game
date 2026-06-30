# External Playtest Protocol

**Status:** Superseded by [`agent-playtest-protocol.md`](agent-playtest-protocol.md)
**Audience:** Facilitators, contributors, and domain reviewers
**Version:** v0.1.39

This historical protocol is retained for context. The active Phase 7 validation
path no longer depends on recruiting external human players; use
[`agent-playtest-protocol.md`](agent-playtest-protocol.md) for current AI-agent
and sub-agent playtest work.

This protocol gives facilitators a repeatable way to run informal external
playtests of the current CLI experience. It is intended to test comprehension,
strategic tension, pacing, causal transparency, and educational debrief value.

This is not a calibrated policy forecast, clinical decision tool, or formal
human-subjects research instrument. If a session will be used for publishable
research, course assessment, employment evaluation, or identifiable participant
analysis, pause and follow the required institutional review, consent, privacy,
and data-retention process before running it.

## Current Playable Scope

The protocol covers the implemented command-line flows:

| Campaign | Current status | Session target |
| --- | --- | --- |
| `stabilization-v1` | Five-turn playable slice | First-time comprehension and debrief quality |
| `competitive-regional-v1` | Bounded three-month preview | Competitive command comprehension and monthly tradeoffs |

The full 24-month competitive campaign, scenario file loading, Medicare and
Medicaid strategic actors, and empirical calibration remain deferred.

## Session Goals

Use each session to answer:

- Can the player understand their role, available choices, and constraints?
- Does the game create meaningful tradeoffs rather than a single obvious path?
- Can the player explain why major outcomes occurred?
- Does the CLI pacing support decision-making without overload?
- Do reports, rationales, and debrief prompts distinguish decision quality from
  outcome quality?
- Are any commands, terms, or displays consistently confusing?

Do not use a single playtest to tune numeric balance or infer real-world policy
effects.

## Participants and Facilitator Role

Recommended participants:

- Graduate health management, policy, or public administration learners.
- Health-system, payer, public-sector, or workforce stakeholders willing to
  comment on plausibility.
- Strategy-game players who can identify pacing and choice-friction issues.

The facilitator should:

- explain that the game is a fictional educational prototype;
- avoid coaching toward a preferred strategy;
- record observations without judging the player;
- prompt the player to think aloud when comfortable;
- keep timestamps for major confusion points;
- separate observed behavior from interpretation in notes.

## Setup

Before the session:

1. Build and test the current branch:

   ```bash
   cargo fmt --check
   cargo test
   ```

2. Start the CLI:

   ```bash
   cargo run
   ```

3. Use a terminal with ANSI color support when practical. The game still runs
   without color, and `NO_COLOR=1 cargo run` can be used when plain output is
   preferred.
4. Use seed `42` unless testing seed variation explicitly.
5. Keep this protocol and [`docs/how-to-play.md`](how-to-play.md) available for
   facilitator reference.

## Stabilization Session Script

Use `stabilization-v1` for first-time product and educational testing.

1. Ask the player to read only the opening dashboard and campaign prompts.
2. Select `stabilization-v1`.
3. Prefer `beginner` mode for first-time learners; use standard interactive mode
   for experienced players.
4. Ask the player to explain their initial strategy in one or two sentences.
5. Let the player complete all five turns without strategic coaching.
6. After each turn, note whether the player can identify:
   - what changed;
   - which actor responded;
   - whether the result was a validation failure, unfavorable outcome, or
     favorable outcome;
   - what uncertainty or observation revision mattered.
7. At the debrief, ask the player to identify one decision they still consider
   reasonable and one decision they would change.

## Competitive Preview Session Script

Use `competitive-regional-v1` after the player understands the basic CLI or when
testing competitive campaign ergonomics.

1. Select `competitive-regional-v1`.
2. Choose `normal` difficulty unless testing difficulty-specific confusion.
3. Ask the player to summarize the monthly executive report before entering
   commands.
4. Let the player complete the three-month preview.
5. At each command prompt, note:
   - whether `help` gives enough information;
   - whether `verb arg=value` syntax is understood;
   - whether AP, cash, and political capital constraints are visible;
   - whether rival observability and monitoring are understood;
   - whether consultant recommendations are treated as advice, not optimal
     answers.
6. After month 3, ask which rival move or event changed their plan.

## Observation Rubric

Use the following ratings for each session. Prefer short evidence notes over
long interpretation.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Comprehension | Player cannot identify role or next action | Player can proceed with facilitator clarification | Player can explain role, actions, and constraints independently |
| Strategic tension | One path appears obviously dominant | Tradeoffs are visible but not always consequential | Player sees multiple defensible strategies with real costs |
| Causal transparency | Outcomes feel opaque | Some actor rationales or effects are understood | Player can trace major outcomes to decisions, actors, and events |
| Pacing | Player is lost or fatigued | Session has occasional friction | Session length and information density feel manageable |
| Action overload | Choices or syntax block play | Player recovers with help text | Player can choose without excessive menu or syntax burden |
| Debrief value | Debrief repeats results only | Debrief supports some reflection | Debrief separates reasoning, uncertainty, outcomes, and tradeoffs |

Also record any obvious exploit, repeated invalid input, or recurring term that
needs glossary or display support.

## Post-Session Prompts

Ask these questions after play:

- What did you think your organization was trying to accomplish?
- Which decision felt most constrained?
- Which report or prompt was hardest to interpret?
- Which actor response felt plausible or implausible?
- Where did uncertainty affect your decision?
- Did the debrief help explain why outcomes occurred?
- What would you need before using this in a classroom or workshop?

For competitive preview sessions, also ask:

- Which rival action mattered most?
- Did monitoring feel useful?
- Did monthly AP limits create strategy or just friction?

## Note Template

```text
Session id:
Date:
Facilitator:
Participant background:
Campaign:
Difficulty:
Seed:
Mode:
Completion status:

Observed confusion points:
-

Notable decisions:
-

Invalid inputs or command friction:
-

Rubric scores:
Comprehension:
Strategic tension:
Causal transparency:
Pacing:
Action overload:
Debrief value:

Quotes or paraphrased reactions:
-

Potential fixes:
-

Deferred or out-of-scope requests:
-
```

Avoid recording names, institutional affiliations, or other identifying details
unless a separate approved process requires and protects that information.

## Synthesis Guidance

After several sessions, summarize patterns rather than isolated preferences:

- repeated comprehension failures;
- commands or terms that consistently need explanation;
- decisions players interpret as fake choices;
- debrief prompts that produce useful reflection;
- places where the game appears to imply unsupported policy authority;
- requests that belong in deferred tracks such as scenario loading, longer
  competitive campaign runtime, or new strategic actors.

Recommended follow-up artifacts are versioned playtest findings documents, for
example `docs/playtest-findings-v0.1.39.md` or later. Do not overwrite prior
findings files.
