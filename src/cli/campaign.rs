use crate::model::{CampaignId, CliError, CompetitiveRunConfig, Ruleset, SessionOutcome};

use super::display::{print_block, print_line, render_executive_report, style};
use super::input::ReadLineOutcome;
use super::io::{
  parse_campaign_choice, parse_difficulty_choice, parse_seed_choice, read_campaign_choice,
  read_difficulty_choice, read_seed_choice,
};
use crate::competitive::mock_observation_month1;
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
  let calendar = PolicyCalendar::new_month(1);
  let observation = mock_observation_month1(config.difficulty);
  let ap_budget = config.difficulty.human_ap_per_month();
  let report = render_executive_report(calendar, &observation, ap_budget, ap_budget);

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
  print_line(&style::dim(
    "Competitive campaign preview only (slice I1+I2). Monthly command entry, simultaneous \
     resolution, and the full 24-month campaign ship in slices I3–I8.",
  ));
  print_line(&style::dim(
    "Select stabilization-v1 (campaign 1) for the playable five-turn demo.",
  ));

  SessionOutcome::CompetitivePreview
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{DEFAULT_SEED, Difficulty, default_ruleset};

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
    let outcome = run_competitive_stub(
      &default_ruleset(),
      CompetitiveRunConfig {
        seed: DEFAULT_SEED,
        difficulty: Difficulty::Normal,
      },
    );
    assert_eq!(outcome, SessionOutcome::CompetitivePreview);
  }
}
