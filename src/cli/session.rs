use crate::artifact::{describe_replay_artifact_error, write_replay_artifact};
use crate::inputs::resolve_inputs;
use crate::model::{
  CampaignId, CliError, CompetitiveRuleset, ExperienceMode, History, INTERACTIVE_TURN_COUNT,
  PlayMode, PlayerCommand, ReplayArtifact, ResumeState, Ruleset, RunConfig, SessionOutcome,
  SessionSave, default_ruleset, genesis_state,
};
use crate::scenario::default_stabilization_scenario;
use crate::sim::{observe_for_player, transition};

use super::beginner::{format_beginner_menu, parse_beginner_choice};
use super::campaign::{
  read_competitive_run_config, resume_competitive_campaign, run_competitive_stub, select_campaign,
};
use super::display::{
  format_command_prompt, print_block, print_interactive_results, print_line,
  print_pre_run_briefing, print_turn_briefing_block, print_turn_resolution_block,
  print_turn_uncertainty_block, style, turn_executive_briefing, turn_resolution_summary,
  turn_uncertainty_preview,
};
use super::guidance::{new_player_cue_lines, turn_hint};
use super::input::ReadLineOutcome;
use super::io::{
  parse_play_mode_choice, parse_replay_export_path, parse_resume_choice,
  parse_seed_choice_with_default, read_beginner_choice, read_command_line,
  read_competitive_resume_choice, read_play_mode_choice, read_replay_export_path,
  read_resume_choice, read_seed_choice, stdin_uses_fallback_input,
};
use super::output::print_demo;
use super::parse::{
  parse_coalition_command, parse_competitor_command, parse_policy_command,
  parse_stabilize_access_command, parse_workforce_command,
};
use super::persistence::{
  delete_competitive_session_save, delete_session_save, first_run_complete,
  load_competitive_session_save, load_session_save, mark_first_run_complete, write_session_save,
};
use super::strategy::{
  build_history_for_strategy_from_genesis, default_interactive_commands, strategy_plan,
};

type TurnParser = fn(&str) -> Result<PlayerCommand, CliError>;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum InteractiveRunResult {
  Completed(History),
  QuitEarly { history: History, next_turn: u32 },
}

struct StabilizationRunSetup {
  config: RunConfig,
  initial_state: crate::model::WorldState,
}

