# Contributor Documentation

This index separates current instructions from dated evidence. Current
documentation must describe the checked-in code and tests; historical and
workspace records preserve what was known at an earlier slice and are not
current implementation instructions.

## Document authority

| Class | Location | Authority |
| --- | --- | --- |
| Product direction | `README.md`, `docs/proposal.md`, `docs/roadmap.md`, `docs/design_principles.md` | Current intent and scope |
| Software SDD | `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md` | Current state, boundaries, and release history |
| Active design/reference | `docs/design/`, `docs/reference/`, `docs/research/`, `docs/validation/` | Current mechanics, terminology, evidence, and workflows |
| GUI/presentation | `gui/README.md`, `docs/guides/gui-how-to-play.md`, visual/audio roadmap, asset READMEs | Current GUI contracts and player/contributor operation |
| Decision records | `docs/decision-records/` | Point-in-time decisions; later records supersede changed direction |
| Generated/registry records | `assets/`, generated credits, release manifests | Machine-produced or provenance-controlled outputs; do not hand-edit generated files |
| Historical evidence | `docs/history/` | Immutable prior findings, milestones, and superseded plans |
| Agent workspace | `_workspace/` | Dated handoffs and experiment artifacts; append current handoffs, do not rewrite prior slices |

## Software contributor path

1. Read [SPEC](../SPEC.md) and [ARCHITECTURE](../ARCHITECTURE.md).
2. Review the [core loop](design/core-loop-spec.md), [system boundary](design/system-boundary.md), and [MCP interface](reference/mcp-agent-interface.md) relevant to the change.
3. Use the [versioning policy](reference/versioning-policy.md) and
   [release metadata check](guides/contributor-release-check.md).
4. Consult the [decision records](decision-records/README.md) before changing
   an accepted boundary.
5. Run the documentation-currentness checker before committing documentation.

## GUI and presentation path

1. Read the current [GUI roadmap](visual_audio_enhancement_roadmap.md),
   [design principles](design_principles.md), and [presentation architecture](../ARCHITECTURE.md).
2. Confirm that every semantic visual/audio element has an actor-visible host
   source, written equivalent, safe unknown state, and replay-safe boundary.
3. Keep commands, legality, transitions, history, replay, checkpoints, and
   debriefs host-owned. Browser navigation, drafts, settings, motion, and audio
   remain presentation state.
4. Use the [GUI player guide](guides/gui-how-to-play.md) and
   [GUI technical reference](../gui/README.md) for current operation.
5. Treat Chromium evergreen desktop as the default browser target. Codex
   browser inspection is development evidence; non-default engines are
   deferred.

## Game and domain design path

Use the [glossary](reference/glossary.md), [actor cards](design/actor-cards.md),
[action catalog](design/action-catalog-draft.md), campaign briefs, scenario
format, [evidence registry](research/evidence-registry.md), and [workforce
ledger](research/workforce-ledger.md). Route breadth through the
[expansion proposal review](design/expansion-proposal-review.md).

## AI-native validation path

The active validation path uses deterministic MCP/GUI adapters, AI-agent
profiles, source-bound traces, replay/hash checks, accessibility-mode checks,
and presentation/domain QA. These establish technical and gameplay evidence,
not human learning, lived accessibility, legal clearance, calibration, balance,
or policy validity. Those limits are recorded honestly but do not stop routine
technical progression; unsafe or unverifiable assets remain excluded.

See the [playtesting protocol](validation/playtesting.md), [MCP playtesting
guide](guides/mcp-playtesting-guide.md), and repository-local [agent harness](harness/health-policy-strategy-game/team-spec.md).

## Player guides

- [CLI guide](guides/how-to-play.md)
- [GUI guide](guides/gui-how-to-play.md)

## Historical context

The [history index](history/README.md) explains retained findings and why they
should not be treated as present-tense instructions.
