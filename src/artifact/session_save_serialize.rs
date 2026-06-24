use crate::model::{ExperienceMode, SessionSave};

use super::serialize::{serialize_transition, serialize_world_state};

pub const SESSION_SAVE_VERSION: &str = "session-save-0.1.27";

pub fn serialize_experience_mode(mode: ExperienceMode) -> &'static str {
  match mode {
    ExperienceMode::Standard => "standard",
    ExperienceMode::Beginner => "beginner",
  }
}

pub fn serialize_session_save(save: &SessionSave) -> String {
  let mut lines = vec![
    SESSION_SAVE_VERSION.to_string(),
    format!("ruleset={}", save.ruleset_version),
    format!("seed={}", save.seed),
    format!(
      "experience_mode={}",
      serialize_experience_mode(save.experience_mode)
    ),
    format!("next_turn={}", save.next_turn),
    serialize_world_state("genesis", &save.history.genesis),
    format!("transition_count={}", save.history.transitions.len()),
  ];

  for transition in &save.history.transitions {
    lines.extend(serialize_transition(transition));
  }

  lines.join("\n")
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{History, genesis_state};

  #[test]
  fn serialize_includes_version_and_next_turn() {
    let save = SessionSave {
      ruleset_version: "0.1.0".to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Beginner,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };

    let text = serialize_session_save(&save);
    assert!(text.starts_with(SESSION_SAVE_VERSION));
    assert!(text.contains("experience_mode=beginner"));
    assert!(text.contains("next_turn=1"));
    assert!(text.contains("transition_count=0"));
  }
}
