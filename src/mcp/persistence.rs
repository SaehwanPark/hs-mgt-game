use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};

use crate::artifact::{
  describe_session_save_error, deserialize_affiliation_replay,
  deserialize_competitive_session_save, serialize_affiliation_replay,
  serialize_competitive_session_save, serialize_session_save, verify_affiliation_replay,
  verify_session_save,
};
use crate::model::{
  AffiliationReplayArtifact, AffiliationRuleset, CompetitiveRuleset, CompetitiveSessionSave,
  Ruleset, SessionSave, hash_competitive_state,
};

pub const GUI_COMPETITIVE_SAVE_SCHEMA_VERSION: &str = "gui-competitive-save-v1";
pub const GUI_STABILIZATION_SAVE_SCHEMA_VERSION: &str = "gui-stabilization-save-v1";
pub const GUI_AFFILIATION_SAVE_SCHEMA_VERSION: &str = "gui-affiliation-save-v1";
const GUI_CHECKPOINT_ARCHIVE_SUFFIX: &str = ".checkpoints";

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct GuiCompetitiveSessionSave {
  pub schema_version: String,
  pub session_id: String,
  pub save: CompetitiveSessionSave,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct GuiStabilizationSessionSave {
  pub schema_version: String,
  pub session_id: String,
  pub save_text: String,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct GuiAffiliationSessionSave {
  pub schema_version: String,
  pub session_id: String,
  pub save_text: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum GuiSessionSave {
  Competitive(CompetitiveSessionSave),
  Stabilization(SessionSave),
  Affiliation(AffiliationReplayArtifact),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GuiCheckpointStorage {
  Archive,
  Legacy,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct GuiSessionCheckpoint {
  pub session_id: String,
  pub storage: GuiCheckpointStorage,
  pub save: GuiSessionSave,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct GuiCheckpointDiscovery {
  pub checkpoints: Vec<GuiSessionCheckpoint>,
  pub invalid_entry_count: usize,
}

pub fn write_competitive_session_save(
  path: &Path,
  session_id: &str,
  save: &CompetitiveSessionSave,
) -> Result<(), String> {
  let wrapper = GuiCompetitiveSessionSave {
    schema_version: GUI_COMPETITIVE_SAVE_SCHEMA_VERSION.to_string(),
    session_id: session_id.to_string(),
    save: save.clone(),
  };
  let text = serde_json::to_string_pretty(&wrapper)
    .map_err(|error| format!("unable to serialize GUI competitive save: {error}"))?;
  write_gui_save_text(path, &text)
}

pub fn write_stabilization_session_save(
  path: &Path,
  session_id: &str,
  save: &SessionSave,
) -> Result<(), String> {
  let wrapper = GuiStabilizationSessionSave {
    schema_version: GUI_STABILIZATION_SAVE_SCHEMA_VERSION.to_string(),
    session_id: session_id.to_string(),
    save_text: serialize_session_save(save),
  };
  let text = serde_json::to_string_pretty(&wrapper)
    .map_err(|error| format!("unable to serialize GUI stabilization save: {error}"))?;
  write_gui_save_text(path, &text)
}

pub fn write_affiliation_session_save(
  path: &Path,
  session_id: &str,
  save: &AffiliationReplayArtifact,
) -> Result<(), String> {
  let wrapper = GuiAffiliationSessionSave {
    schema_version: GUI_AFFILIATION_SAVE_SCHEMA_VERSION.to_string(),
    session_id: session_id.to_string(),
    save_text: serialize_affiliation_replay(save),
  };
  let text = serde_json::to_string_pretty(&wrapper)
    .map_err(|error| format!("unable to serialize GUI affiliation save: {error}"))?;
  write_gui_save_text(path, &text)
}

fn write_gui_save_text(path: &Path, text: &str) -> Result<(), String> {
  let parent = path
    .parent()
    .filter(|parent| !parent.as_os_str().is_empty())
    .ok_or_else(|| format!("GUI save path has no parent: {}", path.display()))?;
  fs::create_dir_all(parent).map_err(|error| {
    format!(
      "unable to create GUI save directory {}: {error}",
      parent.display()
    )
  })?;
  let temporary_path = path.with_file_name(format!(
    ".{}.tmp",
    path
      .file_name()
      .and_then(|name| name.to_str())
      .unwrap_or("competitive-session.save")
  ));
  fs::write(&temporary_path, text).map_err(|error| {
    format!(
      "unable to write temporary GUI save at {}: {error}",
      temporary_path.display()
    )
  })?;
  #[cfg(windows)]
  if path.is_file() {
    fs::remove_file(path)
      .map_err(|error| format!("unable to replace GUI save at {}: {error}", path.display()))?;
  }
  fs::rename(&temporary_path, path)
    .map_err(|error| format!("unable to replace GUI save at {}: {error}", path.display()))
}

pub fn gui_session_checkpoint_path(
  path: &Path,
  session_id: &str,
) -> Result<std::path::PathBuf, String> {
  if session_id.is_empty()
    || !session_id
      .bytes()
      .all(|byte| byte.is_ascii_alphanumeric() || byte == b'-' || byte == b'_')
  {
    return Err(format!(
      "invalid GUI session ID for checkpoint path: '{session_id}'"
    ));
  }
  Ok(gui_checkpoint_archive_dir(path)?.join(format!("{session_id}.save")))
}

fn gui_checkpoint_archive_dir(path: &Path) -> Result<PathBuf, String> {
  let file_name = path
    .file_name()
    .and_then(|name| name.to_str())
    .filter(|name| !name.is_empty())
    .ok_or_else(|| format!("GUI save path has no file name: {}", path.display()))?;
  Ok(path.with_file_name(format!("{file_name}{GUI_CHECKPOINT_ARCHIVE_SUFFIX}")))
}

pub fn load_competitive_session_save(
  path: &Path,
  session_id: &str,
  ruleset: &CompetitiveRuleset,
) -> Result<Option<CompetitiveSessionSave>, String> {
  if !path.is_file() {
    return Ok(None);
  }
  let text = fs::read_to_string(path)
    .map_err(|error| format!("unable to read GUI save at {}: {error}", path.display()))?;
  load_competitive_session_save_text(&text, path, session_id, ruleset)
}

fn load_competitive_session_save_text(
  text: &str,
  path: &Path,
  session_id: &str,
  ruleset: &CompetitiveRuleset,
) -> Result<Option<CompetitiveSessionSave>, String> {
  let wrapper: GuiCompetitiveSessionSave = serde_json::from_str(text)
    .map_err(|error| format!("GUI save parse error at {}: {error}", path.display()))?;
  if wrapper.schema_version != GUI_COMPETITIVE_SAVE_SCHEMA_VERSION {
    return Err(format!(
      "unsupported GUI save schema '{}'",
      wrapper.schema_version
    ));
  }
  if wrapper.session_id != session_id {
    return Ok(None);
  }
  let save = deserialize_competitive_session_save(
    &serialize_competitive_session_save(&wrapper.save),
    ruleset,
  )
  .map_err(|error| {
    format!(
      "invalid GUI competitive save: {}",
      describe_session_save_error(&error)
    )
  })?;
  validate_competitive_save(&save, ruleset)?;
  Ok(Some(save))
}

pub fn load_stabilization_session_save(
  path: &Path,
  session_id: &str,
  ruleset: &Ruleset,
) -> Result<Option<SessionSave>, String> {
  if !path.is_file() {
    return Ok(None);
  }
  let text = fs::read_to_string(path)
    .map_err(|error| format!("unable to read GUI save at {}: {error}", path.display()))?;
  load_stabilization_session_save_text(&text, path, session_id, ruleset)
}

fn load_stabilization_session_save_text(
  text: &str,
  path: &Path,
  session_id: &str,
  ruleset: &Ruleset,
) -> Result<Option<SessionSave>, String> {
  let wrapper: GuiStabilizationSessionSave = serde_json::from_str(text)
    .map_err(|error| format!("GUI save parse error at {}: {error}", path.display()))?;
  if wrapper.schema_version != GUI_STABILIZATION_SAVE_SCHEMA_VERSION {
    return Err(format!(
      "unsupported GUI save schema '{}'",
      wrapper.schema_version
    ));
  }
  if wrapper.session_id != session_id {
    return Ok(None);
  }
  verify_session_save(&wrapper.save_text, ruleset)
    .map(Some)
    .map_err(|error| {
      format!(
        "invalid GUI stabilization save: {}",
        describe_session_save_error(&error)
      )
    })
}

pub fn load_affiliation_session_save(
  path: &Path,
  session_id: &str,
  ruleset: &AffiliationRuleset,
) -> Result<Option<AffiliationReplayArtifact>, String> {
  if !path.is_file() {
    return Ok(None);
  }
  let text = fs::read_to_string(path)
    .map_err(|error| format!("unable to read GUI save at {}: {error}", path.display()))?;
  load_affiliation_session_save_text(&text, path, session_id, ruleset)
}

fn load_affiliation_session_save_text(
  text: &str,
  path: &Path,
  session_id: &str,
  ruleset: &AffiliationRuleset,
) -> Result<Option<AffiliationReplayArtifact>, String> {
  let wrapper: GuiAffiliationSessionSave = serde_json::from_str(text)
    .map_err(|error| format!("GUI save parse error at {}: {error}", path.display()))?;
  if wrapper.schema_version != GUI_AFFILIATION_SAVE_SCHEMA_VERSION {
    return Err(format!(
      "unsupported GUI save schema '{}'",
      wrapper.schema_version
    ));
  }
  if wrapper.session_id != session_id {
    return Ok(None);
  }
  let artifact = deserialize_affiliation_replay(&wrapper.save_text)
    .map_err(|error| format!("invalid GUI affiliation save: {error}"))?;
  verify_affiliation_replay(&wrapper.save_text, ruleset)
    .map_err(|error| format!("invalid GUI affiliation save: {error}"))?;
  Ok(Some(artifact))
}

pub fn load_gui_session_save(
  path: &Path,
  session_id: &str,
  competitive_ruleset: &CompetitiveRuleset,
  stabilization_ruleset: &Ruleset,
  affiliation_ruleset: &AffiliationRuleset,
) -> Result<Option<GuiSessionSave>, String> {
  if !path.is_file() {
    return Ok(None);
  }
  let text = fs::read_to_string(path)
    .map_err(|error| format!("unable to read GUI save at {}: {error}", path.display()))?;
  let value: serde_json::Value = serde_json::from_str(&text)
    .map_err(|error| format!("GUI save parse error at {}: {error}", path.display()))?;
  let schema = value
    .get("schema_version")
    .and_then(serde_json::Value::as_str)
    .ok_or_else(|| format!("GUI save at {} has no schema version", path.display()))?;
  match schema {
    GUI_COMPETITIVE_SAVE_SCHEMA_VERSION => {
      load_competitive_session_save(path, session_id, competitive_ruleset)
        .map(|save| save.map(GuiSessionSave::Competitive))
    }
    GUI_STABILIZATION_SAVE_SCHEMA_VERSION => {
      load_stabilization_session_save(path, session_id, stabilization_ruleset)
        .map(|save| save.map(GuiSessionSave::Stabilization))
    }
    GUI_AFFILIATION_SAVE_SCHEMA_VERSION => {
      load_affiliation_session_save(path, session_id, affiliation_ruleset)
        .map(|save| save.map(GuiSessionSave::Affiliation))
    }
    other => Err(format!("unsupported GUI save schema '{other}'")),
  }
}

fn load_gui_session_save_text(
  text: &str,
  path: &Path,
  session_id: &str,
  competitive_ruleset: &CompetitiveRuleset,
  stabilization_ruleset: &Ruleset,
  affiliation_ruleset: &AffiliationRuleset,
) -> Result<Option<GuiSessionSave>, String> {
  let value: serde_json::Value = serde_json::from_str(text)
    .map_err(|error| format!("GUI save parse error at {}: {error}", path.display()))?;
  let schema = value
    .get("schema_version")
    .and_then(serde_json::Value::as_str)
    .ok_or_else(|| format!("GUI save at {} has no schema version", path.display()))?;
  match schema {
    GUI_COMPETITIVE_SAVE_SCHEMA_VERSION => {
      load_competitive_session_save_text(text, path, session_id, competitive_ruleset)
        .map(|save| save.map(GuiSessionSave::Competitive))
    }
    GUI_STABILIZATION_SAVE_SCHEMA_VERSION => {
      load_stabilization_session_save_text(text, path, session_id, stabilization_ruleset)
        .map(|save| save.map(GuiSessionSave::Stabilization))
    }
    GUI_AFFILIATION_SAVE_SCHEMA_VERSION => {
      load_affiliation_session_save_text(text, path, session_id, affiliation_ruleset)
        .map(|save| save.map(GuiSessionSave::Affiliation))
    }
    other => Err(format!("unsupported GUI save schema '{other}'")),
  }
}

pub fn load_gui_session_checkpoint(
  path: &Path,
  session_id: &str,
  competitive_ruleset: &CompetitiveRuleset,
  stabilization_ruleset: &Ruleset,
  affiliation_ruleset: &AffiliationRuleset,
) -> Result<Option<GuiSessionSave>, String> {
  let archive_dir = gui_checkpoint_archive_dir(path)?;
  let checkpoint_path = gui_session_checkpoint_path(path, session_id)?;
  let archive_is_real_directory = fs::symlink_metadata(&archive_dir)
    .map(|metadata| metadata.is_dir() && !metadata.file_type().is_symlink())
    .unwrap_or(false);
  if archive_is_real_directory
    && let Ok(metadata) = fs::symlink_metadata(&checkpoint_path)
    && metadata.is_file()
    && let Ok(Some(save)) = load_gui_session_save(
      &checkpoint_path,
      session_id,
      competitive_ruleset,
      stabilization_ruleset,
      affiliation_ruleset,
    )
  {
    return Ok(Some(save));
  }
  load_gui_session_save(
    path,
    session_id,
    competitive_ruleset,
    stabilization_ruleset,
    affiliation_ruleset,
  )
}

pub fn read_gui_session_checkpoint_artifact(
  path: &Path,
  session_id: &str,
  storage: GuiCheckpointStorage,
  competitive_ruleset: &CompetitiveRuleset,
  stabilization_ruleset: &Ruleset,
  affiliation_ruleset: &AffiliationRuleset,
) -> Result<Option<Vec<u8>>, String> {
  let candidate = match storage {
    GuiCheckpointStorage::Archive => gui_session_checkpoint_path(path, session_id)?,
    GuiCheckpointStorage::Legacy => path.to_path_buf(),
  };
  let metadata = match fs::symlink_metadata(&candidate) {
    Ok(metadata) => metadata,
    Err(error) if error.kind() == std::io::ErrorKind::NotFound => return Ok(None),
    Err(error) => {
      return Err(format!(
        "unable to inspect GUI checkpoint artifact {}: {error}",
        candidate.display()
      ));
    }
  };
  if metadata.file_type().is_symlink() || !metadata.is_file() {
    return Err(format!(
      "GUI checkpoint artifact is not a regular file: {}",
      candidate.display()
    ));
  }
  let bytes = fs::read(&candidate).map_err(|error| {
    format!(
      "unable to read GUI checkpoint artifact {}: {error}",
      candidate.display()
    )
  })?;
  let text = std::str::from_utf8(&bytes).map_err(|error| {
    format!(
      "GUI checkpoint artifact is not valid UTF-8 at {}: {error}",
      candidate.display()
    )
  })?;
  if load_gui_session_save_text(
    text,
    &candidate,
    session_id,
    competitive_ruleset,
    stabilization_ruleset,
    affiliation_ruleset,
  )?
  .is_none()
  {
    return Ok(None);
  }
  Ok(Some(bytes))
}

pub fn discover_gui_session_checkpoints(
  path: &Path,
  competitive_ruleset: &CompetitiveRuleset,
  stabilization_ruleset: &Ruleset,
  affiliation_ruleset: &AffiliationRuleset,
) -> Result<GuiCheckpointDiscovery, String> {
  let archive_dir = gui_checkpoint_archive_dir(path)?;
  let mut checkpoints = Vec::new();
  let mut archive_session_ids = BTreeSet::new();
  let mut invalid_entry_count = 0;

  match fs::symlink_metadata(&archive_dir) {
    Ok(metadata) if metadata.is_dir() && !metadata.file_type().is_symlink() => {
      for entry in fs::read_dir(&archive_dir).map_err(|error| {
        format!(
          "unable to read GUI checkpoint archive {}: {error}",
          archive_dir.display()
        )
      })? {
        let entry = entry.map_err(|error| {
          format!(
            "unable to inspect GUI checkpoint archive {}: {error}",
            archive_dir.display()
          )
        })?;
        let candidate = entry.path();
        let metadata = match fs::symlink_metadata(&candidate) {
          Ok(metadata) => metadata,
          Err(_) => {
            invalid_entry_count += 1;
            continue;
          }
        };
        let is_symlink = metadata.file_type().is_symlink();
        let is_file = metadata.is_file();
        if candidate.extension().and_then(|value| value.to_str()) != Some("save") {
          if is_file || is_symlink {
            invalid_entry_count += 1;
          }
          continue;
        }
        let Some(session_id) = candidate.file_stem().and_then(|value| value.to_str()) else {
          invalid_entry_count += 1;
          continue;
        };
        let Ok(expected_path) = gui_session_checkpoint_path(path, session_id) else {
          invalid_entry_count += 1;
          continue;
        };
        if expected_path != candidate {
          invalid_entry_count += 1;
          continue;
        }
        archive_session_ids.insert(session_id.to_string());
        if is_symlink {
          invalid_entry_count += 1;
          continue;
        }
        if !is_file {
          continue;
        }
        match load_gui_session_save(
          &candidate,
          session_id,
          competitive_ruleset,
          stabilization_ruleset,
          affiliation_ruleset,
        ) {
          Ok(Some(save)) => {
            checkpoints.push(GuiSessionCheckpoint {
              session_id: session_id.to_string(),
              storage: GuiCheckpointStorage::Archive,
              save,
            });
          }
          Ok(None) | Err(_) => invalid_entry_count += 1,
        }
      }
    }
    Ok(metadata) if metadata.file_type().is_symlink() || metadata.is_file() => {
      invalid_entry_count += 1;
    }
    Ok(_) => {}
    Err(error) if error.kind() != std::io::ErrorKind::NotFound => {
      return Err(format!(
        "unable to inspect GUI checkpoint archive {}: {error}",
        archive_dir.display()
      ));
    }
    Err(_) => {}
  }

  if path.is_file() {
    let legacy_id = fs::read_to_string(path)
      .ok()
      .and_then(|text| serde_json::from_str::<serde_json::Value>(&text).ok())
      .and_then(|value| {
        value
          .get("session_id")
          .and_then(serde_json::Value::as_str)
          .map(str::to_string)
      });
    if let Some(session_id) = legacy_id {
      if gui_session_checkpoint_path(path, &session_id).is_err() {
        invalid_entry_count += 1;
      } else if !archive_session_ids.contains(&session_id) {
        match load_gui_session_save(
          path,
          &session_id,
          competitive_ruleset,
          stabilization_ruleset,
          affiliation_ruleset,
        ) {
          Ok(Some(save)) => checkpoints.push(GuiSessionCheckpoint {
            session_id,
            storage: GuiCheckpointStorage::Legacy,
            save,
          }),
          Ok(None) | Err(_) => invalid_entry_count += 1,
        }
      }
    } else {
      invalid_entry_count += 1;
    }
  }

  checkpoints.sort_by(|left, right| left.session_id.cmp(&right.session_id));
  Ok(GuiCheckpointDiscovery {
    checkpoints,
    invalid_entry_count,
  })
}

#[derive(Debug)]
enum GuiSessionSaveRemovalError {
  Io(String),
  InvalidContent(String),
}

impl std::fmt::Display for GuiSessionSaveRemovalError {
  fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
    match self {
      Self::Io(message) | Self::InvalidContent(message) => formatter.write_str(message),
    }
  }
}

fn remove_gui_session_save(
  path: &Path,
  session_id: &str,
) -> Result<(), GuiSessionSaveRemovalError> {
  if !path.is_file() {
    return Ok(());
  }
  let text = fs::read_to_string(path).map_err(|error| {
    GuiSessionSaveRemovalError::Io(format!(
      "unable to read GUI save at {}: {error}",
      path.display()
    ))
  })?;
  let value: serde_json::Value = serde_json::from_str(&text).map_err(|error| {
    GuiSessionSaveRemovalError::InvalidContent(format!(
      "GUI save parse error at {}: {error}",
      path.display()
    ))
  })?;
  let schema = value
    .get("schema_version")
    .and_then(serde_json::Value::as_str)
    .ok_or_else(|| {
      GuiSessionSaveRemovalError::InvalidContent(format!(
        "GUI save at {} has no schema version",
        path.display()
      ))
    })?;
  let stored_session_id = value
    .get("session_id")
    .and_then(serde_json::Value::as_str)
    .ok_or_else(|| {
      GuiSessionSaveRemovalError::InvalidContent(format!(
        "GUI save at {} has no session ID",
        path.display()
      ))
    })?;
  if stored_session_id == session_id
    && matches!(
      schema,
      GUI_COMPETITIVE_SAVE_SCHEMA_VERSION
        | GUI_STABILIZATION_SAVE_SCHEMA_VERSION
        | GUI_AFFILIATION_SAVE_SCHEMA_VERSION
    )
  {
    fs::remove_file(path).map_err(|error| {
      GuiSessionSaveRemovalError::Io(format!(
        "unable to remove GUI save at {}: {error}",
        path.display()
      ))
    })?;
  }
  Ok(())
}

pub fn remove_gui_session_checkpoint(path: &Path, session_id: &str) -> Result<(), String> {
  let checkpoint_path = gui_session_checkpoint_path(path, session_id)?;
  if let Err(error) = remove_gui_session_save(path, session_id) {
    match error {
      GuiSessionSaveRemovalError::InvalidContent(error) if path.is_file() => {
        fs::remove_file(path).map_err(|remove_error| {
          format!(
            "unable to remove invalid legacy GUI save at {}: {remove_error} (original cleanup error: {error})",
            path.display()
          )
        })?;
      }
      GuiSessionSaveRemovalError::Io(error) => return Err(error),
      GuiSessionSaveRemovalError::InvalidContent(error) => return Err(error),
    }
  }
  if checkpoint_path.is_file() {
    fs::remove_file(&checkpoint_path).map_err(|error| {
      format!(
        "unable to remove GUI checkpoint at {}: {error}",
        checkpoint_path.display()
      )
    })?;
  }
  if let Some(archive_dir) = checkpoint_path.parent()
    && let Err(error) = fs::remove_dir(archive_dir)
    && !matches!(
      error.kind(),
      std::io::ErrorKind::NotFound | std::io::ErrorKind::DirectoryNotEmpty
    )
  {
    return Err(format!(
      "unable to remove empty GUI checkpoint archive {}: {error}",
      archive_dir.display()
    ));
  }
  Ok(())
}

fn validate_competitive_save(
  save: &CompetitiveSessionSave,
  ruleset: &CompetitiveRuleset,
) -> Result<(), String> {
  let mut expected_prior_turn = save.history.genesis.turn;
  let mut final_state = &save.history.genesis;
  for transition in &save.history.transitions {
    let mut expected_prior = final_state.clone();
    let month_index = expected_prior.policy_calendar.month_index;
    let inputs = crate::inputs::resolve_competitive_inputs(
      save.seed,
      month_index,
      expected_prior.policy_calendar.is_annual_tick(),
    );
    let mut events = Vec::new();
    crate::sim::apply_month_start_tick(&mut expected_prior, &inputs, &mut events);
    if transition.prior != expected_prior {
      return Err(format!(
        "invalid GUI competitive save: transition prior state does not match the deterministic month-start state at turn {}",
        transition.prior.turn
      ));
    }
    if transition.prior.turn != expected_prior_turn {
      return Err(format!(
        "invalid GUI competitive save: transition prior turn {} does not match expected turn {}",
        transition.prior.turn, expected_prior_turn
      ));
    }
    if transition.aggregated.month_index != transition.prior.policy_calendar.month_index {
      return Err(format!(
        "invalid GUI competitive save: aggregated actions month {} does not match prior month {}",
        transition.aggregated.month_index, transition.prior.policy_calendar.month_index
      ));
    }
    if transition.next.turn != transition.prior.turn + 1 {
      return Err(format!(
        "invalid GUI competitive save: transition next turn {} is not one month after prior turn {}",
        transition.next.turn, transition.prior.turn
      ));
    }
    if transition.next.policy_calendar.month_index
      != transition.prior.policy_calendar.month_index + 1
    {
      return Err(format!(
        "invalid GUI competitive save: transition next month {} does not follow prior month {}",
        transition.next.policy_calendar.month_index, transition.prior.policy_calendar.month_index
      ));
    }
    let expected_hash = hash_competitive_state(&transition.next, ruleset);
    if transition.state_hash != expected_hash {
      return Err(format!(
        "invalid GUI competitive save: state hash mismatch at turn {}",
        transition.next.turn
      ));
    }
    expected_prior_turn = transition.next.turn;
    final_state = &transition.next;
  }
  if save.next_month != final_state.policy_calendar.month_index {
    return Err(format!(
      "invalid GUI competitive save: next month {} does not match current month {}",
      save.next_month, final_state.policy_calendar.month_index
    ));
  }
  crate::competitive::regenerate_competitive_history(&save.history, ruleset, save.seed)
    .map_err(|error| format!("invalid GUI competitive save: {}", error.message()))?;
  Ok(())
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::{build_multi_month_resolution_history, genesis_competitive_world};
  use crate::model::{
    AFFILIATION_REPLAY_ARTIFACT_VERSION, AffiliationHistory, CompetitiveHistory, Difficulty,
    ExperienceMode, History, default_affiliation_ruleset, default_competitive_ruleset,
    default_ruleset, genesis_state,
  };
  use crate::scenario::default_regional_affiliation_scenario;
  #[cfg(unix)]
  use std::os::unix::fs::symlink;

  #[test]
  fn gui_save_round_trip_requires_matching_opaque_session_id() {
    let directory =
      std::env::temp_dir().join(format!("hs-mgt-game-gui-save-{}", std::process::id()));
    let path = directory.join("competitive.save");
    let ruleset = default_competitive_ruleset();
    let save = CompetitiveSessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      difficulty: Difficulty::Normal,
      history: CompetitiveHistory {
        genesis: genesis_competitive_world(Difficulty::Normal),
        transitions: Vec::new(),
      },
      next_month: 1,
    };

    write_competitive_session_save(&path, "session-7", &save).expect("write GUI save");
    let missing =
      load_competitive_session_save(&path, "session-8", &ruleset).expect("mismatched ID read");
    assert!(missing.is_none());
    let restored = load_competitive_session_save(&path, "session-7", &ruleset)
      .expect("matching ID read")
      .expect("matching save");
    assert_eq!(restored.seed, 42);
    assert_eq!(restored.next_month, 1);

    remove_gui_session_save(&path, "session-8").expect("mismatched ID removal");
    assert!(path.is_file());
    remove_gui_session_save(&path, "session-7").expect("matching ID removal");
    assert!(!path.exists());
    let _ = fs::remove_file(&path);
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn gui_checkpoint_archive_keeps_session_files_independent() {
    let directory =
      std::env::temp_dir().join(format!("hs-mgt-game-gui-archive-{}", std::process::id()));
    let path = directory.join("gui.save");
    let ruleset = default_ruleset();
    let first = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    let mut second = first.clone();
    second.seed = 43;
    let first_path = gui_session_checkpoint_path(&path, "session-1").expect("first path");
    let second_path = gui_session_checkpoint_path(&path, "session-2").expect("second path");
    write_stabilization_session_save(&first_path, "session-1", &first).expect("first checkpoint");
    write_stabilization_session_save(&second_path, "session-2", &second)
      .expect("second checkpoint");
    assert_ne!(first_path, second_path);
    assert!(first_path.is_file());
    assert!(second_path.is_file());

    let restored_first = load_gui_session_checkpoint(
      &path,
      "session-1",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("first archive read")
    .expect("first archive");
    let restored_second = load_gui_session_checkpoint(
      &path,
      "session-2",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("second archive read")
    .expect("second archive");
    let GuiSessionSave::Stabilization(restored_first) = restored_first else {
      panic!("first archive campaign");
    };
    let GuiSessionSave::Stabilization(restored_second) = restored_second else {
      panic!("second archive campaign");
    };
    assert_eq!(restored_first.seed, 42);
    assert_eq!(restored_second.seed, 43);

    remove_gui_session_checkpoint(&path, "session-1").expect("remove first checkpoint");
    assert!(!first_path.exists());
    assert!(second_path.is_file());
    remove_gui_session_checkpoint(&path, "session-2").expect("remove second checkpoint");
    assert!(!second_path.exists());
    assert!(!path.with_file_name("gui.save.checkpoints").exists());
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn checkpoint_discovery_orders_valid_entries_and_skips_invalid_files() {
    let directory =
      std::env::temp_dir().join(format!("hs-mgt-game-gui-discovery-{}", std::process::id()));
    let path = directory.join("gui.save");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(
      &gui_session_checkpoint_path(&path, "session-2").expect("session 2 path"),
      "session-2",
      &save,
    )
    .expect("archive session 2");
    write_stabilization_session_save(
      &gui_session_checkpoint_path(&path, "session-1").expect("session 1 path"),
      "session-1",
      &save,
    )
    .expect("archive session 1");
    let archive_dir = gui_checkpoint_archive_dir(&path).expect("archive directory");
    fs::write(archive_dir.join("invalid.save"), "{not-json").expect("invalid archive entry");
    fs::write(archive_dir.join("unsupported.txt"), "not a checkpoint")
      .expect("unsupported archive entry");
    write_stabilization_session_save(&path, "session-0", &save).expect("legacy session");

    let discovery = discover_gui_session_checkpoints(
      &path,
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("checkpoint discovery");
    assert_eq!(discovery.invalid_entry_count, 2);
    assert_eq!(
      discovery
        .checkpoints
        .iter()
        .map(|checkpoint| checkpoint.session_id.as_str())
        .collect::<Vec<_>>(),
      ["session-0", "session-1", "session-2"]
    );
    assert_eq!(
      discovery.checkpoints[0].storage,
      GuiCheckpointStorage::Legacy
    );
    assert!(
      discovery
        .checkpoints
        .iter()
        .skip(1)
        .all(|checkpoint| checkpoint.storage == GuiCheckpointStorage::Archive)
    );

    remove_gui_session_checkpoint(&path, "session-0").expect("remove legacy session");
    remove_gui_session_checkpoint(&path, "session-1").expect("remove archive session 1");
    remove_gui_session_checkpoint(&path, "session-2").expect("remove archive session 2");
    fs::remove_file(archive_dir.join("invalid.save")).expect("remove invalid entry");
    fs::remove_file(archive_dir.join("unsupported.txt")).expect("remove unsupported entry");
    let _ = fs::remove_dir(&archive_dir);
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn malformed_archive_shadows_discovery_but_load_falls_back_to_legacy() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-discovery-collision-{}",
      std::process::id()
    ));
    let path = directory.join("gui.save");
    let archive_path =
      gui_session_checkpoint_path(&path, "session-collision").expect("collision archive path");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(&archive_path, "session-collision", &save)
      .expect("archive checkpoint");
    write_stabilization_session_save(&path, "session-collision", &save).expect("legacy checkpoint");
    fs::write(&archive_path, "{not-json").expect("malformed archive checkpoint");

    let discovery = discover_gui_session_checkpoints(
      &path,
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("checkpoint discovery");
    assert_eq!(discovery.invalid_entry_count, 1);
    assert!(discovery.checkpoints.is_empty());
    let restored = load_gui_session_checkpoint(
      &path,
      "session-collision",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("legacy fallback load")
    .expect("legacy checkpoint");
    assert!(matches!(restored, GuiSessionSave::Stabilization(_)));

    fs::remove_file(&archive_path).expect("remove malformed archive");
    remove_gui_session_save(&path, "session-collision").expect("remove legacy checkpoint");
    let _ = fs::remove_dir(archive_path.parent().expect("archive directory"));
    let _ = fs::remove_dir(&directory);
  }

  #[cfg(unix)]
  #[test]
  fn checkpoint_discovery_rejects_archive_symlinks() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-discovery-symlink-{}",
      std::process::id()
    ));
    let external_directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-discovery-external-{}",
      std::process::id()
    ));
    let path = directory.join("gui.save");
    let external_path = external_directory.join("external.save");
    let link_path =
      gui_session_checkpoint_path(&path, "session-link").expect("symlink archive path");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(&external_path, "session-link", &save)
      .expect("external checkpoint");
    write_stabilization_session_save(&path, "session-link", &save).expect("legacy checkpoint");
    fs::create_dir_all(link_path.parent().expect("archive directory"))
      .expect("create archive directory");
    symlink(&external_path, &link_path).expect("archive symlink");

    let discovery = discover_gui_session_checkpoints(
      &path,
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("checkpoint discovery");
    assert_eq!(discovery.invalid_entry_count, 1);
    assert!(discovery.checkpoints.is_empty());
    let restored = load_gui_session_checkpoint(
      &path,
      "session-link",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("legacy fallback load")
    .expect("legacy checkpoint");
    assert!(matches!(restored, GuiSessionSave::Stabilization(_)));

    fs::remove_file(&link_path).expect("remove archive symlink");
    fs::remove_file(&external_path).expect("remove external checkpoint");
    remove_gui_session_save(&path, "session-link").expect("remove legacy checkpoint");
    let _ = fs::remove_dir(link_path.parent().expect("archive directory"));
    let _ = fs::remove_dir(&directory);
    let _ = fs::remove_dir(&external_directory);
  }

  #[cfg(unix)]
  #[test]
  fn checkpoint_discovery_rejects_archive_directory_symlinks() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-discovery-directory-symlink-{}",
      std::process::id()
    ));
    let external_directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-discovery-directory-external-{}",
      std::process::id()
    ));
    let path = directory.join("gui.save");
    let archive_dir = gui_checkpoint_archive_dir(&path).expect("archive directory");
    let external_archive_dir = external_directory.join("external.checkpoints");
    let session_id = "session-directory-link";
    let external_path = external_archive_dir.join(format!("{session_id}.save"));
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(&external_path, session_id, &save)
      .expect("external checkpoint");
    write_stabilization_session_save(&path, session_id, &save).expect("legacy checkpoint");
    symlink(&external_archive_dir, &archive_dir).expect("archive directory symlink");

    let discovery = discover_gui_session_checkpoints(
      &path,
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("checkpoint discovery");
    assert_eq!(discovery.invalid_entry_count, 1);
    assert_eq!(discovery.checkpoints.len(), 1);
    assert_eq!(discovery.checkpoints[0].session_id, session_id);
    assert_eq!(
      discovery.checkpoints[0].storage,
      GuiCheckpointStorage::Legacy
    );
    let restored = load_gui_session_checkpoint(
      &path,
      session_id,
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("legacy fallback load")
    .expect("legacy checkpoint");
    assert!(matches!(restored, GuiSessionSave::Stabilization(_)));

    fs::remove_file(&archive_dir).expect("remove archive directory symlink");
    fs::remove_file(&external_path).expect("remove external checkpoint");
    remove_gui_session_save(&path, session_id).expect("remove legacy checkpoint");
    let _ = fs::remove_dir(&external_archive_dir);
    let _ = fs::remove_dir(&external_directory);
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn legacy_single_file_checkpoint_remains_a_read_fallback() {
    let directory =
      std::env::temp_dir().join(format!("hs-mgt-game-gui-legacy-{}", std::process::id()));
    let path = directory.join("gui.save");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(&path, "session-legacy", &save).expect("legacy checkpoint");
    let restored = load_gui_session_checkpoint(
      &path,
      "session-legacy",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("legacy checkpoint read")
    .expect("legacy checkpoint");
    assert!(matches!(restored, GuiSessionSave::Stabilization(_)));
    remove_gui_session_checkpoint(&path, "session-legacy").expect("remove legacy checkpoint");
    assert!(!path.exists());
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn malformed_legacy_checkpoint_does_not_block_archive_cleanup() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-legacy-invalid-{}",
      std::process::id()
    ));
    let path = directory.join("gui.save");
    let checkpoint_path = gui_session_checkpoint_path(&path, "session-invalid")
      .expect("invalid legacy test checkpoint path");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(&checkpoint_path, "session-invalid", &save)
      .expect("archive checkpoint");
    fs::write(&path, "{not-json").expect("malformed legacy checkpoint");

    remove_gui_session_checkpoint(&path, "session-invalid")
      .expect("malformed legacy residue must not block cleanup");
    assert!(!path.exists());
    assert!(!checkpoint_path.exists());
    assert!(
      !checkpoint_path
        .parent()
        .expect("archive directory")
        .exists()
    );
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn checkpoint_cleanup_preserves_valid_legacy_checkpoint_for_other_session() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-legacy-other-{}",
      std::process::id()
    ));
    let path = directory.join("gui.save");
    let checkpoint_path =
      gui_session_checkpoint_path(&path, "session-target").expect("target checkpoint path");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    write_stabilization_session_save(&checkpoint_path, "session-target", &save)
      .expect("archive checkpoint");
    write_stabilization_session_save(&path, "session-other", &save)
      .expect("other legacy checkpoint");

    remove_gui_session_checkpoint(&path, "session-target")
      .expect("target cleanup must preserve other legacy checkpoint");
    assert!(!checkpoint_path.exists());
    assert!(path.is_file());
    remove_gui_session_save(&path, "session-other").expect("other legacy cleanup");
    assert!(!path.exists());
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn checkpoint_archive_rejects_path_unsafe_session_ids() {
    let path = std::env::temp_dir().join("hs-mgt-game-gui-safe-id.save");
    let error = gui_session_checkpoint_path(&path, "../escape").expect_err("unsafe ID");
    assert!(error.contains("invalid GUI session ID"));
    let _ = fs::remove_file(path);
  }

  #[test]
  fn malformed_gui_save_fails_closed() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-malformed-save-{}.save",
      std::process::id()
    ));
    fs::write(&path, "{not-json").expect("malformed save");
    let error = load_competitive_session_save(&path, "session-7", &default_competitive_ruleset())
      .expect_err("malformed save must fail closed");
    assert!(error.contains("GUI save parse error"));
    let _ = fs::remove_file(&path);
  }

  #[test]
  fn invalid_history_linkage_fails_closed() {
    let ruleset = default_competitive_ruleset();
    let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 2)
      .expect("build competitive history");
    let mut prior_mismatch = CompetitiveSessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      difficulty: Difficulty::Normal,
      history: history.clone(),
      next_month: 3,
    };
    prior_mismatch.history.transitions[1]
      .prior
      .market
      .regional_demand_index += 1;
    let prior_error = validate_competitive_save(&prior_mismatch, &ruleset)
      .expect_err("disconnected prior state must fail");
    assert!(prior_error.contains("deterministic month-start state"));

    let mut month_mismatch = CompetitiveSessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      difficulty: Difficulty::Normal,
      history,
      next_month: 3,
    };
    month_mismatch.history.transitions[0].aggregated.month_index += 1;
    let month_error = validate_competitive_save(&month_mismatch, &ruleset)
      .expect_err("misdated aggregated actions must fail");
    assert!(month_error.contains("aggregated actions month"));
  }

  #[test]
  fn tampered_competitive_effect_fails_replay_regeneration() {
    let ruleset = default_competitive_ruleset();
    let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 2)
      .expect("build competitive history");
    let mut save = CompetitiveSessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      difficulty: Difficulty::Normal,
      history,
      next_month: 3,
    };
    save.history.transitions[1].effects[0].delta += 1;

    let error = validate_competitive_save(&save, &ruleset).expect_err("tampered effect");
    assert!(error.contains("replay transition mismatch"));
  }

  #[test]
  fn stabilization_save_round_trip_requires_matching_opaque_session_id() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-stabilization-{}",
      std::process::id()
    ));
    let path = directory.join("stabilization.save");
    let ruleset = default_ruleset();
    let save = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };

    write_stabilization_session_save(&path, "session-7", &save).expect("write GUI save");
    let missing = load_gui_session_save(
      &path,
      "session-8",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("mismatched ID read");
    assert!(missing.is_none());
    let restored = load_gui_session_save(
      &path,
      "session-7",
      &default_competitive_ruleset(),
      &ruleset,
      &default_affiliation_ruleset(),
    )
    .expect("matching ID read")
    .expect("matching save");
    assert!(matches!(restored, GuiSessionSave::Stabilization(_)));

    remove_gui_session_save(&path, "session-8").expect("mismatched ID removal");
    assert!(path.is_file());
    remove_gui_session_save(&path, "session-7").expect("matching ID removal");
    assert!(!path.exists());
    let _ = fs::remove_file(&path);
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn stabilization_save_replaces_the_latest_checkpoint() {
    let directory =
      std::env::temp_dir().join(format!("hs-mgt-game-gui-replace-{}", std::process::id()));
    let path = directory.join("stabilization.save");
    let ruleset = default_ruleset();
    let first = SessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };
    let mut second = first.clone();
    second.seed = 43;
    write_stabilization_session_save(&path, "session-7", &first).expect("first write");
    write_stabilization_session_save(&path, "session-7", &second).expect("replacement write");
    let restored = load_stabilization_session_save(&path, "session-7", &ruleset)
      .expect("replacement read")
      .expect("replacement save");
    assert_eq!(restored.seed, 43);
    let _ = fs::remove_file(&path);
    let _ = fs::remove_dir(&directory);
  }

  #[test]
  fn affiliation_save_round_trip_verifies_replay_and_requires_matching_opaque_session_id() {
    let directory = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-affiliation-{}",
      std::process::id()
    ));
    let path = directory.join("affiliation.save");
    let ruleset = default_affiliation_ruleset();
    let genesis = default_regional_affiliation_scenario()
      .expect("affiliation scenario")
      .initial_affiliation_world_state()
      .expect("affiliation genesis");
    let save = AffiliationReplayArtifact {
      artifact_version: AFFILIATION_REPLAY_ARTIFACT_VERSION.to_string(),
      seed: 42,
      ruleset_version: ruleset.version.to_string(),
      history: AffiliationHistory {
        genesis,
        transitions: Vec::new(),
      },
    };

    write_affiliation_session_save(&path, "session-7", &save).expect("write GUI save");
    let missing = load_gui_session_save(
      &path,
      "session-8",
      &default_competitive_ruleset(),
      &default_ruleset(),
      &ruleset,
    )
    .expect("mismatched ID read");
    assert!(missing.is_none());
    let restored = load_gui_session_save(
      &path,
      "session-7",
      &default_competitive_ruleset(),
      &default_ruleset(),
      &ruleset,
    )
    .expect("matching ID read")
    .expect("matching save");
    assert!(matches!(restored, GuiSessionSave::Affiliation(_)));

    remove_gui_session_save(&path, "session-8").expect("mismatched ID removal");
    assert!(path.is_file());
    remove_gui_session_save(&path, "session-7").expect("matching ID removal");
    assert!(!path.exists());
    let _ = fs::remove_file(&path);
    let _ = fs::remove_dir(&directory);
  }
}
