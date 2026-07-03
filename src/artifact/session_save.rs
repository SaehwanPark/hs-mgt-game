use crate::model::{History, ReplayArtifactError, Ruleset, SessionSave, SessionSaveError};
use crate::replay::replay;

use super::parse::{parse_experience_mode, parse_transition_block, parse_world_state_line};
use super::session_save_serialize::SESSION_SAVE_VERSION;

pub fn deserialize_session_save(text: &str) -> Result<SessionSave, SessionSaveError> {
  let raw_lines: Vec<&str> = text
    .lines()
    .map(str::trim)
    .filter(|line| !line.is_empty())
    .collect();

  if raw_lines.is_empty() {
    return Err(SessionSaveError::ParseError {
      line: 0,
      detail: "empty session save".to_string(),
    });
  }

  if raw_lines[0] != SESSION_SAVE_VERSION {
    return Err(SessionSaveError::UnsupportedVersion {
      found: raw_lines[0].to_string(),
    });
  }

  let mut ruleset_version = None;
  let mut seed = None;
  let mut experience_mode = None;
  let mut next_turn = None;
  let mut genesis = None;
  let mut transition_count = None;
  let mut transitions = Vec::new();
  let mut index = 1;

  while index < raw_lines.len() {
    let line = raw_lines[index];
    index += 1;

    if let Some(stripped) = line.strip_prefix("ruleset=") {
      ruleset_version = Some(stripped.to_string());
      continue;
    }
    if let Some(stripped) = line.strip_prefix("seed=") {
      seed = Some(
        stripped
          .parse::<u64>()
          .map_err(|_| map_parse_error(index, "invalid seed"))?,
      );
      continue;
    }
    if let Some(stripped) = line.strip_prefix("experience_mode=") {
      experience_mode = Some(parse_experience_mode(stripped).map_err(map_replay_error)?);
      continue;
    }
    if let Some(stripped) = line.strip_prefix("next_turn=") {
      next_turn = Some(
        stripped
          .parse::<u32>()
          .map_err(|_| map_parse_error(index, "invalid next_turn"))?,
      );
      continue;
    }
    if line.starts_with("genesis=") {
      genesis = Some(parse_world_state_line(line, "genesis").map_err(map_replay_error)?);
      continue;
    }
    if let Some(stripped) = line.strip_prefix("transition_count=") {
      transition_count = Some(
        stripped
          .parse::<usize>()
          .map_err(|_| map_parse_error(index, "invalid transition_count"))?,
      );
      continue;
    }
    if line == "[transition]" {
      let mut block = Vec::new();
      while index < raw_lines.len() && raw_lines[index] != "[/transition]" {
        block.push(raw_lines[index]);
        index += 1;
      }
      if index >= raw_lines.len() {
        return Err(SessionSaveError::ParseError {
          line: index,
          detail: "unterminated transition block".to_string(),
        });
      }
      transitions.push(parse_transition_block(&block).map_err(map_replay_error)?);
      index += 1;
    }
  }

  let expected_count = transition_count.ok_or_else(|| SessionSaveError::ParseError {
    line: 0,
    detail: "missing transition_count".to_string(),
  })?;
  if transitions.len() != expected_count {
    return Err(SessionSaveError::ParseError {
      line: 0,
      detail: format!(
        "transition_count {expected_count} does not match parsed transitions {}",
        transitions.len()
      ),
    });
  }

  let next_turn = next_turn.ok_or_else(|| SessionSaveError::ParseError {
    line: 0,
    detail: "missing next_turn".to_string(),
  })?;

  if !(1..=crate::model::INTERACTIVE_TURN_COUNT + 1).contains(&next_turn) {
    return Err(SessionSaveError::ParseError {
      line: 0,
      detail: format!("next_turn {next_turn} is out of range"),
    });
  }

  if transitions.len() as u32 + 1 != next_turn {
    return Err(SessionSaveError::ParseError {
      line: 0,
      detail: format!(
        "next_turn {next_turn} does not match committed transition count {}",
        transitions.len()
      ),
    });
  }

  Ok(SessionSave {
    ruleset_version: ruleset_version.ok_or_else(|| SessionSaveError::ParseError {
      line: 0,
      detail: "missing ruleset".to_string(),
    })?,
    seed: seed.ok_or_else(|| SessionSaveError::ParseError {
      line: 0,
      detail: "missing seed".to_string(),
    })?,
    experience_mode: experience_mode.ok_or_else(|| SessionSaveError::ParseError {
      line: 0,
      detail: "missing experience_mode".to_string(),
    })?,
    history: History {
      genesis: genesis.ok_or_else(|| SessionSaveError::ParseError {
        line: 0,
        detail: "missing genesis".to_string(),
      })?,
      transitions,
    },
    next_turn,
  })
}

pub fn verify_session_save(text: &str, ruleset: &Ruleset) -> Result<SessionSave, SessionSaveError> {
  let save = deserialize_session_save(text)?;
  if save.ruleset_version != ruleset.version {
    return Err(SessionSaveError::RulesetMismatch {
      expected: ruleset.version.to_string(),
      found: save.ruleset_version,
    });
  }

  replay(&save.history, ruleset).map_err(SessionSaveError::ReplayFailed)?;
  Ok(save)
}

pub fn describe_session_save_error(error: &SessionSaveError) -> String {
  match error {
    SessionSaveError::UnsupportedVersion { found } => {
      format!("unsupported session save version {found}")
    }
    SessionSaveError::RulesetMismatch { expected, found } => {
      format!("ruleset mismatch: expected {expected}, found {found}")
    }
    SessionSaveError::ParseError { line, detail } => {
      if *line == 0 {
        format!("session save parse error: {detail}")
      } else {
        format!("session save parse error at line {line}: {detail}")
      }
    }
    SessionSaveError::ReplayFailed(crate::model::ReplayError::InvalidTransition(
      validation_error,
    )) => format!("session save replay failed during transition: {validation_error:?}"),
    SessionSaveError::ReplayFailed(crate::model::ReplayError::StateHashMismatch {
      turn,
      expected,
      actual,
    }) => format!(
      "session save replay failed at turn {turn}: expected hash {expected}, actual {actual}"
    ),
    SessionSaveError::IoError(message) => message.clone(),
  }
}

fn map_parse_error(line: usize, detail: &str) -> SessionSaveError {
  SessionSaveError::ParseError {
    line,
    detail: detail.to_string(),
  }
}

fn map_replay_error(error: ReplayArtifactError) -> SessionSaveError {
  match error {
    ReplayArtifactError::ParseError { line, detail } => {
      SessionSaveError::ParseError { line, detail }
    }
    ReplayArtifactError::UnsupportedVersion { found } => {
      SessionSaveError::UnsupportedVersion { found }
    }
    ReplayArtifactError::RulesetMismatch { expected, found } => {
      SessionSaveError::RulesetMismatch { expected, found }
    }
    ReplayArtifactError::ReplayFailed(replay_error) => SessionSaveError::ReplayFailed(replay_error),
    ReplayArtifactError::IoError(message) => SessionSaveError::IoError(message),
  }
}

#[cfg(test)]
#[path = "session_save_tests.rs"]
mod session_save_tests;
