use super::{ExperienceMode, History, ReplayError};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SessionSave {
  pub ruleset_version: String,
  pub seed: u64,
  pub experience_mode: ExperienceMode,
  pub history: History,
  pub next_turn: u32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum SessionSaveError {
  UnsupportedVersion { found: String },
  RulesetMismatch { expected: String, found: String },
  ParseError { line: usize, detail: String },
  ReplayFailed(ReplayError),
  IoError(String),
}
