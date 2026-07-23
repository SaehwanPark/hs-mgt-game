mod action;
mod campaign_coverage;
mod presentation;
mod regional_world;
mod resolution;
mod server;
mod session;

pub use action::{
  ACTION_CATALOG_SCHEMA_VERSION, ActionCatalogEnvelope, ActionParameter, ActionPreview, ActionSpec,
  VALIDATION_SCHEMA_VERSION, ValidateTurnEnvelope,
};
pub use campaign_coverage::{CAMPAIGN_COVERAGE_SCHEMA_VERSION, CampaignCoverageEnvelope};
pub use presentation::{PRESENTATION_SCHEMA_VERSION, ReadOnlyPresentationEnvelope};
pub use regional_world::{REGIONAL_WORLD_SCHEMA_VERSION, RegionalWorldEnvelope};
pub use resolution::{
  RESOLUTION_SCHEMA_VERSION, ResolutionEffect, ResolutionEnvelope, ResolutionSnapshot,
  ResolutionStep,
};
pub use server::{McpGameServer, run_stdio_server};
pub use session::{
  EndSessionRequest, GameSessionStore, GetActionCatalogRequest, GetCampaignCoverageRequest,
  GetHistoryRequest, GetObservationRequest, GetPresentationRequest, GetRegionalWorldRequest,
  GetReplayRequest, GetResolutionRequest, HISTORY_SCHEMA_VERSION, McpErrorMessage,
  REPLAY_SCHEMA_VERSION, SessionEnvelope, StartSessionRequest, SubmitTurnRequest,
  ValidateTurnRequest,
};
