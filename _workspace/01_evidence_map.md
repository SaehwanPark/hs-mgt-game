# Evidence Map - Competitive Campaign Length & Autosave

## Assumptions
- Competitive campaign players require autosave to prevent loss of progress over longer campaign runs (24 months).
- Replaying and verifying competitive campaigns is needed for diagnostics and educational debriefing.

## Precedents
- **Stabilization Autosave (`session.save`):** Uses a text-based format in `.config/hs-mgt-game/session.save`. We will implement a similar format for competitive campaigns.
- **Replay Serialization:** Stabilization supports exporting `replay-artifact-*.json` (or similar). We will support exporting a competitive replay serialization format on campaign completion.
