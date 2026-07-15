mod action;
mod presentation;
mod resolution;
mod server;
mod session;

pub use action::{
  ACTION_CATALOG_SCHEMA_VERSION, ActionCatalogEnvelope, ActionParameter, ActionPreview, ActionSpec,
  VALIDATION_SCHEMA_VERSION, ValidateTurnEnvelope,
};
pub use presentation::{PRESENTATION_SCHEMA_VERSION, ReadOnlyPresentationEnvelope};
pub use resolution::{
  RESOLUTION_SCHEMA_VERSION, ResolutionEffect, ResolutionEnvelope, ResolutionSnapshot,
  ResolutionStep,
};
pub use server::{McpGameServer, run_stdio_server};
pub use session::{
  EndSessionRequest, GameSessionStore, GetActionCatalogRequest, GetHistoryRequest,
  GetObservationRequest, GetPresentationRequest, GetResolutionRequest, McpErrorMessage,
  SessionEnvelope, StartSessionRequest, SubmitTurnRequest, ValidateTurnRequest,
};
