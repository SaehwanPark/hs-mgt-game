use crate::model::{
  CampaignId, CliError, CompetitiveHistory, CompetitiveRuleset, CompetitiveRunConfig,
  CompetitiveSessionSave, CompetitiveTransition, CompetitiveWorldState, PlayerResources, Ruleset,
  SessionOutcome, SystemMonthlyBatch, default_competitive_ruleset,
};
use crate::sim::{observe_for_human, validate_competitive_batch};

use super::competitive_parse::{competitive_command_help_lines, parse_competitive_batch};
use super::display::{print_block, print_line, render_executive_report, style};
use super::error::describe_cli_error;
use super::input::ReadLineOutcome;
use super::io::{
  parse_campaign_choice, parse_difficulty_choice, parse_seed_choice, read_campaign_choice,
  read_competitive_command_batch, read_difficulty_choice, read_seed_choice,
  read_validation_demo_choice, stdin_uses_fallback_input,
};
use super::persistence::{
  delete_competitive_session_save, describe_persistence_error, write_competitive_session_save,
};
use crate::competitive::{
  genesis_competitive_world_with_ruleset, genesis_roster_lines, human_batch_for_month,
  observation_from_genesis, resolution_summary_lines, resolve_competitive_month,
  validation_demo_by_id, validation_demo_menu_lines, validation_resources_for_demo,
};

const COMPETITIVE_CAMPAIGN_MONTHS: u32 = 24;

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

pub fn run_competitive_stub(
  _ruleset: &Ruleset,
  config: CompetitiveRunConfig,
  initial_world: Option<CompetitiveWorldState>,
) -> SessionOutcome {
  run_competitive_preview_internal(config, None, initial_world)
}

#[allow(dead_code)]
pub fn run_competitive_preview(
  config: CompetitiveRunConfig,
  demo_input: Option<String>,
  initial_world: Option<CompetitiveWorldState>,
) -> SessionOutcome {
  run_competitive_preview_internal(config, Some(demo_input), initial_world)
}

fn run_competitive_preview_internal(
  config: CompetitiveRunConfig,
  demo_input: Option<Option<String>>,
  initial_world: Option<CompetitiveWorldState>,
) -> SessionOutcome {
  let ruleset = default_competitive_ruleset();
  let world = initial_world
    .unwrap_or_else(|| genesis_competitive_world_with_ruleset(config.difficulty, &ruleset));

  print_line(&style::label_value(
    "Campaign",
    CampaignId::CompetitiveRegionalV1.as_str(),
  ));
  print_line(&style::label_value(
    "Difficulty",
    &format!(
      "{} ({} AI rival{})",
      world.difficulty.label(),
      world.rival_count(),
      if world.rival_count() == 1 { "" } else { "s" }
    ),
  ));
  print_line(&style::label_value("Seed", &config.seed.to_string()));
  print_line("");
  print_line(&style::subsection("REGIONAL MARKET ROSTER (genesis)"));
  for line in genesis_roster_lines(&world) {
    print_line(&line);
  }

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

  let demo_input = match demo_input {
    Some(input) => input,
    None => read_validation_demo_input(),
  };

  match demo_input {
    None => return SessionOutcome::QuitNoSave,
    Some(input) if input.is_empty() => {
      print_line(&style::dim("Skipped validation demo."));
    }
    Some(input) => run_validation_demo(&input, config.difficulty, &ruleset),
  }

  print_line("");
  print_line(&style::subsection("COMPETITIVE CAMPAIGN LOOP"));
  match run_competitive_month_loop(world, Vec::new(), &ruleset, config.seed) {
    Ok(history) => {
      print_competitive_completed(history);
      SessionOutcome::Completed
    }
    Err(CompetitiveLoopError::Quit) => SessionOutcome::QuitSaved,
    Err(CompetitiveLoopError::Cli(error)) => {
      print_line(&style::warning(&format!(
        "{} Could not parse human batch: {}",
        style::EMOJI_WARNING,
        describe_cli_error(&error)
      )));
      SessionOutcome::CompetitivePreview
    }
    Err(CompetitiveLoopError::Validation(error)) => {
      print_line(&style::warning(&format!(
        "{} Competitive month resolution failed: {}",
        style::EMOJI_WARNING,
        error.message()
      )));
      SessionOutcome::CompetitivePreview
    }
  }
}

