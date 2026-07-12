use crate::model::{CompetitiveRuleset, CompetitiveSessionSave, SessionSaveError};

pub fn serialize_competitive_session_save(save: &CompetitiveSessionSave) -> String {
  serde_json::to_string_pretty(save).unwrap_or_default()
}

pub fn deserialize_competitive_session_save(
  text: &str,
  ruleset: &CompetitiveRuleset,
) -> Result<CompetitiveSessionSave, SessionSaveError> {
  let mut save: CompetitiveSessionSave =
    serde_json::from_str(text).map_err(|error| SessionSaveError::ParseError {
      line: 0,
      detail: format!("JSON parse error: {error}"),
    })?;

  if save.ruleset_version != ruleset.version {
    return Err(SessionSaveError::RulesetMismatch {
      expected: ruleset.version.to_string(),
      found: save.ruleset_version,
    });
  }

  align_risk_postures(&mut save.history.genesis);
  for transition in &mut save.history.transitions {
    align_risk_postures(&mut transition.prior);
    align_risk_postures(&mut transition.next);
  }

  Ok(save)
}

fn align_risk_postures(state: &mut crate::model::CompetitiveWorldState) {
  let risk_posture = match state.difficulty {
    crate::model::Difficulty::Easy => crate::model::RiskPosture::Conservative,
    crate::model::Difficulty::Normal => crate::model::RiskPosture::Moderate,
    crate::model::Difficulty::Hard | crate::model::Difficulty::Expert => {
      crate::model::RiskPosture::Aggressive
    }
  };
  for player in &mut state.players {
    if let crate::model::PlayerController::Ai(ref mut profile) = player.controller {
      profile.risk_posture = risk_posture;
    }
  }
}
