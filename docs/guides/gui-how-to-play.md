# How to Play in GUI Mode

The live browser GUI provides the competitive regional, stabilization, and
regional-affiliation campaigns through a local Rust host. It does not require
MCP setup, a separate web server, or manual JavaScript adapter injection.

## Requirements

- A Rust toolchain with Cargo.
- A current Chromium-based desktop browser with JavaScript modules enabled.
  The repository's compatibility matrix certifies the documented evergreen
  Chromium surface; Firefox and WebKit are not certified yet. Audio is
  optional and uses the browser Web Audio API.
- A local checkout of this repository.

The launcher supports `competitive-regional-v1`, `stabilization-v1`, and
`regional-affiliation-v1`. The competitive campaign uses its action catalog;
the stabilization and regional-affiliation campaigns use the typed
`campaign-coverage-v1` panel for host-shaped decisions. Custom scenarios still
use `cargo run`.

The host also exposes `campaign-coverage-v1` for a typed competitive read of
the current player-visible metrics, public signals, process summaries, action
metadata, history, and terminal debrief. This read does not replace the
competitive catalog/validation/submit sequence or reveal private rival state.
In the normal competitive GUI it appears as a companion panel after
start/load and accepted monthly refreshes; if that optional read is unavailable,
the action rail remains usable.

For a first session, start with the documented Normal/seed-42 defaults, then
adjust presentation settings only if they reduce friction. These controls are
local browser presentation preferences; they do not change commands, host
validation, simulation outcomes, or replay history.

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
   Normal difficulty, and select **Start competitive regional session**. For
   stabilization or regional affiliation, choose that campaign and select the
   same start button; difficulty is not used for those campaign-coverage
   sessions.

The server listens only on your computer's loopback interface. It does not make
the game available to other computers and does not provide network multiplayer.
At startup it prints the application-config path used for explicit checkpoint
files for all three campaigns; the file is host-owned and is never sent to the
browser.

## Follow the first session

The First-session path panel selects a rail from the host campaign. Competitive
sessions track seven action handoffs:

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

For stabilization and regional affiliation, the rail instead tracks five
campaign-coverage handoffs: start/load, inspect the visible campaign envelope,
choose a host-shaped decision, review the committed stage, and continue. These
campaigns do not use the competitive local-draft or validation steps.

After each accepted GUI decision, the host automatically requests a checkpoint
through the same host-only path. The GUI reports the committed transition count
when autosave succeeds; if it fails, the committed session remains active and
the written status gives the error. **Save host checkpoint** remains available
as a manual retry. The host stores one checkpoint file per opaque session ID in
its sibling archive; after a host restart, choose **Find saved checkpoints** to
inspect validated metadata, select **Use this session ID**, and then choose
**Load existing session** or **Restore host checkpoint**. Manual opaque-ID entry
remains available. The browser never receives the saved artifact, and a missing
or colliding checkpoint is reported as a recoverable error.

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

## Settings and accessibility

The **Accessibility and settings** panel is available before or during a live
session:

- **Low-distraction mode** combines Reduced motion, Large text, visible cue
  explanations, muted audio, and reduced notifications. While active, the
  individual presentation and audio controls are locked to that safe recipe;
  turning it off restores the prior local presentation/audio preferences.
- **Reduced motion** removes non-essential pacing and uses immediate written
  updates. It does not remove a result or a control.
- **Show optional cue explanations** keeps written explanations for audio/event
  cues visible when enabled. Written decisions, observations, results, history,
  and debrief remain complete either way.
- **Text size** supports **Standard** and **Large**. Choose **Large** when the
  default scale is difficult to read; browser zoom remains an additional local
  option.

The initial reduced-motion value follows the browser's `prefers-reduced-motion`
preference when available. Settings are stored in the browser when storage is
available and otherwise remain session-local; a storage failure does not block
play. Low-distraction mode is a local presentation preference, not a host game
mode.

## Optional audio

Audio starts off. Select **Enable audio** after the page opens; browsers require
a user gesture before sound can start. Use **Mute audio** for a complete audio
silence, **Cues only** when you want event/interface feedback without music,
**Music only mute** to remove music, or **Reduced notifications** for fewer
repeated cues. Master, music, interface, event, and ambience volumes are
independent sliders.

