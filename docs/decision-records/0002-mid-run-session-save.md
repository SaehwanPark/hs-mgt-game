# ADR-0002: Mid-Run Session Save

**Status:** Accepted  
**Date:** 2026-06-24  
**Deciders:** Project contributors

## Context

Interactive CLI play spans five turns with free-form or beginner-mode input. Players
need to quit safely and resume later without conflating classroom replay artifacts
with interactive session state.

[ADR-0001](0001-deterministic-transition-and-stochastic-input-boundary.md) states
that `replay-artifact-0.1.15` is for post-run reproducibility and analysis, not
mid-run saves.

## Decision

1. **Separate save format.** `session-save-0.1.27` stores ruleset id, seed,
   experience mode, genesis state, committed transitions, and `next_turn` (1-based).
   It reuses transition serialization from replay artifacts but is versioned and
   parsed independently.

2. **User config location.** Autosave writes to
   `$XDG_CONFIG_HOME/hs-mgt-game/session.save`, falling back to
   `~/.config/hs-mgt-game/session.save`. A one-line `settings` file in the same
   directory records `first_run_complete=true` for new-player cues.

3. **Autosave on voluntary quit only.** Global `q`/`quit`/`exit` during interactive
   play writes a partial save. Completed runs delete the autosave. Preset paths do
   not autosave.

4. **Resume on startup.** When a valid save exists, the CLI prompts `r` resume or
   `n` start over before the normal briefing flow. Resume verifies partial history
   via `replay()` before continuing.

5. **Global help.** `?`/`help` at any prompt shows contextual guidance without
   advancing session state.

6. **Beginner mode overlay.** `b` at play-mode selection enables per-turn
   multiple-choice options mapped to the three preset strategy paths for that turn.
   Experience mode is stored in the session save.

## Consequences

### Positive

- Interactive sessions can pause without manual replay artifact editing.
- Save semantics stay separate from classroom export artifacts.
- Beginner guidance does not change the deterministic transition core.

### Negative / tradeoffs

- Save format must stay aligned with transition serialization when artifacts evolve.
- Single autosave slot only; no multi-run library.
- Config directory path depends on environment variables.

### Follow-ups

- Scenario loader may embed initial state; save format may gain scenario id.
- Migration policy when `session-save` version bumps.

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Reuse replay artifact for mid-run save | ADR-0001 rejected conflating analysis export with resume |
| Autosave every turn | Out of scope; quit-only reduces I/O and surprise |
| Save in cwd | User chose user config dir for portability |

## Verification

- Round-trip and partial-history session save tests in `src/artifact/session_save_tests.rs`.
- `cargo test` golden seed-42 preset hash unchanged.
- Resume replays committed transitions before continuing.

## Related Documents

- [ADR-0001](0001-deterministic-transition-and-stochastic-input-boundary.md)
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)
