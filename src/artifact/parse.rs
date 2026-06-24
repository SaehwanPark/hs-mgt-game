use crate::model::{
  ActorDecision, ActorDecisionRecord, AttributedEffect, CoalitionDecision, Event, InsurerDecision,
  LaborDecision, Observation, PlayMode, PlayerCommand, ReplayArtifactError, ResolvedInputs,
  StatePolicyDecision, StrategyPath, Transition, WorldState,
};

use super::text::unescape_artifact_text;

pub fn parse_world_state_line(
  line: &str,
  expected_prefix: &str,
) -> Result<WorldState, ReplayArtifactError> {
  let (prefix, payload) = line
    .split_once('=')
    .ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("expected {expected_prefix}=..."),
    })?;

  if prefix != expected_prefix {
    return Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("expected {expected_prefix}, found {prefix}"),
    });
  }

  let mut fields = std::collections::BTreeMap::new();
  for part in payload.split(',') {
    let (key, value) = part
      .split_once(':')
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid world-state field {part}"),
      })?;
    fields.insert(key.to_string(), value.to_string());
  }

  let read_i32 = |key: &str| -> Result<i32, ReplayArtifactError> {
    fields
      .get(key)
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("missing world-state field {key}"),
      })?
      .parse::<i32>()
      .map_err(|_| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid integer for world-state field {key}"),
      })
  };

  let read_u32 = |key: &str| -> Result<u32, ReplayArtifactError> {
    fields
      .get(key)
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("missing world-state field {key}"),
      })?
      .parse::<u32>()
      .map_err(|_| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid unsigned integer for world-state field {key}"),
      })
  };

  Ok(WorldState {
    turn: read_u32("turn")?,
    cash: read_i32("cash")?,
    staffed_beds: read_i32("staffed_beds")?,
    access_index: read_i32("access_index")?,
    quality_index: read_i32("quality_index")?,
    workforce_trust: read_i32("workforce_trust")?,
    community_trust: read_i32("community_trust")?,
    commercial_rate: read_i32("commercial_rate")?,
    policy_pressure: read_i32("policy_pressure")?,
  })
}

pub fn parse_player_command(payload: &str) -> Result<PlayerCommand, ReplayArtifactError> {
  let mut parts = payload.split(',');
  let kind = parts
    .next()
    .ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing command kind".to_string(),
    })?;

  let mut fields = std::collections::BTreeMap::new();
  for part in parts {
    let (key, value) = part
      .split_once(':')
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid command field {part}"),
      })?;
    fields.insert(key.to_string(), value.to_string());
  }

  let read_i32 = |key: &str| -> Result<i32, ReplayArtifactError> {
    fields
      .get(key)
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("missing command field {key}"),
      })?
      .parse::<i32>()
      .map_err(|_| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid integer for command field {key}"),
      })
  };

  match kind {
    "StabilizeAccess" => Ok(PlayerCommand::StabilizeAccess {
      add_staffed_beds: read_i32("add_staffed_beds")?,
      capital_spend: read_i32("capital_spend")?,
      requested_commercial_rate: read_i32("requested_commercial_rate")?,
    }),
    "RespondToStateAccessMandate" => Ok(PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend: read_i32("advocacy_spend")?,
      access_commitment: read_i32("access_commitment")?,
    }),
    "RespondToWorkforcePressure" => Ok(PlayerCommand::RespondToWorkforcePressure {
      retention_spend: read_i32("retention_spend")?,
      schedule_relief_commitment: read_i32("schedule_relief_commitment")?,
    }),
    "JoinRegionalAccessCoalition" => Ok(PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment: read_i32("coalition_investment")?,
      shared_access_commitment: read_i32("shared_access_commitment")?,
    }),
    other => Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("unknown command kind {other}"),
    }),
  }
}

pub fn parse_resolved_inputs(payload: &str) -> Result<ResolvedInputs, ReplayArtifactError> {
  let mut fields = std::collections::BTreeMap::new();
  for part in payload.split(',') {
    let (key, value) = part
      .split_once(':')
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid resolved-input field {part}"),
      })?;
    fields.insert(key.to_string(), value.to_string());
  }

  let read_i32 = |key: &str| -> Result<i32, ReplayArtifactError> {
    fields
      .get(key)
      .ok_or_else(|| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("missing resolved-input field {key}"),
      })?
      .parse::<i32>()
      .map_err(|_| ReplayArtifactError::ParseError {
        line: 0,
        detail: format!("invalid integer for resolved-input field {key}"),
      })
  };

  Ok(ResolvedInputs {
    measurement_noise: read_i32("measurement_noise")?,
    delayed_access_report: read_i32("delayed_access_report")?,
    labor_sick_call_delta: read_i32("labor_sick_call_delta")?,
    policy_signal: read_i32("policy_signal")?,
    coalition_leverage_signal: read_i32("coalition_leverage_signal")?,
    access_measurement_revision: read_i32("access_measurement_revision")?,
  })
}

