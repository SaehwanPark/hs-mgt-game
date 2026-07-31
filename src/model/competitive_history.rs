use super::{
  AggregatedMonthlyActions, AttributedEffect, CompetitiveValidationError, CompetitiveWorldState,
  Event,
};

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct CompetitiveTransition {
  pub prior: CompetitiveWorldState,
  pub aggregated: AggregatedMonthlyActions,
  pub events: Vec<Event>,
  pub effects: Vec<AttributedEffect>,
  pub next: CompetitiveWorldState,
  pub state_hash: String,
  #[serde(default)]
  pub consultant_options: Vec<crate::model::ConsultantOption>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CompetitiveReplayError {
  Validation(CompetitiveValidationError),
  TransitionMismatch {
    turn: u32,
  },
  StateHashMismatch {
    turn: u32,
    expected: String,
    actual: String,
  },
}

impl CompetitiveReplayError {
  pub fn message(&self) -> String {
    match self {
      Self::Validation(error) => error.message(),
      Self::TransitionMismatch { turn } => {
        format!("competitive replay transition mismatch at turn {turn}")
      }
      Self::StateHashMismatch {
        turn,
        expected,
        actual,
      } => format!(
        "competitive replay state hash mismatch at turn {turn}: expected {expected}, got {actual}"
      ),
    }
  }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct CompetitiveHistory {
  pub genesis: CompetitiveWorldState,
  pub transitions: Vec<CompetitiveTransition>,
}

impl CompetitiveHistory {
  pub fn final_state(&self) -> &CompetitiveWorldState {
    self
      .transitions
      .last()
      .map(|transition| &transition.next)
      .unwrap_or(&self.genesis)
  }
}
