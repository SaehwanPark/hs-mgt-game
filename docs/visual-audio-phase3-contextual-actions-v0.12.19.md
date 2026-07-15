# Visual and Audio Phase 3 — Contextual Action Submission

Status: Implemented for the `competitive-regional-v1` campaign.

Date: 2026-07-15

Phase 3 adds the first graphical decision-to-submit path. It lets an executive
build and revise one canonical competitive batch, validate it through the host,
and submit it without typing CLI syntax. Monthly resolution animation and
causal feedback remain Phase 4.

## Typed action catalog and validation contract

The host exposes two non-mutating reads:

| Contract | Purpose | Authority/source |
| --- | --- | --- |
| `competitive-actions-v1` via `get_action_catalog` | Seven existing command families, canonical templates, parameters/options/bounds, and descriptive delay/uncertainty/constraint labels | Existing competitive command vocabulary plus host presentation metadata |
| `competitive-validation-v1` via `validate_turn` | Canonical batch text, valid/invalid result, aggregate `ActionCost`, per-action preview, and recoverable errors | Existing parser, `CompetitiveCommand::action_cost`, and `validate_competitive_batch` |

The catalog covers `hold`, `invest`, `recruit`, `monitor`, `negotiate`,
`commit`, and `project`. It contains no new command family, private rival
field, resolved stochastic input, or outcome forecast. Numeric bounds and costs
are not reimplemented in the browser; the host returns the validation result.

## Source and authority map

The browser receives a command template and parameter metadata, substitutes the
selected values into that template, and keeps the resulting canonical text in
local draft state. The host parses and validates the complete semicolon-separated
batch. A valid response supplies exact aggregate AP/cash/political-capital cost
and descriptive previews. An invalid response is data for revision, not a
transition error that the browser must reconstruct.

`submit_turn` remains the only mutation. The browser calls it only when the
unchanged draft has a host validation response with `valid: true`. A rejected
submission leaves the current read-only envelope and draft available for retry;
a successful response is followed by a fresh read-only presentation when the
adapter provides one.

## Draft and submit behavior

The action adapter is injected at the host boundary:

```js
window.HsMgtGameActionAdapter = {
  sessionId: "session-1",
  async getPresentation(sessionId) {},
  async getActionCatalog(sessionId) {},
  async validateTurn(sessionId, commandText) {},
  async submitTurn(commandText) {},
};
```

The page renders generic forms from the catalog. A player can add Hold or a
parameterized command, revise an existing row, remove it, validate the full
batch, read host-returned costs/delays/constraints/uncertainty, and submit the
validated month. Changing a draft invalidates the previous validation. Missing
adapter methods fail closed to read-only behavior. The browser does not expose
the legacy command text field in the action-builder path.

## Static review checklist

1. Load a session with the action adapter and inspect all catalogued command
   families and canonical templates.
2. Add at least two actions using graphical controls; confirm the draft rows
   show canonical text.
3. Revise one draft and remove another; confirm validation is cleared.
4. Validate a valid batch and verify exact host-returned aggregate costs and
   per-action metadata.
5. Validate an invalid batch and recover by revising it without a turn change.
6. Attempt submit before validation and confirm no adapter transition call.
7. Submit a validated batch and inspect the committed host response/read-only
   refresh; no outcome should be promised before resolution.
8. Exercise missing adapter, adapter error, narrow viewport, keyboard, and
   no-network/no-asset behavior.

Automated checks cover command-family/catalog markers, host-validation wiring,
no local cost formula, no-submit-before-validation, syntax, and asset/network
boundaries. They are technical/interface-task proxies only; they do not
establish human usability, engagement, lived accessibility, learning,
classroom effectiveness, domain validity, calibration, balance, or policy
validity.

## Explicit non-goals and next gate

This phase does not implement resolution animation, causal overlays, replay
playback, audio, assets, mobile support, instructor true-state views, other
campaigns, or a second parser. It does not change transition formulas,
randomness, replay verification, history semantics, or debrief generation.

Phase 4 is the next candidate: committed monthly resolution sequencing,
skippable/reviewable motion, direct causal overlays, operating breakdown, and
non-mutating replay of the resolution presentation.
