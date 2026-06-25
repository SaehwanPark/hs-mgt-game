# ADR-0006: Stata-Like CLI Layer

**Status:** Accepted  
**Date:** 2026-06-24  
**Deciders:** Project contributors

## Context

The competitive sketch requires human commands entered in a Stata-like style with
syntax highlighting, autocomplete, and in-game help. Earlier project lessons
deferred a general command parser for the stabilization vertical slice, which uses
numeric prompts and turn-locked parsers.

The competitive campaign needs a documented boundary so CLI parsing does not
violate ADR-0001 by entangling I/O with `transition()`.

## Decision

1. **Competitive campaign only.** Stata-like REPL applies to
   `competitive-regional-v1` entry. Stabilization demo keeps existing prompt UX
   until explicitly migrated.

2. **Parse → validate → transition.** CLI layer (`cli/repl.rs`, `cli/parse.rs`)
   maps command strings to typed `PlayerCommand` values. Validation and
   simulation remain in `sim/` and `model/`.

3. **Grammar.** `verb arg=value` per [`cli-command-grammar-draft.md`](../cli-command-grammar-draft.md).
   Meta commands (`help`, `quit`, `status`, `log`) handled in REPL, not passed
   to transition.

4. **Presentation features.** Syntax highlighting and tab completion are TTY
   affordances using existing `cli/display/style.rs` tokens. `NO_COLOR` disables
   highlighting.

5. **Deterministic replay.** Replay artifacts store typed command batches, not
   raw strings, to avoid parse-version ambiguity. Optional `command_log` field
   for instructor display only.

6. **LESSONS override.** Document in `LESSONS.md` that competitive-track parser
   is intentional scoped exception to parser deferral, not a project-wide
   framework commitment.

## Consequences

### Positive

- Familiar analytical CLI idiom for graduate users
- Reproducible command transcripts for classroom review
- Clear separation preserves testable simulation core

### Negative / tradeoffs

- New parse/test surface area
- Two CLI interaction models coexist until stabilization migrates
- Autocomplete maintenance tied to action catalog changes

### Follow-ups

- Implement `cli/repl.rs` in slice I8 (after action economy and multi-system state)
- Colocated parse tests for grammar edge cases
- Consider shared `help` content generated from action catalog

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Extend numeric prompts to competitive | Does not meet sketch; poor scaling for verb catalog |
| Full shell (shlex + scripts) | Over-engineered for MVP |
| Parser inside transition | Violates ADR-0001 and testability |
| Migrate stabilization first | Regression risk; user chose parallel campaign |

## Verification

- CLI grammar draft and action catalog aligned
- Future tests: parse errors never call `transition()`
- `cargo test` stabilization golden unchanged

## Related Documents

- [ADR-0001](0001-deterministic-transition-and-stochastic-input-boundary.md)
- [`cli-command-grammar-draft.md`](../cli-command-grammar-draft.md)
- [`LESSONS.md`](../../LESSONS.md)
