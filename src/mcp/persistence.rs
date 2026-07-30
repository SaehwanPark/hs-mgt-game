use std::fs;
use std::path::Path;

use serde::{Deserialize, Serialize};

use crate::artifact::{
  describe_session_save_error, deserialize_competitive_session_save,
  serialize_competitive_session_save, serialize_session_save, verify_session_save,
};
use crate::model::{
  CompetitiveRuleset, CompetitiveSessionSave, Ruleset, SessionSave, hash_competitive_state,
};

pub const GUI_COMPETITIVE_SAVE_SCHEMA_VERSION: &str = "gui-competitive-save-v1";
pub const GUI_STABILIZATION_SAVE_SCHEMA_VERSION: &str = "gui-stabilization-save-v1";

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

#[derive(Clone, Debug)]
pub enum GuiSessionSave {
  Competitive(CompetitiveSessionSave),
  Stabilization(SessionSave),
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
  let wrapper: GuiCompetitiveSessionSave = serde_json::from_str(&text)
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
  let wrapper: GuiStabilizationSessionSave = serde_json::from_str(&text)
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

pub fn load_gui_session_save(
  path: &Path,
  session_id: &str,
  competitive_ruleset: &CompetitiveRuleset,
  stabilization_ruleset: &Ruleset,
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
    other => Err(format!("unsupported GUI save schema '{other}'")),
  }
}

pub fn remove_gui_session_save(path: &Path, session_id: &str) -> Result<(), String> {
  if !path.is_file() {
    return Ok(());
  }
  let text = fs::read_to_string(path)
    .map_err(|error| format!("unable to read GUI save at {}: {error}", path.display()))?;
  let value: serde_json::Value = serde_json::from_str(&text)
    .map_err(|error| format!("GUI save parse error at {}: {error}", path.display()))?;
  let schema = value
    .get("schema_version")
    .and_then(serde_json::Value::as_str)
    .ok_or_else(|| format!("GUI save at {} has no schema version", path.display()))?;
  let stored_session_id = value
    .get("session_id")
    .and_then(serde_json::Value::as_str)
    .ok_or_else(|| format!("GUI save at {} has no session ID", path.display()))?;
  if stored_session_id == session_id
    && matches!(
      schema,
      GUI_COMPETITIVE_SAVE_SCHEMA_VERSION | GUI_STABILIZATION_SAVE_SCHEMA_VERSION
    )
  {
    fs::remove_file(path)
      .map_err(|error| format!("unable to remove GUI save at {}: {error}", path.display()))?;
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
  Ok(())
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::{build_multi_month_resolution_history, genesis_competitive_world};
  use crate::model::{
    CompetitiveHistory, Difficulty, ExperienceMode, History, default_competitive_ruleset,
    default_ruleset, genesis_state,
  };

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
    let missing =
      load_gui_session_save(&path, "session-8", &default_competitive_ruleset(), &ruleset)
        .expect("mismatched ID read");
    assert!(missing.is_none());
    let restored =
      load_gui_session_save(&path, "session-7", &default_competitive_ruleset(), &ruleset)
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
}
