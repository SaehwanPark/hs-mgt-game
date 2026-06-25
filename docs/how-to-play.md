# How To Play

This guide is for first-time players of the Health Policy Strategy Game CLI.
It teaches what to do each turn, what commands mean, and how to recover when a
run starts going badly.

## What this game is

You play as a health-system leader in a fictional US market. You make strategy
decisions under pressure from finance, workforce, policy, and competitors.

Two campaigns are currently visible in the CLI:

- `stabilization-v1` (implemented): five-turn executive demo.
- `competitive-regional-v1` (implemented as a bounded preview): three-month
  competitive loop with one human system and AI rivals.

The game is deterministic for a given seed and set of choices. A poor outcome
can still follow a reasonable decision when uncertainty and rival behavior
interact.

## First session quickstart

1. Run the game:

   ```bash
   cargo run
   ```

2. Choose a campaign:
   - Enter or `1` for stabilization (recommended first run).
   - `2` or `c` for competitive preview.
3. If you picked competitive, choose a difficulty:
   - Easy: 1 AI rival, 4 AP/month.
   - Normal: 2 AI rivals, 3 AP/month.
   - Hard: 3 AI rivals, 3 AP/month.
   - Expert: 4 AI rivals, 2 AP/month.
4. Choose play style:
   - `i` (or Enter): interactive.
   - `b`: beginner guided choices (stabilization flow).
   - `1`/`2`/`3`: preset strategy paths.
5. Set seed (or press Enter for default `42`).
6. Play through all turns/months.
7. Use global commands any time:
   - `?` or `help` for context
   - `q`, `quit`, or `exit` to leave

## Game structure from your perspective

## Stabilization (`stabilization-v1`)

For each of 5 turns, you:

1. Read your observation and briefing.
2. (Interactive mode) review uncertainty preview.
3. Enter turn-specific numeric command fields.
4. Submit and watch NPC response plus turn summary.
5. Continue to next turn.

At run end, you get replay verification and a debrief.

## Competitive preview (`competitive-regional-v1`)

For each month in the 3-month preview, you:

1. Read the executive report.
2. Enter one command batch (Stata-like verbs).
3. Submit; AI rivals submit simultaneously.
4. Review resolution summary.
5. Repeat next month with updated conditions.

Note: full 24-month competitive campaign is still deferred; current player flow
is a bounded preview.

## Key terminology

- `True state`: full modeled world state inside the engine.
- `Observation`: what you (or another actor) are allowed to see.
- `Resolved inputs`: seeded uncertainty values computed before transition.
- `AP (action points)`: your monthly command-capacity budget (competitive).
- `Political capital`: resource used by selected strategic commands.
- `Simultaneous resolution`: all player monthly batches are resolved together.
- `Replay`: deterministic re-check from genesis over committed history.
- `Debrief`: end-of-run explanation of why outcomes happened.
- `Decision quality`: whether your choice was reasonable with available info.
- `Outcome quality`: what happened after all responses and uncertainty.

For the full contributor/domain glossary, see `docs/glossary.md`.

## Commands

## Stabilization input style

Stabilization interactive prompts ask for integer fields per turn (for example,
capital spend, access commitment, schedule relief). The prompt always shows:

- exact field names,
- valid ranges,
- and a default command line you can accept.

Use Enter to accept defaults where the prompt allows.

## Competitive command cheat sheet

Use `verb arg=value` syntax. You can chain commands with semicolons.

Examples:

```text
invest domain=beds amount=25
recruit role=nurse headcount=5
monitor target=northlake depth=2
negotiate payer=carrier_a rate_posture=neutral
commit pledge_type=access level=3
project kind=ehr_epic budget=60
hold
```

Batch example:

```text
monitor target=summit depth=1; invest domain=outpatient amount=15
```

Global/meta helpers in competitive prompt:

- `help` or `?`: list command usage.
- `Enter` on empty input: submit fallback batch.
- `q`/`quit`/`exit`: quit the session.

## Gameplay walkthrough (example interaction)

Scenario: you are in competitive Month 2 on Normal difficulty.

Executive report highlights:

- Rival Northlake announced bed expansion last month.
- Your cash runway shows `watch`.
- Nursing vacancy remains elevated.
- Consultant options suggest either fast bed investment or workforce-first.

Your decision:

```text
monitor target=northlake depth=1; recruit role=nurse headcount=4
```

Why this can be strong:

- `monitor` improves next-month intel before a larger capital move.
- `recruit` addresses workforce pressure without immediate large cash burn.
- You keep AP and cash flexibility if rivals escalate unexpectedly.

Possible next-month follow-up:

```text
invest domain=beds amount=20
```

if intel confirms market-share risk and your runway improves.

Lesson: you are not trying to "solve" one month. You are managing tempo under
uncertainty while preserving options.

## If the game feels too difficult

Use this triage playbook.

1. Protect capacity to respond:
   - avoid spending all AP on one theme every month;
   - keep at least one flexible action open when possible.
2. Respect cash runway signals:
   - if runway is `watch` or `strained`, prioritize lower-burn actions;
   - delay large `project` or high `invest` commitments unless essential.
3. Buy information before big commitments:
   - use `monitor` when rival intent is unclear.
4. Use `hold` strategically:
   - a deliberate pass can be correct when information is weak and downside is high.
5. Prefer reversible actions early:
   - small recruit/invest steps often outperform one large irreversible bet.
6. Focus on decision quality, not perfection:
   - strong process beats chasing one "best" move that may not exist.

## Practical beginner patterns

- Conservative month: `monitor` + light `recruit`.
- Balanced month: medium `invest` + one legitimacy move (`commit`).
- Information-first month: `monitor`, then adjust next month with better intel.

## FAQ and troubleshooting

Q: I entered a command and got an error. Did I lose the month?  
A: No. Validation errors do not advance the month; fix command syntax/limits and
retry.

Q: Why did a "good" decision still lead to a bad result?  
A: Rival actions, delayed effects, and seeded uncertainty can produce adverse
outcomes. Debrief helps separate decision quality from outcome quality.

Q: Is competitive a full campaign already?  
A: Not yet. Current competitive flow is a bounded three-month preview.

Q: I want a less overwhelming first run.  
A: Start with `stabilization-v1` and beginner mode (`b`), then move to
competitive once the loop feels familiar.

## Learn more

- Core loop: `docs/core-loop-spec.md`
- Competitive gameplay spec: `docs/gameplay-competitive-sketch.md`
- Command grammar draft: `docs/cli-command-grammar-draft.md`
- Action catalog: `docs/action-catalog-draft.md`
- Executive report schema: `docs/executive-report-format.md`
- Glossary: `docs/glossary.md`
