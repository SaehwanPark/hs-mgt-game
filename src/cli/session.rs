use std::io;

use crate::artifact::{describe_replay_artifact_error, write_replay_artifact};
use crate::inputs::resolve_inputs;
use crate::model::{
  CliError, History, PlayMode, PlayerCommand, ReplayArtifact, Ruleset, RunConfig, default_ruleset,
  genesis_state,
};
use crate::sim::{observe_for_player, transition};

use super::display::{
  format_command_prompt, print_interactive_results, print_line, print_pre_run_briefing,
  print_turn_briefing_block, print_turn_resolution_block, print_turn_uncertainty_block, style,
  turn_executive_briefing, turn_resolution_summary, turn_uncertainty_preview,
};
use super::export::read_replay_export_path;
use super::io::{read_command_line, read_play_mode_choice, read_seed_choice};
use super::output::print_demo;
use super::parse::{
  parse_coalition_command, parse_competitor_command, parse_policy_command,
  parse_stabilize_access_command, parse_workforce_command,
};
use super::strategy::{build_history_for_strategy, default_interactive_commands, strategy_plan};

pub fn run() -> Result<(), CliError> {
  let ruleset = default_ruleset();
  read_run_config().and_then(|config| run_session(config, &ruleset))
}

pub fn read_run_config() -> Result<RunConfig, CliError> {
  print_pre_run_briefing(&genesis_state());
  let play_mode = read_play_mode_choice()?;
  let seed = read_seed_choice()?;
  Ok(RunConfig { seed, play_mode })
}
pub fn run_session(config: RunConfig, ruleset: &Ruleset) -> Result<(), CliError> {
  let history = match config.play_mode {
    PlayMode::Preset(strategy) => {
      print_line(&style::label_value(
        "Selected preset",
        strategy_plan(strategy).name,
      ));
      build_history_for_strategy(strategy, config.seed, ruleset)
        .map_err(CliError::InvalidStrategyPlan)?
    }
    PlayMode::Interactive => {
      print_line(&style::label_value("Selected play mode", "Interactive"));
      run_interactive_history(config.seed, ruleset)?
    }
  };

  match config.play_mode {
    PlayMode::Preset(_) => print_demo(config.seed, &history, ruleset),
    PlayMode::Interactive => print_interactive_results(config.seed, &history, ruleset),
  }

  if std::io::IsTerminal::is_terminal(&io::stdin()) {
    if let Some(path) = read_replay_export_path()? {
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

  Ok(())
}
pub fn run_interactive_history(seed: u64, ruleset: &Ruleset) -> Result<History, CliError> {
  let genesis = genesis_state();
  let mut state = genesis.clone();
  let mut transitions = Vec::new();
  let defaults = default_interactive_commands();

  let turn_parsers: [fn(&str) -> Result<PlayerCommand, CliError>; 5] = [
    parse_stabilize_access_command,
    parse_policy_command,
    parse_workforce_command,
    parse_coalition_command,
    parse_competitor_command,
  ];

  for (turn_index, parse_command) in turn_parsers.iter().enumerate() {
    let turn_number = turn_index as u32 + 1;
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

    let prompt = format_command_prompt(turn_number, ruleset, &defaults[turn_index]);
    let command = parse_command(&read_command_line(&prompt)?)?;
    let transition =
      transition(&state, command, inputs, ruleset).map_err(CliError::InvalidInteractiveCommand)?;

    print_turn_resolution_block(&turn_resolution_summary(&transition));

    state = transition.next.clone();
    transitions.push(transition);
  }

  Ok(History {
    genesis,
    transitions,
  })
}
