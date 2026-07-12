use crate::model::{
  AFFILIATION_REPLAY_ARTIFACT_VERSION, AffiliationReplayArtifact, AffiliationRuleset,
  AffiliationValidationError,
};

pub fn serialize_affiliation_replay(artifact: &AffiliationReplayArtifact) -> String {
  serde_json::to_string_pretty(artifact).unwrap_or_default()
}

pub fn deserialize_affiliation_replay(text: &str) -> Result<AffiliationReplayArtifact, String> {
  let artifact: AffiliationReplayArtifact =
    serde_json::from_str(text).map_err(|error| format!("JSON parse error: {error}"))?;
  if artifact.artifact_version != AFFILIATION_REPLAY_ARTIFACT_VERSION {
    return Err(format!(
      "unsupported affiliation replay artifact version '{}'",
      artifact.artifact_version
    ));
  }
  Ok(artifact)
}

pub fn verify_affiliation_replay(
  text: &str,
  ruleset: &AffiliationRuleset,
) -> Result<crate::model::AffiliationWorldState, String> {
  let artifact = deserialize_affiliation_replay(text)?;
  if artifact.ruleset_version != ruleset.version {
    return Err(format!(
      "affiliation replay ruleset '{}' does not match '{}'",
      artifact.ruleset_version, ruleset.version
    ));
  }
  crate::affiliation::replay_affiliation(&artifact.history, ruleset)
    .map_err(|error: AffiliationValidationError| error.message())
}
