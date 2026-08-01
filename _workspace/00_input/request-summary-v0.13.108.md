# Request summary: v0.13.108 Firefox multi-campaign launch smoke

## User objective

Continue the visual/audio enhancement roadmap through bounded implementation,
single-reviewer PR, merge, cleanup, and re-audit loops without converting
technical evidence into human or release approval.

## Selected slice

The v0.13.107 re-audit left Firefox full-campaign certification open. The
available Firefox runtime can exercise the live GUI host, so this slice extends
the bounded Marionette smoke to start each currently supported campaign:

- competitive regional market;
- stabilization tutorial; and
- regional affiliation.

Each result must return a host-issued opaque session ID, the expected campaign
label, a non-demo shell, and a complete document state. This is launch/read
continuity evidence only; it is not full campaign certification.

## Non-goals

- No simulation, replay, save-artifact, asset, audio, or browser-policy change.
- No Safari/WebKit permission change or real-device claim.
- No human accessibility, educational, provenance, content, or public-release
  decision.
