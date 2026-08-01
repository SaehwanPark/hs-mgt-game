# Request summary: v0.13.107 Firefox browser-refresh resume smoke

## User objective

Continue the visual/audio enhancement roadmap until no unmet item remains,
using the repository workflow of bounded plan, implementation, one medium-
effort code review, squash merge, temporary-branch cleanup, and re-audit.

## Selected slice

The v0.13.106 re-audit found no remaining technical implementation gap, but the
cross-browser/device gate remains a blocking runtime-certification item. The
current machine has an executable Firefox 147.0.2 and the existing bounded
Marionette smoke passes. This slice adds a stronger, still source-bound smoke
for the new browser-refresh resume policy:

- start a competitive host session in Firefox;
- save one explicit host checkpoint;
- refresh the page with the stored value containing only the opaque session ID;
- verify one host-backed resume reaches the same session and visible shell; and
- keep Firefox support, full-campaign certification, WebKit, real-device,
  human-accessibility, and public-release decisions pending.

## Non-goals

- No simulation or replay changes.
- No browser save-artifact serialization or parsing.
- No Safari/WebKit permission changes.
- No support-policy promotion or human/runtime certification claim.
- No asset, audio, screenshot, or campaign-content changes.
