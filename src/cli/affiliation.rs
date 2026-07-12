use crate::affiliation::{genesis_affiliation_world, resolve_affiliation_turn};
use crate::artifact::{serialize_affiliation_replay, verify_affiliation_replay};
use crate::debrief::affiliation_debrief;
use crate::model::{
  AffiliationCommand, AffiliationHistory, AffiliationPosture, IntegrationDecision, SessionOutcome,
  default_affiliation_ruleset,
};

use super::display::{print_line, style};
use super::input::ReadLineOutcome;
use super::io::{parse_replay_export_path, read_replay_export_path, stdin_uses_fallback_input};
use super::io::{parse_seed_choice, read_command_line, read_seed_choice};

pub fn run_affiliation_campaign(scenario: Option<&crate::scenario::Scenario>) -> SessionOutcome {
  let seed = match read_seed_choice() {
    Ok(ReadLineOutcome::Payload(input)) => match parse_seed_choice(&input) {
      Ok(seed) => seed,
      Err(error) => {
        print_line(&style::warning(&format!("Invalid seed: {error:?}")));
        return SessionOutcome::QuitNoSave;
      }
    },
    Ok(ReadLineOutcome::Quit) | Err(_) => return SessionOutcome::QuitNoSave,
  };

  let ruleset = default_affiliation_ruleset();
  let mut current = match genesis_affiliation_world(scenario) {
    Ok(state) => state,
    Err(error) => {
      print_line(&style::warning(&format!(
        "Affiliation scenario failed: {error}"
      )));
      return SessionOutcome::QuitNoSave;
    }
  };
  let genesis = current.clone();
  let mut transitions = Vec::new();

  print_line(&style::label_value("Campaign", "regional-affiliation-v1"));
  print_line(&style::label_value("Seed", &seed.to_string()));
  print_line("");

  while current.turn < crate::model::AFFILIATION_TURN_COUNT {
    let observation = crate::affiliation::observe_affiliation(&current);
    print_affiliation_observation(&observation);
    let command = loop {
      print_line("Command:");
      match read_command_line("affiliation command", current.turn + 1) {
        Ok(ReadLineOutcome::Quit) => return SessionOutcome::QuitNoSave,
        Ok(ReadLineOutcome::Payload(input)) => match parse_affiliation_command(&input) {
          Ok(command) => break command,
          Err(error) => print_line(&style::warning(&error)),
        },
        Err(_) => return SessionOutcome::QuitNoSave,
      }
    };

    match resolve_affiliation_turn(&current, command, seed, &ruleset) {
      Ok(transition) => {
        print_line(&style::subsection("STAGE RESOLUTION"));
        for event in &transition.events {
          print_line(&format!("{}: {}", event.actor, event.description));
        }
        print_line(&format!("State hash: {}", transition.state_hash));
        current = transition.next.clone();
        transitions.push(transition);
      }
      Err(error) => print_line(&style::warning(&error.message())),
    }
  }

  let history = AffiliationHistory {
    genesis,
    transitions,
  };
  print_line(&style::success("Completed regional affiliation scenario."));
  print_line(&style::subsection("AFFILIATION DEBRIEF"));
  for line in affiliation_debrief(&history) {
    print_line(&format!("  {line}"));
  }
  if !stdin_uses_fallback_input()
    && let Ok(ReadLineOutcome::Payload(input)) = read_replay_export_path()
    && let Some(path) = parse_replay_export_path(&input)
  {
    let ruleset = default_affiliation_ruleset();
    let artifact = crate::model::AffiliationReplayArtifact {
      artifact_version: crate::model::AFFILIATION_REPLAY_ARTIFACT_VERSION.to_string(),
      seed,
      ruleset_version: ruleset.version.clone(),
      history: history.clone(),
    };
    let text = serialize_affiliation_replay(&artifact);
    match std::fs::write(&path, text) {
      Ok(()) => print_line(&style::success(&format!("Replay export complete: {path}"))),
      Err(error) => print_line(&style::warning(&format!("Replay export failed: {error}"))),
    }
    let _ = verify_affiliation_replay(&serialize_affiliation_replay(&artifact), &ruleset);
  }
  SessionOutcome::Completed
}

pub fn parse_affiliation_command(input: &str) -> Result<AffiliationCommand, String> {
  let parts = input.split_whitespace().collect::<Vec<_>>();
  match parts.as_slice() {
    ["assess"] => Ok(AffiliationCommand::AssessPartner),
    ["hold"] => Ok(AffiliationCommand::Hold),
    ["posture", value] => Ok(AffiliationCommand::ChoosePosture {
      posture: match value.strip_prefix("choice=").unwrap_or("") {
        "independent" => AffiliationPosture::Independent,
        "defer" => AffiliationPosture::Deferred,
        "pursue" => AffiliationPosture::Pursue,
        _ => return Err("posture expects choice=independent|defer|pursue".to_string()),
      },
    }),
    ["commit", community, workforce, continuity] => Ok(AffiliationCommand::SetCommitments {
      community: parse_value(community, "community")?,
      workforce: parse_value(workforce, "workforce")?,
      continuity: parse_value(continuity, "continuity")?,
    }),
    ["submit_review"] => Ok(AffiliationCommand::SubmitReview),
    ["await_review"] => Ok(AffiliationCommand::AwaitReview),
    ["integrate", value] => Ok(AffiliationCommand::ChooseIntegration {
      decision: match value.strip_prefix("decision=").unwrap_or("") {
        "begin" => IntegrationDecision::Begin,
        "decline" => IntegrationDecision::Decline,
        _ => return Err("integrate expects decision=begin|decline".to_string()),
      },
    }),
    _ => Err("commands: assess, posture choice=..., commit <community> <workforce> <continuity>, submit_review, await_review, integrate decision=..., hold".to_string()),
  }
}

fn parse_value(value: &str, label: &str) -> Result<i32, String> {
  let value = value
    .strip_prefix(&format!("{label}="))
    .ok_or_else(|| format!("commit expects {label}=<1..8>"))?;
  value
    .parse::<i32>()
    .map_err(|_| format!("invalid {label} value '{value}'"))
}

fn print_affiliation_observation(observation: &crate::model::AffiliationObservation) {
  print_line(&style::subsection(&format!(
    "AFFILIATION STAGE {} — {:?}",
    observation.turn, observation.stage
  )));
  print_line(&format!(
    "Riverside: cash {}, access {}, quality {}, workforce trust {}, community trust {}, market share {}",
    observation.cash,
    observation.access_index,
    observation.quality_index,
    observation.workforce_trust,
    observation.community_trust,
    observation.market_share_index,
  ));
  print_line(&format!("Partner: {}", observation.partner_name));
  if let Some(condition) = observation.reported_condition {
    print_line(&format!("Reported partner condition: {condition:?}"));
  }
  print_line(&format!("Status: {:?}", observation.status));
  for alternative in &observation.alternatives {
    print_line(&format!("Alternative: {alternative}"));
  }
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn affiliation_command_parser_accepts_stage_commands() {
    assert_eq!(
      parse_affiliation_command("assess"),
      Ok(AffiliationCommand::AssessPartner)
    );
    assert_eq!(
      parse_affiliation_command("posture choice=pursue"),
      Ok(AffiliationCommand::ChoosePosture {
        posture: AffiliationPosture::Pursue
      })
    );
    assert_eq!(
      parse_affiliation_command("commit community=3 workforce=4 continuity=5"),
      Ok(AffiliationCommand::SetCommitments {
        community: 3,
        workforce: 4,
        continuity: 5
      })
    );
  }
}