Audio emphasizes information already visible on the page. Every cue has a
written equivalent, and muted or unsupported audio never prevents play. For
campaign coverage, host-supplied music/cue metadata is optional and remains
limited to the existing catalog; the written stage and decision surface stays
complete when it is absent or muted.

After a campaign decision commits, expand **Decision-time observation** in the
history entry to revisit the visible information that preceded that command.
This is host-supplied written context, not a hidden-state or outcome forecast.

In **Committed history and replay**, use **Previous row**, **Next row**,
**Play replay**, and **Pause replay** to review the visible committed summaries.
The selected row shows its command, optional observation, visible events/effects,
and state hash in written text. These controls move a local review cursor only;
they do not submit a command or regenerate the simulation. The host verifies
competitive replay determinism before returning the visible projection. An
empty replay says that no committed rows exist, and a failed refresh preserves
the last valid view.

## Credits and provenance

Open **Asset credits and provenance** in the settings panel to inspect the
registered visual and audio sources used by the presentation. The disclosure
is text-first and keyboard-accessible. It describes contributor/release
provenance; it is not a claim that an asset is a real institution, person, or
policy authority.

## Load an existing session

Choose **Find saved checkpoints** under **Saved host checkpoints** to request a
host-owned metadata list. The list shows campaign, opaque session ID, committed
transition count, and whether the entry is from the current archive or the
legacy fallback. Select **Use this session ID**, then choose **Load existing
session**. You can also copy a session ID displayed by the current GUI and enter
it manually. For
`competitive-regional-v1`, `stabilization-v1`, or `regional-affiliation-v1`,
each accepted decision requests autosave; select **Save host checkpoint** before
stopping the host if you want an explicit retry. A browser refresh or manual
load after a restart attempts that host checkpoint once when the opaque ID
matches an archived checkpoint file, then refreshes the ordinary
presentation/campaign/action/history/replay reads. Without a successful
checkpoint, stopping or restarting the host invalidates the live session ID.

## Stop the GUI

Return to the server terminal and press Ctrl-C. All in-memory GUI sessions end
when the process stops; each autosaved competitive, stabilization, or
regional-affiliation checkpoint remains in the host application's sibling
checkpoint archive until that recovered session is ended. Older single-file
checkpoints remain readable as a migration fallback.

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

The ID may belong to a different host, may have no explicit competitive
checkpoint, or may be typed incorrectly. The GUI attempts one host checkpoint
load after an unknown live-session response. If that also fails, start a new
session or enter a matching saved ID; no replacement session is created.

### The browser was refreshed

When browser storage is available, the GUI retains only the opaque host-issued
session ID and attempts the normal host read after refresh. If the live session
is unknown, it tries the host checkpoint load once; this recovers only an
explicitly saved competitive session from the same host's configured file.
Stale or unmatched IDs are cleared with written guidance, while transient
failures preserve the ID for retry. Browser storage never contains commands,
observations, outcomes, hashes, or true state.

### Audio is silent

Select **Enable audio**, check browser/tab mute settings, raise Master and the
relevant channel volume, and return focus to the page. Continue with the written
equivalents if Web Audio is unavailable.

### Settings reset after restarting the browser

The GUI keeps settings in local browser storage when available, but private
browsing, blocked storage, or browser policy can make them session-local. Set
the preferences again after starting a session; this does not affect the host
session or replay.

### Text or motion is difficult to follow

Choose **Large** text, enable **Reduced motion**, and use the written resolution
controls (**Skip to result** or **Review all**) when pacing is distracting. The
host result remains unchanged.

## Scope, safety, and limitations

This is a fictional educational simulation and research prototype. It is not a
calibrated policy forecast or an operational, clinical, financial, regulatory,
or legal decision tool. The current rules, seed, commands, and explicit
stochastic inputs produce a bounded game outcome; they do not estimate what a
real institution, policy, payer, workforce, or community will do.

The GUI is local and in-memory. Browser refresh recovery may retain only the
opaque host session ID and reload the same running host process; it does not
survive a stopped/restarted host. Competitive actions and campaign-coverage
decisions remain host-owned. The host remains
authoritative, and actor-specific observations intentionally omit private rival
state and unresolved hidden inputs. Current technical checks do not replace
human accessibility, educational, audio-quality, provenance, resemblance,
browser/device, full-campaign, persistence, or public-release review. Do not
use the game to make real-world decisions or infer that a fictional institution
represents a real organization or person.