pub fn parse_actor_decision(payload: &str) -> Result<ActorDecision, ReplayArtifactError> {
  let mut parts = payload.split(':');
  let family = parts
    .next()
    .ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing actor decision family".to_string(),
    })?;
  let variant = parts
    .next()
    .ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing actor decision variant".to_string(),
    })?;

  match (family, variant) {
    ("Insurer", "Accept") => Ok(ActorDecision::Insurer(InsurerDecision::Accept)),
    ("Insurer", "Reject") => Ok(ActorDecision::Insurer(InsurerDecision::Reject)),
    ("Insurer", "Counter") => {
      let offered_rate = parts
        .next()
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: "missing insurer counter rate".to_string(),
        })?
        .parse::<i32>()
        .map_err(|_| ReplayArtifactError::ParseError {
          line: 0,
          detail: "invalid insurer counter rate".to_string(),
        })?;
      Ok(ActorDecision::Insurer(InsurerDecision::Counter {
        offered_rate,
      }))
    }
    ("StatePolicy", "GrantFlexibility") => Ok(ActorDecision::StatePolicy(
      StatePolicyDecision::GrantFlexibility,
    )),
    ("StatePolicy", "ProceedWithMandate") => Ok(ActorDecision::StatePolicy(
      StatePolicyDecision::ProceedWithMandate,
    )),
    ("StatePolicy", "EscalateOversight") => Ok(ActorDecision::StatePolicy(
      StatePolicyDecision::EscalateOversight,
    )),
    ("Labor", "Cooperative") => Ok(ActorDecision::Labor(LaborDecision::Cooperative)),
    ("Labor", "LimitedSupport") => Ok(ActorDecision::Labor(LaborDecision::LimitedSupport)),
    ("Labor", "WorkAction") => Ok(ActorDecision::Labor(LaborDecision::WorkAction)),
    ("Coalition", "FullPartnership") => {
      Ok(ActorDecision::Coalition(CoalitionDecision::FullPartnership))
    }
    ("Coalition", "LimitedParticipation") => Ok(ActorDecision::Coalition(
      CoalitionDecision::LimitedParticipation,
    )),
    ("Coalition", "CoalitionWithdrawal") => Ok(ActorDecision::Coalition(
      CoalitionDecision::CoalitionWithdrawal,
    )),
    _ => Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("unknown actor decision {payload}"),
    }),
  }
}

pub fn parse_play_mode(payload: &str) -> Result<PlayMode, ReplayArtifactError> {
  match payload {
    "interactive" => Ok(PlayMode::Interactive),
    "preset:1" => Ok(PlayMode::Preset(StrategyPath::AccessStabilization)),
    "preset:2" => Ok(PlayMode::Preset(StrategyPath::FiscalCaution)),
    "preset:3" => Ok(PlayMode::Preset(StrategyPath::AggressiveBargaining)),
    other => Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("unknown play mode {other}"),
    }),
  }
}

pub fn parse_quoted_field(payload: &str, key: &str) -> Result<String, ReplayArtifactError> {
  let marker = format!("{key}:\"");
  let start = payload
    .find(&marker)
    .ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("missing quoted field {key}"),
    })?
    + marker.len();
  let mut escaped = String::new();
  let mut chars = payload[start..].chars();

  while let Some(ch) = chars.next() {
    if ch == '"' {
      return unescape_artifact_text(&escaped);
    }

    if ch == '\\' {
      let next = chars
        .next()
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: format!("unterminated quoted field {key}"),
        })?;
      escaped.push('\\');
      escaped.push(next);
      continue;
    }

    escaped.push(ch);
  }

  Err(ReplayArtifactError::ParseError {
    line: 0,
    detail: format!("unterminated quoted field {key}"),
  })
}

