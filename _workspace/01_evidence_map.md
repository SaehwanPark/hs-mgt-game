# Evidence Map — Visual and Audio Phase 1 Static Desktop v0.12.17

## Scope

Phase 1 tests the visual information architecture with injected actor-visible
data for one competitive month. It does not claim live DTO parity or human
usability.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 1 requirements.
- Phase 0 alignment and ADR-0011.
- Current `gui/` proof, MCP session envelopes, competitive observations,
  commands, history, and debrief surfaces.
- README, SPEC, architecture, design principles, and project harness spec.

## Mechanisms and Institutions

The fixture represents Riverside Community Health and public rival signals in a
fictional regional market. The player remains an executive making institutional
decisions. Facilities, workforce, capacity, access, operations, and pending
processes are presented as inspectable institutional surfaces.

## Actor Incentives and Information

The player sees cash, margin, AP, political capital, trust, access/quality,
staffing/capacity, public rival signals, visible process timing, direct monthly
results, legal command hints, history, and debrief. Private rival actions, true
state, resolved inputs, and hidden future outcomes remain absent or explicitly
labeled unavailable.

## Assumptions

- The `presentation_fixture` is display data, not simulation state.
- Entity selection changes local presentation only.
- Existing adapter submission remains the only non-empty command path.
- Semantic HTML, CSS tokens, and native browser controls are sufficient for the
  static architecture gate without a frontend dependency.

## Unresolved Questions

- Whether a typed live adapter is needed after fixture-task review.
- Which fields require structured projection rather than current MCP strings.
- How live loading, errors, explicit missingness, and replay/hash views should be
  represented in Phase 2.

## Design Implications

- Information hierarchy can be validated before live DTO expansion.
- Source labels and unavailable markers must remain visible as the interface
  becomes richer.
- Action previews must communicate cost, delay, constraint, and uncertainty
  without resolving or promising an outcome.

## Risks

Static fixture success can overstate live parity or human comprehension. The
fixture must not drift into a second scenario or duplicate simulation formulas;
Phase 2 requires a source-by-source adapter decision before live integration.