pub fn run(scenario_path: Option<std::path::PathBuf>) -> Result<SessionOutcome, CliError> {
  let ruleset = default_ruleset();

  // If a scenario path was provided, load and run it directly (bypassing campaign selection/resume prompts).
  if let Some(path) = scenario_path {
    let scenario = crate::scenario::load_scenario_file(&path).map_err(|error| {
      CliError::ScenarioLoadFailed(format!("could not load scenario file: {error}"))
    })?;
    if scenario.campaign_id == "competitive-regional-v1" {
      let comp_ruleset = crate::model::default_competitive_ruleset();
      crate::scenario::validate_competitive_scenario(&scenario, &comp_ruleset)
        .map_err(|error| CliError::ScenarioLoadFailed(format!("invalid scenario: {error}")))?;

      let systems_len = scenario.systems.as_ref().map(|s| s.len()).unwrap_or(0);
      let difficulty = match systems_len {
        2 => crate::model::Difficulty::Easy,
        3 => crate::model::Difficulty::Normal,
        4 => crate::model::Difficulty::Hard,
        _ => crate::model::Difficulty::Expert,
      };

      use crate::cli::input::ReadLineOutcome;
      use crate::cli::io::{parse_seed_choice, read_seed_choice};
      let seed = loop {
        match read_seed_choice()? {
          ReadLineOutcome::Quit => return Ok(SessionOutcome::QuitNoSave),
          ReadLineOutcome::Payload(input) => match parse_seed_choice(&input) {
            Ok(seed) => break seed,
            Err(CliError::InvalidSeed(s)) => {
              print_line(&style::warning(&format!(
                "{} Seed '{}' is not a valid unsigned integer",
                style::EMOJI_WARNING,
                s
              )));
            }
            Err(error) => return Err(error),
          },
        }
      };

      let config = crate::model::CompetitiveRunConfig { seed, difficulty };
      let initial_world = scenario
        .initial_competitive_world_state(config.difficulty, &comp_ruleset)
        .map_err(|error| CliError::ScenarioLoadFailed(format!("invalid initial state: {error}")))?;
      return Ok(run_competitive_stub(&ruleset, config, Some(initial_world)));
    } else {
      crate::scenario::validate_stabilization_scenario(&scenario, &ruleset)
        .map_err(|error| CliError::ScenarioLoadFailed(format!("invalid scenario: {error}")))?;
      let Some(setup) = read_stabilization_run_setup(&ruleset, &scenario)? else {
        return Ok(SessionOutcome::QuitNoSave);
      };
      return run_session_from_genesis(setup.config, &ruleset, &setup.initial_state);
    }
  }

  let comp_ruleset = crate::model::default_competitive_ruleset();

  if session_save_exists_interactive(&ruleset)? {
    loop {
      match read_resume_choice()? {
        ReadLineOutcome::Quit => return Ok(SessionOutcome::QuitNoSave),
        ReadLineOutcome::Payload(input) => match parse_resume_choice(&input) {
          Ok(true) => {
            let config = resume_run_config(&ruleset)?;
            return run_session(config, &ruleset);
          }
          Ok(false) => {
            delete_session_save().map_err(|error| {
              CliError::SessionSaveFailed(super::persistence::describe_persistence_error(&error))
            })?;
            break;
          }
          Err(CliError::InvalidResumeChoice(choice)) => {
            print_line(&style::warning(&format!(
              "{} '{choice}' is not valid; use r to resume or n to start over",
              style::EMOJI_WARNING
            )));
          }
          Err(error) => return Err(error),
        },
      }
    }
  } else if competitive_session_save_exists_interactive(&comp_ruleset)? {
    loop {
      match read_competitive_resume_choice()? {
        ReadLineOutcome::Quit => return Ok(SessionOutcome::QuitNoSave),
        ReadLineOutcome::Payload(input) => match parse_resume_choice(&input) {
          Ok(true) => {
            let save = load_competitive_session_save(&comp_ruleset).map_err(|error| {
              CliError::SessionSaveFailed(super::persistence::describe_persistence_error(&error))
            })?;
            return Ok(resume_competitive_campaign(save));
          }
          Ok(false) => {
            delete_competitive_session_save().map_err(|error| {
              CliError::SessionSaveFailed(super::persistence::describe_persistence_error(&error))
            })?;
            break;
          }
          Err(CliError::InvalidResumeChoice(choice)) => {
            print_line(&style::warning(&format!(
              "{} '{choice}' is not valid; use r to resume or n to start over",
              style::EMOJI_WARNING
            )));
          }
          Err(error) => return Err(error),
        },
      }
    }
  }

  let Some(campaign) = select_campaign()? else {
    return Ok(SessionOutcome::QuitNoSave);
  };

  match campaign {
    CampaignId::StabilizationV1 => {
      let scenario = default_stabilization_scenario().map_err(|error| {
        CliError::ScenarioLoadFailed(format!("default stabilization scenario: {error}"))
      })?;
      let Some(setup) = read_stabilization_run_setup(&ruleset, &scenario)? else {
        return Ok(SessionOutcome::QuitNoSave);
      };
      run_session_from_genesis(setup.config, &ruleset, &setup.initial_state)
    }
    CampaignId::CompetitiveRegionalV1 => {
      let Some(config) = read_competitive_run_config()? else {
        return Ok(SessionOutcome::QuitNoSave);
      };
      Ok(run_competitive_stub(&ruleset, config, None))
    }
  }
}

pub fn read_stabilization_run_config(ruleset: &Ruleset) -> Result<Option<RunConfig>, CliError> {
  let scenario = default_stabilization_scenario().map_err(|error| {
    CliError::ScenarioLoadFailed(format!("default stabilization scenario: {error}"))
  })?;
  Ok(read_stabilization_run_setup(ruleset, &scenario)?.map(|setup| setup.config))
}