pub fn intern_static_label(value: &str) -> Result<&'static str, ReplayArtifactError> {
  match value {
    "health_system_ceo" => Ok("health_system_ceo"),
    "health_system" => Ok("health_system"),
    "commercial_insurer" => Ok("commercial_insurer"),
    "state_policy_officials" => Ok("state_policy_officials"),
    "nursing_workforce" => Ok("nursing_workforce"),
    "regional_provider_coalition" => Ok("regional_provider_coalition"),
    "capacity investment" => Ok("capacity investment"),
    "staffing constraint" => Ok("staffing constraint"),
    "policy response" => Ok("policy response"),
    "workforce response" => Ok("workforce response"),
    "schedule relief" => Ok("schedule relief"),
    "coalition response" => Ok("coalition response"),
    "coalition investment" => Ok("coalition investment"),
    "commercial insurer" => Ok("commercial insurer"),
    "public bargaining friction" => Ok("public bargaining friction"),
    "failed negotiation" => Ok("failed negotiation"),
    "state policy response" => Ok("state policy response"),
    "nursing workforce" => Ok("nursing workforce"),
    "work action signal" => Ok("work action signal"),
    "regional provider coalition" => Ok("regional provider coalition"),
    "coalition withdrawal" => Ok("coalition withdrawal"),
    "cash" => Ok("cash"),
    "staffed_beds" => Ok("staffed_beds"),
    "access_index" => Ok("access_index"),
    "quality_index" => Ok("quality_index"),
    "workforce_trust" => Ok("workforce_trust"),
    "community_trust" => Ok("community_trust"),
    "commercial_rate" => Ok("commercial_rate"),
    "policy_pressure" => Ok("policy_pressure"),
    other => Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("unknown static label {other}"),
    }),
  }
}

pub fn intern_policy_briefing(value: &str) -> Result<&'static str, ReplayArtifactError> {
  match value {
    "state officials are increasing scrutiny of access and affordability" => {
      Ok("state officials are increasing scrutiny of access and affordability")
    }
    "state policy attention is stable" => Ok("state policy attention is stable"),
    other => Err(ReplayArtifactError::ParseError {
      line: 0,
      detail: format!("unknown policy briefing {other}"),
    }),
  }
}

