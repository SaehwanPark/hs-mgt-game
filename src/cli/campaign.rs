use crate::model::{
  CampaignId, CliError, CompetitiveRunConfig, PlayerResources, Ruleset, SessionOutcome,
  default_competitive_ruleset,
};
use crate::sim::validate_competitive_batch;

use super::display::{print_block, print_line, render_executive_report, style};
use super::input::ReadLineOutcome;
use super::io::{
  parse_campaign_choice, parse_difficulty_choice, parse_seed_choice, read_campaign_choice,
  read_difficulty_choice, read_seed_choice, read_validation_demo_choice,
};
use crate::competitive::{
  mock_observation_month1, validation_demo_by_id, validation_demo_menu_lines,
  validation_resources_for_demo,
};
use crate::model::PolicyCalendar;

pub fn select_campaign() -> Result<Option<CampaignId>, CliError> {
  loop {
    match read_campaign_choice()? {
      ReadLineOutcome::Quit => return Ok(None),
      ReadLineOutcome::Payload(input) => match parse_campaign_choice(&input) {
        Ok(campaign) => return Ok(Some(campaign)),
        Err(CliError::InvalidCampaignChoice(choice)) => {
          print_line(&style::warning(&format!(
            "{} Campaign '{choice}' is not available; use Enter, 1, or 2",
            style::EMOJI_WARNING
          )));
        }
        Err(error) => return Err(error),
      },
    }
  }
}

pub fn read_competitive_run_config() -> Result<Option<CompetitiveRunConfig>, CliError> {
  let difficulty = loop {
    match read_difficulty_choice()? {
      ReadLineOutcome::Quit => return Ok(None),
      ReadLineOutcome::Payload(input) => match parse_difficulty_choice(&input) {
        Ok(difficulty) => break difficulty,
        Err(CliError::InvalidDifficultyChoice(choice)) => {
          print_line(&style::warning(&format!(
            "{} Difficulty '{choice}' is not available; use Enter, 1, 2, 3, or 4",
            style::EMOJI_WARNING
          )));
        }
        Err(error) => return Err(error),
      },
    }
  };

  let seed = loop {
    match read_seed_choice()? {
      ReadLineOutcome::Quit => return Ok(None),
      ReadLineOutcome::Payload(input) => match parse_seed_choice(&input) {
        Ok(seed) => break seed,
        Err(CliError::InvalidSeed(seed)) => {
          print_line(&style::warning(&format!(
            "{} Seed '{seed}' is not a valid unsigned integer",
            style::EMOJI_WARNING
          )));
        }
        Err(error) => return Err(error),
      },
    }
  };

  Ok(Some(CompetitiveRunConfig { seed, difficulty }))
}

pub fn run_competitive_stub(_ruleset: &Ruleset, config: CompetitiveRunConfig) -> SessionOutcome {
  run_competitive_preview(config, read_validation_demo_input())
}

fn read_validation_demo_input() -> Option<String> {
  match read_validation_demo_choice() {
    Ok(ReadLineOutcome::Quit) => None,
    Ok(ReadLineOutcome::Payload(input)) => Some(input),
    Err(_) => Some(String::new()),
  }
}

pub fn run_competitive_preview(
  config: CompetitiveRunConfig,
  demo_input: Option<String>,
) -> SessionOutcome {
  let ruleset = default_competitive_ruleset();
  let resources = PlayerResources::genesis(config.difficulty, &ruleset);
  let calendar = PolicyCalendar::new_month(1);
  let observation = mock_observation_month1(config.difficulty);
  let ap_budget = config.difficulty.human_ap_per_month();
  let report = render_executive_report(
    calendar,
    &observation,
    ap_budget,
    ap_budget,
    resources.political_capital,
    ruleset.political_capital_cap,
  );

  print_line(&style::label_value(
    "Campaign",
    CampaignId::CompetitiveRegionalV1.as_str(),
  ));
  print_line(&style::label_value(
    "Difficulty",
    &format!(
      "{} ({} AI rival{})",
      config.difficulty.label(),
      config.difficulty.k_rivals(),
      if config.difficulty.k_rivals() == 1 {
        ""
      } else {
        "s"
      }
    ),
  ));
  print_line(&style::label_value("Seed", &config.seed.to_string()));
  print_line("");

  print_block(&report);

  print_line("");
  print_line(&style::subsection(
    "ACTION ECONOMY VALIDATION DEMO (slice I3)",
  ));
  print_line("Select a preset command batch to validate AP, cash, and political capital:");
  for line in validation_demo_menu_lines() {
    print_line(&line);
  }
  print_line("  Enter — skip validation demo");
  print_line("");

  match demo_input {
    None => return SessionOutcome::QuitNoSave,
    Some(input) if input.is_empty() => {
      print_line(&style::dim("Skipped validation demo."));
    }
    Some(input) => run_validation_demo(&input, config.difficulty, &ruleset),
  }

  print_line("");
  print_line(&style::dim(
    "Competitive campaign preview (slices I1–I3). Monthly command entry, simultaneous \
     resolution, and the full 24-month campaign ship in slices I4–I8.",
  ));
  print_line(&style::dim(
    "Select stabilization-v1 (campaign 1) for the playable five-turn demo.",
  ));

  SessionOutcome::CompetitivePreview
}

