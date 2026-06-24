use super::{History, PlayMode, ReplayError};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ReplayArtifact {
  pub seed: u64,
  pub play_mode: PlayMode,
  pub ruleset_version: String,
  pub history: History,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ReplayArtifactError {
  UnsupportedVersion { found: String },
  RulesetMismatch { expected: String, found: String },
  ParseError { line: usize, detail: String },
  ReplayFailed(ReplayError),
  IoError(String),
}
