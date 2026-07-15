# Mechanism Design — Visual/audio Phase 11 first-session launch/load v0.12.27

## Goal and Roadmap Phase

Implement the launch/load boundary required by the first competitive vertical
slice in the visual/audio proposal. This is Phase 11 after the merged Phase 10
presentation hardening. The slice is an adapter/UI lifecycle boundary, not a
new simulation mechanism.

## Slice Boundary

- Campaign: `competitive-regional-v1` only for new starts.
- Setup: seed (default 42) and difficulty (`easy`, `normal`, `hard`, or
  `expert`) selected in the browser.
- Load: an existing session ID entered by the user and read through the
  existing presentation/action clients.
- Outcome: an initial host envelope is rendered, with briefing, regional
  market, player system, facilities, legal action surface, and session status
  available through existing components.
- Excluded: campaign transitions, command submission, scenario file input,
  session persistence, authentication, transport, assets, and audio changes.

## Actors and Authority

- The human executive owns only the setup choice and load request.
- The browser launcher owns form state, pending/error status, and the currently
  selected adapter session ID.
- The host/MCP session store owns campaign parsing, seed/difficulty validation,
  scenario validation, session allocation, initial state, actor observations,
  and all subsequent transitions.
- No actor strategy or utility is changed.

## State, Beliefs, and Observations

- Before start, there is no browser-owned game state and no valid first-month
  observation to display as live data.
- A successful `startSession` returns the host's session envelope, including
  `session_id`, campaign, seed, difficulty, turn, max turns, done state, and
  initial observation/legal-command fields. The GUI then obtains the typed
  `competitive-read-only-v1` presentation by session ID.
- A successful load reads an existing host session by ID. The launcher does not
  inspect hidden state or reconstruct a session from local settings.
- Failed or malformed start/load responses preserve the current rendered
  session, show a recoverable status, and expose no guessed data.

## Commands, Events, and Effects

- `startSession` maps to the existing host `start_session` operation and does
  not submit a game command or advance a turn.
- `loadSession` calls the existing client `load(sessionId)` path and does not
  submit a command or advance a turn.
- The existing `session_loaded` event remains the only capture event emitted
  after a successful visible presentation load.
- No stochastic inputs, delayed effects, transition summaries, history entries,
  hashes, replay records, or debrief lines are created by the launcher itself.

## Strategic Interaction

There is no new strategic interaction. Campaign, seed, difficulty, and session
ID are lifecycle inputs. The launcher must not rank difficulty, promise a
strategy, label a seed as favorable, or imply that starting a session is an
outcome.

## Assumptions and Parameters

- New start always sends `campaign: "competitive-regional-v1"`.
- Seed is a finite non-negative integer; invalid or empty input is rejected
  before the adapter call.
- Difficulty is allowlisted to the four host-supported labels and defaults to
  `normal`.
- Adapter response must expose a non-empty `session_id`; alias-only or
  malformed responses are rejected so the browser never guesses authority.
- The active session ID is replaced only after a successful subsequent
  presentation load, preventing a failed start from discarding the current
  view.

## Educational Debrief Hooks

The launcher only improves access to the existing observation and decision
surfaces. It does not add guidance, strategy advice, causal explanations, or
learning claims. Existing history, resolution, and debrief content remain
host-provided after play.

## Determinism and Replay Notes

Starting with the same host-supported campaign, seed, difficulty, and scenario
produces the same host initial state under existing session semantics. The
browser contributes no randomness and stores no simulation state. Navigation,
form state, and the selected session ID are presentation/client state and do
not enter commands, transitions, history, hashes, replay artifacts, or
debriefs.

## Open Questions

- A deployed browser transport for `startSession` remains future integration
  work; this slice tests the adapter boundary with a fake host adapter.
- A user-facing scenario picker and saved-session browser require separate
  scope and release decisions.
- Real first-time launch success and accessibility require browser/agent or
  human evidence beyond static tests.
