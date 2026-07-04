#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Observation {
  pub actor: &'static str,
  pub reported_access_index: i32,
  pub reported_quality_index: i32,
  pub prior_access_revision: i32,
  pub policy_briefing: &'static str,
  pub market_competition_briefing: &'static str,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Event {
  pub actor: &'static str,
  pub description: String,
}

impl serde::Serialize for Event {
  fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
  where
    S: serde::Serializer,
  {
    #[derive(serde::Serialize)]
    struct RawEvent {
      actor: String,
      description: String,
    }
    RawEvent {
      actor: self.actor.to_string(),
      description: self.description.clone(),
    }
    .serialize(serializer)
  }
}

impl<'de> serde::Deserialize<'de> for Event {
  fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
  where
    D: serde::Deserializer<'de>,
  {
    #[derive(serde::Deserialize)]
    struct RawEvent {
      actor: String,
      description: String,
    }
    let raw = RawEvent::deserialize(deserializer)?;
    Ok(Event {
      actor: Box::leak(raw.actor.into_boxed_str()),
      description: raw.description,
    })
  }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AttributedEffect {
  pub source: &'static str,
  pub metric: &'static str,
  pub delta: i32,
}

impl serde::Serialize for AttributedEffect {
  fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
  where
    S: serde::Serializer,
  {
    #[derive(serde::Serialize)]
    struct RawEffect {
      source: String,
      metric: String,
      delta: i32,
    }
    RawEffect {
      source: self.source.to_string(),
      metric: self.metric.to_string(),
      delta: self.delta,
    }
    .serialize(serializer)
  }
}

impl<'de> serde::Deserialize<'de> for AttributedEffect {
  fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
  where
    D: serde::Deserializer<'de>,
  {
    #[derive(serde::Deserialize)]
    struct RawEffect {
      source: String,
      metric: String,
      delta: i32,
    }
    let raw = RawEffect::deserialize(deserializer)?;
    Ok(AttributedEffect {
      source: Box::leak(raw.source.into_boxed_str()),
      metric: Box::leak(raw.metric.into_boxed_str()),
      delta: raw.delta,
    })
  }
}
