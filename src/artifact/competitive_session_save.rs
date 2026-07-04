use crate::model::{CompetitiveRuleset, CompetitiveSessionSave, SessionSaveError};

pub fn serialize_competitive_session_save(save: &CompetitiveSessionSave) -> String {
  serde_json::to_string_pretty(save).unwrap_or_default()
}

pub fn deserialize_competitive_session_save(
  text: &str,
  ruleset: &CompetitiveRuleset,
) -> Result<CompetitiveSessionSave, SessionSaveError> {
  let save: CompetitiveSessionSave =
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

  Ok(save)
}