pub fn resume_competitive_campaign(save: CompetitiveSessionSave) -> SessionOutcome {
  let comp_ruleset = default_competitive_ruleset();

  print_line("");
  print_line(&style::subsection(&format!(
    "RESUMING COMPETITIVE CAMPAIGN (Month {}, seed {})",
    save.next_month, save.seed
  )));

  match run_competitive_month_loop(
    save.history.genesis,
    save.history.transitions,
    &comp_ruleset,
    save.seed,
  ) {
    Ok(history) => {
      print_competitive_completed(history);
      SessionOutcome::Completed
    }
    Err(CompetitiveLoopError::Quit) => SessionOutcome::QuitSaved,
    Err(CompetitiveLoopError::Cli(error)) => {
      print_line(&style::warning(&format!(
        "{} Could not parse human batch: {}",
        style::EMOJI_WARNING,
        describe_cli_error(&error)
      )));
      SessionOutcome::CompetitivePreview
    }
    Err(CompetitiveLoopError::Validation(error)) => {
      print_line(&style::warning(&format!(
        "{} Competitive month resolution failed: {}",
        style::EMOJI_WARNING,
        error.message()
      )));
      SessionOutcome::CompetitivePreview
    }
  }
}

fn print_competitive_completed(history: CompetitiveHistory) {
  print_line("");
  print_line(&style::success(&format!(
    "Completed {} competitive months.",
    history.transitions.len()
  )));
  print_line(&style::label_value(
    "Final turn",
    &history.final_state().turn.to_string(),
  ));
  print_line(&style::label_value(
    "Next report month",
    &format!(
      "Year {}, Month {}",
      history.final_state().policy_calendar.year,
      history.final_state().policy_calendar.month_in_year
    ),
  ));
  print_line("");
  print_line(&style::subsection(
    "Competitive Debrief & Instructor Review",
  ));
  for line in crate::debrief::competitive_debrief(&history) {
    print_line(&format!("  {line}"));
  }

  if std::io::IsTerminal::is_terminal(&std::io::stdin()) {
    match super::io::read_replay_export_path() {
      Ok(ReadLineOutcome::Quit) => {}
      Ok(ReadLineOutcome::Payload(input)) => {
        let trimmed = input.trim();
        if !trimmed.is_empty() {
          let path = std::path::PathBuf::from(trimmed);
          let text = serde_json::to_string_pretty(&history).unwrap_or_default();
          match std::fs::write(&path, text) {
            Ok(()) => {
              print_line(&style::success(&format!(
                "{} Replay export complete: {}",
                style::EMOJI_SUCCESS,
                path.display()
              )));
            }
            Err(error) => {
              print_line(&style::warning(&format!(
                "{} Replay export failed: {error}",
                style::EMOJI_WARNING
              )));
            }
          }
        }
      }
      Err(_) => {}
    }
  }
}

#[derive(Debug)]
enum CompetitiveLoopError {
  Quit,
  Cli(CliError),
  Validation(crate::model::CompetitiveValidationError),
}

impl From<crate::model::CompetitiveValidationError> for CompetitiveLoopError {
  fn from(error: crate::model::CompetitiveValidationError) -> Self {
    Self::Validation(error)
  }
}