fn run_validation_demo(
  input: &str,
  difficulty: crate::model::Difficulty,
  ruleset: &crate::model::CompetitiveRuleset,
) {
  let demo_id = match input.trim().parse::<u32>() {
    Ok(id) => id,
    Err(_) => {
      print_line(&style::warning(&format!(
        "{} Demo choice '{input}' is not a number; use 1–5",
        style::EMOJI_WARNING
      )));
      return;
    }
  };

  let Some(demo) = validation_demo_by_id(demo_id) else {
    print_line(&style::warning(&format!(
      "{} Demo '{demo_id}' is not available; use 1–5",
      style::EMOJI_WARNING
    )));
    return;
  };

  let resources = validation_resources_for_demo(demo_id, difficulty, ruleset);
  print_line(&style::label_value("Demo", demo.label));
  print_line(&style::label_value(
    "Resources",
    &format!(
      "cash={}, political_capital={}, ap_budget={}",
      resources.cash, resources.political_capital, resources.ap_budget
    ),
  ));

  match validate_competitive_batch(demo.commands, &resources, ruleset) {
    Ok(()) => print_line(&style::success("Validation passed.")),
    Err(error) => print_line(&style::warning(&format!(
      "{} Validation failed: {}",
      style::EMOJI_WARNING,
      error.message()
    ))),
  }
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{DEFAULT_SEED, Difficulty};

  #[test]
  fn empty_campaign_choice_defaults_to_stabilization() {
    assert_eq!(
      parse_campaign_choice("").unwrap(),
      CampaignId::StabilizationV1
    );
    assert_eq!(
      parse_campaign_choice("1").unwrap(),
      CampaignId::StabilizationV1
    );
  }

  #[test]
  fn competitive_campaign_choice_is_parsed() {
    assert_eq!(
      parse_campaign_choice("2").unwrap(),
      CampaignId::CompetitiveRegionalV1
    );
  }

  #[test]
  fn invalid_campaign_choice_is_error() {
    assert_eq!(
      parse_campaign_choice("9"),
      Err(CliError::InvalidCampaignChoice("9".to_string()))
    );
  }

  #[test]
  fn competitive_stub_returns_preview_outcome() {
    let outcome = run_competitive_preview(
      CompetitiveRunConfig {
        seed: DEFAULT_SEED,
        difficulty: Difficulty::Normal,
      },
      Some(String::new()),
    );
    assert_eq!(outcome, SessionOutcome::CompetitivePreview);
  }

  #[test]
  fn validation_demo_one_passes_at_genesis() {
    let ruleset = default_competitive_ruleset();
    let resources = validation_resources_for_demo(1, Difficulty::Normal, &ruleset);
    let demo = validation_demo_by_id(1).expect("demo 1");
    assert!(validate_competitive_batch(demo.commands, &resources, &ruleset).is_ok());
  }

  #[test]
  fn validation_demo_two_fails_ap_budget() {
    let ruleset = default_competitive_ruleset();
    let resources = validation_resources_for_demo(2, Difficulty::Normal, &ruleset);
    let demo = validation_demo_by_id(2).expect("demo 2");
    assert!(validate_competitive_batch(demo.commands, &resources, &ruleset).is_err());
  }
}
