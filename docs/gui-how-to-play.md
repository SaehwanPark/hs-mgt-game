# How to Play in GUI Mode

The live browser GUI provides the competitive regional campaign through a local
Rust host. It does not require MCP setup, a separate web server, or manual
JavaScript adapter injection.

## Requirements

- A Rust toolchain with Cargo.
- A current browser with JavaScript modules enabled. Audio is optional and uses
  the browser Web Audio API.
- A local checkout of this repository.

The GUI currently supports `competitive-regional-v1`. Use `cargo run` for the
stabilization, regional-affiliation, or custom-scenario play.

## Start the GUI

1. Open a terminal in the repository root.
2. Run:

   ```bash
   cargo run --bin hs-mgt-game-gui
   ```

3. Keep the terminal running. After compilation, it prints a line like:

   ```text
   Health Policy Strategy Game GUI: http://127.0.0.1:7878
   ```

4. Open that URL in your browser.
5. Leave the campaign set to `competitive-regional-v1`, use seed `42`, choose
   Normal difficulty, and select **Start competitive session**.

The server listens only on your computer's loopback interface. It does not make
the game available to other computers and does not provide network multiplayer.

## Play the first month

The First-month path panel tracks seven presentation handoffs:

1. **Start or load:** create a session or load an ID from this running host.
2. **Inspect:** read the executive briefing, regional market, Riverside detail,
   visible resources, capacity, workforce, payer, and rival signals.
3. **Draft:** choose parameters in a contextual action form and add it locally.
4. **Validate:** add at least two drafts, review their canonical commands, then
   select **Validate draft with host**.
5. **Submit:** if validation passes and you have not changed the draft, select
   **Submit validated month**.
6. **Resolution:** read, play, pause, skip, or review the committed monthly
   resolution. Skipping animation does not skip the game result.
7. **Continue:** inspect the refreshed observation for the next month.

Drafting does not advance time. Validation checks action points, cash, political
capital, command syntax, and other host-owned constraints without committing the
month. Editing or removing a validated draft requires validation again.

## What the interface shows

- **Seed:** controls reproducible uncertainty. The same seed and decisions
  reproduce the same run.
- **Difficulty:** changes rival count and available monthly action points.
- **Action points (AP):** limit the command batch you may commit this month.
- **Pending processes:** visible commitments or delayed effects, not guaranteed
  future outcomes.
- **Resolution:** host-derived before/after observations and direct committed
  effects from immutable history.
- **State hash:** a replay/audit identifier for the committed state.

Rival private state and unresolved stochastic inputs are deliberately not shown.

## Optional audio

Audio starts off. Select **Enable audio** after the page opens; browsers require
a user gesture before sound can start. You can mute audio, reduce notifications,
or adjust master, music, interface, event, and ambience volumes independently.

Audio emphasizes information already visible on the page. Every cue has a
written equivalent, and muted or unsupported audio never prevents play.

## Load an existing session

Copy a session ID displayed by the current GUI and enter it under **Existing
session ID**, then select **Load existing session**. Session IDs exist only in
the memory of the currently running `hs-mgt-game-gui` process. Stopping or
restarting that process invalidates them.

## Stop the GUI

Return to the server terminal and press Ctrl-C. All in-memory GUI sessions end
when the process stops.

## Use a different port

If port 7878 is busy, choose another loopback port:

```bash
cargo run --bin hs-mgt-game-gui -- --bind 127.0.0.1:8787
```

Open the exact URL printed by that process.

## Troubleshooting

### The browser says connection refused

Confirm the Cargo command is still running and that compilation completed. Open
the printed URL rather than a bookmarked port from an older run.

### The terminal says the address is already in use

Another process is using that port. Stop the older GUI host or use the alternate
port command above.

### I see demo data and Start says no host is configured

You opened `gui/index.html` directly or used a generic static file server. Stop
that server and run `cargo run --bin hs-mgt-game-gui`; only the Rust GUI host
injects the live adapter.

### The seed is rejected

Use a non-negative whole number within JavaScript's safe integer range. Seed
`42` is the recommended first run.

### Validation rejects my draft

The month has not advanced. Read the validation message, reduce or revise the
draft to fit visible resources and command constraints, then validate again.

### Submission or refresh fails

The interface keeps the last successfully rendered session. Use **Retry current
read** when offered. If submission was rejected, revise and validate again. Do
not assume a month committed unless a resolution or refreshed host response is
shown.

### An existing session ID is unknown

The ID belongs to a different or stopped server process, or it was typed
incorrectly. Start a new session in the current process.

### Audio is silent

Select **Enable audio**, check browser/tab mute settings, raise Master and the
relevant channel volume, and return focus to the page. Continue with the written
equivalents if Web Audio is unavailable.

## Scope and safety

The GUI is local, competitive-only, and in-memory. It is not a hosted service,
network multiplayer client, calibrated policy forecast, or operational,
clinical, financial, regulatory, or legal decision tool.