fn run_competitive_month_loop(
  genesis: CompetitiveWorldState,
  initial_transitions: Vec<CompetitiveTransition>,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<CompetitiveHistory, CompetitiveLoopError> {
  let mut transitions = initial_transitions;
  let mut current = if let Some(last) = transitions.last() {
    last.next.clone()
  } else {
    genesis.clone()
  };
  let mut prior_aggregated = transitions.last().map(|t| t.aggregated.clone());

  let start_month = transitions.len() as u32;

  for _ in start_month..COMPETITIVE_CAMPAIGN_MONTHS {
    print_competitive_month_report(&current, prior_aggregated.as_ref(), ruleset);

    let human_batch = match read_human_batch_for_world(&current, ruleset) {
      Ok(batch) => batch,
      Err(CompetitiveLoopError::Quit) => {
        let history = CompetitiveHistory {
          genesis: genesis.clone(),
          transitions: transitions.clone(),
        };
        let save = CompetitiveSessionSave {
          ruleset_version: ruleset.version.to_string(),
          seed,
          difficulty: genesis.difficulty,
          history,
          next_month: current.policy_calendar.month_index,
        };
        match write_competitive_session_save(&save) {
          Ok(()) => {
            print_line(&style::success(&format!(
              "{} Competitive campaign session saved; resume on next launch with c/2",
              style::EMOJI_SUCCESS
            )));
          }
          Err(error) => {
            print_line(&style::warning(&format!(
              "{} Competitive autosave failed: {}",
              style::EMOJI_WARNING,
              describe_persistence_error(&error)
            )));
          }
        }
        return Err(CompetitiveLoopError::Quit);
      }
      Err(other) => return Err(other),
    };

    print_line("");
    print_line(&style::subsection(&format!(
      "MONTH {} RESOLUTION",
      current.policy_calendar.month_index
    )));
    print_line("Resolving simultaneous player batches (human entry + AI rivals)...");
    print_line("");

    let transition = resolve_competitive_month(&current, ruleset, seed, human_batch)?;
    for line in resolution_summary_lines(&transition) {
      print_line(&line);
    }
    print_line("");

    prior_aggregated = Some(transition.aggregated.clone());
    current = transition.next.clone();
    transitions.push(transition);
  }

  // Campaign completed successfully, delete autosave
  let _ = delete_competitive_session_save();

  Ok(CompetitiveHistory {
    genesis,
    transitions,
  })
}

fn print_competitive_month_report(
  world: &CompetitiveWorldState,
  prior_aggregated: Option<&crate::model::AggregatedMonthlyActions>,
  ruleset: &CompetitiveRuleset,
) {
  let human = world.human_system().expect("human system");
  let observation = if world.turn == 0 {
    observation_from_genesis(world)
  } else {
    observe_for_human(world, prior_aggregated)
  };
  let ap_budget = world.difficulty.human_ap_per_month();
  let report = render_executive_report(
    world.policy_calendar,
    &observation,
    ap_budget,
    ap_budget,
    human.resources.political_capital,
    ruleset.political_capital_cap,
  );

  print_block(&report);
  print_line("");
  print_line(&style::subsection(&format!(
    "MONTH {} COMMAND ENTRY",
    world.policy_calendar.month_index
  )));
  print_line(
    "Enter Stata-like commands for Riverside (system 0), or press Enter for fallback batch.",
  );
  for line in competitive_command_help_lines() {
    print_line(&format!("  {}", format_competitive_help_line(&line)));
  }
  print_line(&format!(
    "  {}",
    style::command_prompt_label(
      "Prompt: riverside> (Type ? or help for detailed command descriptions, Tab: complete command verbs)"
    )
  ));
  print_line("");
}

fn format_competitive_help_line(line: &str) -> String {
  if line.starts_with("Separate ") {
    return style::dim(line);
  }

  if line.contains(char::is_whitespace) {
    let mut parts = line.splitn(2, char::is_whitespace);
    let verb = parts.next().unwrap_or_default();
    let rest = parts.next().unwrap_or("").trim();
    if rest.is_empty() {
      style::command_token(verb)
    } else {
      format!(
        "{} {}",
        style::command_token(verb),
        style::argument_token(rest)
      )
    }
  } else {
    style::command_token(line)
  }
}

fn read_human_batch_for_world(
  world: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
) -> Result<SystemMonthlyBatch, CompetitiveLoopError> {
  let fallback_batch = human_batch_for_month(world.turn);
  if stdin_uses_fallback_input() {
    return Ok(fallback_batch);
  }

  let human_resources = world
    .human_system()
    .expect("human system")
    .resources
    .clone();

  match read_competitive_human_batch(&human_resources, ruleset, fallback_batch) {
    Ok(None) => Err(CompetitiveLoopError::Quit),
    Ok(Some(batch)) => Ok(batch),
    Err(error) => Err(CompetitiveLoopError::Cli(error)),
  }
}

fn read_competitive_human_batch(
  resources: &PlayerResources,
  ruleset: &CompetitiveRuleset,
  fallback_batch: SystemMonthlyBatch,
) -> Result<Option<SystemMonthlyBatch>, CliError> {
  match read_competitive_command_batch()? {
    ReadLineOutcome::Quit => Ok(None),
    ReadLineOutcome::Payload(input) => {
      if input.trim().is_empty() {
        return Ok(Some(fallback_batch));
      }
      let commands = parse_competitive_batch(&input)?;
      validate_competitive_batch(&commands, resources, ruleset)
        .map_err(|error| CliError::InvalidCommandInput(error.message()))?;
      Ok(Some(SystemMonthlyBatch::new(0, commands)))
    }
  }
}

fn read_validation_demo_input() -> Option<String> {
  match read_validation_demo_choice() {
    Ok(ReadLineOutcome::Quit) => None,
    Ok(ReadLineOutcome::Payload(input)) => Some(input),
    Err(error) => {
      print_line(&style::warning(&format!(
        "{} Could not read validation demo choice: {error:?}",
        style::EMOJI_WARNING
      )));
      Some(String::new())
    }
  }
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
  fn competitive_stub_returns_completed_outcome() {
    let outcome = run_competitive_preview(
      CompetitiveRunConfig {
        seed: DEFAULT_SEED,
        difficulty: Difficulty::Normal,
      },
      Some(String::new()),
      None,
    );
    assert_eq!(outcome, SessionOutcome::Completed);
  }

  #[test]
  fn competitive_month_loop_runs_twenty_four_months_in_non_tty_context() {
    let ruleset = default_competitive_ruleset();
    let world = genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let history =
      run_competitive_month_loop(world, Vec::new(), &ruleset, DEFAULT_SEED).expect("history");

    assert_eq!(history.transitions.len(), 24);
    assert_eq!(history.final_state().turn, 24);
    assert_eq!(history.final_state().policy_calendar.month_index, 25);
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

  #[test]
  fn validation_demo_three_fails_cash_at_genesis() {
    let ruleset = default_competitive_ruleset();
    let resources = validation_resources_for_demo(3, Difficulty::Normal, &ruleset);
    let demo = validation_demo_by_id(3).expect("demo 3");
    assert!(validate_competitive_batch(demo.commands, &resources, &ruleset).is_err());
  }

  #[test]
  fn validation_demo_four_fails_political_capital() {
    let ruleset = default_competitive_ruleset();
    let resources = validation_resources_for_demo(4, Difficulty::Normal, &ruleset);
    let demo = validation_demo_by_id(4).expect("demo 4");
    assert_eq!(resources.political_capital, 2);
    assert!(validate_competitive_batch(demo.commands, &resources, &ruleset).is_err());
  }

  #[test]
  fn validation_demo_five_passes_project_at_genesis() {
    let ruleset = default_competitive_ruleset();
    let resources = validation_resources_for_demo(5, Difficulty::Normal, &ruleset);
    let demo = validation_demo_by_id(5).expect("demo 5");
    assert!(validate_competitive_batch(demo.commands, &resources, &ruleset).is_ok());
  }
}
