use std::fs;

use crate::model::{
  History, ReplayArtifact, ReplayArtifactError, ReplayError, ReplayVerification, Ruleset,
};
use crate::replay::replay;

use super::parse::{parse_play_mode, parse_transition_block, parse_world_state_line};
use super::serialize::{REPLAY_ARTIFACT_VERSION, serialize_replay_artifact};

pub fn deserialize_replay_artifact(text: &str) -> Result<ReplayArtifact, ReplayArtifactError> {
  let raw_lines: Vec<&str> = text
    .lines()
    .map(str::trim)
    .filter(|line| !line.is_empty())
    .collect();

  if raw_lines.is_empty() {
    return Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: "empty replay artifact".to_string(),
    });
  }

  if raw_lines[0] != REPLAY_ARTIFACT_VERSION {
    return Err(ReplayArtifactError::UnsupportedVersion {
      found: raw_lines[0].to_string(),
    });
  }

  let mut ruleset_version = None;
  let mut seed = None;
  let mut play_mode = None;
  let mut genesis = None;
  let mut transition_count = None;
  let mut transitions = Vec::new();
  let mut index = 1;

  while index < raw_lines.len() {
    let line = raw_lines[index];
    index += 1;

    if line.starts_with("ruleset=") {
      ruleset_version = Some(line["ruleset=".len()..].to_string());
      continue;
    }
    if line.starts_with("seed=") {
      seed = Some(line["seed=".len()..].parse::<u64>().map_err(|_| {
        ReplayArtifactError::ParseError {
          line: index,
          detail: "invalid seed".to_string(),
        }
      })?);
      continue;
    }
    if line.starts_with("play_mode=") {
      play_mode = Some(parse_play_mode(&line["play_mode=".len()..])?);
      continue;
    }
    if line.starts_with("genesis=") {
      genesis = Some(parse_world_state_line(line, "genesis")?);
      continue;
    }
    if line.starts_with("transition_count=") {
      transition_count = Some(line["transition_count=".len()..].parse::<usize>().map_err(
        |_| ReplayArtifactError::ParseError {
          line: index,
          detail: "invalid transition_count".to_string(),
        },
      )?);
      continue;
    }
    if line == "[transition]" {
      let mut block = Vec::new();
      while index < raw_lines.len() && raw_lines[index] != "[/transition]" {
        block.push(raw_lines[index]);
        index += 1;
      }
      if index >= raw_lines.len() {
        return Err(ReplayArtifactError::ParseError {
          line: index,
          detail: "unterminated transition block".to_string(),
        });
      }
      transitions.push(parse_transition_block(&block)?);
      index += 1;
    }
  }

  let expected_count = transition_count.ok_or_else(|| ReplayArtifactError::ParseError {
    line: 0,
    detail: "missing transition_count".to_string(),
  })?;
  if transitions.len() != expected_count {
    return Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!(
        "transition_count {expected_count} does not match parsed transitions {}",
        transitions.len()
      ),
    });
  }

  Ok(ReplayArtifact {
    seed: seed.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing seed".to_string(),
    })?,
    play_mode: play_mode.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing play_mode".to_string(),
    })?,
    ruleset_version: ruleset_version.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing ruleset".to_string(),
    })?,
    history: History {
      genesis: genesis.ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: "missing genesis".to_string(),
      })?,
      transitions,
    },
  })
}

pub fn verify_replay_artifact(
  text: &str,
  ruleset: &Ruleset,
) -> Result<ReplayVerification, ReplayArtifactError> {
  let artifact = deserialize_replay_artifact(text)?;
  if artifact.ruleset_version != ruleset.version {
    return Err(ReplayArtifactError::RulesetMismatch {
      expected: ruleset.version.to_string(),
      found: artifact.ruleset_version,
    });
  }

  replay(&artifact.history, ruleset).map_err(ReplayArtifactError::ReplayFailed)
}

pub fn write_replay_artifact(
  path: &str,
  artifact: &ReplayArtifact,
) -> Result<(), ReplayArtifactError> {
  fs::write(path, serialize_replay_artifact(artifact)).map_err(|error| {
    ReplayArtifactError::IoError(format!(
      "unable to write replay artifact to {path}: {error}"
    ))
  })
}

pub fn describe_replay_artifact_error(error: &ReplayArtifactError) -> String {
  match error {
    ReplayArtifactError::UnsupportedVersion { found } => {
      format!("unsupported replay artifact version {found}")
    }
    ReplayArtifactError::RulesetMismatch { expected, found } => {
      format!("ruleset mismatch: expected {expected}, found {found}")
    }
    ReplayArtifactError::ParseError { line, detail } => {
      if *line == 0 {
        format!("replay artifact parse error: {detail}")
      } else {
        format!("replay artifact parse error at line {line}: {detail}")
      }
    }
    ReplayArtifactError::ReplayFailed(ReplayError::InvalidTransition(validation_error)) => {
      format!("replay verification failed during transition: {validation_error:?}")
    }
    ReplayArtifactError::ReplayFailed(ReplayError::StateHashMismatch {
      turn,
      expected,
      actual,
    }) => format!(
      "replay verification failed at turn {turn}: expected hash {expected}, actual {actual}"
    ),
    ReplayArtifactError::IoError(message) => message.clone(),
  }
}
