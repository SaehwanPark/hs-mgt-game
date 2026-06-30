# CLI Command Grammar Draft

**Status:** Phase 6.0 design artifact  
**Audience:** CLI implementers  
**Campaign:** `competitive-regional-v1` only (stabilization demo keeps numeric prompts)

## Design goals

- Stata-like `verb arg=value` entry with reproducible command log
- Syntax highlighting when stdout is a TTY and `NO_COLOR` is unset
- Tab autocomplete, currently implemented for verbs only
- In-game `help` without leaving the session
- Parse layer only — no simulation logic (ADR-0006)

## Grammar

```text
command     := verb (ws arg)*
verb        := lowercase identifier
arg         := name "=" value
name        := lowercase identifier
value       := integer | identifier | quoted_string
ws          := space | tab
batch       := command (";" ws command)* | command newline+
```

### Examples

```text
invest domain=beds amount=25
recruit role=nurse headcount=5
monitor target=northlake depth=2
commit pledge_type=access level=3
project kind=ehr_epic budget=60
hold
```

### Batch entry

- Semicolon separates commands on one line: `invest domain=beds amount=20; commit pledge_type=access level=2`
- Empty submit with no input defaults to `hold` (teaching safety)
- `submit` or blank line after multi-line entry ends batch (implementation choice in I8)

## Meta commands

| Input | Action |
| --- | --- |
| `help` | List verbs with one-line description |
| `help <verb>` | Show arguments, costs, example |
| `?` | Alias for `help` |
| `quit` / `q` | Exit command path; stabilization autosave uses ADR-0002, competitive save semantics remain deferred |
| `status` | Show remaining AP, cash, political capital |
| `log` | Show commands submitted this month (preview before submit) |

## Syntax highlighting (TTY)

| Token | Style | Example |
| --- | --- | --- |
| verb | bold cyan | `invest` |
| arg name | dim white | `domain` |
| operator | white | `=` |
| integer value | yellow | `25` |
| enum value | green | `beds` |
| string value | magenta | `"Q2 target"` |
| comment | dim | `// optional end-of-line` |

Comments: `//` to end of line ignored (optional in MVP).

## Autocomplete

- After empty or partial line, Tab completes verb from action catalog
- After `verb `, Tab cycles arg names required for verb
- After `name=`, Tab cycles enum values if arg is enum type
- No filesystem completion

## Error messages

```text
error: unknown verb "invst"
error: invest requires argument domain=
error: amount=200 exceeds max_capital_spend (40)
error: insufficient action points (need 2, have 1)
error: insufficient cash (need 25, have 18)
```

Errors do not advance the month.

## Command log and replay

- Store typed `PlayerCommand` batches in replay artifacts (canonical per ADR-0006).
- Optional `command_log` raw strings for instructor display only.
- Parse must be deterministic: same string → same typed command

## Related documents

- [`action-catalog-draft.md`](action-catalog-draft.md)
- ADR-0006
- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md) §12
