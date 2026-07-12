# Evidence Map — GUI Thin-Client Proof v0.12.11

| Requirement | Authority | Result | Limit |
| --- | --- | --- | --- |
| Existing output contract | `gui/app.mjs` + MCP envelope fields | observation, legal commands, history, debrief rendered | Demo envelope is fixture data. |
| Server authority | adapter boundary and submit smoke test | legality/submission delegated | No live adapter in static proof. |
| No duplicated state | static source audit | no transition/parser/network code | Not a production security audit. |
| Asset license | `gui/README.md` and source scan | zero external assets | No downloaded asset review needed. |
| Local accessibility of surface | local HTTP server | both files served | Browser backend unavailable for visual QA. |

Conclusion: thin-client proof is supported; production GUI promotion remains
out of scope.