pub fn parse_transition_block(lines: &[&str]) -> Result<Transition, ReplayArtifactError> {
  let mut command = None;
  let mut resolved_inputs = None;
  let mut state_hash = None;
  let mut prior = None;
  let mut next = None;
  let mut observation = None;
  let mut actor_decision = None;
  let mut events = Vec::new();
  let mut effects = Vec::new();
  let mut expected_event_count = None;
  let mut expected_effect_count = None;
  let mut declared_turn = None;

  for line in lines {
    if line.starts_with("turn=") {
      declared_turn = Some(line["turn=".len()..].parse::<u32>().map_err(|_| {
        ReplayArtifactError::ParseError {
          line: 0,
          detail: "invalid transition turn".to_string(),
        }
      })?);
      continue;
    }
    if line.starts_with("event_count=") {
      expected_event_count = Some(line["event_count=".len()..].parse::<usize>().map_err(|_| {
        ReplayArtifactError::ParseError {
          line: 0,
          detail: "invalid event_count".to_string(),
        }
      })?);
      continue;
    }
    if line.starts_with("effect_count=") {
      expected_effect_count = Some(line["effect_count=".len()..].parse::<usize>().map_err(
        |_| ReplayArtifactError::ParseError {
          line: 0,
          detail: "invalid effect_count".to_string(),
        },
      )?);
      continue;
    }
    if line.starts_with("command=") {
      command = Some(parse_player_command(&line["command=".len()..])?);
      continue;
    }
    if line.starts_with("resolved_inputs=") {
      resolved_inputs = Some(parse_resolved_inputs(&line["resolved_inputs=".len()..])?);
      continue;
    }
    if line.starts_with("state_hash=") {
      state_hash = Some(line["state_hash=".len()..].to_string());
      continue;
    }
    if line.starts_with("prior=") {
      prior = Some(parse_world_state_line(line, "prior")?);
      continue;
    }
    if line.starts_with("next=") {
      next = Some(parse_world_state_line(line, "next")?);
      continue;
    }
    if line.starts_with("observation=") {
      let payload = &line["observation=".len()..];
      let actor = intern_static_label(
        payload
          .split(',')
          .next()
          .and_then(|part| part.strip_prefix("actor:"))
          .ok_or_else(|| ReplayArtifactError::ParseError {
            line: 0,
            detail: "invalid observation actor".to_string(),
          })?,
      )?;
      let read_field = |key: &str| -> Result<i32, ReplayArtifactError> {
        let marker = format!("{key}:");
        let value = payload
          .split(',')
          .find(|part| part.starts_with(&marker))
          .and_then(|part| part.strip_prefix(&marker))
          .ok_or_else(|| ReplayArtifactError::ParseError {
            line: 0,
            detail: format!("missing observation field {key}"),
          })?
          .split(',')
          .next()
          .unwrap_or("")
          .trim_end_matches('"');
        value
          .parse::<i32>()
          .map_err(|_| ReplayArtifactError::ParseError {
            line: 0,
            detail: format!("invalid observation field {key}"),
          })
      };
      observation = Some(Observation {
        actor,
        reported_access_index: read_field("reported_access_index")?,
        reported_quality_index: read_field("reported_quality_index")?,
        prior_access_revision: read_field("prior_access_revision")?,
        policy_briefing: intern_policy_briefing(&parse_quoted_field(payload, "policy_briefing")?)?,
      });
      continue;
    }
    if line.starts_with("actor_decision=") {
      let payload = &line["actor_decision=".len()..];
      let actor = intern_static_label(
        payload
          .split(',')
          .next()
          .and_then(|part| part.strip_prefix("actor:"))
          .ok_or_else(|| ReplayArtifactError::ParseError {
            line: 0,
            detail: "invalid actor_decision actor".to_string(),
          })?,
      )?;
      let decision = payload
        .split(',')
        .find(|part| part.starts_with("decision:"))
        .and_then(|part| part.strip_prefix("decision:"))
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: "missing actor_decision decision".to_string(),
        })?;
      actor_decision = Some(ActorDecisionRecord {
        actor,
        decision: parse_actor_decision(decision)?,
        rationale: parse_quoted_field(payload, "rationale")?,
      });
      continue;
    }
    if let Some(rest) = line.strip_prefix("event=") {
      let mut parts = rest.splitn(3, ',');
      let _index = parts
        .next()
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: "missing event index".to_string(),
        })?;
      let actor = intern_static_label(
        parts
          .next()
          .and_then(|part| part.strip_prefix("actor:"))
          .ok_or_else(|| ReplayArtifactError::ParseError {
            line: 0,
            detail: "invalid event actor".to_string(),
          })?,
      )?;
      let description_payload = parts
        .next()
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: "missing event description".to_string(),
        })?;
      events.push(Event {
        actor,
        description: parse_quoted_field(description_payload, "description")?,
      });
      continue;
    }
    if let Some(rest) = line.strip_prefix("effect=") {
      let mut parts = rest.split(',');
      let _index = parts
        .next()
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: "missing effect index".to_string(),
        })?;
      let source = intern_static_label(
        parts
          .next()
          .and_then(|part| part.strip_prefix("source:"))
          .ok_or_else(|| ReplayArtifactError::ParseError {
            line: 0,
            detail: "invalid effect source".to_string(),
          })?,
      )?;
      let metric = intern_static_label(
        parts
          .next()
          .and_then(|part| part.strip_prefix("metric:"))
          .ok_or_else(|| ReplayArtifactError::ParseError {
            line: 0,
            detail: "invalid effect metric".to_string(),
          })?,
      )?;
      let delta = parts
        .next()
        .and_then(|part| part.strip_prefix("delta:"))
        .ok_or_else(|| ReplayArtifactError::ParseError {
          line: 0,
          detail: "invalid effect delta".to_string(),
        })?
        .parse::<i32>()
        .map_err(|_| ReplayArtifactError::ParseError {
          line: 0,
          detail: "invalid effect delta integer".to_string(),
        })?;
      effects.push(AttributedEffect {
        source,
        metric,
        delta,
      });
    }
  }

  let next = next.ok_or_else(|| ReplayArtifactError::ParseError {
    line: 0,
    detail: "missing transition next state".to_string(),
  })?;
  if let Some(turn) = declared_turn {
    if turn != next.turn {
      return Err(ReplayArtifactError::ParseError {
        line: 0,
        detail: format!(
          "transition turn {turn} does not match next state turn {}",
          next.turn
        ),
      });
    }
  }
  if let Some(event_count) = expected_event_count {
    if events.len() != event_count {
      return Err(ReplayArtifactError::ParseError {
        line: 0,
        detail: format!(
          "event_count {event_count} does not match parsed events {}",
          events.len()
        ),
      });
    }
  }
  if let Some(effect_count) = expected_effect_count {
    if effects.len() != effect_count {
      return Err(ReplayArtifactError::ParseError {
        line: 0,
        detail: format!(
          "effect_count {effect_count} does not match parsed effects {}",
          effects.len()
        ),
      });
    }
  }

  Ok(Transition {
    prior: prior.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing transition prior state".to_string(),
    })?,
    command: command.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing transition command".to_string(),
    })?,
    resolved_inputs: resolved_inputs.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing transition resolved inputs".to_string(),
    })?,
    observation: observation.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing transition observation".to_string(),
    })?,
    actor_decision: actor_decision.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing transition actor decision".to_string(),
    })?,
    events,
    effects,
    next,
    state_hash: state_hash.ok_or_else(|| ReplayArtifactError::ParseError {
      line: 0,
      detail: "missing transition state hash".to_string(),
    })?,
  })
}
