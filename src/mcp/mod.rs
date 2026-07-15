mod presentation;
mod server;
mod session;

pub use presentation::{PRESENTATION_SCHEMA_VERSION, ReadOnlyPresentationEnvelope};
pub use server::{McpGameServer, run_stdio_server};
pub use session::{
  EndSessionRequest, GameSessionStore, GetHistoryRequest, GetObservationRequest,
  GetPresentationRequest, McpErrorMessage, SessionEnvelope, StartSessionRequest, SubmitTurnRequest,
};
