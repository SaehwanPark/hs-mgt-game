# Evidence Map — Visual and Audio Phase 0 Alignment v0.12.16

## Scope

Phase 0 translates the visual/audio proposal into a bounded presentation
decision for one competitive month. It does not implement the client.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md`, especially Sections 11–14.
- `SPEC.md`, `ARCHITECTURE.md`, canonical product documents, and ADR-0008/0009.
- `src/mcp/session.rs`, `src/model/campaign.rs`, competitive observation and
  command modules, `gui/`, and existing GUI contract tests.

## Mechanisms and Institutions

The game remains an executive institutional strategy simulation. The first
presentation target is Riverside Community Health in a regional competitive
market. The client exposes workforce, capacity, access, operations, payer/policy,
market, rival-public-information, project, and debrief surfaces only when they
are already actor-visible.

## Actor Incentives and Information

The player sees `PlayerObservation`, visible legal-command hints, committed
transition summaries, history hashes, and debrief output. Rival private commands,
resolved stochastic inputs, true unreported values, private utility, and future
hidden effects remain excluded. Advisor text is advisory, not binding.

## Assumptions

- Browser-native HTML/CSS/ES modules and SVG are sufficient for the first static
  desktop; no new dependency is needed.
- Current MCP envelopes are inventory evidence, while structured DTOs remain a
  later adapter gap.
- Audio and mood are presentation mappings from visible/committed events, not
  simulation state.

## Unresolved Questions

- Which Phase 2 adapter projections are necessary after static fixture review?
- Which browser hosting mode is justified by later evidence?
- Which individual assets pass provenance review when Phase 5 is promoted?

## Design Implications

- Every graphical action must round-trip through an existing competitive command
  family and host validation.
- Every displayed value and audio cue needs a visible source or an explicit
  missingness label.
- Visual and audio feedback must keep organizational outcomes, actor utility,
  social welfare, decision quality, and educational evaluation distinct.

## Risks

The current MCP surface is partly string-based, so a later DTO promotion could
accidentally duplicate formulas or expose hidden state. AI/static accessibility
checks are technical proxies only; they cannot establish lived human access.