fn read_stabilization_run_setup(
  _ruleset: &Ruleset,
  scenario: &crate::scenario::Scenario,
) -> Result<Option<StabilizationRunSetup>, CliError> {
  let initial_state = scenario.initial_world_state();

  print_pre_run_briefing(&initial_state);
  maybe_show_new_player_cues();

  let selection = loop {
    match read_play_mode_choice()? {
      ReadLineOutcome::Quit => return Ok(None),
      ReadLineOutcome::Payload(input) => match parse_play_mode_choice(&input) {
        Ok(selection) => break selection,
        Err(CliError::InvalidPlayModeChoice(choice)) => {
          print_line(&style::warning(&format!(
            "{} Play mode '{choice}' is not available; use Enter, i, b, 1, 2, or 3",
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
      ReadLineOutcome::Payload(input) => {
        match parse_seed_choice_with_default(&input, scenario.default_seed) {
          Ok(seed) => break seed,
          Err(CliError::InvalidSeed(seed)) => {
            print_line(&style::warning(&format!(
              "{} Seed '{seed}' is not a valid unsigned integer",
              style::EMOJI_WARNING
            )));
          }
          Err(error) => return Err(error),
        }
      }
    }
  };

  Ok(
    Some(RunConfig {
      seed,
      play_mode: selection.play_mode,
      experience_mode: selection.experience_mode,
      resume: None,
    })
    .map(|config| StabilizationRunSetup {
      config,
      initial_state,
    }),
  )
}

fn session_save_exists_interactive(ruleset: &Ruleset) -> Result<bool, CliError> {
  if !super::persistence::session_save_exists() {
    return Ok(false);
  }

  match load_session_save(ruleset) {
    Ok(_) => Ok(true),
    Err(error) => {
      print_line(&style::warning(&format!(
        "{} Ignoring invalid autosave: {}",
        style::EMOJI_WARNING,
        super::persistence::describe_persistence_error(&error)
      )));
      let _ = delete_session_save();
      Ok(false)
    }
  }
}

fn competitive_session_save_exists_interactive(
  ruleset: &CompetitiveRuleset,
) -> Result<bool, CliError> {
  if !super::persistence::competitive_session_save_exists() {
    return Ok(false);
  }

  match load_competitive_session_save(ruleset) {
    Ok(_) => Ok(true),
    Err(error) => {
      print_line(&style::warning(&format!(
        "{} Ignoring invalid competitive autosave: {}",
        style::EMOJI_WARNING,
        super::persistence::describe_persistence_error(&error)
      )));
      let _ = delete_competitive_session_save();
      Ok(false)
    }
  }
}

fn resume_run_config(ruleset: &Ruleset) -> Result<RunConfig, CliError> {
  let save = load_session_save(ruleset).map_err(|error| {
    CliError::SessionSaveFailed(super::persistence::describe_persistence_error(&error))
  })?;

  print_line(&style::success(&format!(
    "{} Resuming interactive session at turn {} (seed {})",
    style::EMOJI_SUCCESS,
    save.next_turn,
    save.seed
  )));

  Ok(RunConfig {
    seed: save.seed,
    play_mode: PlayMode::Interactive,
    experience_mode: save.experience_mode,
    resume: Some(ResumeState {
      history: save.history,
      next_turn: save.next_turn,
    }),
  })
}

fn maybe_show_new_player_cues() {
  if !first_run_complete() {
    print_block(&new_player_cue_lines());
    let _ = mark_first_run_complete();
  }
}

#[allow(dead_code)]
pub fn read_run_config(ruleset: &Ruleset) -> Result<Option<RunConfig>, CliError> {
  // Stabilization-only setup; campaign routing lives in `run()`.
  read_stabilization_run_config(ruleset)
}

pub fn run_session(config: RunConfig, ruleset: &Ruleset) -> Result<SessionOutcome, CliError> {
  let genesis = genesis_state();
  run_session_from_genesis(config, ruleset, &genesis)
}

fn run_session_from_genesis(
  config: RunConfig,
  ruleset: &Ruleset,
  initial_state: &crate::model::WorldState,
) -> Result<SessionOutcome, CliError> {
  let interactive_result = match config.play_mode {
    PlayMode::Preset(strategy) => {
      print_line(&style::label_value(
        "Selected preset",
        strategy_plan(strategy).name,
      ));
      let history = build_history_for_strategy_from_genesis(
        strategy_plan(strategy),
        config.seed,
        ruleset,
        initial_state.clone(),
      )
      .map_err(CliError::InvalidStrategyPlan)?;
      print_demo(config.seed, &history, ruleset);
      InteractiveRunResult::Completed(history)
    }
    PlayMode::Interactive => {
      let mode_label = match config.experience_mode {
        ExperienceMode::Standard => "Interactive (standard)",
        ExperienceMode::Beginner => "Beginner (guided)",
      };
      print_line(&style::label_value("Selected play mode", mode_label));
      let result = run_interactive_history_from_genesis(
        config.seed,
        ruleset,
        config.experience_mode,
        config.resume.as_ref(),
        initial_state,
      )?;
      match &result {
        InteractiveRunResult::Completed(history) => {
          print_interactive_results(config.seed, history, ruleset);
        }
        InteractiveRunResult::QuitEarly { .. } => {}
      }
      result
    }
  };

  match interactive_result {
    InteractiveRunResult::QuitEarly { history, next_turn } => {
      let save = SessionSave {
        ruleset_version: ruleset.version.to_string(),
        seed: config.seed,
        experience_mode: config.experience_mode,
        history,
        next_turn,
      };
      match write_session_save(&save) {
        Ok(()) => {
          print_line(&style::success(&format!(
            "{} Session saved; resume on next launch with r",
            style::EMOJI_SUCCESS
          )));
          Ok(SessionOutcome::QuitSaved)
        }
        Err(error) => {
          print_line(&style::warning(&format!(
            "{} Autosave failed: {}",
            style::EMOJI_WARNING,
            super::persistence::describe_persistence_error(&error)
          )));
          Ok(SessionOutcome::QuitNoSave)
        }
      }
    }
    InteractiveRunResult::Completed(history) => {
      let _ = delete_session_save();

      if !stdin_uses_fallback_input() {
        match read_replay_export_path()? {
          ReadLineOutcome::Quit => return Ok(SessionOutcome::QuitNoSave),
          ReadLineOutcome::Payload(input) => {
            if let Some(path) = parse_replay_export_path(&input) {
              let artifact = ReplayArtifact {
                seed: config.seed,
                play_mode: config.play_mode,
                ruleset_version: ruleset.version.to_string(),
                history,
              };

              match write_replay_artifact(&path, &artifact) {
                Ok(()) => print_line(&style::success(&format!(
                  "{} Replay artifact written to {path}",
                  style::EMOJI_SUCCESS
                ))),
                Err(error) => super::display::eprint_error(&format!(
                  "Replay export failed: {}",
                  describe_replay_artifact_error(&error)
                )),
              }
            }
          }
        }
      }

      Ok(SessionOutcome::Completed)
    }
  }
}

pub fn run_interactive_history(
  seed: u64,
  ruleset: &Ruleset,
  experience_mode: ExperienceMode,
  resume: Option<&ResumeState>,
) -> Result<InteractiveRunResult, CliError> {
  let genesis = genesis_state();
  run_interactive_history_from_genesis(seed, ruleset, experience_mode, resume, &genesis)
}

pub fn run_interactive_history_from_genesis(
  seed: u64,
  ruleset: &Ruleset,
  experience_mode: ExperienceMode,
  resume: Option<&ResumeState>,
  initial_state: &crate::model::WorldState,
) -> Result<InteractiveRunResult, CliError> {
  let (genesis, mut state, mut transitions, start_turn) = if let Some(resume) = resume {
    let state = resume
      .history
      .transitions
      .last()
      .map(|transition| transition.next.clone())
      .unwrap_or_else(|| resume.history.genesis.clone());
    (
      resume.history.genesis.clone(),
      state,
      resume.history.transitions.clone(),
      resume.next_turn,
    )
  } else {
    let genesis = initial_state.clone();
    (genesis.clone(), genesis, Vec::new(), 1)
  };

  let defaults = default_interactive_commands();
  let turn_parsers: [TurnParser; 5] = [
    parse_stabilize_access_command,
    parse_policy_command,
    parse_workforce_command,
    parse_coalition_command,
    parse_competitor_command,
  ];

  for turn_number in start_turn..=INTERACTIVE_TURN_COUNT {
    let turn_index = (turn_number - 1) as usize;
    let parse_command = turn_parsers[turn_index];
    let inputs = resolve_inputs(seed, &state, ruleset);
    let observation = observe_for_player(&state, &inputs);

    print_turn_uncertainty_block(
      turn_number,
      &turn_uncertainty_preview(&state, &observation, turn_number, ruleset),
    );

    print_turn_briefing_block(
      turn_number,
      &turn_executive_briefing(&state, &observation, turn_number),
    );

    if experience_mode == ExperienceMode::Standard
      && let Some(hint) = turn_hint(turn_number)
    {
      print_line(&style::dim(hint));
    }

    let command = match experience_mode {
      ExperienceMode::Beginner => loop {
        let menu = format_beginner_menu(turn_number, &state, &observation, ruleset);
        match read_beginner_choice(&menu, turn_number)? {
          ReadLineOutcome::Quit => {
            return Ok(InteractiveRunResult::QuitEarly {
              history: History {
                genesis: genesis.clone(),
                transitions: transitions.clone(),
              },
              next_turn: turn_number,
            });
          }
          ReadLineOutcome::Payload(input) => match parse_beginner_choice(&input, turn_number) {
            Ok(command) => break command,
            Err(message) => {
              print_line(&style::warning(&format!(
                "{} {message}",
                style::EMOJI_WARNING
              )));
            }
          },
        }
      },
      ExperienceMode::Standard => {
        let prompt = format_command_prompt(turn_number, ruleset, &defaults[turn_index]);
        loop {
          match read_command_line(&prompt, turn_number)? {
            ReadLineOutcome::Quit => {
              return Ok(InteractiveRunResult::QuitEarly {
                history: History {
                  genesis: genesis.clone(),
                  transitions: transitions.clone(),
                },
                next_turn: turn_number,
              });
            }
            ReadLineOutcome::Payload(input) => match parse_command(&input) {
              Ok(command) => break command,
              Err(CliError::InvalidCommandInput(message)) => {
                print_line(&style::warning(&format!(
                  "{} {message}",
                  style::EMOJI_WARNING
                )));
              }
              Err(error) => return Err(error),
            },
          }
        }
      }
    };

    let transition_record =
      transition(&state, command, inputs, ruleset).map_err(CliError::InvalidInteractiveCommand)?;

    print_turn_resolution_block(&turn_resolution_summary(&transition_record));

    state = transition_record.next.clone();
    transitions.push(transition_record);
  }

  Ok(InteractiveRunResult::Completed(History {
    genesis,
    transitions,
  }))
}
