use crate::artifact::session_save::{deserialize_session_save, verify_session_save};
use crate::artifact::session_save_serialize::{SESSION_SAVE_VERSION, serialize_session_save};
use crate::model::{ExperienceMode, History, SessionSave, default_ruleset, genesis_state};
use crate::test_support::demo_history;

#[test]
fn round_trip_partial_session_save() {
  let ruleset = default_ruleset();
  let full_history = demo_history();
  let partial = History {
    genesis: full_history.genesis.clone(),
    transitions: full_history.transitions[..2].to_vec(),
  };

  let save = SessionSave {
    ruleset_version: ruleset.version.to_string(),
    seed: 42,
    experience_mode: ExperienceMode::Beginner,
    history: partial.clone(),
    next_turn: 3,
  };

  let text = serialize_session_save(&save);
  assert!(text.starts_with(SESSION_SAVE_VERSION));

  let restored = deserialize_session_save(&text).unwrap();
  assert_eq!(restored.seed, 42);
  assert_eq!(restored.next_turn, 3);
  assert_eq!(restored.experience_mode, ExperienceMode::Beginner);
  assert_eq!(restored.history.transitions.len(), 2);

  verify_session_save(&text, &ruleset).unwrap();
}

#[test]
fn unsupported_version_is_rejected() {
  let text = "session-save-0.0.0\nruleset=demo\nseed=1\nexperience_mode=standard\nnext_turn=1\ngenesis=turn:0,cash:100,staffed_beds:120,access_index:70,quality_index:72,workforce_trust:68,community_trust:71,commercial_rate:100,policy_pressure:35\ntransition_count=0";
  let error = deserialize_session_save(text).unwrap_err();
  assert!(matches!(
    error,
    crate::model::SessionSaveError::UnsupportedVersion { .. }
  ));
}

#[test]
fn ruleset_mismatch_is_rejected() {
  let save = SessionSave {
    ruleset_version: "wrong-ruleset".to_string(),
    seed: 42,
    experience_mode: ExperienceMode::Standard,
    history: History {
      genesis: genesis_state(),
      transitions: Vec::new(),
    },
    next_turn: 1,
  };

  let text = serialize_session_save(&save);
  let ruleset = default_ruleset();
  let error = verify_session_save(&text, &ruleset).unwrap_err();
  assert!(matches!(
    error,
    crate::model::SessionSaveError::RulesetMismatch { .. }
  ));
}
