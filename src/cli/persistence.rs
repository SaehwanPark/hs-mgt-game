use std::fs;
use std::path::PathBuf;

use crate::artifact::{describe_session_save_error, serialize_session_save, verify_session_save};
use crate::model::{Ruleset, SessionSave, SessionSaveError};

pub fn config_dir() -> PathBuf {
  if let Ok(xdg) = std::env::var("XDG_CONFIG_HOME") {
    PathBuf::from(xdg).join("hs-mgt-game")
  } else if let Ok(home) = std::env::var("HOME") {
    PathBuf::from(home).join(".config").join("hs-mgt-game")
  } else {
    PathBuf::from(".config").join("hs-mgt-game")
  }
}

pub fn session_save_path() -> PathBuf {
  config_dir().join("session.save")
}

pub fn settings_path() -> PathBuf {
  config_dir().join("settings")
}

pub fn session_save_exists() -> bool {
  session_save_path().is_file()
}

pub fn load_session_save(ruleset: &Ruleset) -> Result<SessionSave, SessionSaveError> {
  let path = session_save_path();
  let text = fs::read_to_string(&path).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to read session save at {}: {error}",
      path.display()
    ))
  })?;
  verify_session_save(&text, ruleset)
}

pub fn write_session_save(save: &SessionSave) -> Result<(), SessionSaveError> {
  let dir = config_dir();
  fs::create_dir_all(&dir).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to create config directory {}: {error}",
      dir.display()
    ))
  })?;

  let path = session_save_path();
  fs::write(&path, serialize_session_save(save)).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to write session save to {}: {error}",
      path.display()
    ))
  })
}

pub fn delete_session_save() -> Result<(), SessionSaveError> {
  let path = session_save_path();
  if !path.is_file() {
    return Ok(());
  }

  fs::remove_file(&path).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to delete session save at {}: {error}",
      path.display()
    ))
  })
}

pub fn describe_persistence_error(error: &SessionSaveError) -> String {
  describe_session_save_error(error)
}

pub fn first_run_complete() -> bool {
  let path = settings_path();
  fs::read_to_string(path)
    .map(|text| {
      text
        .lines()
        .any(|line| line.trim() == "first_run_complete=true")
    })
    .unwrap_or(false)
}

pub fn mark_first_run_complete() -> Result<(), SessionSaveError> {
  let dir = config_dir();
  fs::create_dir_all(&dir).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to create config directory {}: {error}",
      dir.display()
    ))
  })?;

  let path = settings_path();
  fs::write(&path, "first_run_complete=true\n").map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to write settings to {}: {error}",
      path.display()
    ))
  })
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{ExperienceMode, History, SessionSave, genesis_state};

  #[test]
  fn delete_session_save_is_idempotent_when_missing() {
    let _ = delete_session_save();
  }

  #[test]
  fn session_save_round_trip_fields() {
    use crate::artifact::deserialize_session_save;

    let save = SessionSave {
      ruleset_version: "demo-ruleset-0.1.0".to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };

    let text = serialize_session_save(&save);
    let restored = deserialize_session_save(&text).unwrap();
    assert_eq!(restored.seed, 42);
    assert_eq!(restored.next_turn, 1);
    assert_eq!(restored.experience_mode, ExperienceMode::Standard);
  }
}
